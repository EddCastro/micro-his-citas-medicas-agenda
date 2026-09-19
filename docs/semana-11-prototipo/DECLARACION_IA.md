# Declaración de uso de inteligencia artificial — Semana 11

## Identificación

| Dato | Información |
|---|---|
| Módulo | ASII-05 — Citas médicas y agenda |
| Estudiante | Eddy Adolfo Castro Véliz |
| Código | 1890-23-16857 |
| GitHub | EddCastro |
| Issue | #5 |
| Semana | 11 — Mejores prácticas para diseño móvil/web |
| Rama | `feature/week-11-prototipo` |

## Herramienta utilizada

Claude, de Anthropic, empleada como apoyo al análisis, al diseño, a la
redacción y a la generación de diagramas, maquetas y scripts de verificación.

La herramienta trabajó sobre una copia del repositorio en un entorno aislado.
La revisión, la publicación de las ramas y la apertura de los pull requests
corresponden al estudiante.

## Propósito del uso

- Completar el prototipo navegable con enrutamiento por pasos, roles y simulación de errores.
- Escribir el script de verificación con Playwright y axe-core ligado al backlog de la semana 9.
- Generar las capturas desktop y móvil y el mapa de navegación.

## Prompts relevantes

1. Construir un prototipo navegable desktop y móvil del flujo con camino feliz y un error crítico de concurrencia.
2. Mantener los roles de la matriz de la semana 5 y los estados del dominio.
3. Escribir una verificación automática por cada criterio verificable del backlog de la semana 9.
4. Comprobar que las reglas de los campos coincidan con los FormRequest del backend.
5. Generar el mapa de navegación y las capturas de cada paso en ambos tamaños.

## Contenido aceptado

- El error de concurrencia como error crítico del prototipo.
- La trampa de foco en los diálogos, agregada después de que la verificación detectara que Tab salía del diálogo.
- La verificación automatizada como evidencia de cada criterio del backlog y de las reglas del backend.

## Contenido modificado o rechazado

- Se descartó usar Figma u otra herramienta externa: un prototipo HTML se abre sin cuentas y se puede verificar automáticamente.
- Se descartó conectar el prototipo al backend Laravel: la consigna pide un prototipo del flujo, no la integración.
- Se descartó presentar el 409 como respuesta actual del backend; se documenta como diseño propuesto.

## Errores detectados y corregidos

| Hallazgo | Corrección |
|---|---|
| La primera verificación falló en H-09: con Tab el foco salía del diálogo de cancelación. | Se agregó la trampa de foco en los diálogos; la verificación pasó a cumplir. |
| La comprobación de H-01 solo veía citas pendientes porque la agenda mostraba el día de la cita nueva. | La prueba cambia a la fecha con los tres estados antes de comprobar. |
| Las capturas de escritorio cortaban los botones inferiores. | Se capturan a página completa. |

## Validación humana

El estudiante recorrió el prototipo en escritorio y en teléfono con los tres roles, ejecutó la verificación automatizada (40 de 40 criterios, código de salida `0`), validó el mapa con `-checkonly` (código de salida `0`) y revisó cada captura.

## Responsabilidad académica

La inteligencia artificial se empleó como herramienta de apoyo. El diseño, las
decisiones, la validación y la preparación para la defensa oral corresponden
al estudiante, quien asume la responsabilidad académica sobre el contenido
entregado.
