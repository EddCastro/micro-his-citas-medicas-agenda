# Declaración de uso de inteligencia artificial — Semana 9

## Identificación

| Dato | Información |
|---|---|
| Módulo | ASII-05 — Citas médicas y agenda |
| Estudiante | Eddy Adolfo Castro Véliz |
| Código | 1890-23-16857 |
| GitHub | EddCastro |
| Issue | #5 |
| Semana | 9 — Evaluación del diseño, usabilidad y accesibilidad |
| Rama | `feature/week-09-usabilidad` |

## Herramienta utilizada

Claude, de Anthropic, empleada como apoyo al análisis, al diseño, a la
redacción y a la generación de diagramas, maquetas y scripts de verificación.

La herramienta trabajó sobre una copia del repositorio en un entorno aislado.
La revisión, la publicación de las ramas y la apertura de los pull requests
corresponden al estudiante.

## Propósito del uso

- Recorrer los wireframes de la semana 8 contra las heurísticas de Nielsen y WCAG 2.2 AA.
- Escribir el script que mide contrastes y operabilidad por teclado y recorta la evidencia.
- Proponer la fórmula de priorización y los criterios verificables.

## Prompts relevantes

1. Evaluar el flujo UX de la semana 8 con las 10 heurísticas de Nielsen y WCAG 2.2 AA en teclado, foco, contraste, etiquetas, mensajes y prevención de errores.
2. Medir el contraste de cada color usado en los wireframes con la fórmula de luminancia relativa.
3. Contar cuántos horarios de la grilla son alcanzables con Tab.
4. Proponer una priorización que pese más los fallos que afectan citas, cancelación y concurrencia.
5. Redactar para cada corrección un criterio que pueda comprobarse con sí o no.

## Contenido aceptado

- Los 11 hallazgos, respaldados por capturas y mediciones reproducibles.
- La fórmula severidad × frecuencia × peso del concepto.
- La promoción de H-01 y H-03 a P1 por bloquear por completo la tarea.

## Contenido modificado o rechazado

- Se descartó reportar como hallazgo el tamaño de los horarios: 34 px supera el mínimo de 24 px de WCAG 2.5.8.
- Se descartó marcar como fallo la autenticación accesible, porque corresponde a ASII-01.
- Se ajustó la severidad de H-11 a 1 por ser un problema cosmético de bordes.

## Errores detectados y corregidos

| Hallazgo | Corrección |
|---|---|
| El resumen del checklist contaba 6 criterios parciales y 11 no cumplidos, pero la tabla tenía 5 y 12. | Se recontaron los 19 criterios y se corrigió el resumen. |
| El aviso de éxito verde también incumplía contraste (4.11:1), y no estaba previsto en la lista de hallazgos. | Se incorporó a H-05 con su medición. |

## Validación humana

El estudiante ejecutó el script de medición (código de salida `0`), comparó cada ratio con el mínimo de WCAG, revisó que cada captura muestre el problema descrito y recontó los totales del checklist.

## Responsabilidad académica

La inteligencia artificial se empleó como herramienta de apoyo. El diseño, las
decisiones, la validación y la preparación para la defensa oral corresponden
al estudiante, quien asume la responsabilidad académica sobre el contenido
entregado.
