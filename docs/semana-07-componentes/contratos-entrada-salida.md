# Contratos de entrada y salida — Semana 7

Contratos de los componentes del flujo **solicitud, validación de
disponibilidad y confirmación o cancelación de cita**. Cada tabla separa lo
que **existe** en la rama `feature/asii-05-semana-06-parcial-eddcastro` de lo
que se **propone** esta semana, para no presentar como implementado lo que no
lo está (mismo criterio que la matriz de la semana 6).

## 1. Backend — casos de uso (Application)

### RequestAppointment — CU-01

| Aspecto | Existe | Propuesto |
|---|---|---|
| Entrada | `RequestAppointmentInput { patientId, doctorId, specialtyId, scheduledAt ('Y-m-d H:i:s'), durationMin (5–480, 30 por defecto), reason (opcional, máx. 500) }`, validado por `StoreAppointmentRequest` | — |
| Salida | `AppointmentData { id, patient_id, doctor_id, specialty_id, scheduled_at, duration_min, status: 'pendiente', reason, notes }` | — |
| Reglas | RN-01, 02, 09 en la entidad; RN-04 médico existe; RN-05 especialidad; RN-06 jornada; RN-07/08 sin cruce | — |
| Errores | `AppointmentRuleViolation` (un solo tipo) | `code()` por regla: `APPOINTMENT_PAST_DATE`, `APPOINTMENT_INVALID_DURATION`, `DOCTOR_SPECIALTY_MISMATCH`, `DOCTOR_OUTSIDE_WORKING_HOURS`, `APPOINTMENT_SLOT_TAKEN` |
| Concurrencia | `transaction()` + bloqueo dentro de `hasOverlap()` | Bloqueo explícito con `AgendaLock::lockDoctorDay()` |
| Idempotencia | No implementada | Cabecera `Idempotency-Key` del contrato de la semana 5 |

### ConfirmAppointment — CU-02

| Aspecto | Existe | Propuesto |
|---|---|---|
| Entrada | `appointmentId: int` | Medio de contacto (teléfono, correo, presencial), previsto en la narrativa de la semana 1 |
| Salida | `AppointmentData` con estado `confirmada` | — |
| Errores | `AppointmentNotFound` (404), `transicionInvalida` (422) | `code()`: `APPOINTMENT_NOT_FOUND`, `APPOINTMENT_INVALID_TRANSITION` |
| Concurrencia | Ninguna: `findById → confirm → update` | `findByIdForUpdate` dentro de `transaction()` |

### CancelAppointment — CU-03

| Aspecto | Existe | Propuesto |
|---|---|---|
| Entrada | `appointmentId: int`, `reason: string` (3 a 500 caracteres en `CancelAppointmentRequest`; no vacío en la entidad, RN-12) | — |
| Salida | `AppointmentData` con estado `cancelada` | — |
| Efecto | El motivo se guarda en `notes` y el estado deja de bloquear el horario (`bloqueaHorario() = false`) | — |
| Errores | `AppointmentNotFound`, `transicionInvalida`, `motivoDeCancelacionRequerido` | `code()`: `APPOINTMENT_CANCEL_REASON_REQUIRED` y los anteriores |
| Concurrencia | Ninguna | Igual que confirmar |

### GetAgenda — CU-05

| Aspecto | Existe |
|---|---|
| Entrada | `doctorId?`, `patientId?`, `date?`, `status?`, `limit` (100 por defecto) |
| Salida | `AppointmentData[]` ordenadas por fecha |
| Errores | Ninguno propio; filtra siempre por tenant |

## 2. Backend — dominio y puertos

| Componente | Estado | Entrada | Salida | Errores |
|---|---|---|---|---|
| `Appointment::schedule` | Existe | tenant, paciente, médico, especialidad, fecha, duración, motivo | Cita `pendiente` | Fecha pasada, duración, campos obligatorios |
| `Appointment::confirm` / `cancel` | Existe | — / motivo | Nuevo estado | Transición inválida, motivo requerido |
| `AppointmentStatus::bloqueaHorario` | Existe | Estado | `bool` (pendiente y confirmada bloquean) | — |
| `AppointmentRepository::hasOverlap` | Existe | tenant, médico, inicio, duración, excepto | `bool` | — |
| `AppointmentRepository::transaction` | Existe | `callable` | Resultado del callable | Revierte ante excepción |
| `DoctorAvailabilityRepository` | Existe | tenant, médico, especialidad o intervalo | `bool` | — |
| `TenantContext::tenantId` | Existe | — | Tenant del middleware | `RuntimeException` sin tenant |
| `AppointmentRepository::findByIdForUpdate` | Propuesto | tenant, id | Cita bloqueada o `null` | — |
| `AgendaLock::lockDoctorDay` | Propuesto | tenant, médico, fecha | `void` | Tiempo de espera agotado |
| `TimeSlot::overlaps` | Propuesto | Otro intervalo | `bool` | — |

## 3. Presentation — traducción de errores

| Situación | Hoy | Propuesto (`ErrorMapper`, contrato semana 5) |
|---|---|---|
| Regla de negocio incumplida | 422 `{message}` | 422 `{message, code, request_id}` |
| Horario ocupado | 422 `{message}` | **409** `APPOINTMENT_SLOT_TAKEN` |
| Violación del índice único | No se traduce | 409 `APPOINTMENT_SLOT_TAKEN` |
| Cita inexistente o de otro tenant | 404 `{message}` | 404 `APPOINTMENT_NOT_FOUND` |
| Formato inválido | 422 de `FormRequest` | Sin cambio |

## 4. Frontend — componentes Vue (todos propuestos)

La implementación de las semanas 4 a 6 se entrega como API, sin interfaz. Los
componentes siguientes se proponen sobre la base de interfaz de ASII-26 y son
los que usan los wireframes de la semana 8.

| Componente | Props (entrada) | Eventos (salida) | Estados que muestra | Endpoint |
|---|---|---|---|---|
| `AppointmentRequestView` | `role` del usuario | — | Paso activo | — |
| `PatientPicker` | `query` | `select(patientId)` | Vacío, cargando, sin resultados | ASII-03 |
| `DoctorSpecialtyFilter` | `specialties[]`, `doctors[]` | `change({specialtyId, doctorId, date})` | Cargando, error de carga | ASII-04 |
| `AvailabilitySlotGrid` | `slots[]`, `selected`, `loading` | `select(slot)` | Cargando, vacío, con horarios | Fuente de horarios libres* |
| `AppointmentSummaryDialog` | `draft` | `confirm()`, `back()` | Enviando, éxito, conflicto | `POST /appointments` |
| `AppointmentCard` + `StatusBadge` | `appointment` | `confirm(id)`, `cancel(id)` | Pendiente, confirmada, cancelada | `GET /appointments` |
| `CancelAppointmentDialog` | `appointment` | `submit(reason)`, `close()` | Validación, enviando, error | `PATCH /{id}/cancel` |
| `useAppointmentsApi` | Llamadas tipadas | `Promise<Result>` | Traduce `code` a mensaje | Todos |

\* Hoy no existe un endpoint que devuelva los horarios libres de un médico. El
contrato de la semana 5 lo prevé como interfaz de ASII-04
(`GET /api/v1/doctors/{id}/availability?date=`). La jornada tampoco se expone
hoy por HTTP: vive detrás de `DoctorAvailabilityRepository`. Se declara como
dependencia abierta con ASII-04 y no como parte de este refactor, que no amplía
el módulo.

### Reglas del cliente

- La interfaz decide qué mostrar según `code`, nunca según el texto de
  `message`.
- Ante `APPOINTMENT_SLOT_TAKEN`, la vista vuelve a la grilla, la recarga y
  conserva paciente, médico y motivo.
- `useAppointmentsApi` genera la `Idempotency-Key` una vez por borrador y la
  reutiliza al reintentar.
- Los botones se muestran según la matriz de roles de la semana 5; el backend
  vuelve a validar.
