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
main ──────────────────────────────── base estable
  └── developer ───────────────────── integración de entregas
        ├── feature/week-01-uml ───── PR #1
        └── feature/week-02-solid ─── PR #2
```

Cada semana se desarrolla en su propia rama `feature/week-NN-tema`, con commits
separados por artefacto, y se integra a `developer` mediante pull request.

## Entregas por semana

| Semana | Tema | Ubicación | PR |
|---|---|---|---|
| 1 | Conceptos generales, orientación a objetos y UML | [`docs/semana-01-uml`](docs/semana-01-uml) | #1 |
| 2 | Proceso y modelo de diseño; principios SOLID | [`docs/semana-02-solid`](docs/semana-02-solid) | #2 |

Ambas carpetas están disponibles en la rama `developer`.

### Semana 1 — UML

Modela el proceso de solicitud, validación de disponibilidad y confirmación o
cancelación de cita: narrativa de alcance y actores, diagrama de casos de uso,
diagrama de actividad con decisiones y excepciones, diagrama de secuencia
global y matriz de trazabilidad.

### Semana 2 — SOLID

Aplica el principio de inversión de dependencias al mismo flujo: 16 requisitos
funcionales, 12 no funcionales, 26 criterios de aceptación, la fuente del
principio y el diseño antes y después de aplicarlo.

## Micro-HIS en PHP vanilla

La rama `main` contiene además el micro-monolito desarrollado como actividad
independiente: PHP 8.2 sin framework, cuatro capas separadas, PDO con
sentencias preparadas y diez pruebas automatizadas.

```powershell
git clone https://github.com/EddCastro/micro-his-citas-medicas-agenda.git
cd micro-his-citas-medicas-agenda
Copy-Item .env.example .env
php tests/all.php
```

Su documentación está en [`docs/modulos/mod05`](docs/modulos/mod05).

## Artefactos

Los diagramas se entregan como fuentes editables `.puml` acompañadas de sus
exportaciones `.png`. Cada semana incluye además su declaración de uso de
inteligencia artificial y una guía de defensa oral.

## Datos

Todos los datos utilizados son ficticios. El repositorio no contiene
credenciales, secretos ni información clínica identificable.
