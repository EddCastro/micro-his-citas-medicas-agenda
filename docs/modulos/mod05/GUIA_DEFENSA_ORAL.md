# Guia de defensa oral - Tarea 3

Documento de preparacion personal. Contiene las preguntas mas probables sobre
el modulo y la respuesta que el estudiante debe poder dar sin apoyo externo.

## Identificacion

| Dato | Informacion |
|---|---|
| Modulo | ASII-05 - Citas medicas y agenda |
| Estudiante | Eddy Adolfo Castro Veliz |
| Flujo | Solicitud, validacion de disponibilidad y confirmacion o cancelacion de cita |

## Resumen en treinta segundos

Micro-monolito en PHP 8.2 vanilla, sin framework, organizado en cuatro capas.
El dominio define la entidad `Appointment` y dos contratos Repository. Los
casos de uso dependen de esos contratos, nunca de PDO. La persistencia los
implementa con SQLite mediante sentencias preparadas, y existen dobles en
memoria que cumplen los mismos contratos para probar sin base de datos. Diez
pruebas automatizadas se ejecutan con `php tests/all.php`.

## Preguntas sobre arquitectura

**Por que las interfaces estan en Domain y no en Persistence.**
Porque quien define la necesidad es el negocio, no el almacenamiento. Si la
interfaz viviera en `Persistence`, la capa de negocio dependeria de la de
infraestructura. Al declararla en `Domain`, es `Persistence` quien depende del
dominio. Esa es la inversion de dependencias.

**Que gano separando en capas si el proyecto es pequeno.**
Puedo probar las reglas sin base de datos y puedo cambiar el motor sin tocar la
logica. Las pruebas unitarias corren con dobles y no necesitan SQLite.

**Por que dos contratos y no uno solo con mas metodos.**
Guardar citas y consultar disponibilidad son responsabilidades distintas. En el
sistema hospitalario completo, la disponibilidad medica pertenece al modulo de
medicos, no al de citas. Separarlas permite que esa implementacion se sustituya
por una integracion con el otro modulo sin tocar el repositorio de citas.

**Que hace exactamente el controlador.**
Recibe un arreglo con datos primitivos, los convierte a los tipos del dominio y
llama al caso de uso. No tiene SQL ni decide reglas.

## Preguntas sobre el dominio

**Por que `schedule()` y `restore()` en lugar de un solo constructor.**
`schedule()` crea una cita nueva y exige fecha futura y estado pendiente.
`restore()` reconstruye una cita que ya existe en la base. Si usara la misma
validacion, seria imposible leer desde la base una cita del mes pasado, porque
la regla de fecha futura la rechazaria.

**Por que el constructor es privado.**
Para que nadie pueda crear una cita saltandose las validaciones. La unica forma
de obtener un `Appointment` es a traves de los dos constructores nombrados.

**Que estados existen y que transiciones son validas.**
Pendiente, confirmada y cancelada. Desde pendiente se puede confirmar o
cancelar. Desde confirmada solo se puede cancelar. Desde cancelada no hay
salida: ni confirmar ni volver a cancelar.

**Por que una cita cancelada no se elimina.**
Para conservar trazabilidad. El registro permanece, cambia su estado, y la
consulta de cruces lo excluye porque solo considera pendientes y confirmadas.

## Preguntas sobre persistencia

**Como se detecta un cruce de horarios.**
Se comparan intervalos. Hay cruce cuando el inicio de la nueva cita es anterior
al fin de la existente y el fin de la nueva es posterior al inicio de la
existente. La consulta calcula el fin de cada cita sumando su duracion a la
hora programada, y excluye las canceladas.

**Por que sentencias preparadas.**
Separan el SQL de los datos. El valor nunca se interpreta como parte de la
instruccion, lo que elimina la inyeccion SQL, y el motor puede reutilizar el
plan de ejecucion.

**Por que SQLite.**
No requiere servidor y viene con la extension `pdo_sqlite` de PHP. Cualquiera
puede clonar el repositorio y ejecutar las pruebas sin instalar nada. El motor
no esta fijado en el codigo: se define en `DB_DSN` dentro de `.env`.

**Que pasaria si cambio a MySQL o PostgreSQL.**
Cambiaria el DSN y revisaria la consulta de cruces, porque usa la funcion
`datetime()` de SQLite. El resto del codigo no cambia, porque `Domain` y
`Application` no conocen el motor.

## Preguntas sobre pruebas

**Que es un doble de prueba y para que sirve.**
Una implementacion alternativa del mismo contrato, construida para la prueba.
`InMemoryAvailabilityRepository` devuelve el resultado que le indico por
constructor, asi puedo forzar el rechazo por horario no disponible sin cargar
una agenda. Para el error de persistencia uso una clase anonima cuyo `save()`
lanza una excepcion.

**Por que hay pruebas unitarias y de integracion.**
Las unitarias verifican las reglas de forma aislada y rapida. Las de
integracion verifican que las clases PDO y el esquema SQL funcionan de verdad
contra una base real. Sin las segundas, el codigo de persistencia no tendria
ninguna evidencia de que ejecuta.

**Como se demuestra que las pruebas realmente pasan.**
El runner devuelve `exit(1)` si algo falla. El codigo de salida `0` confirma que
las diez fueron aprobadas, no solo que el script termino.

## Modificacion practica sugerida

Ante la peticion de modificar una regla, la mas segura es exigir una duracion
minima en `Appointment`:

```php
if ($durationMinutes < 15) {
    throw new DomainException('La duracion minima de una cita es de 15 minutos.');
}
```

Despues:

1. Ejecutar `php tests/all.php`.
2. Explicar que la prueba de duracion invalida sigue pasando, porque cero
   tambien es menor que quince.
3. Agregar la regla a la tabla de `ESPECIFICACION.md` para no romper la
   trazabilidad.

Una alternativa util es limitar la antelacion maxima de una cita.

## Limitaciones que debo reconocer

- No hay autoloader PSR-4; las dependencias se declaran con `require`.
- No existe front controller HTTP: el controlador se invoca por metodo.
- La validacion de disponibilidad y la escritura no ocurren dentro de una
  transaccion, por lo que dos solicitudes simultaneas podrian pasar ambas la
  validacion. La mitigacion seria envolver la operacion en una transaccion y
  revalidar antes de escribir.
- No estan implementados reagendamiento, lista de espera ni consulta de agenda,
  porque quedan fuera del flujo asignado.

Reconocer estas limitaciones es preferible a defender algo que el codigo no
hace. Cada una tiene una mitigacion identificada.

## Que no debo afirmar

- Que el modulo esta integrado con el sistema hospitalario. No lo esta.
- Que soporta concurrencia. No hay transaccion.
- Que valida permisos o tenant. Eso corresponde a otros modulos.
