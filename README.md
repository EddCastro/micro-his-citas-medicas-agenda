# ASII-05 — Citas médicas y agenda

Repositorio personal del módulo **Citas médicas y agenda** del proyecto final
de Análisis de Sistemas II.

| Dato | Información |
|---|---|
| Estudiante | Eddy Adolfo Castro Véliz |
| Código | 1890-23-16857 |
| GitHub | EddCastro |
| Módulo | ASII-05 — Citas médicas y agenda |
| Docente | Ing. Richard Ortíz |

## Flujo de ramas

```
main ──────────────────────────────────────── base estable
  └── developer ───────────────────────────── integración de entregas
        ├── feature/week-01-uml ───────────── PR #1
        ├── feature/week-02-solid ─────────── PR #2
        ├── feature/week-03-arquitectura ──── PR #3
        ├── feature/week-04-capas-repository  PR #4
        ├── feature/week-05-api-microservicios PR #5
        ├── feature/week-06-parcial ───────── PR #6
        ├── feature/week-07-componentes ───── PR #7
        ├── feature/week-08-ux ────────────── PR #8
        ├── feature/week-09-usabilidad ────── PR #9
        ├── feature/week-10-movil ─────────── PR #10
        └── feature/week-11-prototipo ─────── PR #11
```

Cada semana se desarrolla en su propia rama `feature/week-NN-tema`, con commits
separados por artefacto, y se integra a `developer` mediante pull request.

## Entregas por semana

| Semana | Tema | Ubicación | PR |
|---|---|---|---|
| 1 | Conceptos generales, orientación a objetos y UML | [`docs/semana-01-uml`](docs/semana-01-uml) | #1 |
| 2 | Proceso y modelo de diseño; principios SOLID | [`docs/semana-02-solid`](docs/semana-02-solid) | #2 |
| 3 | Diseño arquitectónico, vistas y patrones | [`docs/semana-03-arquitectura`](docs/semana-03-arquitectura) | #3 |
| 4 | Arquitectura en capas y patrón Repository | [`docs/semana-04-capas-repository`](docs/semana-04-capas-repository) | #4 |
| 5 | Cliente-servidor, API REST, microservicios e integración | [`docs/semana-05-api-microservicios`](docs/semana-05-api-microservicios) | #5 |
| 6 | Primera evaluación parcial | [`docs/semana-06-parcial`](docs/semana-06-parcial) | #6 |
| 7 | Diseño de componentes y refactorización | [`docs/semana-07-componentes`](docs/semana-07-componentes) | #7 |
| 8 | Diseño de experiencia de usuario | [`docs/semana-08-ux`](docs/semana-08-ux) | #8 |
| 9 | Evaluación del diseño, usabilidad y accesibilidad | [`docs/semana-09-usabilidad`](docs/semana-09-usabilidad) | #9 |
| 10 | Diseño para movilidad | [`docs/semana-10-movil`](docs/semana-10-movil) | #10 |
| 11 | Mejores prácticas para diseño móvil/web | [`docs/semana-11-prototipo`](docs/semana-11-prototipo) · [`prototipo/`](prototipo) | #11 |

Todas las carpetas están disponibles en la rama `developer`.

### Semana 1 — UML

Modela el proceso de solicitud, validación de disponibilidad y confirmación o
cancelación de cita: narrativa de alcance y actores, diagrama de casos de uso,
diagrama de actividad con decisiones y excepciones, diagrama de secuencia
global y matriz de trazabilidad.

### Semana 2 — SOLID

Aplica el principio de inversión de dependencias al mismo flujo: 16 requisitos
funcionales, 12 no funcionales, 26 criterios de aceptación, la fuente del
principio y el diseño antes y después de aplicarlo.

### Semana 3 — Arquitectura

Vista arquitectónica de alto nivel del módulo dentro del Sistema Hospitalario
Integrado, con sus dependencias hacia usuarios, permisos, pacientes, médicos,
notificaciones y auditoría, más el diagrama de componentes por capas.

### Semana 4 — Capas y Repository

Responsabilidades de las capas Presentation, Application, Domain y
Persistence; contratos Repository declarados en el dominio; decisión
arquitectónica con alternativas descartadas; diagramas de clases, secuencia y
vista de datos; y evidencia de ejecución de las pruebas.

### Semana 5 — Cliente-servidor y microservicios

Contrato de API con formato uniforme de errores, idempotencia, versionado y
paginación; evaluación de una frontera de microservicio con cinco criterios
medibles; propiedad de datos, seguridad, resiliencia, observabilidad y
consistencia; y ruta de migración por etapas reversibles.

La conclusión es que el módulo **no se extrae** como microservicio en esta
etapa, porque ninguno de los umbrales definidos se alcanza.

### Semana 6 — Primera evaluación parcial

Defensa de la arquitectura conectando actores, UML, requisitos, SOLID, capas,
Repository y contrato de API. Incluye presentación de ocho diapositivas con
notas del orador, un diagrama trazable que recorre las seis semanas hasta la
evidencia ejecutable, y una matriz decisión → evidencia con 36 entradas.

El **cambio práctico defendido** cierra la condición de carrera declarada como
limitación desde la semana 3: bloqueo pesimista sobre la agenda del médico más
un índice único parcial en la base de datos, con seis pruebas de integración
que lo evidencian.

### Semana 7 — Componentes y refactorización

Componentes backend (existentes) y frontend (propuestos) del flujo, con sus
contratos de entrada, salida y error. Refactor conceptual sobre el código
Laravel del punto de mayor acoplamiento,
`EloquentAppointmentRepository::hasOverlap()`, que además de consultar
bloqueaba la agenda solo si detectaba una transacción abierta. El análisis
encontró también que confirmar y cancelar se ejecutan sin transacción. El
refactor hace explícito el bloqueo, deja la consulta sin efectos, protege las
transiciones y tipa los errores.

### Semana 8 — Experiencia de usuario

User flow por rol (Recepcionista, Enfermera, Médico), seis wireframes
anotados y el catálogo de estados, mensajes, validaciones y reglas de
interacción, incluida la protección de datos del paciente.

### Semana 9 — Usabilidad y accesibilidad

Evaluación de los wireframes con las heurísticas de Nielsen y WCAG 2.2 AA.
Once hallazgos con evidencia medida (contraste y teclado) y un backlog
priorizado por severidad, frecuencia y peso en el módulo, con un criterio
verificable por corrección.

### Semana 10 — Movilidad

Cinco pantallas a 320, 375 y 430 px, reglas de breakpoint en 600 y 1024 px, y
dos escenarios móviles: conflicto de concurrencia en ventanilla y conexión
limitada en Enfermería.

### Semana 11 — Prototipo navegable

Prototipo HTML en [`prototipo/index.html`](prototipo/index.html), desktop y
móvil, con camino feliz y error crítico de concurrencia (409), mapa de
navegación y capturas. Una verificación automatizada con Playwright y
axe-core confirma 40 de 40 criterios, entre ellos el cierre de los once
hallazgos de la semana 9 y las reglas de los formularios del backend.

En línea: https://eddcastro.github.io/micro-his-citas-medicas-agenda/prototipo/

## Micro-HIS en PHP vanilla

La rama `main` contiene el micro-monolito que sustenta las semanas 3 a 6:
PHP 8.2 sin framework, cuatro capas separadas, PDO con sentencias preparadas y
diez pruebas automatizadas.

```powershell
git clone https://github.com/EddCastro/micro-his-citas-medicas-agenda.git
cd micro-his-citas-medicas-agenda
Copy-Item .env.example .env
php tests/all.php
```

Su documentación está en [`docs/modulos/mod05`](docs/modulos/mod05).

## Implementación en el repositorio grupal

El módulo también está implementado sobre Laravel dentro del repositorio del
proyecto final, con 59 pruebas propias distribuidas en dominio, aplicación,
integración y concurrencia.

## Artefactos

Los diagramas se entregan como fuentes editables `.puml` acompañadas de sus
exportaciones `.png`. Cada semana incluye además su declaración de uso de
inteligencia artificial.

## Datos

Todos los datos utilizados son ficticios. El repositorio no contiene
credenciales, secretos ni información clínica identificable.
