# Declaración de uso de inteligencia artificial — Semana 7

| Dato | Información |
|---|---|
| Módulo | ASII-05 — Citas médicas y agenda |
| Estudiante | Eddy Adolfo Castro Véliz |
| Código | 1890-23-16857 |
| Semana | 7 — Diseño de componentes y refactorización |

## Herramienta utilizada

Claude, de Anthropic, como apoyo al análisis, a la redacción y a la generación
de diagramas y maquetas.

## Propósito

- Identificar el punto de mayor acoplamiento a partir del código real del módulo.
- Proponer la separación en política de dominio, puertos y adaptadores.
- Redactar los contratos de entrada y salida de cada componente.
- Generar los diagramas PlantUML de componentes y antes/después.

## Contenido aceptado

- La elección de `isAvailable()` como punto de mayor acoplamiento, respaldada por la tabla de responsabilidades.
- La separación en `SlotPolicy`, `TimeSlot`, `DoctorScheduleProvider`, `AgendaReader`, `TransactionRunner` y `AgendaLock`.
- El `ErrorMapper` como único punto de traducción de excepciones a códigos HTTP.

## Contenido modificado o rechazado

- Se descartó implementar el refactor en código en esta semana: la consigna pide un refactor conceptual y sin ampliar el módulo.
- Se rechazó agregar reagendamiento o lista de espera a los componentes, por estar fuera del flujo asignado.
- Se mantuvieron los códigos de error del contrato de la semana 5 en lugar de crear códigos nuevos.

## Validación humana

El estudiante comparó el "antes" con el código real de `PdoAvailabilityRepository` y con el cambio práctico de la semana 6, verificó que los contratos coincidan con el contrato de API de la semana 5 y revisó que los diagramas se generen sin errores.

## Responsabilidad académica

Las decisiones de diseño y la preparación para la defensa oral corresponden al
estudiante, quien asume la responsabilidad académica sobre el contenido
entregado.
