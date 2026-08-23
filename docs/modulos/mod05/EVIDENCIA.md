# Evidencia de implementacion y validacion

## Identificacion

| Dato | Informacion |
|---|---|
| Modulo | ASII-05 - Citas medicas y agenda |
| Estudiante | Eddy Adolfo Castro Veliz |
| GitHub | EddCastro |
| Actividad | Tarea 3 - Micro-monolito en PHP vanilla |
| Repositorio | https://github.com/EddCastro/micro-his-citas-medicas-agenda |
| Rama | `main` |

## 1. Entorno de ejecucion

Comando:

```powershell
php -v
```

Salida:

```text
PHP 8.2.33 (cli) (built: Jul 28 2026 10:29:00) (ZTS Visual C++ 2019 x64)
Copyright (c) The PHP Group
Zend Engine v4.2.33, Copyright (c) Zend Technologies
```

La consigna exige PHP 8.2 o superior. La version instalada cumple el requisito.

Comando:

```powershell
php -m | Select-String -Pattern "^PDO$|^pdo_sqlite$|^sqlite3$"
```

Salida:

```text
PDO
pdo_sqlite
sqlite3
```

Las extensiones necesarias para el acceso a datos estan disponibles.

## 2. Reproduccion desde una instalacion limpia

```powershell
git clone https://github.com/EddCastro/micro-his-citas-medicas-agenda.git
cd micro-his-citas-medicas-agenda
Copy-Item .env.example .env
php tests/all.php
```

No se requiere Composer, servidor de base de datos ni dependencias externas.
Las pruebas de integracion construyen la base SQLite en memoria aplicando
`database/schema.sql`, por lo que no dejan archivos residuales.

## 3. Ejecucion de la suite de pruebas

Comando:

```powershell
php tests/all.php
```

Salida:

```text
== Pruebas unitarias (dobles en memoria) ==
[OK] camino feliz: solicitar, confirmar y cancelar
[OK] regla: horario no disponible
[OK] regla de dominio: fecha pasada
[OK] error de persistencia mediante doble

Resultado: 4 aprobadas, 0 fallidas.
Todas las pruebas fueron aprobadas.

== Pruebas de integracion (SQLite via PDO) ==
[OK] integracion PDO: persiste y recupera la cita
[OK] integracion PDO: rechaza colision de horario
[OK] integracion PDO: cancelar libera el horario
[OK] integracion PDO: fuera de jornada no disponible
[OK] regla de dominio: no confirmar dos veces
[OK] regla de dominio: duracion invalida

Resultado: 6 aprobadas, 0 fallidas.
Todas las pruebas de integracion fueron aprobadas.

Resultado global: TODAS LAS PRUEBAS APROBADAS
```

Codigo de salida obtenido: `0`.

El runner devuelve `exit(1)` ante cualquier fallo, por lo que el codigo `0`
confirma que las diez pruebas fueron aprobadas y no solo que el script
termino de ejecutarse.

## 4. Cobertura exigida por la consigna

La consigna requiere probar al menos camino feliz, regla de dominio y error de
persistencia mediante dobles o una base de prueba. La suite cubre las tres
categorias y agrega verificacion sobre persistencia real.

| Requisito de la consigna | Prueba que lo cubre | Archivo |
|---|---|---|
| Camino feliz | `camino feliz: solicitar, confirmar y cancelar` | `tests/run.php` |
| Regla de dominio | `regla de dominio: fecha pasada` | `tests/run.php` |
| Regla de dominio | `regla de dominio: duracion invalida` | `tests/integration.php` |
| Regla de dominio | `regla de dominio: no confirmar dos veces` | `tests/integration.php` |
| Error de persistencia mediante doble | `error de persistencia mediante doble` | `tests/run.php` |
| Base de prueba real | Cuatro pruebas de integracion sobre SQLite | `tests/integration.php` |

## 5. Trazabilidad entre criterios de aceptacion y pruebas

Los criterios provienen de `ESPECIFICACION.md`.

| Criterio | Prueba que lo verifica |
|---|---|
| CA-01 Solicitud valida | `integracion PDO: persiste y recupera la cita` |
| CA-02 Fecha pasada | `regla de dominio: fecha pasada` |
| CA-03 Duracion invalida | `regla de dominio: duracion invalida` |
| CA-04 Fuera de jornada | `integracion PDO: fuera de jornada no disponible` |
| CA-05 Cruce con cita activa | `integracion PDO: rechaza colision de horario` |
| CA-06 Horario de cita cancelada | `integracion PDO: cancelar libera el horario` |
| CA-07 Confirmar cita pendiente | `camino feliz: solicitar, confirmar y cancelar` |
| CA-08 Confirmar cita ya confirmada | `regla de dominio: no confirmar dos veces` |
| CA-09 Cancelar cita | `camino feliz: solicitar, confirmar y cancelar` |
| CA-10 Fallo de persistencia | `error de persistencia mediante doble` |

Los diez criterios de aceptacion tienen una prueba automatizada asociada.

## 6. Detalle de las pruebas de integracion

Las pruebas de integracion no usan dobles: instancian
`PdoAppointmentRepository` y `PdoAvailabilityRepository` contra una base SQLite
creada con el esquema real del proyecto.

| Prueba | Comportamiento verificado |
|---|---|
| Persiste y recupera la cita | Una cita solicitada se guarda mediante `INSERT` preparado y se reconstruye desde la base con estado pendiente. |
| Rechaza colision de horario | Una segunda solicitud que se solapa quince minutos con una cita existente es rechazada por la consulta de cruce. |
| Cancelar libera el horario | Tras cancelar, el mismo intervalo admite una cita nueva, lo que confirma que el estado cancelado no bloquea. |
| Fuera de jornada no disponible | Una solicitud a las 20:00 con jornada de 08:00 a 17:00 es rechazada al consultar `doctor_availability`. |

La verificacion de cruce es la operacion mas compleja del modulo: compara el
intervalo solicitado contra las citas activas del medico usando aritmetica de
fechas en SQL y excluye las citas canceladas.

## 7. Arbol de archivos versionados

Comando:

```powershell
git ls-files
```

Salida:

```text
.env.example
.gitignore
README.md
config/env.php
database/schema.sql
docs/modulos/mod05/ADR-001-arquitectura.md
docs/modulos/mod05/DECLARACION_IA.md
docs/modulos/mod05/ESPECIFICACION.md
docs/modulos/mod05/EVIDENCIA.md
docs/modulos/mod05/diagramas/caso-uso.puml
docs/modulos/mod05/diagramas/clases.puml
docs/modulos/mod05/diagramas/componentes.puml
docs/modulos/mod05/diagramas/secuencia.puml
docs/modulos/mod05/diagramas/vista-datos.puml
src/Application/CancelAppointment.php
src/Application/ConfirmAppointment.php
src/Application/RequestAppointment.php
src/Domain/Appointment.php
src/Domain/AppointmentRepository.php
src/Domain/AvailabilityRepository.php
src/Persistence/InMemoryAppointmentRepository.php
src/Persistence/InMemoryAvailabilityRepository.php
src/Persistence/PdoAppointmentRepository.php
src/Persistence/PdoAvailabilityRepository.php
src/Presentation/AppointmentController.php
tests/all.php
tests/integration.php
tests/run.php
```

El repositorio no versiona el archivo `.env`, la base SQLite local ni
directorios de dependencias. Esas rutas estan declaradas en `.gitignore`.

## 8. Correspondencia entre capas y archivos

| Capa | Archivos |
|---|---|
| Presentation | `src/Presentation/AppointmentController.php` |
| Application | `src/Application/RequestAppointment.php`, `ConfirmAppointment.php`, `CancelAppointment.php` |
| Domain | `src/Domain/Appointment.php`, `AppointmentRepository.php`, `AvailabilityRepository.php` |
| Persistence | `src/Persistence/PdoAppointmentRepository.php`, `PdoAvailabilityRepository.php`, `InMemoryAppointmentRepository.php`, `InMemoryAvailabilityRepository.php` |
| Configuracion | `config/env.php`, `.env.example` |
| Datos | `database/schema.sql` |
| Pruebas | `tests/run.php`, `tests/integration.php`, `tests/all.php` |

Las cuatro capas exigidas por la consigna estan presentes y separadas en
directorios distintos.

## 9. Historial de Git

Comando:

```powershell
git log --oneline --decorate -n 12
```

Salida:

```text
9829c4e (HEAD -> main) test(mod05): add PDO integration suite and enforce confirm transition
521dc57 (origin/main) chore(mod05): remove invalid UML renders
985ea48 chore(mod05): remove test diagram image
c12d60f docs(mod05): add rendered UML diagrams
22f5698 docs(mod05): add AI declaration
dc06d8c docs(mod05): add implementation evidence
21a5612 docs(mod05): add UML architecture diagrams
0ce634b docs(mod05): add architecture decision record
c79d04a docs(mod05): add appointment specification
cbb1c01 docs: add implementation evidence
edcde95 docs: add implementation evidence
ba8c5bb chore: ignore local sqlite validation files
```

El historial refleja una construccion incremental: primero la entidad y sus
reglas, despues los contratos, los casos de uso, la persistencia, los dobles,
las pruebas y finalmente la documentacion.

Los mensajes siguen la convencion de Conventional Commits con un ambito
explicito, lo que permite identificar el proposito de cada cambio sin leer el
diff.

## 10. Persistencia y seguridad de las consultas

Todas las operaciones sobre la base utilizan `PDO::prepare` con parametros
nombrados. No existe concatenacion de valores dentro de las sentencias SQL.

| Archivo | Operacion | Sentencia |
|---|---|---|
| `PdoAppointmentRepository` | Guardar cita | `INSERT` preparado con cinco parametros |
| `PdoAppointmentRepository` | Recuperar cita | `SELECT` preparado por identificador |
| `PdoAppointmentRepository` | Actualizar estado | `UPDATE` preparado |
| `PdoAvailabilityRepository` | Validar jornada | `SELECT COUNT(*)` sobre `doctor_availability` |
| `PdoAvailabilityRepository` | Detectar cruces | `SELECT COUNT(*)` con aritmetica de fechas y exclusion de canceladas |

El esquema aplica restricciones a nivel de base: `CHECK` sobre el rango de
`weekday`, `CHECK` de duracion positiva, `CHECK` sobre los estados validos e
indices por medico para las consultas de disponibilidad.

## 11. Configuracion separada del codigo

La consigna exige que la configuracion permanezca fuera del codigo fuente.

- `.env.example` documenta las variables necesarias sin contener valores
  reales.
- `config/env.php` carga las variables en tiempo de ejecucion.
- `.gitignore` impide versionar el archivo `.env`.

Valor de `DB_PASSWORD` en la plantilla: vacio. El repositorio no contiene
credenciales.

## 12. Datos utilizados

Los identificadores empleados en las pruebas son ficticios: `1001` y `1002`
para pacientes, `2001` para medicos. No corresponden a personas reales y no se
registra informacion clinica.

## 13. Limitaciones conocidas

- El proyecto no incluye autoloader PSR-4; las dependencias se declaran con
  `require` explicitos en los puntos de entrada.
- `AppointmentController` expone un metodo invocable, pero no existe todavia un
  front controller HTTP.
- La validacion de disponibilidad y la escritura de la cita no se ejecutan
  dentro de una transaccion, por lo que una condicion de carrera entre dos
  solicitudes simultaneas no queda descartada.
- El modulo no implementa reagendamiento, lista de espera ni consulta de agenda
  por rango de fechas, funciones que quedan fuera del flujo asignado.

Estas limitaciones delimitan el alcance de la entrega y no afectan el
cumplimiento del flujo requerido.

## 14. Nota sobre la publicacion del repositorio

El repositorio permanecio configurado como privado y sin colaboradores hasta el
22 de agosto de 2026. Ese dia se cambio su visibilidad a publica y se agrego al
docente como colaborador, de modo que el enlace entregado pueda consultarse.

Los commits posteriores a esa fecha corresponden a la ampliacion de la suite de
pruebas y a la correccion de la documentacion para asegurar coherencia entre
los artefactos y el codigo.
