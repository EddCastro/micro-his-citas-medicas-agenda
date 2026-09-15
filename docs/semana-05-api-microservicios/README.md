# Semana 5 — Cliente-servidor, API REST, microservicios e integración

Módulo **ASII-05 — Citas médicas y agenda**.

| Dato | Información |
|---|---|
| Estudiante | Eddy Adolfo Castro Véliz |
| Código | 1890-23-16857 |
| GitHub | EddCastro |
| Correo | ecastrov5@miumg.edu.gt |
| Issue | #5 |
| Rama del repositorio grupal | `feat/mod05-citas-medicas-agenda` |

## Tarea

Evolucionar el mismo Micro-HIS de citas médicas y el flujo de solicitud,
validación de disponibilidad y confirmación o cancelación de cita hacia un
diseño cliente-servidor, y evaluar una frontera de microservicio.

La consigna advierte de forma explícita que no se construya infraestructura de
producción ni se divida el sistema sin una justificación medible. Esta entrega
se mantiene por tanto en el plano del diseño.

## Decisión principal

**El módulo no se separa como microservicio en esta etapa.** La evaluación de
la frontera candidata concluye que el costo operativo supera el beneficio con
el volumen y la organización actuales.

En su lugar se consolida el diseño cliente-servidor sobre el monolito modular
existente, se especifica el contrato de API y se definen umbrales medibles que,
de alcanzarse, justificarían la extracción.

El razonamiento completo está en
[`evaluacion-microservicio.md`](evaluacion-microservicio.md).

## Documentos

| Documento | Contenido |
|---|---|
| [contrato-api.md](contrato-api.md) | Endpoints, payloads, errores, idempotencia, versionado y paginación |
| [evaluacion-microservicio.md](evaluacion-microservicio.md) | Frontera candidata, acoplamiento, criterios medibles, decisión y migración razonada |
| [atributos-calidad.md](atributos-calidad.md) | Propiedad de datos, comunicación, seguridad, resiliencia, observabilidad y consistencia |
| [plan-integracion.md](plan-integracion.md) | Plan de issue, rama, worktree y pull request |
| [DECLARACION_IA.md](DECLARACION_IA.md) | Declaración de uso de inteligencia artificial |

## Diagramas

| Diagrama | Qué representa |
|---|---|
| `cliente-servidor.puml` | Capas cliente, servidor y datos con los puntos de control |
| `frontera-microservicio.puml` | Frontera candidata y sus dependencias hacia otros módulos |
| `secuencia-resiliencia.puml` | Solicitud de cita con tiempo de espera, reintento e idempotencia |

Cada uno se entrega como fuente editable `.puml` con su exportación `.png`.

## Alcance de la entrega

Incluye:

- Contrato de API del módulo con su política de errores y de idempotencia.
- Evaluación de una frontera de microservicio con criterios medibles.
- Definición de propiedad de datos y modo de comunicación entre módulos.
- Atributos de seguridad, resiliencia, observabilidad y consistencia.
- Ruta de migración por etapas con condiciones de activación.
- Plan de integración mediante issue, rama, worktree y pull request.

No incluye:

- Infraestructura de producción, orquestadores ni despliegue.
- Extracción efectiva del módulo a un servicio independiente.
- Implementación de colas, malla de servicios ni pasarela de API.

## Datos

Todos los datos utilizados en ejemplos son ficticios. El repositorio no
contiene credenciales, secretos ni información clínica identificable.
