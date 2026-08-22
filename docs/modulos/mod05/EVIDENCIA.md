# Evidencia de implementación

## Módulo

Micro-HIS Citas Médicas y Agenda

## Arquitectura implementada

El módulo fue desarrollado aplicando separación por capas:

- Domain:
  - Entidad Appointment.
  - Reglas de negocio.
  - Contratos Repository.

- Application:
  - Solicitud de citas.
  - Confirmación de citas.
  - Cancelación de citas.

- Persistence:
  - Implementación PDO con SQLite.
  - Repositorios InMemory para pruebas.

- Presentation:
  - AppointmentController como punto de entrada.

## Patrón aplicado

Repository Pattern.

Permite separar la lógica del negocio del mecanismo de almacenamiento.

## Validaciones ejecutadas

Comando:

php tests/run.php

Resultado:

4 pruebas aprobadas.
0 pruebas fallidas.

Casos validados:

- Creación, confirmación y cancelación de citas.
- Rechazo por horario no disponible.
- Rechazo por fecha pasada.
- Simulación de error de persistencia.

## Persistencia

Motor utilizado:

SQLite mediante PDO.

Características:

- Sentencias preparadas.
- Separación mediante repositorios.
- Validación de disponibilidad médica.

## Diagramas

Se incluyen:

- Caso de uso.
- Diagrama de clases.
- Diagrama de secuencia.
- Diagrama de componentes.
- Vista de datos.

## Repositorio

https://github.com/EddCastro/micro-his-citas-medicas-agenda
