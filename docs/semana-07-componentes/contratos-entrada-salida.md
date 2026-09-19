# Contratos de entrada y salida — Semana 7

Contratos de los componentes del flujo **solicitud, validación de
disponibilidad y confirmación o cancelación de cita**. Cada contrato indica qué
recibe el componente, qué devuelve y qué errores puede producir. Los códigos de
negocio son los definidos en el contrato de API de la semana 5.

## 1. Backend — casos de uso (capa Application)

### QueryAvailability

| Aspecto | Definición |
|---|---|
| Entrada | `doctorId: int`, `date: Y-m-d`, `durationMin: int` (15–120) |
| Salida | `TimeSlot[]` libres, ordenados por hora de inicio |
| Errores | `422 APPOINTMENT_INVALID_DURATION`, `404` médico inexistente en el tenant |
| Efectos | Ninguno. Solo lectura, sin bloqueo |
| Expuesto como | `GET /api/v1/doctors/{id}/availability?date=&duration=` |

### RequestAppointment

| Aspecto | Definición |
|---|---|
| Entrada | `RequestAppointmentInput { patientId, doctorId, specialtyId, scheduledAt, durationMin, reason, idempotencyKey }` |
| Salida | `AppointmentOutput { id, status: "pendiente", scheduledAt, endsAt, doctorId, patientId }` |
| Errores | `422 APPOINTMENT_PAST_DATE`, `422 APPOINTMENT_INVALID_DURATION`, `422 DOCTOR_OUTSIDE_WORKING_HOURS`, `409 APPOINTMENT_SLOT_TAKEN` |
| Efectos | Una fila en `appointments`; evento de auditoría |
| Concurrencia | Bloqueo del par médico + día dentro de la transacción; índice único parcial como segunda defensa |
| Idempotencia | La misma `Idempotency-Key` devuelve la cita ya creada, sin duplicarla |

### ConfirmAppointment

| Aspecto | Definición |
|---|---|
| Entrada | `appointmentId: int`, `contactChannel` (teléfono, correo, presencial), `note?` |
| Salida | `AppointmentOutput` con `status: "confirmada"` |
| Errores | `404` cita inexistente o de otro tenant, `422 APPOINTMENT_INVALID_TRANSITION` |
| Efectos | Cambio de estado y registro del medio de contacto |

### CancelAppointment

| Aspecto | Definición |
|---|---|
| Entrada | `appointmentId: int`, `reason: string` (obligatorio, 5–250 caracteres) |
| Salida | `AppointmentOutput` con `status: "cancelada"` |
| Errores | `404`, `422 APPOINTMENT_INVALID_TRANSITION`, `422 APPOINTMENT_CANCEL_REASON_REQUIRED` |
| Efectos | Cambio de estado; el intervalo queda libre porque el índice parcial excluye canceladas |

## 2. Backend — dominio y puertos

| Componente | Entrada | Salida | Errores |
|---|---|---|---|
| `TimeSlot` | `start`, `end` | Objeto inmutable; `overlaps()`, `within()` | `InvalidTimeSlot` si `end <= start` |
| `SlotPolicy::assertBookable` | Turnos del médico, citas activas, intervalo pedido | `void` | `OutsideWorkingHours`, `SlotTaken` |
| `SlotPolicy::freeSlots` | Turnos, citas activas, duración | `TimeSlot[]` | — |
| `Appointment::confirm / cancel` | — / motivo | Nuevo estado | `InvalidTransition` |
| `DoctorScheduleProvider::shiftsOf` | `doctorId`, `date` | `TimeSlot[]` de jornada | `ScheduleUnavailable` → se rechaza, no se agenda a ciegas |
| `AgendaReader::busySlotsOf` | `doctorId`, `date` | `TimeSlot[]` de citas pendientes o confirmadas | — |
| `AgendaLock::lockDoctorDay` | `doctorId`, `date` | `void` | Tiempo de espera agotado → `409` |
| `TransactionRunner::run` | `callable` | Resultado del callable | Revierte ante cualquier excepción |

## 3. Presentation — traducción de errores

`ErrorMapper` es el único lugar donde una excepción de dominio se convierte en
respuesta HTTP:

| Excepción | HTTP | `code` |
|---|---|---|
| `PastDate` | 422 | `APPOINTMENT_PAST_DATE` |
| `OutsideWorkingHours` | 422 | `DOCTOR_OUTSIDE_WORKING_HOURS` |
| `SlotTaken` | 409 | `APPOINTMENT_SLOT_TAKEN` |
| `InvalidTransition` | 422 | `APPOINTMENT_INVALID_TRANSITION` |
| `CancelReasonRequired` | 422 | `APPOINTMENT_CANCEL_REASON_REQUIRED` |
| `AppointmentNotFound` | 404 | `APPOINTMENT_NOT_FOUND` |

## 4. Frontend — componentes Vue

| Componente | Props (entrada) | Eventos (salida) | Estados que muestra |
|---|---|---|---|
| `AppointmentRequestView` | `role` del usuario autenticado | — | Orquesta el paso activo |
| `PatientPicker` | `query` | `select(patientId)` | vacío, cargando, sin resultados |
| `DoctorSpecialtyFilter` | `specialties[]`, `doctors[]` | `change({specialtyId, doctorId, date})` | cargando, error de carga |
| `AvailabilitySlotGrid` | `slots[]`, `selected`, `loading` | `select(slot)` | cargando, vacío ("sin horarios"), con horarios |
| `AppointmentSummaryDialog` | `draft` (paciente, médico, horario, motivo) | `confirm()`, `back()` | enviando, éxito, conflicto 409 |
| `AppointmentCard` + `StatusBadge` | `appointment` | `confirm(id)`, `cancel(id)` | pendiente, confirmada, cancelada (texto + ícono) |
| `CancelAppointmentDialog` | `appointment` | `submit(reason)`, `close()` | validación del motivo, enviando, error |
| `useAppointmentsApi` | Llamadas tipadas | `Promise<Result>` | Convierte `code` en mensaje de usuario |

### Reglas del cliente

- `useAppointmentsApi` genera la `Idempotency-Key` una sola vez por borrador de
  cita y la reutiliza si el usuario reintenta, para que un doble clic o una
  reconexión no creen dos citas.
- La interfaz decide qué mostrar según `code`, nunca según el texto de
  `message`.
- Ante `409 APPOINTMENT_SLOT_TAKEN`, la vista vuelve a `AvailabilitySlotGrid`,
  recarga los horarios y conserva paciente, médico y motivo ya capturados.
- Los botones Confirmar y Cancelar se muestran solo si el rol tiene el permiso
  de la matriz de la semana 5; el backend vuelve a validarlo.
