# ADR-001: Arquitectura por capas y patron Repository sobre Laravel

## Estado

Aceptado.

## Contexto

El modulo ASII-05 debe implementar una capacidad vertical completa sobre el
repositorio base del Sistema Hospitalario Integrado: Laravel 12, PHP 8.2,
autenticacion JWT, permisos con Spatie y aislamiento multi-tenant mediante el
middleware `tenant`.

La regla central obligatoria del modulo es que no se confirme una cita fuera de
disponibilidad ni en un intervalo ya ocupado, y que la cancelacion libere el
horario de forma consistente. Esa regla debe poder verificarse de forma
determinista, sin depender de una base de datos poblada.

Restricciones heredadas del repositorio base:

- La tabla `appointments` ya existe y no debe modificarse: pertenece al
  scaffold comun y otros modulos la consultan.
- Los identificadores de paciente, medico y especialidad son claves foraneas
  reales hacia tablas de otros modulos.
- Toda operacion debe permanecer dentro del tenant activo.

La implementacion directa dentro de un controlador Eloquent haria imposible
probar las reglas sin base de datos y ataria la logica de agenda al ORM.

## Decision

Se adopta una arquitectura por capas con dependencias dirigidas hacia el
dominio, aplicando el patron Repository como frontera entre la logica de
negocio y la persistencia.

### Distribucion

| Capa | Directorio | Responsabilidad |
|---|---|---|
| Presentation | `app/Http/Controllers/Api/V1`, `app/Http/Requests` | Validar el formato de entrada, invocar el caso de uso y traducir el resultado a una respuesta HTTP. |
| Application | `app/Application/Modulo05` | Orquestar cada caso de uso dependiendo unicamente de contratos. |
| Domain | `app/Domain/Modulo05` | Entidad de agenda, estados y reglas invariantes. Sin Eloquent, sin SQL, sin HTTP. |
| Infrastructure | `app/Infrastructure/Modulo05` | Implementar los contratos con Eloquent y consultas SQL. |

### Direccion de las dependencias

Los contratos `AppointmentRepository` y `DoctorAvailabilityRepository` se
declaran en `Domain`. Los casos de uso los reciben por constructor y no conocen
la implementacion concreta. El enlace se registra en `AppServiceProvider`.

En consecuencia, `Infrastructure` depende de `Domain` y no a la inversa. Esta
es la misma inversion de dependencias documentada en la actividad de SOLID del
modulo.

## Decisiones especificas

### 1. La entidad de dominio no es un modelo Eloquent

`Appointment` es una clase pura de PHP que valida sus invariantes en el
constructor y expone transiciones explicitas: `confirm()`, `cancel()` y
`reschedule()`. El modelo Eloquent se usa solo dentro de `Infrastructure` para
leer y escribir filas.

Si la entidad extendiera `Model`, cualquier prueba de una regla de negocio
necesitaria una conexion a base de datos y las invariantes podrian evadirse
asignando propiedades directamente.

### 2. Constructores nombrados: `schedule()` y `restore()`

`schedule()` crea una cita nueva y exige fecha futura y estado inicial
`pendiente`. `restore()` reconstruye una cita ya persistida sin volver a
aplicar la validacion temporal.

Sin esa separacion seria imposible leer desde la base una cita cuya fecha ya
paso, porque la regla de fecha futura la rechazaria durante la reconstruccion.

### 3. Dos contratos separados

Guardar y recuperar citas es una responsabilidad distinta de conocer la jornada
laboral de un medico. En el sistema completo la disponibilidad pertenece al
modulo ASII-04.

Separar `DoctorAvailabilityRepository` permite sustituir su implementacion por
una integracion con ese modulo sin modificar los casos de uso ni el repositorio
de citas.

### 4. Tabla propia de disponibilidad

El modulo ASII-04 desarrollo su disponibilidad medica en un proyecto PHP
vanilla independiente, fuera del backend Laravel. A la fecha de esta entrega no
existe en `main` ninguna tabla ni servicio que exponga la jornada de un medico.

Sin esa informacion la regla central obligatoria es inverificable. Se crea por
tanto la migracion `doctor_availabilities`, aislada tras un contrato propio.

Cuando ASII-04 publique su fuente oficial, la sustitucion consiste en escribir
una implementacion alternativa del mismo contrato y cambiar un enlace en
`AppServiceProvider`. Ningun caso de uso cambia.

Alternativa descartada: validar unicamente cruces contra `appointments`. Se
descarto porque permitiria agendar a las tres de la madrugada, lo que
incumpliria la regla central del modulo.

### 5. Validacion de correspondencia entre medico y especialidad

La tabla `appointments` exige `specialty_id`, y la tabla `doctors` declara la
especialidad de cada medico. La base acepta cualquier combinacion, de modo que
sin una regla explicita seria posible registrar una cita de una especialidad
que el medico no atiende.

La comprobacion se realiza en el caso de uso, no en la entidad, porque requiere
consultar datos externos al agregado.

### 6. Deteccion de cruces en la base de datos

La comparacion de intervalos se resuelve mediante una consulta que aprovecha el
indice `idx_appt_doctor_date`, en lugar de cargar las citas del dia en memoria.

La consulta calcula el fin de cada cita sumando su duracion al inicio y excluye
los estados que no bloquean el horario. Al reagendar se excluye ademas la
propia cita.

### 7. Validacion y escritura dentro de una transaccion

La comprobacion de disponibilidad y la insercion se ejecutan dentro de una
transaccion. Una comprobacion previa aislada no descarta que dos solicitudes
simultaneas reserven el mismo intervalo.

Esto reduce la ventana de condicion de carrera, aunque no la elimina por
completo sin un bloqueo explicito sobre las filas del medico.

### 8. El tenant se obtiene del contexto, no del cliente

El identificador de tenant lo resuelve el middleware `tenant` a partir de la
cabecera `X-Tenant-ID` ya validada. Los casos de uso lo reciben mediante un
contrato `TenantContext`.

Aceptar el tenant como parametro de la peticion permitiria que un cliente
consultara datos de otro hospital.

## Consecuencias

### Positivas

- Las reglas de negocio se verifican con dobles en memoria, sin base de datos.
- La fuente de disponibilidad puede sustituirse sin tocar la logica de agenda.
- Cada capa tiene una razon de cambio identificable.
- El acceso a datos queda concentrado en `Infrastructure`.

### Negativas

- Mayor cantidad de clases que una solucion basada solo en Eloquent.
- Se mantiene una traduccion entre la entidad de dominio y el modelo Eloquent.
- La tabla de disponibilidad debera reconciliarse con ASII-04 cuando ese modulo
  publique la suya.
- El enlace de contratos obliga a mantener actualizado `AppServiceProvider`.

## Alternativas descartadas

### Logica dentro del controlador

Descartada. Concentra validacion, negocio, persistencia y respuesta en una sola
clase, e impide probar las reglas sin base de datos.

### Active Record con el modelo Eloquent como entidad

Descartada. Acopla las reglas al esquema y permite evadir las invariantes
mediante asignacion masiva.

### Modificar la tabla `appointments`

Descartada. La tabla pertenece al scaffold comun y otros modulos dependen de su
estructura. Cualquier cambio exigiria coordinacion previa con el equipo.

## Trazabilidad

| Decision | Evidencia |
|---|---|
| Entidad pura de dominio | Pruebas unitarias sin acceso a base de datos |
| Contratos en Domain | Enlace declarado en `AppServiceProvider` |
| Dobles de prueba | `tests/Fakes/Modulo05` |
| Deteccion de cruces | Pruebas de repositorio sobre base de prueba |
| Aislamiento por tenant | Prueba de acceso entre tenants distintos |
| Regla central obligatoria | Pruebas de jornada, cruce y liberacion al cancelar |
