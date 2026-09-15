# Contrato de API — Módulo ASII-05

Contrato del módulo de citas médicas dentro del Sistema Hospitalario
Integrado. Define la interfaz que el cliente consume y las garantías que el
servidor ofrece.

## Convenciones generales

| Aspecto | Definición |
|---|---|
| Prefijo | `/api/v1` |
| Formato | JSON en solicitud y respuesta |
| Codificación | UTF-8 |
| Fechas | `Y-m-d H:i:s` en zona del hospital |
| Autenticación | Token JWT en cabecera `Authorization: Bearer` |
| Hospital activo | Cabecera `X-Tenant-ID` validada por middleware |
| Correlación | Cabecera `X-Request-Id`, generada si el cliente no la envía |

### Versionado

La versión viaja en la ruta. Un cambio compatible —agregar un campo opcional a
la respuesta o un filtro opcional a la consulta— no incrementa la versión. Un
cambio incompatible —eliminar un campo, cambiar su tipo o su significado, o
volver obligatorio un parámetro opcional— exige publicar `/api/v2` y mantener
la versión anterior durante un período de transición.

## Endpoints

| Método | Ruta | Caso de uso | Éxito |
|---|---|---|---|
| POST | `/appointments` | CU-01 Solicitar cita | 201 |
| PATCH | `/appointments/{id}/confirm` | CU-02 Confirmar cita | 200 |
| PATCH | `/appointments/{id}/cancel` | CU-03 Cancelar cita | 200 |
| PATCH | `/appointments/{id}/reschedule` | CU-04 Reagendar cita | 200 |
| GET | `/appointments` | CU-05 Consultar agenda | 200 |

Las operaciones de cambio de estado usan `PATCH` porque modifican un atributo
de un recurso existente, no lo reemplazan por completo.

## POST /appointments

Registra una cita en estado pendiente.

### Solicitud

```json
{
  "patient_id": 1,
  "doctor_id": 1,
  "specialty_id": 1,
  "scheduled_at": "2026-10-05 10:00:00",
  "duration_min": 30,
  "reason": "Control general"
}
```

Cabecera opcional `Idempotency-Key` con un identificador único generado por el
cliente.

### Respuesta 201

```json
{
  "data": {
    "id": 1,
    "patient_id": 1,
    "doctor_id": 1,
    "specialty_id": 1,
    "scheduled_at": "2026-10-05 10:00:00",
    "duration_min": 30,
    "status": "pendiente",
    "reason": "Control general",
    "notes": null
  }
}
```

### Idempotencia

Una solicitud de cita no es naturalmente idempotente: repetirla crearía dos
citas. Para que el cliente pueda reintentar con seguridad tras un tiempo de
espera agotado, se define la cabecera `Idempotency-Key`.

El servidor registra la clave junto con el identificador de la cita creada. Si
recibe la misma clave dentro de una ventana de veinticuatro horas, devuelve la
cita original con código 200 en lugar de crear otra.

Sin esa cabecera, un reintento tras un tiempo de espera puede producir una cita
duplicada o un rechazo por cruce con la cita que sí llegó a crearse.

## PATCH /appointments/{id}/confirm

Sin cuerpo. Cambia el estado de pendiente a confirmada.

Es naturalmente idempotente en su efecto observable: confirmar una cita ya
confirmada no altera el estado. El servidor devuelve 422 porque la transición
no es válida, lo que informa al cliente sin modificar datos.

## PATCH /appointments/{id}/cancel

```json
{ "reason": "El paciente no puede asistir" }
```

El motivo es obligatorio y se conserva en el registro.

## PATCH /appointments/{id}/reschedule

```json
{ "scheduled_at": "2026-10-06 11:00:00" }
```

Conserva el identificador y el estado de la cita. Revalida jornada y cruces,
excluyendo la propia cita de la comparación.

## GET /appointments

### Filtros

| Parámetro | Tipo | Descripción |
|---|---|---|
| `doctor_id` | entero | Citas de un médico |
| `patient_id` | entero | Historial de un paciente |
| `date` | `Y-m-d` | Citas de un día |
| `status` | enumerado | pendiente, confirmada, completada, cancelada, no_asistio |
| `page` | entero | Página solicitada, por defecto 1 |
| `per_page` | entero | Elementos por página, por defecto 25, máximo 100 |

El hospital activo se aplica siempre de forma implícita y no figura entre los
filtros.

### Respuesta

```json
{
  "data": [ { "id": 1, "status": "pendiente" } ],
  "meta": {
    "page": 1,
    "per_page": 25,
    "total": 48
  }
}
```

La paginación se declara desde ahora porque la agenda de un hospital crece sin
límite superior. Introducirla más tarde sería un cambio incompatible.

## Errores

Formato uniforme para toda respuesta de error:

```json
{
  "message": "El horario solicitado ya se encuentra ocupado.",
  "code": "APPOINTMENT_SLOT_TAKEN",
  "request_id": "0f3a9c1e-..."
}
```

| Código HTTP | Situación |
|---|---|
| 400 | Falta la cabecera de hospital |
| 401 | Token ausente, expirado o inválido |
| 403 | El usuario carece del permiso requerido |
| 404 | La cita no existe en el hospital activo |
| 409 | Conflicto de concurrencia detectado al escribir |
| 422 | Regla de negocio incumplida o formato inválido |
| 429 | Límite de solicitudes excedido |
| 500 | Error no controlado |

### Códigos de negocio

| Código | Significado |
|---|---|
| `APPOINTMENT_PAST_DATE` | La fecha solicitada no es futura |
| `APPOINTMENT_INVALID_DURATION` | La duración no es positiva |
| `DOCTOR_SPECIALTY_MISMATCH` | El médico no atiende la especialidad |
| `DOCTOR_OUTSIDE_WORKING_HOURS` | El horario cae fuera de la jornada |
| `APPOINTMENT_SLOT_TAKEN` | El intervalo ya está ocupado |
| `APPOINTMENT_INVALID_TRANSITION` | La transición de estado no es válida |
| `APPOINTMENT_CANCEL_REASON_REQUIRED` | La cancelación no indica motivo |

El código simbólico permite que el cliente reaccione de forma distinta a cada
caso sin depender del texto del mensaje, que puede traducirse o reformularse.

### Distinción entre inexistente y ajeno

Una cita de otro hospital devuelve 404, igual que una inexistente. La
distinción revelaría la existencia de registros ajenos y constituiría una fuga
de información entre hospitales.

## Permisos por operación

El sistema define seis roles en su semilla: `Admin`, `Médico`, `Enfermera`,
`TecnicoLab`, `Recepcionista` y `Bioquimico`.

### Estado actual

Las rutas del módulo aplican hoy los middleware `tenant` y `jwt.auth`. **No
aplican todavía un permiso específico**, porque la semilla del proyecto solo
declara el permiso `lab.results.validate`, correspondiente al módulo ASII-20.

Este apartado documenta por tanto el esquema propuesto, no el implementado. La
distinción es deliberada: el contrato describe lo que existe, y señala como
propuesta lo que aún no.

### Permisos propuestos

| Permiso | Operación |
|---|---|
| `appointments.create` | Solicitar cita |
| `appointments.confirm` | Confirmar cita |
| `appointments.cancel` | Cancelar cita |
| `appointments.reschedule` | Reagendar cita |
| `appointments.view` | Consultar agenda |

### Matriz de roles

| Operación | Recepcionista | Admin | Médico | Enfermera |
|---|:---:|:---:|:---:|:---:|
| POST `/appointments` | Sí | Sí | No | No |
| PATCH `/{id}/confirm` | Sí | Sí | No | Sí |
| PATCH `/{id}/cancel` | Sí | Sí | No | No |
| PATCH `/{id}/reschedule` | Sí | Sí | No | No |
| GET `/appointments` | Sí | Sí | Sí | Sí |

`TecnicoLab` y `Bioquimico` no participan en el flujo de agenda.

### Criterio de la matriz

La recepción registra, reagenda y cancela, porque es quien atiende al paciente
en ventanilla. La enfermera confirma, porque es quien contacta al paciente
antes de la cita. El médico solo consulta su agenda: no registra ni cancela
citas propias, para que la ocupación de su horario la gobierne recepción.

Toda operación de lectura devuelve únicamente citas del hospital activo, con
independencia del rol.

## Límites de uso

| Alcance | Límite |
|---|---|
| Por usuario autenticado | 120 solicitudes por minuto |
| Escrituras por usuario | 30 solicitudes por minuto |

Al excederse se responde 429 con la cabecera `Retry-After`. El límite protege
la base de datos de una ráfaga accidental del cliente.

## Contrato de disponibilidad

El módulo consume la jornada laboral del médico a través del contrato interno
`DoctorAvailabilityRepository`, que hoy resuelve contra una tabla local.

Cuando el módulo ASII-04 publique su fuente oficial, la operación equivalente
expuesta como interfaz sería:

```
GET /api/v1/doctors/{id}/availability?date=2026-10-05
```

Con respuesta que declare las franjas activas del día. La sustitución
consistiría en escribir una implementación del mismo contrato que consuma esa
ruta, sin modificar ningún caso de uso del módulo de citas.
