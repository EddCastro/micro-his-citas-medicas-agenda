# Declaración de uso de inteligencia artificial — Semana 5

| Dato | Información |
|---|---|
| Módulo | ASII-05 — Citas médicas y agenda |
| Estudiante | Eddy Adolfo Castro Véliz |
| Código | 1890-23-16857 |
| Semana | 5 — Cliente-servidor, API REST, microservicios e integración |

## Herramienta utilizada

Claude, de Anthropic, como apoyo al análisis y a la redacción. No ejecutó
comandos en el equipo ni publicó cambios en el repositorio.

## Propósito

- Estructurar el contrato de API a partir de los endpoints ya implementados.
- Plantear criterios medibles para evaluar la frontera de microservicio.
- Organizar los atributos de seguridad, resiliencia, observabilidad y
  consistencia.
- Redactar la ruta de migración por etapas.

## Prompts relevantes

- Definir el contrato de API del módulo incluyendo formato de errores,
  idempotencia, versionado y paginación.
- Proponer criterios medibles que justifiquen o descarten extraer el módulo
  como microservicio.
- Analizar qué costos introduciría la extracción sobre el flujo de solicitud
  de cita.
- Definir el comportamiento del módulo cuando la fuente de disponibilidad no
  responde.
- Plantear una ruta de migración por etapas reversibles con condiciones de
  activación.

## Contenido aceptado

- La estructura del contrato con códigos simbólicos de negocio además del
  código HTTP.
- El uso de una clave de idempotencia en la creación, por no ser una operación
  naturalmente idempotente.
- Los cinco criterios medibles de extracción y sus umbrales.
- La ruta de migración en cuatro etapas con un punto de retorno explícito.

## Contenido modificado o rechazado

- Se rechazó proponer la extracción del módulo como microservicio. La consigna
  advierte de no dividir el sistema sin justificación medible, y ninguno de los
  criterios definidos alcanza su umbral en el estado actual del proyecto.
- Se descartó incluir infraestructura de despliegue, colas o pasarela de API,
  por quedar fuera del alcance indicado.
- Se ajustó la degradación ante fallo de la disponibilidad hacia el rechazo y
  no hacia el permiso, porque agendar sin validar la jornada incumpliría la
  regla central del módulo.
- Se limitó el reintento automático a lecturas y a escrituras con clave de
  idempotencia, para no producir citas duplicadas.

## Validación humana

El estudiante revisó que el contrato corresponda a los endpoints realmente
implementados, verificó que los criterios de extracción sean observables con
las métricas disponibles, validó la sintaxis de los diagramas y aprobó cada
documento antes de incorporarlo.

## Responsabilidad académica

Las decisiones de diseño, la evaluación de la frontera y la preparación para
la defensa oral corresponden al estudiante, quien asume la responsabilidad
académica sobre el contenido entregado.
