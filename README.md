# Micro-HIS: Citas medicas y agenda

Micro-monolito educativo en PHP 8.2 vanilla que implementa el flujo de
solicitud, validacion de disponibilidad y confirmacion o cancelacion de una
cita medica.

## Datos de la entrega

| Dato | Informacion |
|---|---|
| Curso | Analisis de Sistemas II - Codigo 037 |
| Docente | Ing. Richard Ortiz |
| Estudiante | Eddy Adolfo Castro Veliz |
| Codigo | 1890-23-16857 |
| GitHub | EddCastro |
| Modulo | ASII-05 - Citas medicas y agenda |
| Actividad | Tarea 3 - Micro servicios y monolito |

## Alcance de este repositorio

Este repositorio corresponde **unicamente a la Tarea 3**, cuya consigna exige
PHP vanilla sin framework y un repositorio personal compartido con el docente.

Las demas actividades del modulo se desarrollan en el repositorio grupal del
proyecto final:
`https://github.com/compilations-teams/sistema-hospitalario-integrado-SistenasII-2026`
en la rama `feature/asii-05-citas-medicas-y-agenda-eddcastro`.

## Ejecucion

Requisitos: PHP 8.2 o superior con las extensiones `pdo` y `pdo_sqlite`. No se
necesita Composer, servidor web ni motor de base de datos externo.

```powershell
git clone https://github.com/EddCastro/micro-his-citas-medicas-agenda.git
cd micro-his-citas-medicas-agenda
Copy-Item .env.example .env
php tests/all.php
```

Salida esperada: diez pruebas aprobadas y codigo de salida `0`.

## Estructura

```
src/
  Presentation/    AppointmentController
  Application/     RequestAppointment, ConfirmAppointment, CancelAppointment
  Domain/          Appointment, AppointmentRepository, AvailabilityRepository
  Persistence/     Implementaciones PDO y dobles en memoria
config/            Carga de variables de entorno
database/          schema.sql
tests/             run.php, integration.php, all.php
docs/modulos/mod05/  Documentacion y diagramas
```

## Arquitectura

Cuatro capas con dependencias dirigidas hacia el dominio:

| Capa | Responsabilidad |
|---|---|
| Presentation | Convierte la entrada a tipos del dominio e invoca un caso de uso. |
| Application | Orquesta el caso de uso dependiendo solo de abstracciones. |
| Domain | Entidad, reglas invariantes y contratos Repository. |
| Persistence | Implementa los contratos con PDO y SQLite, y provee dobles de prueba. |

Los contratos `AppointmentRepository` y `AvailabilityRepository` se declaran en
`Domain`. En consecuencia, `Persistence` depende de `Domain` y no al reves.

La justificacion completa esta en
[`ADR-001-arquitectura.md`](docs/modulos/mod05/ADR-001-arquitectura.md).

## Reglas implementadas

- Una cita no puede programarse en una fecha pasada.
- La duracion debe ser mayor que cero.
- El horario debe estar dentro de la jornada del medico.
- No se admite cruce con una cita pendiente o confirmada del mismo medico.
- Una cita cancelada no bloquea el horario.
- Toda cita se crea en estado pendiente.
- Una cita cancelada no puede confirmarse.
- Una cita confirmada no puede confirmarse de nuevo.
- Una cita cancelada no puede cancelarse de nuevo.

Cada regla y su punto de verificacion estan detallados en
[`ESPECIFICACION.md`](docs/modulos/mod05/ESPECIFICACION.md).

## Pruebas

| Suite | Comando | Cobertura |
|---|---|---|
| Unitarias | `php tests/run.php` | Casos de uso con dobles en memoria. Cuatro pruebas. |
| Integracion | `php tests/integration.php` | Repositorios PDO sobre SQLite real. Seis pruebas. |
| Completa | `php tests/all.php` | Ejecuta ambas y devuelve un codigo de salida global. |

Las pruebas de integracion aplican `database/schema.sql` sobre una base en
memoria, por lo que no dejan archivos residuales.

## Documentacion

| Documento | Contenido |
|---|---|
| [ESPECIFICACION.md](docs/modulos/mod05/ESPECIFICACION.md) | Problema, actores, reglas, criterios de aceptacion y contratos. |
| [ADR-001-arquitectura.md](docs/modulos/mod05/ADR-001-arquitectura.md) | Decisiones de diseno, alternativas descartadas y consecuencias. |
| [EVIDENCIA.md](docs/modulos/mod05/EVIDENCIA.md) | Comandos ejecutados, salidas reales, arbol de archivos e historial. |
| [DECLARACION_IA.md](docs/modulos/mod05/DECLARACION_IA.md) | Herramientas, prompts, hallazgos y validacion humana. |
| [GUIA_DEFENSA_ORAL.md](docs/modulos/mod05/GUIA_DEFENSA_ORAL.md) | Preparacion para la defensa individual. |

Los cinco diagramas UML se encuentran en
[`docs/modulos/mod05/diagramas/`](docs/modulos/mod05/diagramas) como fuentes
editables `.puml` y exportaciones `.png`.

## Configuracion

La configuracion permanece fuera del codigo. `.env.example` documenta las
variables necesarias, `config/env.php` las carga en tiempo de ejecucion y
`.gitignore` impide versionar el archivo `.env`.

## Limitaciones conocidas

- No se incluye autoloader PSR-4; las dependencias se declaran con `require`.
- No existe front controller HTTP: el controlador se invoca por metodo.
- La validacion de disponibilidad y la escritura no ocurren dentro de una
  transaccion.
- Reagendamiento, lista de espera y consulta de agenda quedan fuera del flujo
  asignado.

## Datos

Todos los datos utilizados son ficticios. El repositorio no contiene
credenciales, secretos ni informacion clinica identificable.
