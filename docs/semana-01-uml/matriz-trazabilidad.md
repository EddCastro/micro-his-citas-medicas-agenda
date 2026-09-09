# Matriz de trazabilidad — Tarea 1 UML

## Módulo

**ASII-05: Citas médicas y agenda**

## Proceso modelado

Solicitud, validación de disponibilidad y confirmación o cancelación de cita.

## Actores principales

- Paciente.
- Recepcionista.
- Módulo de Médicos y Disponibilidad.
- Sistema de Notificaciones.

## Enunciado del proceso

El paciente solicita una cita médica por medio de recepción. La recepcionista registra los datos del paciente, médico, especialidad, fecha y hora solicitada. El sistema valida que el paciente se encuentre activo, que el médico atienda la especialidad indicada y que el horario esté disponible sin cruces con otras citas activas.

Cuando las validaciones son satisfactorias, la cita se registra inicialmente en estado pendiente. Posteriormente, el paciente puede confirmar la cita, cancelarla indicando un motivo o no responder. Cada cambio de estado debe quedar registrado y el resultado debe notificarse al paciente.

## Excepciones principales

| Código | Excepción | Resultado esperado |
|---|---|---|
| EX-01 | Paciente inexistente o inactivo | Se rechaza la solicitud y se informa el error. |
| EX-02 | Médico o especialidad no válidos | No se registra la cita y se solicita corregir los datos. |
| EX-03 | Horario fuera de la disponibilidad médica | Se informa que el horario no está disponible. |
| EX-04 | Cruce con otra cita activa | Se impide registrar la nueva cita en ese horario. |
| EX-05 | Paciente no confirma ni cancela | La cita permanece en estado pendiente. |

## Matriz requisito → diagrama → elemento UML

| Requisito | Descripción | Casos de uso | Actividad | Secuencia global |
|---|---|---|---|---|
| RF-01 | Registrar una solicitud de cita. | CU-01 Solicitar cita | Paciente solicita cita e ingreso de datos | Mensajes 1 al 3 |
| RF-02 | Validar que el paciente exista y esté activo. | CU-05 Validar paciente y datos | Decisión: ¿Paciente válido y activo? | Mensajes 5 al 11 |
| RF-03 | Validar médico y especialidad. | CU-02 Consultar disponibilidad médica | Decisión: ¿Médico y especialidad válidos? | Mensajes 12 al 17 |
| RF-04 | Verificar disponibilidad y cruces de horario. | CU-02 Consultar disponibilidad médica | Decisión: ¿Horario disponible? | Mensajes 18 al 23 |
| RF-05 | Crear la cita en estado pendiente. | CU-01 Solicitar cita | Registrar cita en estado pendiente | Mensajes 24 al 33 |
| RF-06 | Confirmar una cita pendiente. | CU-03 Confirmar cita | Rama: paciente confirma | Mensajes 34 al 44 |
| RF-07 | Cancelar una cita conservando el motivo. | CU-04 Cancelar cita | Rama: paciente cancela | Mensajes 45 al 55 |
| RF-08 | Registrar cada cambio de estado. | CU-06 Registrar cambio de estado | Registrar cambio de estado | INSERT appointment_status_history |
| RF-09 | Notificar el resultado al paciente. | CU-07 Notificar resultado | Notificación de registro, confirmación o cancelación | Servicio de Notificaciones |
| RF-10 | Mantener la cita pendiente cuando no exista respuesta. | CU-01 Solicitar cita | Rama: sin respuesta | Mensaje 56 |

## Coherencia entre diagramas

Los tres diagramas representan el mismo proceso:

1. El diagrama de casos de uso delimita actores y objetivos.
2. El diagrama de actividad representa decisiones, excepciones y resultados.
3. El diagrama de secuencia global muestra participantes, mensajes, validaciones y persistencia.

Los estados utilizados de manera consistente son:

- pendiente;
- confirmada;
- cancelada.

Los errores comunes modelados son:

- paciente no válido;
- médico o especialidad no válidos;
- falta de disponibilidad;
- cruce con otra cita activa.
