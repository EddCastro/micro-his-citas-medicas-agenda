# Especificacion - Modulo 05: Citas medicas y agenda

## Identificacion

| Dato | Informacion |
|---|---|
| Modulo | ASII-05 - Citas medicas y agenda |
| Estudiante | Eddy Adolfo Castro Veliz |
| GitHub | EddCastro |
| Actividad | Tarea 3 - Micro-monolito en PHP vanilla |
| Flujo asignado | Solicitud, validacion de disponibilidad y confirmacion o cancelacion de cita |

## Problema

La programacion manual de citas permite registrar atenciones en horarios en que
el medico no labora o que ya se encuentran ocupados. Esto genera sobrecupo,
esperas innecesarias y perdida de trazabilidad sobre el estado real de cada
cita.

## Actores

| Actor | Responsabilidad en este alcance |
|---|---|
| Personal administrativo | Registra la solicitud, confirma y cancela citas. |
| Paciente | Origina la solicitud y responde la confirmacion. |
| Medico | Aporta la jornada laboral contra la que se valida la disponibilidad. |

## Historia de usuario

Como personal administrativo quiero registrar una cita para un paciente con un
medico disponible, de modo que el sistema impida horarios fuera de jornada y
cruces con citas activas.

## Alcance

- Solicitar una cita validando fecha, duracion y disponibilidad.
- Verificar la jornada laboral del medico.
- Impedir cruces con citas activas.
- Persistir la cita en estado pendiente.
- Confirmar una cita pendiente.
- Cancelar una cita pendiente o confirmada.

## No alcance

- Autenticacion, roles y permisos.
- Reagendamiento y lista de espera.
- Notificaciones al paciente.
- Expediente clinico y facturacion.
- Interfaz grafica de usuario.

Estos elementos corresponden a otros modulos del Sistema Hospitalario Integrado
o a actividades posteriores del curso.

## Reglas de negocio

| Codigo | Regla | Se verifica en |
|---|---|---|
| RN-01 | Una cita no puede programarse en una fecha pasada. | `Appointment::schedule()` |
| RN-02 | La duracion debe ser mayor que cero. | `Appointment::__construct()` |
| RN-03 | El paciente y el medico son obligatorios. | `Appointment::__construct()` |
| RN-04 | El horario debe estar dentro de la jornada del medico. | `PdoAvailabilityRepository::isAvailable()` |
| RN-05 | No se admite cruce con una cita pendiente o confirmada del mismo medico. | `PdoAvailabilityRepository::isAvailable()` |
| RN-06 | Una cita cancelada no bloquea el horario. | Consulta de colision |
| RN-07 | Toda cita se crea en estado pendiente. | `Appointment::schedule()` |
| RN-08 | Una cita cancelada no puede confirmarse. | `Appointment::confirm()` |
| RN-09 | Una cita confirmada no puede confirmarse de nuevo. | `Appointment::confirm()` |
| RN-10 | Una cita cancelada no puede cancelarse de nuevo. | `Appointment::cancel()` |

## Criterios de aceptacion

| Codigo | Escenario | Resultado esperado |
|---|---|---|
| CA-01 | Solicitud valida dentro de jornada y sin cruces | Se registra una cita en estado pendiente y se devuelve su identificador. |
| CA-02 | Solicitud con fecha pasada | Se rechaza con excepcion de dominio y no se persiste. |
| CA-03 | Solicitud con duracion cero o negativa | Se rechaza con excepcion de dominio. |
| CA-04 | Solicitud fuera de la jornada del medico | Se rechaza por horario no disponible. |
| CA-05 | Solicitud que se cruza con una cita activa | Se rechaza por horario no disponible. |
| CA-06 | Solicitud en el horario de una cita cancelada | Se acepta, porque el horario quedo libre. |
| CA-07 | Confirmar una cita pendiente | El estado cambia a confirmada. |
| CA-08 | Confirmar una cita ya confirmada | Se rechaza y el estado no cambia. |
| CA-09 | Cancelar una cita pendiente o confirmada | El estado cambia a cancelada. |
| CA-10 | Fallo del mecanismo de persistencia | El error se propaga y no se reporta exito. |

## Contratos del modulo

### AppointmentRepository - puerto de persistencia

Definido en `src/Domain/AppointmentRepository.php`.

| Operacion | Entrada | Salida |
|---|---|---|
| `save` | Appointment | int: identificador asignado |
| `findById` | int | Appointment o null |
| `update` | int, Appointment | void |

### AvailabilityRepository - puerto de disponibilidad

Definido en `src/Domain/AvailabilityRepository.php`.

| Operacion | Entrada | Salida |
|---|---|---|
| `isAvailable` | doctorId, scheduledAt, durationMinutes | bool |

### Casos de uso

| Caso de uso | Entrada | Salida | Error posible |
|---|---|---|---|
| `RequestAppointment` | patientId, doctorId, scheduledAt, durationMinutes | int: identificador de la cita | DomainException por regla incumplida |
| `ConfirmAppointment` | appointmentId | void | DomainException si no existe o la transicion es invalida |
| `CancelAppointment` | appointmentId | void | DomainException si no existe o ya estaba cancelada |

## Estados de la cita

```
              schedule()
                  |
                  v
             [pendiente] ---- confirm() ----> [confirmada]
                  |                                |
               cancel()                         cancel()
                  |                                |
                  v                                v
             [cancelada] <-----------------------
```

Desde `cancelada` no existe transicion de salida: ni confirmar ni cancelar de
nuevo son operaciones validas.

## Regla de cruce de intervalos

Dos citas se cruzan cuando el inicio de la nueva es anterior al fin de la
existente y el fin de la nueva es posterior al inicio de la existente.

Los estados pendiente y confirmada bloquean el intervalo. El estado cancelada
no lo bloquea, por lo que el horario de una cita cancelada vuelve a estar
disponible.

## Datos

Todos los datos utilizados en pruebas y ejemplos son ficticios. Los
identificadores de paciente y medico son numeros arbitrarios sin
correspondencia con personas reales. El repositorio no contiene credenciales,
secretos ni informacion clinica identificable.
