# Declaración de uso de inteligencia artificial

## Datos generales

- **Estudiante:** Eddy Adolfo Castro Véliz
- **Módulo:** ASII-05 — Citas médicas y agenda
- **Actividad:** Diagramas UML por módulo
- **Herramienta utilizada:** ChatGPT de OpenAI

## Propósito del uso

La herramienta de inteligencia artificial se utilizó como apoyo para:

- analizar la consigna asignada;
- organizar el flujo de solicitud, validación, confirmación y cancelación de citas;
- proponer una estructura inicial para los diagramas UML;
- generar borradores de código PlantUML;
- revisar la coherencia entre los diagramas;
- orientar la generación de imágenes PNG;
- apoyar la elaboración de la matriz de trazabilidad.

## Prompts e instrucciones relevantes

Entre las instrucciones proporcionadas a la herramienta se incluyeron:

- analizar el módulo ASII-05: Citas médicas y agenda;
- modelar el proceso de solicitud, validación de disponibilidad y confirmación o cancelación de cita;
- generar diagramas de casos de uso, actividad y secuencia global;
- mantener coherencia entre actores, decisiones, mensajes y excepciones;
- utilizar PlantUML como fuente editable;
- incluir trazabilidad entre requisitos y elementos UML.

## Partes aceptadas

Se aceptaron y utilizaron como base:

- la estructura general de los tres diagramas;
- los nombres de actores y participantes;
- los flujos principales y alternativos;
- las excepciones de paciente inválido, médico o especialidad no válidos y horario no disponible;
- la estructura de la matriz de trazabilidad;
- los comandos para validar y generar los diagramas con PlantUML.

## Partes revisadas o modificadas

Durante la revisión se realizaron los siguientes ajustes:

- se separó el diagrama general de la Semana 1 del proceso específico solicitado en la tarea;
- se corrigió el formato de mensajes multilínea del diagrama de secuencia;
- se modificó la distribución del diagrama de casos de uso para mejorar su legibilidad;
- se sustituyeron algunas flechas de asociación por líneas simples;
- se agruparon objetivo, excepciones y resultados en una leyenda;
- se verificó que los estados pendiente, confirmada y cancelada fueran consistentes en los tres diagramas.

## Validación humana

La validación fue realizada manualmente mediante:

- revisión del código fuente `.puml`;
- validación sintáctica con PlantUML usando `-checkonly`;
- generación local de imágenes PNG;
- inspección visual de cada diagrama;
- comparación entre los diagramas y la consigna individual;
- revisión de la matriz de trazabilidad.

El resultado de la validación de PlantUML fue exitoso, con código de salida `0`.

## Responsabilidad académica

La inteligencia artificial se utilizó únicamente como herramienta de apoyo. La ejecución de los comandos, revisión de archivos, validación visual, decisiones finales y preparación para la defensa oral corresponden al estudiante.
