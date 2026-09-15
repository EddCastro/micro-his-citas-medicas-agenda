# Matriz decisión → evidencia

Cada decisión de diseño del módulo ASII-05, con el motivo que la sostiene y el
lugar exacto donde puede comprobarse.

| Dato | Información |
|---|---|
| Módulo | ASII-05 — Citas médicas y agenda |
| Estudiante | Eddy Adolfo Castro Véliz |
| Código | 1890-23-16857 |
| Semana | 6 — Primera evaluación parcial |

## Decisiones de modelado

| # | Decisión | Motivo | Evidencia |
|---|---|---|---|
| D-01 | Cinco casos de uso, no solo tres | La agenda médica exige reagendar y consultar, no solo crear y cancelar | `semana-01-uml/casos-de-uso-solicitud-cita.puml` |
| D-02 | Tres actores diferenciados | Recepción registra, médico consulta, paciente origina | `semana-01-uml/narrativa-alcance.md` |
| D-03 | Trazabilidad requisito → diagrama → elemento | Permite verificar que ningún requisito quedó sin modelar | `semana-01-uml/matriz-trazabilidad.md` |

## Decisiones de requisitos

| # | Decisión | Motivo | Evidencia |
|---|---|---|---|
| D-04 | 16 RF y 12 RNF codificados | Sin código no hay trazabilidad hacia la prueba | `semana-02-solid/requisitos-rf-rnf.md` |
| D-05 | 15 criterios de aceptación verificables | Un criterio que no se puede probar no es criterio | `semana-02-solid/criterios-aceptacion.md` |
| D-06 | Aplicar inversión de dependencias | La lógica de agenda no debe depender del ORM | `semana-02-solid/diseno-dip-antes-despues.md` |

## Decisiones de arquitectura

| # | Decisión | Motivo | Evidencia |
|---|---|---|---|
| D-07 | Cuatro capas con dependencias hacia el dominio | Aísla la razón de cambio de cada capa | `ADR-001-arquitectura.md`, sección Decisión |
| D-08 | Contratos declarados en `Domain`, no en `Infrastructure` | Si vivieran junto a la implementación, el negocio dependería del ORM | `app/Domain/Modulo05/Repositorios/` |
| D-09 | Entidad pura, no modelo Eloquent | Permite probar reglas sin base de datos; impide evadir invariantes por asignación masiva | `AppointmentTest`, 15 pruebas sin base |
| D-10 | Constructores `schedule()` y `restore()` | Sin la separación sería imposible leer una cita pasada desde la base | `test_restore_admite_una_cita_ya_pasada` |
| D-11 | Dos contratos separados, no uno con más métodos | La disponibilidad pertenece a ASII-04; separarla permite sustituir la fuente | `DoctorAvailabilityRepository` |
| D-12 | Tabla propia de disponibilidad | ASII-04 no la expone en el backend; sin ella la regla central es inverificable | `2026_08_23_000000_create_doctor_availabilities_table.php` |
| D-13 | No modificar la tabla `appointments` del andamiaje | Otros módulos dependen de su estructura | `git diff` no toca esa migración |

## Decisiones de persistencia

| # | Decisión | Motivo | Evidencia |
|---|---|---|---|
| D-14 | Detección de cruces en la base, no en memoria | Aprovecha `idx_appt_doctor_date`; cargar la agenda del día no escala | `EloquentAppointmentRepository::hasOverlap()` |
| D-15 | Expresión de fin resuelta por driver | La aritmética de fechas no es portable entre motores | `expresionDeFin()`, tres variantes |
| D-16 | La cita cancelada no se elimina | Conserva trazabilidad; el estado la excluye del cruce | `test_cancelar_libera_el_horario` |
| D-17 | Sentencias preparadas con parámetros nombrados | Elimina la vía principal de inyección | Toda consulta del repositorio |

## Decisiones de interfaz

| # | Decisión | Motivo | Evidencia |
|---|---|---|---|
| D-18 | Cinco endpoints bajo `/api/v1` | Versión en ruta permite convivencia durante una transición | `routes/api.php` |
| D-19 | `PATCH` para cambios de estado, no `PUT` | Modifica un atributo, no reemplaza el recurso | `contrato-api.md` |
| D-20 | Cita ajena devuelve 404, no 403 | Un 403 revelaría que el registro existe en otro hospital | `test_no_recupera_una_cita_de_otro_tenant` |
| D-21 | Código simbólico además del código HTTP | El cliente reacciona sin depender del texto del mensaje | `contrato-api.md`, tabla de códigos |
| D-22 | Clave de idempotencia en la creación | Crear una cita no es naturalmente idempotente; sin ella un reintento duplica | `contrato-api.md`, sección Idempotencia |
| D-23 | Paginación declarada desde el inicio | Introducirla después sería un cambio incompatible | `contrato-api.md`, filtros de `GET` |

## Decisiones de integración

| # | Decisión | Motivo | Evidencia |
|---|---|---|---|
| D-24 | El tenant proviene del contexto, no de la petición | Aceptarlo del cliente permitiría acceder a otro hospital | `RequestTenantContext`, middleware `tenant` |
| D-25 | No extraer el módulo como microservicio | Ninguno de los cinco criterios medibles alcanza su umbral | `evaluacion-microservicio.md` |
| D-26 | Degradación hacia el rechazo ante fallo de disponibilidad | Agendar sin validar jornada incumpliría la regla central | `atributos-calidad.md`, sección Resiliencia |
| D-27 | Migración en cuatro etapas reversibles | Las tres primeras tienen punto de retorno; la cuarta no | `evaluacion-microservicio.md`, Migración razonada |

## Decisiones del cambio práctico

| # | Decisión | Motivo | Evidencia |
|---|---|---|---|
| D-28 | Bloqueo pesimista sobre la agenda del médico | La comprobación previa no descartaba la condición de carrera | `lockDoctorAgenda()` |
| D-29 | Alcance del bloqueo: un médico y un día | Bloquear más reduciría la concurrencia sin necesidad | `test_el_bloqueo_no_impide_agendar_en_otro_dia` |
| D-30 | Índice único parcial como segunda capa | Protege el invariante ante cualquier vía de escritura, no solo la del módulo | `2026_09_14_000000_add_appointment_slot_unique_index.php` |
| D-31 | El índice cubre solo los estados que bloquean | Si cubriera todos, una cita cancelada impediría reutilizar el horario | `test_cancelar_libera_el_horario_bajo_el_indice_parcial` |
| D-32 | SQLite omitido del bloqueo explícito | Serializa las escrituras a nivel de conexión | `lockDoctorAgenda()`, guardia por driver |

## Cobertura de la evidencia

| Nivel | Pruebas | Qué garantiza |
|---|---:|---|
| Dominio | 22 | Invariantes y transiciones sin base de datos |
| Aplicación | 19 | Casos de uso con dobles en memoria |
| Integración | 12 | Adaptadores y SQL sobre base real |
| Concurrencia | 6 | El invariante bajo solicitudes simultáneas |
| **Módulo** | **59** | |
| Suite completa del proyecto | 148 | El módulo no rompe a los demás |

Resultado de la última ejecución: 148 aprobadas, 208 aserciones, código de
salida 0.

## Decisiones sin evidencia ejecutable

Se declaran aparte para no presentarlas como verificadas.

| # | Decisión | Estado |
|---|---|---|
| D-33 | Matriz de permisos por rol | Propuesta; la semilla solo declara `lab.results.validate` |
| D-34 | Límite de solicitudes por usuario | Propuesta; no hay middleware de límite implementado |
| D-35 | Identificador de correlación | Propuesta; requiere acuerdo de todos los módulos |
| D-36 | Restricción de exclusión por rango | Propuesta; requiere la extensión `btree_gist` en PostgreSQL |
