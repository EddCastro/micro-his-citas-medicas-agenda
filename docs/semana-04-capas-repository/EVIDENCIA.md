# Evidencia tecnica - Modulo ASII-05

## Identificacion

| Dato | Informacion |
|---|---|
| Modulo | ASII-05 - Citas medicas y agenda |
| Estudiante | Eddy Adolfo Castro Veliz |
| Codigo | 1890-23-16857 |
| GitHub | EddCastro |
| Issue | #5 |
| Rama | `feat/mod05-citas-medicas-agenda` |
| Base | `origin/main` en `406eb81` |
| Worktree | `../shi-mod05-citas` |

## 1. Entorno de ejecucion

```text
PHP 8.2.33 (cli) (built: Jul 28 2026 10:29:00) (ZTS Visual C++ 2019 x64)
Laravel Framework 12.58.0
PHPUnit 11.5.55
Composer 2.10.2
Node 22.14.0 / npm 10.9.2
```

Extensiones habilitadas para el proyecto: `openssl`, `mbstring`, `curl`,
`fileinfo`, `zip`, `pdo_sqlite`, `pdo_pgsql`, `pgsql`.

## 2. Preparacion desde una instalacion limpia

```powershell
git clone <repositorio>
cd shi-mod05-citas
composer install
Copy-Item .env.example .env
php artisan key:generate
php artisan jwt:secret --force
npm install
npm run build
php artisan test
```

La compilacion del frontend es necesaria porque la prueba `ExampleTest` del
scaffold solicita la ruta raiz, que renderiza una vista con Vite.

## 3. Resultado de la suite completa

```powershell
php artisan test
```

Salida:

```text
   PASS  Tests\Unit\ExampleTest
   PASS  Tests\Unit\Modulo05\AppointmentStatusTest
   PASS  Tests\Unit\Modulo05\AppointmentTest
   PASS  Tests\Unit\Modulo05\AppointmentUseCasesTest
   PASS  Tests\Feature\ExampleTest
   PASS  Tests\Integration\Modulo05\AppointmentRepositoryTest

  Tests:    56 passed (83 assertions)
  Duration: 0.83s
```

Codigo de salida: `0`.

## 4. Distribucion de las pruebas

| Suite | Archivo | Pruebas | Naturaleza |
|---|---|---:|---|
| Unit | `AppointmentTest` | 15 | Invariantes y transiciones de la entidad |
| Unit | `AppointmentStatusTest` | 7 | Reglas de estado y bloqueo de horario |
| Unit | `AppointmentUseCasesTest` | 19 | Casos de uso con dobles en memoria |
| Integration | `AppointmentRepositoryTest` | 12 | Adaptadores Eloquent sobre base real |
| | **Total del modulo** | **53** | |

Las tres restantes corresponden al scaffold base.

La consigna exige un minimo de seis pruebas repartidas entre dominio,
aplicacion e integracion. El modulo aporta 22 de dominio, 19 de aplicacion y
12 de integracion.

## 5. Trazabilidad entre criterios de aceptacion y pruebas

| Criterio | Prueba |
|---|---|
| CA-01 Solicitud valida | `registra una cita valida en estado pendiente` / `persiste y recupera una cita` |
| CA-02 Fecha pasada | `rechaza una fecha en el pasado` |
| CA-03 Duracion invalida | `rechaza una duracion no positiva` |
| CA-04 Especialidad incorrecta | `rechaza una especialidad que el medico no atiende` |
| CA-05 Fuera de jornada | `rechaza un horario fuera de jornada` / `rechaza un dia sin jornada declarada` |
| CA-06 Cruce con cita activa | `detecta un cruce de horarios` |
| CA-07 Horario de cita cancelada | `una cita cancelada libera el horario` |
| CA-08 Confirmar pendiente | `confirma una cita pendiente` |
| CA-09 Confirmar ya confirmada | `no confirma dos veces` |
| CA-10 Cancelar con motivo | `cancela conservando el motivo` |
| CA-11 Cancelar sin motivo | `la cancelacion exige motivo` |
| CA-12 Reagendar a horario libre | `reagenda a un horario libre` |
| CA-13 Reagendar a horario ocupado | `no reagenda a un horario ocupado` |
| CA-14 Agenda por medico y fecha | `la agenda filtra por medico y fecha` |
| CA-15 Acceso entre tenants | `no recupera una cita de otro tenant` / `el cruce no alcanza a otro tenant` |

Los quince criterios tienen al menos una prueba automatizada asociada.

## 6. Verificacion de la regla central obligatoria

Regla: no se confirma una cita fuera de disponibilidad ni en un intervalo ya
ocupado; la cancelacion libera el horario de forma consistente.

| Componente de la regla | Prueba de integracion |
|---|---|
| Respeta la jornada del medico | `rechaza un horario fuera de jornada` |
| Valida el intervalo completo | `rechaza una cita que termina despues del cierre` |
| Exige jornada declarada | `rechaza un dia sin jornada declarada` |
| Impide cruces | `detecta un cruce de horarios` |
| Admite citas contiguas | `no detecta cruce en citas contiguas` |
| Libera al cancelar | `una cita cancelada libera el horario` |

Las seis se ejecutan contra base de datos, no con dobles.

## 7. Hallazgo detectado por las pruebas de integracion

Durante el desarrollo, el modelo Eloquent `App\Models\Appointment` quedo
guardado con el namespace de la entidad de dominio. Las 43 pruebas unitarias
seguian aprobadas, porque el dominio no depende de `app/Models`.

El error solo se manifesto al ejecutar las pruebas de integracion, que cargan
el modelo:

```text
Cannot declare class App\Domain\Modulo05\Entidades\Appointment,
because the name is already in use in app\Models\Appointment.php
```

El caso justifica mantener ambos niveles de prueba: las unitarias verifican
reglas de forma aislada y rapida, pero no pueden detectar defectos en la capa
de infraestructura.

## 8. Contrato de API publicado

```powershell
php artisan route:list --path=appointments
```

```text
GET|HEAD   api/v1/appointments                            AppointmentController@index
POST       api/v1/appointments                            AppointmentController@store
PATCH      api/v1/appointments/{appointment}/cancel       AppointmentController@cancel
PATCH      api/v1/appointments/{appointment}/confirm      AppointmentController@confirm
PATCH      api/v1/appointments/{appointment}/reschedule   AppointmentController@reschedule
```

Las cinco rutas se registran dentro del grupo con middleware `tenant` y
`jwt.auth`.

## 9. Migracion aplicada

```powershell
php artisan migrate
```

```text
2026_08_23_000000_create_doctor_availabilities_table .......... DONE
```

La migracion se ejecuta despues de las diez del scaffold y no modifica ninguna
tabla existente. Su metodo `down()` revierte unicamente la tabla creada.

## 10. Historial de Git

```powershell
git log --oneline origin/main..HEAD
```

```text
add3d8f docs(mod05): add UML diagrams and rendered exports
443383f test(mod05): add repository integration tests over real database
e98e874 feat(mod05): expose appointment API endpoints
0d8815b feat(mod05): implement Eloquent adapters and register bindings
e064216 test(mod05): cover application use cases with in-memory doubles
e8c1e9e feat(mod05): add appointment use cases
f2b5ae9 feat(mod05): add doctor availability schema
b39d295 feat(mod05): define repository ports and application DTOs
d428567 test(mod05): cover appointment domain rules
b145209 feat(mod05): add appointment domain entity and state rules
e083135 docs(mod05): record layered architecture decision
f2014b5 docs(mod05): define appointment module specification
b78a1b8 chore(mod05): configure JWT secret for automated tests
```

Trece commits con proposito, en orden: configuracion, especificacion,
decision arquitectonica, dominio, pruebas de dominio, contratos, esquema,
casos de uso, pruebas de aplicacion, adaptadores, API, pruebas de integracion
y diagramas.

## 11. Archivos aportados

| Capa | Archivos |
|---|---:|
| Domain | 8 |
| Application | 7 |
| Infrastructure | 3 |
| Presentation | 5 |
| Models | 2 |
| Migraciones | 1 |
| Pruebas | 7 |
| Documentacion y diagramas | 12 |

Archivos del scaffold modificados: `app/Providers/AppServiceProvider.php`
(enlaces de contratos), `routes/api.php` (rutas del modulo) y `phpunit.xml`
(secreto de pruebas y suite de integracion).

No se modifico ninguna migracion, modelo ni archivo perteneciente a otro
modulo.

## 12. Aislamiento por tenant

Toda consulta del modulo filtra por `tenant_id`. El identificador se obtiene
del contenedor, donde lo deposita `TenantMiddleware` tras validar la cabecera
`X-Tenant-ID` contra la tabla de tenants.

Las pruebas `no recupera una cita de otro tenant` y `el cruce no alcanza a
otro tenant` verifican que una cita registrada en un hospital no sea visible
ni genere conflicto en otro.

## 13. Limitaciones conocidas

- La tabla `doctor_availabilities` es propia del modulo. Debera reconciliarse
  con ASII-04 cuando ese modulo publique su fuente de disponibilidad.
- La transaccion reduce la ventana de condicion de carrera, pero no la elimina
  sin un bloqueo explicito sobre las filas del medico.
- Las transiciones `completada` y `no_asistio` estan modeladas pero no
  implementadas: corresponden al proceso de atencion.
- No se incluye interfaz de usuario; el modulo se entrega como API.
- Las pruebas se ejecutan sobre SQLite en memoria. La expresion de calculo de
  fin de cita esta resuelta por driver para SQLite, PostgreSQL y MySQL, pero
  la variante de PostgreSQL no se ha ejecutado contra un servidor real.

## 14. Datos

Los datos utilizados en pruebas provienen de las factories del proyecto y son
ficticios. El repositorio no contiene credenciales, secretos ni informacion
clinica identificable.
