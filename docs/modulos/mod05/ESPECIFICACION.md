# Especificación - Módulo Citas Médicas y Agenda

## Problema

El sistema requiere gestionar citas médicas permitiendo solicitar, validar disponibilidad, confirmar y cancelar citas dentro de un hospital.

## Actor principal

Paciente / Personal administrativo.

## Historia de usuario

Como usuario del sistema quiero registrar una cita médica para un paciente con un médico disponible, evitando conflictos de horario.

## Alcance

Incluye:
- Crear solicitud de cita.
- Validar disponibilidad del médico.
- Guardar cita.
- Confirmar cita.
- Cancelar cita.

## No alcance

- Facturación.
- Expediente clínico.
- Gestión de usuarios.

## Reglas de negocio

1. Una cita no puede registrarse en una fecha pasada.
2. Un médico no puede tener dos citas en el mismo intervalo.
3. Una cita solo puede confirmarse si existe disponibilidad.
4. La cancelación debe liberar el horario.

## Criterios de aceptación

- Una cita válida se registra correctamente.
- Una cita con colisión es rechazada.
- Una cita fuera del horario disponible es rechazada.
- Confirmar cambia el estado correctamente.
- Cancelar cambia el estado correctamente.

## Propiedad de datos

Los datos pertenecen a HOSPITAL.
Las referencias externas se manejan mediante UUID lógico.

## Contratos

RequestAppointment:
Entrada:
- patientId
- doctorId
- scheduledAt
- durationMinutes

Salida:
- appointmentId

Repository:
- save()
- findById()
- update()
