# Especificacion - Modulo ASII-05: Citas medicas y agenda

## Identificacion

| Dato | Informacion |
|---|---|
| Modulo | ASII-05 - Citas medicas y agenda |
| Estudiante | Eddy Adolfo Castro Veliz |
| GitHub | EddCastro |
| Issue | #5 |
| Rama | `feat/mod05-citas-medicas-agenda` |
| Worktree | `../shi-mod05-citas` |
| Limite de datos | HOSPITAL - escritura local |

## Problema

La programacion manual de citas permite registrar atenciones fuera de la
jornada del medico o en horarios ya ocupados. Esto genera sobrecupo, esperas
innecesarias y perdida de trazabilidad sobre el estado real de cada cita.

El modulo debe garantizar que toda cita se registre dentro de la disponibilidad
declarada del medico, sin cruces con citas activas, y que cada cambio de estado
quede registrado.

## Regla central obligatoria

No se confirma una cita fuera de disponibilidad ni en un intervalo ya ocupado;
la cancelacion libera el horario de forma consistente.

## Actores

| Actor | Responsabilidad |
|---|---|
| Personal administrativo | Registra, confirma, cancela y reagenda citas. Consulta la agenda diaria. |
| Medico | Consulta su agenda. Su jornada define la disponibilidad. |
| Paciente | Origina la solicitud y responde la confirmacion. |

La identidad y los permisos provienen de ASII-01 y ASII-02. El modulo no
implementa autenticacion propia.

## Casos de uso implementados

| Codigo | Caso de uso | Descripcion |
|---|---|---|
| CU-01 | Solicitar cita | Registra una cita validando paciente, medico, especialidad, jornada y cruces. |
| CU-02 | Confirmar cita | Cambia el estado de pendiente a confirmada. |
| CU-03 | Cancelar cita | Cambia el estado a cancelada conservando el motivo y libera el horario. |
| CU-04 | Reagendar cita | Asigna una nueva fecha validando de nuevo jornada y cruces. |
| CU-05 | Consultar agenda | Lista citas filtrando por medico, paciente, fecha y estado. |

## Fuera de alcance

- Registro maestro de pacientes (ASII-03).
- Catalogo de medicos y especialidades (ASII-04).
- Autenticacion, roles y permisos (ASII-01, ASII-02).
- Notificaciones y recordatorios (ASII-21).
- Lista de espera y oferta de espacios liberados.
- Transiciones posteriores a la atencion: `completada` y `no_asistio`.

Los dos ultimos estados existen en el esquema y se documentan en la maquina de
estados, pero su transicion corresponde al proceso de atencion, no a la gestion
de agenda.

## Modelo de datos

### Tabla existente: `appointments`

Definida en `2026_04_26_110000_create_admissions_and_appointments.php`. El
modulo la consume sin modificar su estructura.

| Columna | Tipo | Nota |
|---|---|---|
| `id` | bigint | Clave primaria |
| `tenant_id` | char(36) | Aislamiento por hospital |
| `patient_id` | FK `patients` | Propiedad de ASII-03 |
| `doctor_id` | FK `doctors` | Propiedad de ASII-04 |
| `specialty_id` | FK `specialties` | Debe coincidir con la del medico |
| `scheduled_at` | datetime | Inicio de la cita |
| `duration_min` | smallint | Duracion, por defecto 30 |
| `status` | enum | pendiente, confirmada, completada, cancelada, no_asistio |
| `reason` | text | Motivo de la cita |
| `notes` | text | Observaciones y motivo de cancelacion |

Indices disponibles y su uso en este modulo:

| Indice | Consulta que atiende |
|---|---|
| `idx_appt_doctor_date` | Agenda del medico por dia y deteccion de cruces |
| `idx_appt_date_status` | Citas del dia en recepcion |
| `idx_appt_patient_date` | Historial de citas del paciente |

### Tabla nueva: `doctor_availabilities`

El modulo ASII-04 no expone todavia la disponibilidad medica en el backend
Laravel. Para cumplir la regla central se crea una tabla propia con un contrato
aislado, sustituible cuando ese modulo la publique.

| Columna | Tipo | Descripcion |
|---|---|---|
| `id` | bigint | Clave primaria |
| `tenant_id` | char(36) | Aislamiento por hospital |
| `doctor_id` | FK `doctors` | Medico al que aplica |
| `weekday` | smallint | 0 domingo a 6 sabado |
| `start_time` | time | Inicio de jornada |
| `end_time` | time | Fin de jornada |
| `active` | boolean | Permite desactivar sin borrar |

Restricciones: `weekday` entre 0 y 6, `start_time` menor que `end_time`.
Indice compuesto por `tenant_id`, `doctor_id` y `weekday`.

## Reglas de negocio

| Codigo | Regla | Se verifica en |
|---|---|---|
| RN-01 | Una cita no puede programarse en una fecha pasada. | `Appointment::schedule()` |
| RN-02 | La duracion debe ser mayor que cero. | `Appointment` |
| RN-03 | El paciente debe existir y pertenecer al tenant activo. | `EloquentAppointmentRepository` |
| RN-04 | El medico debe existir y pertenecer al tenant activo. | `EloquentDoctorAvailabilityRepository` |
| RN-05 | La especialidad solicitada debe coincidir con la del medico. | Caso de uso `RequestAppointment` |
| RN-06 | El horario debe caer dentro de una jornada activa del medico. | `DoctorAvailabilityRepository::isWithinWorkingHours()` |
| RN-07 | No se admite cruce con una cita pendiente o confirmada del mismo medico. | `AppointmentRepository::hasOverlap()` |
| RN-08 | Una cita cancelada no bloquea el horario. | Consulta de cruce |
| RN-09 | Toda cita se crea en estado pendiente. | `Appointment::schedule()` |
| RN-10 | Solo una cita pendiente puede confirmarse. | `Appointment::confirm()` |
| RN-11 | Solo una cita pendiente o confirmada puede cancelarse. | `Appointment::cancel()` |
| RN-12 | La cancelacion exige un motivo. | `Appointment::cancel()` |
| RN-13 | Solo una cita pendiente o confirmada puede reagendarse. | `Appointment::reschedule()` |
| RN-14 | Toda operacion se limita al tenant activo. | `TenantContext` |

## Maquina de estados

```
                  schedule()
                      |
                      v
                 [pendiente] ----- confirm() -----> [confirmada]
                   |     |                            |     |
            cancel()   reschedule()            cancel()   reschedule()
                   |     |                            |     |
                   |     +--> [pendiente]             |     +--> [confirmada]
                   v                                  v
             [cancelada] <-----------------------------
```

Estado terminal para este modulo: `cancelada`. Los estados `completada` y
`no_asistio` se alcanzan desde `confirmada` en el proceso de atencion, fuera
del alcance de esta entrega.

## Regla de cruce de intervalos

Dos citas del mismo medico se cruzan cuando el inicio de la nueva es anterior
al fin de la existente y el fin de la nueva es posterior al inicio de la
existente.

El fin de una cita se calcula sumando `duration_min` a `scheduled_at`. Los
estados `pendiente` y `confirmada` bloquean el intervalo; `cancelada`,
`completada` y `no_asistio` no lo bloquean.

Al reagendar se excluye la propia cita de la comparacion.

## Criterios de aceptacion

| Codigo | Escenario | Resultado esperado |
|---|---|---|
| CA-01 | Solicitud valida dentro de jornada y sin cruces | Se crea una cita pendiente y se devuelve su identificador. |
| CA-02 | Solicitud con fecha pasada | Se rechaza y no se persiste. |
| CA-03 | Solicitud con duracion cero o negativa | Se rechaza. |
| CA-04 | Medico que no atiende la especialidad solicitada | Se rechaza indicando el dato invalido. |
| CA-05 | Solicitud fuera de la jornada del medico | Se rechaza por horario no disponible. |
| CA-06 | Solicitud que se cruza con una cita activa | Se rechaza por horario ocupado. |
| CA-07 | Solicitud en el horario de una cita cancelada | Se acepta, porque el horario quedo libre. |
| CA-08 | Confirmar una cita pendiente | El estado cambia a confirmada. |
| CA-09 | Confirmar una cita ya confirmada o cancelada | Se rechaza y el estado no cambia. |
| CA-10 | Cancelar con motivo | El estado cambia a cancelada y el motivo se conserva. |
| CA-11 | Cancelar sin motivo | Se rechaza. |
| CA-12 | Reagendar a un horario libre | La cita conserva su identificador con la nueva fecha. |
| CA-13 | Reagendar a un horario ocupado | Se rechaza y la fecha original se conserva. |
| CA-14 | Consultar agenda por medico y fecha | Devuelve solo las citas del tenant activo. |
| CA-15 | Acceso a una cita de otro tenant | No se devuelve ni se modifica. |

## Contrato de API

Todas las rutas se publican bajo `/api/v1` y requieren los middleware `tenant`
y `jwt.auth`.

| Metodo | Ruta | Caso de uso | Exito | Error |
|---|---|---|---|---|
| POST | `/appointments` | CU-01 | 201 | 422 regla incumplida |
| PATCH | `/appointments/{id}/confirm` | CU-02 | 200 | 404 / 422 |
| PATCH | `/appointments/{id}/cancel` | CU-03 | 200 | 404 / 422 |
| PATCH | `/appointments/{id}/reschedule` | CU-04 | 200 | 404 / 422 |
| GET | `/appointments` | CU-05 | 200 | 422 filtros invalidos |

### Cuerpo de solicitud - POST /appointments

```json
{
  "patient_id": 1,
  "doctor_id": 1,
  "specialty_id": 1,
  "scheduled_at": "2026-09-01 10:00:00",
  "duration_min": 30,
  "reason": "Control general"
}
```

### Respuesta

```json
{
  "data": {
    "id": 1,
    "status": "pendiente",
    "scheduled_at": "2026-09-01 10:00:00",
    "duration_min": 30
  }
}
```

### Filtros de GET /appointments

`doctor_id`, `patient_id`, `date`, `status`. Todos opcionales; el tenant se
aplica siempre de forma implicita.

## Requisitos no funcionales

| Codigo | Categoria | Condicion verificable |
|---|---|---|
| RNF-01 | Seguridad | Toda operacion exige JWT valido y contexto de tenant. |
| RNF-02 | Aislamiento | Ninguna consulta devuelve datos de otro tenant. |
| RNF-03 | Atomicidad | La validacion de cruce y la escritura ocurren en una transaccion. |
| RNF-04 | Mantenibilidad | Los casos de uso dependen de contratos, no de Eloquent. |
| RNF-05 | Testabilidad | Las reglas se verifican con dobles en memoria, sin base de datos. |
| RNF-06 | Trazabilidad | El motivo de cancelacion se conserva en el registro. |
| RNF-07 | Privacidad | Documentacion y pruebas usan exclusivamente datos ficticios. |

## Dependencias

| Modulo | Aporta |
|---|---|
| ASII-01 | Usuario autenticado y tenant activo |
| ASII-02 | Roles y permisos |
| ASII-03 | Registro de pacientes |
| ASII-04 | Catalogo de medicos y especialidades |

La disponibilidad medica se implementa localmente mientras ASII-04 no la
exponga, mediante un contrato que permite sustituir la fuente sin modificar los
casos de uso.

## Datos

Todos los datos utilizados en pruebas y ejemplos son ficticios. El repositorio
no contiene credenciales, secretos ni informacion clinica identificable.
