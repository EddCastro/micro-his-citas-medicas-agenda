# Reglas de interacción, estados y mensajes — Semana 8

Reglas del flujo **solicitud, validación de disponibilidad y confirmación o
cancelación de cita**. Los identificadores W1–W6 remiten a los wireframes.

## 1. Roles autorizados y lo que ve cada uno

Matriz tomada del contrato de API de la semana 5.

| Rol | Pantalla de inicio | Puede agendar | Puede confirmar | Puede cancelar | Ve el motivo |
|---|---|:---:|:---:|:---:|:---:|
| Recepcionista | Agenda del día (todos los médicos) | Sí | Sí | Sí | En el detalle |
| Admin | Igual que Recepcionista | Sí | Sí | Sí | En el detalle |
| Enfermera | Agenda filtrada en "Pendientes" | No | Sí | No | En el detalle |
| Médico | "Mi agenda", solo lectura | No | No | No | En el detalle |

Las acciones no permitidas **no se muestran**. El backend vuelve a validar el
permiso; ocultar un botón no es un control de seguridad.

## 2. Estructura del flujo principal

| Paso | Pantalla | Decisión del usuario | Salida |
|---|---|---|---|
| Inicio | W1 | Pulsar "Nueva cita" | Paso 1 |
| 1 | W2 | Elegir paciente | Paso 2 o ayuda "registrar en Pacientes" |
| 2 | W2 | Especialidad, médico, fecha, duración | Paso 3 |
| 3 | W3 | Elegir un horario libre | Paso 4 o siguiente fecha con horarios |
| 4 | W4 | Revisar y escribir motivo | Agendar |
| Fin | W5 | — | Cita en estado pendiente |
| Confirmar | W6 | Enfermera registra medio de contacto | Estado confirmada |
| Cancelar | W6 | Recepcionista escribe motivo y confirma | Estado cancelada, horario libre |

## 3. Estados de pantalla

| Estado | Dónde | Comportamiento |
|---|---|---|
| Carga | W1, W3 | Esqueleto con la forma del contenido; el resto de la interfaz sigue usable |
| Vacío | W1 | "No hay citas para este día" + "Nueva cita" (solo si el rol puede) |
| Vacío | W3 | "Sin horarios el <fecha>" + botón a la siguiente fecha con horarios |
| Enviando | W4, W6 | Texto del botón cambia ("Agendando…"), botón deshabilitado |
| Éxito | W5 | Aviso con código de cita, fila resaltada, siguiente paso explicado |
| Error recuperable | W2, W4, W6 | Mensaje con causa y acción; los datos capturados se conservan |

## 4. Catálogo de mensajes

| Situación | Código | Mensaje | Acción ofrecida |
|---|---|---|---|
| Paciente inexistente | — | No encontramos a "<texto>". Verifique el dato o regístrelo en el módulo Pacientes. | Buscar de nuevo |
| Fecha pasada | `APPOINTMENT_PAST_DATE` | Elija una fecha a partir de hoy. | El calendario ya lo impide |
| Fuera de jornada | `DOCTOR_OUTSIDE_WORKING_HOURS` | El médico no atiende en ese horario. | Volver a W3 |
| Horario tomado | `APPOINTMENT_SLOT_TAKEN` | Otro usuario tomó ese horario. Elija otro. | Grilla recargada |
| Motivo de cancelación vacío | `APPOINTMENT_CANCEL_REASON_REQUIRED` | Campo requerido | Foco en el campo |
| Transición inválida | `APPOINTMENT_INVALID_TRANSITION` | Esta cita ya fue cancelada o confirmada por otra persona. | Detalle recargado |
| Sin conexión | — | No pudimos confirmar el registro. Revise la conexión y reintente. | Reintentar (misma clave) |
| Sesión expirada | 401 | Su sesión expiró. | Iniciar sesión |
| Sin permiso | 403 | No tiene permiso para esta acción. | Volver a la agenda |

Los mensajes se eligen por `code`, no por el texto que devuelve el servidor.
Hoy el backend responde 422 con solo `message`; los códigos son los del
contrato de la semana 5 y el `ErrorMapper` propuesto en la semana 7.

## 4.1 Validaciones de formato

Tomadas de los `FormRequest` del backend, para que la interfaz no pida más ni
menos que el servidor.

| Campo | Regla | Origen |
|---|---|---|
| Paciente, médico, especialidad | Obligatorios | `StoreAppointmentRequest` |
| Fecha y hora | Obligatoria, futura | `StoreAppointmentRequest`, RN-01 |
| Duración | 5 a 480 minutos (la interfaz ofrece 15, 30, 45 y 60) | `StoreAppointmentRequest` |
| Motivo de la consulta | Opcional, máximo 500 caracteres | `StoreAppointmentRequest` |
| Motivo de cancelación | Obligatorio, 3 a 500 caracteres | `CancelAppointmentRequest`, RN-12 |

## 5. Reglas de interacción

1. **Prevenir antes que corregir.** El calendario no ofrece fechas pasadas, el
   médico se filtra por especialidad y la grilla solo permite horarios libres.
2. **Consultar no reserva.** La grilla es una foto del momento; la validación
   definitiva ocurre al agendar, bajo bloqueo del médico y día.
3. **Nunca perder lo capturado.** Ante 409, 422, falta de conexión o sesión
   expirada se conservan paciente, médico, horario y motivo.
4. **Un clic, una cita.** El botón se deshabilita al enviar y el reintento usa
   la misma `Idempotency-Key`.
5. **Acción destructiva con confirmación.** Cancelar exige diálogo con los
   datos de la cita y motivo obligatorio.
6. **Volver atrás sin castigo.** Los pasos completados se pueden reabrir desde
   el indicador de pasos o desde "Editar" en el resumen.

## 6. Ayuda contextual

| Punto | Ayuda |
|---|---|
| W2, búsqueda | Texto de ejemplo: "nombre, DPI o No. de expediente" |
| W2, médico | "Filtrado por especialidad" |
| W3, ícono ⓘ | "¿Por qué no veo un horario? Está fuera de la jornada del médico u ocupado por otra cita." |
| W4, pie | "La cita se crea en estado pendiente hasta que Enfermería confirme la asistencia." |
| W4, motivo de consulta | "Opcional" + contador de caracteres (máximo 500) |

## 7. Protección de datos

| Regla | Aplicación |
|---|---|
| Minimización en listas | La agenda muestra nombre e iniciales de apellidos; sin DPI, teléfono ni motivo |
| DPI enmascarado | Solo los 4 últimos dígitos en la búsqueda de paciente |
| Motivo solo en detalle | Abrir el detalle queda registrado en auditoría (ASII-22) |
| Sin datos en la URL | La navegación usa el id de la cita, nunca nombre ni DPI |
| Aislamiento por hospital | Una cita de otro hospital responde igual que una inexistente (404) |
| Sesión | Al expirar, el borrador se conserva solo en memoria del navegador, no en almacenamiento persistente |
