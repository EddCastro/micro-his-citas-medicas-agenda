# Módulo 05 — Citas médicas y agenda

## Descripción del problema

La programación manual o poco organizada de citas médicas puede provocar cruces de horarios, espacios sin utilizar, pacientes sin confirmar y dificultad para encontrar nuevas fechas cuando una cita es cancelada.

También puede suceder que un paciente necesite cambiar su cita y el personal tenga que revisar manualmente la agenda de varios médicos. Si se libera un horario, normalmente no existe un proceso automático para ofrecérselo a otro paciente que esté esperando atención.

El módulo de citas médicas y agenda busca centralizar estas actividades y mantener un control ordenado de la disponibilidad, confirmación, cancelación y reagendamiento de las citas.

## Objetivo

Desarrollar un módulo que permita al personal autorizado consultar la disponibilidad de los médicos, programar citas, confirmar la asistencia de los pacientes, cancelar o reagendar citas y administrar una lista de espera para aprovechar los horarios que sean liberados.

El módulo debe mantener la trazabilidad de los cambios y separar la información de cada hospital mediante el tenant correspondiente.

## Alcance

El módulo inicia cuando un usuario autorizado necesita consultar la disponibilidad de un médico o especialidad.

Después de encontrar un horario disponible, el sistema permite registrar una cita asociada con un paciente, médico, especialidad, fecha, hora y duración.

Antes de la fecha programada, una enfermera o un usuario autorizado podrá contactar al paciente y registrar si la cita fue confirmada.

Cuando un paciente no pueda asistir, la cita podrá cancelarse o reagendarse. En caso de reagendamiento, el sistema deberá consultar nuevamente los horarios disponibles y conservar la relación entre la cita original y la nueva cita.

Cuando una cancelación libere un horario, el sistema revisará la lista de espera y podrá generar una oferta para otro paciente compatible. La oferta tendrá un tiempo limitado para ser aceptada antes de pasar al siguiente paciente.

El módulo también permitirá al médico consultar su agenda por día o por rango de fechas.

## Funcionalidades incluidas

\- Consulta de disponibilidad por médico o especialidad.

\- Programación de citas médicas.

\- Consulta de agenda por médico.

\- Confirmación de citas.

\- Registro del medio y resultado del contacto con el paciente.

\- Cancelación de citas con motivo.

\- Reagendamiento hacia una fecha disponible.

\- Conservación del historial de citas anteriores.

\- Registro de pacientes en lista de espera.

\- Liberación de horarios cancelados.

\- Oferta de espacios disponibles a pacientes en espera.

\- Validación para evitar citas cruzadas.

\- Separación de información por tenant.

\- Control de acceso para usuarios autorizados.

## Límites

\- No incluye el registro general de pacientes, porque corresponde al módulo de pacientes.

\- No incluye la administración completa de médicos y especialidades.

\- No define los horarios laborales, vacaciones o ausencias de los médicos.

\- No implementa por completo el sistema general de roles y permisos.

\- No desarrolla el módulo general de notificaciones del hospital.

\- No incluye consultas médicas, diagnósticos, recetas ni expediente clínico.

\- No elimina citas anteriores cuando se realiza un reagendamiento.

\- No asigna prioridades clínicas de manera automática sin autorización del personal.

## Actores principales

### Recepcionista

Consulta disponibilidad, programa citas, registra cancelaciones, realiza reagendamientos y administra la lista de espera.

### Médico

Consulta las citas asignadas dentro de su agenda y revisa la información básica necesaria para atender al paciente.

### Enfermera

Consulta las citas próximas, contacta al paciente y registra el resultado de la confirmación.

### Paciente

Solicita una cita, confirma su asistencia, cancela, pide un cambio de fecha o acepta un espacio que fue liberado.

### Administrador

Configura las reglas generales del módulo y controla si la funcionalidad de citas se encuentra habilitada.

### Sistema de notificaciones

Envía recordatorios, confirmaciones y avisos cuando un horario queda disponible.

## Dependencias

\- Módulo 02: roles y permisos.

\- Módulo 03: pacientes.

\- Módulo 04: médicos, especialidades y disponibilidad.

\- Módulo 21: alertas y notificaciones internas.

\- Módulo 22: auditoría de movimientos.

\- Módulo 25: QA, pruebas E2E y CI.

\- Módulo 26: diseño base de la interfaz.

## Reglas iniciales del negocio

1\. Una cita debe pertenecer al mismo tenant que el paciente, el médico y el usuario que la registra.

2\. No se puede programar una cita en una fecha anterior a la actual.

3\. No se puede asignar al mismo médico a dos citas que se crucen en el tiempo.

4\. La fecha seleccionada debe encontrarse dentro de la disponibilidad del médico.

5\. Toda cancelación debe conservar su motivo, fecha y usuario responsable.

6\. Una cita reagendada no debe eliminar la cita original.

7\. Un espacio liberado solo puede ser aceptado por un paciente.

8\. La oferta de un espacio liberado debe tener una fecha de vencimiento.

9\. Las notificaciones no deben revelar información clínica sensible.

10\. Las acciones deben limitarse según el rol y los permisos del usuario.

## Flujo general

1\. El personal consulta la disponibilidad del médico.

2\. El sistema muestra los horarios disponibles.

3\. Se selecciona al paciente y se programa la cita.

4\. Antes de la fecha, se realiza el proceso de confirmación.

5\. El paciente puede confirmar, cancelar o solicitar reagendamiento.

6\. Si la cita se cancela, el horario vuelve a estar disponible.

7\. El sistema revisa la lista de espera.

8\. Se ofrece el espacio a un paciente compatible.

9\. Si el paciente acepta, se programa la nueva cita.

10\. Si la oferta vence, se continúa con el siguiente paciente.
