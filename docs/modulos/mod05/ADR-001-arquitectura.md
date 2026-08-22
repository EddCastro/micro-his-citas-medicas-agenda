# ADR-001 - Arquitectura por capas y Repository

## Estado

Aceptado.

## Contexto

El módulo de citas médicas requiere separar reglas del negocio, casos de uso y persistencia para facilitar mantenimiento, pruebas y evolución del sistema.

## Decisión

Se implementa una arquitectura dividida en:

## Domain

Responsable de:
- Entidades del negocio.
- Reglas de validación.
- Contratos Repository.

Componentes:
- Appointment.
- AppointmentRepository.
- AvailabilityRepository.

## Application

Responsable de ejecutar casos de uso:

- Solicitar cita.
- Confirmar cita.
- Cancelar cita.

No contiene lógica de almacenamiento.

## Persistence

Responsable del acceso a datos.

Implementaciones:

- PdoAppointmentRepository.
- PdoAvailabilityRepository.
- InMemory repositories para pruebas.

Utiliza:
- PDO.
- SQLite.
- Sentencias preparadas.

## Presentation

Responsable de recibir solicitudes externas y ejecutar casos de uso.

Componente:

- AppointmentController.

## Consecuencias positivas

- Separación clara de responsabilidades.
- Código más fácil de probar.
- Posibilidad de cambiar SQLite por otro motor.
- Pruebas independientes mediante dobles.

## Consecuencias negativas

- Mayor cantidad de clases.
- Requiere definir contratos antes de implementar persistencia.

## Alternativas descartadas

### Acceso directo a base de datos desde controlador

Descartado porque mezcla presentación, negocio y persistencia.

### Arquitectura monolítica sin capas

Descartada porque dificulta mantenimiento y pruebas.
