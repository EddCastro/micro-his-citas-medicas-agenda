# Plan de integración — Semana 5

Plan de issue, rama, worktree y pull request para la entrega de la semana 5.

## Issue

| Dato | Valor |
|---|---|
| Número | #5 |
| Título | ASII-05: Citas médicas y agenda |
| Responsable | EddCastro |
| Etiqueta de la semana | `semana-05` |

### Criterios de cierre de la semana

- [ ] Contrato de API documentado con errores, idempotencia y paginación
- [ ] Frontera de microservicio evaluada con criterios medibles
- [ ] Decisión de extracción justificada y documentada
- [ ] Propiedad de datos declarada por entidad
- [ ] Seguridad, resiliencia, observabilidad y consistencia definidas
- [ ] Migración razonada por etapas con condiciones de activación
- [ ] Tres diagramas con fuente editable y exportación
- [ ] Pull request abierto hacia la rama de integración

## Ramas

### Repositorio grupal

El detalle de la tarea reside aquí.

| Dato | Valor |
|---|---|
| Base | `origin/main` |
| Rama | `feat/mod05-citas-medicas-agenda` |
| Worktree | `../shi-mod05-citas` |
| Destino del PR | `develop` |
| Ubicación | `docs/modulos/mod05/semana-05/` |

La rama ya existe desde la entrega anterior, por lo que esta semana agrega
commits sobre ella en lugar de crear una nueva.

### Repositorio personal

Evidencia el flujo de ramas exigido por la cátedra.

| Dato | Valor |
|---|---|
| Base | `developer` |
| Rama | `feature/week-05-api-microservicios` |
| Destino del PR | `developer` |
| Ubicación | `docs/semana-05-api-microservicios/` |

## Worktree

El worktree mantiene la rama del módulo en un directorio propio, separado del
directorio donde vive `main`. Así se evita cambiar de rama en el mismo
directorio y se conserva el entorno instalado.

```powershell
git fetch origin
git worktree add ../shi-mod05-citas feat/mod05-citas-medicas-agenda
cd ../shi-mod05-citas
```

## Secuencia de commits

Un commit por artefacto, con ámbito explícito.

| Orden | Mensaje |
|---|---|
| 1 | `docs(week-05): define module API contract` |
| 2 | `docs(week-05): evaluate microservice boundary with measurable criteria` |
| 3 | `docs(week-05): define data ownership and communication` |
| 4 | `docs(week-05): define security, resilience and observability` |
| 5 | `docs(week-05): add client-server and boundary diagrams` |
| 6 | `docs(week-05): add integration plan and AI declaration` |

## Pull request

### Repositorio grupal

| Dato | Valor |
|---|---|
| Título | `docs(mod05): contrato API y evaluación de frontera de microservicio` |
| Origen | `feat/mod05-citas-medicas-agenda` |
| Destino | `develop` |
| Estado | Borrador |
| Revisor | Docente del curso |
| Referencia | `Refs #5` |

### Repositorio personal

| Dato | Valor |
|---|---|
| Título | `docs(week-05): contrato API, frontera de microservicio e integración` |
| Origen | `feature/week-05-api-microservicios` |
| Destino | `developer` |

## Verificación antes de abrir el pull request

| Comprobación | Comando |
|---|---|
| Sintaxis de los diagramas | `java -jar plantuml.jar -checkonly docs/.../*.puml` |
| Suite de pruebas del módulo | `php artisan test` |
| Árbol de trabajo limpio | `git status -s` |
| Sin conflictos con la rama destino | `git merge origin/develop --no-commit --no-ff` |

## Puntos de coordinación

Elementos que requieren acuerdo con el equipo y se plantean en el pull request:

1. **Propiedad de la disponibilidad médica.** El módulo mantiene una tabla
   propia mientras ASII-04 no publique la suya. Debe acordarse quién la
   conserva y cuándo se reconcilia.

2. **Formato uniforme de errores.** El contrato propone un cuerpo con mensaje,
   código simbólico e identificador de solicitud. Conviene que todos los
   módulos adopten el mismo formato para que el cliente lo trate de una sola
   manera.

3. **Identificador de correlación.** Su utilidad depende de que todos los
   módulos propaguen la misma cabecera.

4. **Política de versionado.** El criterio de qué constituye un cambio
   incompatible debe ser común a toda la interfaz del sistema.
