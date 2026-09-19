# Declaración de uso de inteligencia artificial — Semana 7

## Identificación

| Dato | Información |
|---|---|
| Módulo | ASII-05 — Citas médicas y agenda |
| Estudiante | Eddy Adolfo Castro Véliz |
| Código | 1890-23-16857 |
| GitHub | EddCastro |
| Issue | #5 |
| Semana | 7 — Diseño de componentes y refactorización |
| Rama | `feature/week-07-componentes` |

## Herramienta utilizada

Claude, de Anthropic, empleada como apoyo al análisis, al diseño, a la
redacción y a la generación de diagramas, maquetas y scripts de verificación.

La herramienta trabajó sobre una copia del repositorio en un entorno aislado.
La revisión, la publicación de las ramas y la apertura de los pull requests
corresponden al estudiante.

## Propósito del uso

- Revisar el código Laravel del módulo (rama de la semana 6) para identificar el punto de mayor acoplamiento.
- Proponer la separación del bloqueo, la definición única del cruce y la tipificación de errores.
- Redactar los contratos de entrada y salida separando lo existente de lo propuesto.
- Generar los diagramas PlantUML de componentes y de antes y después.

## Prompts relevantes

1. Revisar los casos de uso, puertos y adaptadores del módulo e indicar cuál concentra más conceptos entre citas, agenda, disponibilidad, confirmación, cancelación y concurrencia.
2. Analizar si el bloqueo pesimista de la semana 6 puede dejar de aplicarse sin que ninguna prueba falle.
3. Revisar si confirmar y cancelar son seguros ante dos usuarios simultáneos.
4. Proponer un refactor conceptual que no amplíe el módulo ni contradiga las decisiones D-13, D-14, D-29 y D-30.
5. Separar en los contratos lo implementado de lo propuesto, como en la matriz de la semana 6.

## Contenido aceptado

- La elección de `hasOverlap()` como punto de mayor acoplamiento, con la tabla de conceptos que lo respalda.
- El hallazgo de la escritura concurrente en confirmar y cancelar.
- El puerto `AgendaLock`, `findByIdForUpdate`, `TimeSlot` como referencia de pruebas y `ErrorMapper`.

## Contenido modificado o rechazado

- Se descartó mover la detección de cruces a memoria: contradice la decisión D-14.
- Se descartó un bloqueo optimista con columna de versión: obliga a modificar la tabla `appointments` (D-13).
- Se descartó implementar el refactor en esta semana: la consigna pide un refactor conceptual.
- Se descartó incluir reagendamiento en el flujo, aunque se beneficia del mismo cambio.

## Errores detectados y corregidos

| Hallazgo | Corrección |
|---|---|
| La primera versión analizó el micro-monolito PHP de `main` y afirmaba que jornada y ocupación estaban en el mismo adaptador; en Laravel ya están separadas (D-11). | Se rehízo el análisis sobre el código real de la rama de la semana 6. |
| Los contratos daban el motivo de cancelación como 5–250 caracteres y el motivo de consulta como obligatorio. | Se corrigieron con las reglas reales: cancelación 3–500 en `CancelAppointmentRequest`; motivo de consulta opcional, máximo 500. |
| Se presentaban `ErrorMapper` y la clave de idempotencia como si existieran. | Se marcaron como propuestos en el diagrama y en los contratos. |

## Validación humana

El estudiante comparó cada fragmento del "antes" con los archivos de la rama `feature/asii-05-semana-06-parcial-eddcastro`, verificó que las decisiones de las semanas 4 a 6 se respeten, validó los diagramas con `-checkonly` (código de salida `0`) y revisó que ningún elemento propuesto se presente como implementado.

## Responsabilidad académica

La inteligencia artificial se empleó como herramienta de apoyo. El diseño, las
decisiones, la validación y la preparación para la defensa oral corresponden
al estudiante, quien asume la responsabilidad académica sobre el contenido
entregado.
