# Tarea 1 — Diagramas UML por módulo

## Datos generales

- **Estudiante:** Eddy Adolfo Castro Véliz
- **GitHub:** EddCastro
- **Módulo:** ASII-05 — Citas médicas y agenda
- **Proceso asignado:** Solicitud, validación de disponibilidad y confirmación o cancelación de cita

## Objetivo

Modelar mediante UML el proceso de solicitud de una cita médica, la validación del paciente y de la disponibilidad del médico, así como los resultados de confirmación, cancelación o permanencia en estado pendiente.

## Diagramas elaborados

### Casos de uso

Delimita los actores, objetivos y funciones principales del módulo.

Archivos:

- `casos-de-uso-solicitud-cita.puml`
- `casos-de-uso-solicitud-cita.png`

### Actividad

Representa el flujo principal, las decisiones, las excepciones y los resultados.

Archivos:

- `actividad-solicitud-cita.puml`
- `actividad-solicitud-cita.png`

### Secuencia global

Muestra los participantes, mensajes, validaciones, consultas y respuestas del proceso.

Archivos:

- `secuencia-global-solicitud-cita.puml`
- `secuencia-global-solicitud-cita.png`

## Documentación complementaria

- `matriz-trazabilidad.md`: relaciona requisitos con elementos de los tres diagramas.
- `DECLARACION_IA.md`: documenta el uso de inteligencia artificial y la validación humana.
- `GUIA_DEFENSA_ORAL.md`: contiene los puntos necesarios para explicar y modificar el trabajo.
- `GENERACION_DIAGRAMAS.md`: explica cómo validar las fuentes y generar las imágenes PNG.

## Estados modelados

- pendiente;
- confirmada;
- cancelada.

## Excepciones modeladas

- paciente inexistente o inactivo;
- médico o especialidad no válidos;
- horario no disponible;
- cruce con otra cita activa;
- ausencia de respuesta del paciente.

## Validación

Los tres archivos PlantUML fueron validados localmente con:

    java -jar "$HOME\Tools\PlantUML\plantuml.jar" -checkonly ".\docs\module-05\tarea-01-uml\*.puml"

El comando finalizó con código de salida `0`.

Las imágenes fueron generadas mediante:

    java -jar "$HOME\Tools\PlantUML\plantuml.jar" -tpng ".\docs\module-05\tarea-01-uml\*.puml"

## Datos utilizados

Todos los nombres y datos representados son ficticios. Los diagramas no contienen información clínica identificable.
