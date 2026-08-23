# ADR-001: Arquitectura por capas con patron Repository

## Estado

Aceptado.

## Contexto

La Tarea 3 exige construir un micro-monolito ejecutable en PHP 8.2+ vanilla,
sin framework, que resuelva el flujo de solicitud, validacion de
disponibilidad y confirmacion o cancelacion de una cita medica.

Las restricciones impuestas por la consigna son:

- Separacion en las capas Presentation, Application, Domain y Persistence.
- Acceso a datos mediante PDO con sentencias preparadas.
- Configuracion fuera del codigo.
- Pruebas automatizadas que cubran camino feliz, regla de dominio y error de
  persistencia.
- Prohibicion expresa de utilizar cualquier framework.

Sin un limite explicito entre negocio y almacenamiento, la logica de citas
quedaria mezclada con SQL, lo que impediria probar las reglas sin una base de
datos disponible y ataria el modulo a un motor concreto.

## Decision

Se adopta una arquitectura por capas con dependencias dirigidas hacia el
dominio, y se define el patron Repository como frontera entre la logica de
negocio y la persistencia.

### Distribucion de responsabilidades

| Capa | Responsabilidad | Componentes |
|---|---|---|
| Presentation | Recibe datos externos, los convierte a tipos del dominio e invoca un caso de uso. No contiene SQL ni reglas. | `AppointmentController` |
| Application | Orquesta el caso de uso y depende unicamente de abstracciones. | `RequestAppointment`, `ConfirmAppointment`, `CancelAppointment` |
| Domain | Entidad, reglas invariantes y contratos Repository. No conoce PDO, SQL ni HTTP. | `Appointment`, `AppointmentRepository`, `AvailabilityRepository` |
| Persistence | Implementa los contratos usando PDO y SQLite, y provee dobles en memoria. | `PdoAppointmentRepository`, `PdoAvailabilityRepository`, `InMemoryAppointmentRepository`, `InMemoryAvailabilityRepository` |

### Direccion de las dependencias

Los contratos `AppointmentRepository` y `AvailabilityRepository` se declaran en
`Domain`, no en `Persistence`. Los casos de uso reciben esas interfaces por
constructor y desconocen la implementacion concreta que se les inyecta.

En consecuencia, `Persistence` depende de `Domain`, y no al reves. Esta es la
misma inversion de dependencias documentada en la actividad de SOLID del
modulo.

## Decisiones especificas

### 1. Los contratos viven en Domain

Si las interfaces se declararan en `Persistence`, la capa de negocio dependeria
de la de infraestructura y se perderia la posibilidad de sustituir el
almacenamiento sin tocar las reglas.

### 2. SQLite como motor de esta entrega

SQLite no requiere servidor, se distribuye con la extension `pdo_sqlite` de PHP
y permite ejecutar el proyecto desde una instalacion limpia sin configuracion
adicional. Esto favorece la reproducibilidad exigida por la consigna.

El motor no esta fijado en el codigo: se resuelve por la variable `DB_DSN` en
`.env`, leida por `config/env.php`. Cambiar de motor implica cambiar el DSN y
revisar las funciones especificas de SQLite empleadas en la consulta de
colision.

### 3. Sentencias preparadas en todas las consultas

Todo acceso a datos usa `PDO::prepare` con parametros nombrados. No se
concatenan valores dentro del SQL, lo que elimina la via principal de inyeccion
y permite que el motor reutilice el plan de ejecucion.

### 4. Dos dobles en memoria para pruebas

`InMemoryAppointmentRepository` e `InMemoryAvailabilityRepository` implementan
los mismos contratos que las versiones PDO. Esto permite verificar las reglas
de aplicacion de forma determinista y sin base de datos.

El doble de disponibilidad recibe el resultado esperado por constructor, lo que
facilita provocar el rechazo por horario no disponible sin construir una agenda
completa.

### 5. La validacion de disponibilidad es un contrato aparte

Se separo `AvailabilityRepository` de `AppointmentRepository` en lugar de
agregar un metodo mas al primero. Consultar la jornada de un medico y detectar
cruces es una responsabilidad distinta de guardar y recuperar citas, y en el
sistema completo esa informacion pertenece al modulo de medicos y
disponibilidad.

### 6. La entidad protege sus invariantes

`Appointment` tiene constructor privado y dos constructores nombrados:
`schedule()` para citas nuevas, que exige fecha futura y estado inicial
pendiente, y `restore()` para reconstruir una cita ya persistida sin volver a
aplicar la validacion temporal.

Sin esa separacion seria imposible leer desde la base una cita pasada, porque
la regla de fecha futura la rechazaria.

## Consecuencias

### Positivas

- Las reglas de negocio se prueban sin base de datos.
- El motor de almacenamiento puede sustituirse sin modificar `Domain` ni
  `Application`.
- Cada capa tiene una razon de cambio identificable.
- El uso de sentencias preparadas queda concentrado en `Persistence`.

### Negativas

- Mayor cantidad de archivos y clases que una solucion directa.
- Requiere definir contratos antes de escribir la persistencia.
- Cada implementacion nueva obliga a mantener dos versiones del mismo contrato.
- La ausencia de autoloader obliga a declarar `require` explicitos en los
  puntos de entrada.

## Alternativas descartadas

### Acceso directo a la base desde el controlador

Descartada. Concentra validacion, negocio, persistencia y respuesta en una sola
clase, impide probar reglas sin base de datos y contradice la separacion por
capas exigida.

### Active Record

Descartada. Acopla la entidad al esquema de la base y le atribuye
responsabilidad de persistencia, lo que impide construir una cita en memoria
sin conexion disponible.

### Un unico repositorio con todas las operaciones

Descartada. Mezclaria la gestion de citas con la consulta de disponibilidad
medica, que en el sistema completo pertenece a otro modulo.

## Trazabilidad

| Decision | Evidencia ejecutable |
|---|---|
| Contratos en Domain | `tests/run.php` ejecuta los casos de uso con dobles |
| SQLite via PDO | `tests/integration.php` aplica `database/schema.sql` sobre una base real |
| Sentencias preparadas | `PdoAppointmentRepository` y `PdoAvailabilityRepository` |
| Dobles de prueba | Prueba de error de persistencia mediante clase anonima |
| Invariantes de la entidad | Pruebas de fecha pasada, duracion invalida y confirmacion duplicada |
