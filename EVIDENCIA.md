# Evidencia de implementación

## Módulo
Micro-HIS Citas Médicas y Agenda

## Arquitectura

- Domain: reglas del negocio y entidad Appointment.
- Application: casos de uso para solicitar, confirmar y cancelar citas.
- Persistence: repositorios PDO SQLite y dobles InMemory.
- Presentation: controlador de entrada.

## Validaciones realizadas

Ejecutado:

php tests/run.php

Resultado:

4 pruebas aprobadas.
0 pruebas fallidas.

Casos comprobados:

- Solicitud, confirmación y cancelación de cita.
- Rechazo por horario no disponible.
- Rechazo de fecha pasada.
- Error de persistencia simulado.

## Persistencia

SQLite mediante PDO con sentencias preparadas.

## Repositorio

https://github.com/EddCastro/micro-his-citas-medicas-agenda
