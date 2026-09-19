# Declaración de uso de inteligencia artificial — Semana 10

| Dato | Información |
|---|---|
| Módulo | ASII-05 — Citas médicas y agenda |
| Estudiante | Eddy Adolfo Castro Véliz |
| Código | 1890-23-16857 |
| Semana | 10 — Diseño para movilidad |

## Herramienta utilizada

Claude, de Anthropic, como apoyo al análisis, a la redacción y a la generación
de diagramas y maquetas.

## Propósito

- Construir la versión responsive del flujo en HTML y CSS.
- Automatizar el recorrido a 320, 375 y 430 px para obtener las pantallas.
- Redactar las reglas de breakpoint y los dos escenarios móviles.

## Contenido aceptado

- Cortes en 600 y 1024 px definidos por el contenido.
- Tarjetas en lugar de tabla y grilla de 3 columnas en móvil.
- Reintento con la misma Idempotency-Key ante conexión limitada.

## Contenido modificado o rechazado

- Se descartó un modo sin conexión que guarde citas en el teléfono y las envíe después: agregaría sincronización y conflictos fuera del alcance del módulo.
- Se descartó guardar el borrador en localStorage por contener datos de paciente.
- Se descartó un menú lateral: el módulo tiene un solo flujo.

## Validación humana

El estudiante revisó las pantallas en los tres anchos, comprobó que no haya desplazamiento horizontal a 320 px y verificó que el recorrido automatizado termine sin errores.

## Responsabilidad académica

Las decisiones de diseño y la preparación para la defensa oral corresponden al
estudiante, quien asume la responsabilidad académica sobre el contenido
entregado.
