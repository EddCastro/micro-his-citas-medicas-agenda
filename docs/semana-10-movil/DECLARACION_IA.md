# Declaración de uso de inteligencia artificial — Semana 10

## Identificación

| Dato | Información |
|---|---|
| Módulo | ASII-05 — Citas médicas y agenda |
| Estudiante | Eddy Adolfo Castro Véliz |
| Código | 1890-23-16857 |
| GitHub | EddCastro |
| Issue | #5 |
| Semana | 10 — Diseño para movilidad |
| Rama | `feature/week-10-movil` |

## Herramienta utilizada

Claude, de Anthropic, empleada como apoyo al análisis, al diseño, a la
redacción y a la generación de diagramas, maquetas y scripts de verificación.

La herramienta trabajó sobre una copia del repositorio en un entorno aislado.
La revisión, la publicación de las ramas y la apertura de los pull requests
corresponden al estudiante.

## Propósito del uso

- Construir la versión responsive del flujo en HTML y CSS.
- Automatizar el recorrido a 320, 375 y 430 px para obtener las pantallas.
- Redactar las reglas de breakpoint y los dos escenarios móviles.

## Prompts relevantes

1. Adaptar el flujo a 320–430 px jerarquizando datos y acciones y reduciendo la carga cognitiva.
2. Definir breakpoints a partir del contenido y listar qué cambia en cada uno.
3. Aplicar en el diseño móvil las correcciones P1 del backlog de la semana 9.
4. Plantear dos escenarios móviles reales del hospital con decisiones de contenido y de error.
5. Definir la recuperación ante conexión limitada sin duplicar citas.

## Contenido aceptado

- Cortes en 600 y 1024 px definidos por el contenido.
- Tarjetas en lugar de tabla y grilla de 3 columnas en móvil.
- Reintento con la misma Idempotency-Key ante conexión limitada.

## Contenido modificado o rechazado

- Se descartó un modo sin conexión que guarde citas en el teléfono y las envíe después: agregaría sincronización y conflictos fuera del alcance del módulo.
- Se descartó guardar el borrador en localStorage por contener datos de paciente.
- Se descartó un menú lateral: el módulo tiene un solo flujo.

## Errores detectados y corregidos

| Hallazgo | Corrección |
|---|---|
| El botón deshabilitado se veía azul oscuro cuando el cursor quedaba encima, porque el estilo `:hover` del botón primario tenía más prioridad. | Se agregó `.btn[disabled]:hover` y se regeneraron las pantallas. |
| En móvil, los controles del prototipo ocupaban casi un tercio de la pantalla. | Se volvieron plegables (`<details>`) y quedan cerrados por debajo de 600 px. |

| El prototipo exigía el motivo de la consulta y pedía 5–250 caracteres para cancelar, reglas distintas a las del backend. | Se alinearon con `StoreAppointmentRequest` y `CancelAppointmentRequest`: motivo de consulta opcional con contador hasta 500; cancelación de 3 a 500 caracteres. |

## Validación humana

El estudiante revisó las pantallas en los tres anchos, comprobó que no haya desplazamiento horizontal a 320 px y verificó que el recorrido automatizado termine sin errores de JavaScript.

## Responsabilidad académica

La inteligencia artificial se empleó como herramienta de apoyo. El diseño, las
decisiones, la validación y la preparación para la defensa oral corresponden
al estudiante, quien asume la responsabilidad académica sobre el contenido
entregado.
