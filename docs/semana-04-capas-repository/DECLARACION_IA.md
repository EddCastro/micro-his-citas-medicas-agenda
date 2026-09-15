# Declaracion de uso de inteligencia artificial - Modulo ASII-05

## Identificacion

| Dato | Informacion |
|---|---|
| Modulo | ASII-05 - Citas medicas y agenda |
| Estudiante | Eddy Adolfo Castro Veliz |
| GitHub | EddCastro |
| Rama | `feat/mod05-citas-medicas-agenda` |

## Herramienta utilizada

Claude, de Anthropic, empleada como apoyo al analisis, al diseno y a la
redaccion durante toda la construccion del modulo.

La herramienta no ejecuto comandos en el equipo ni publico cambios en el
repositorio. Toda ejecucion, verificacion y confirmacion corresponde al
estudiante.

## Proposito del uso

- Revisar el repositorio base y las convenciones ya establecidas por otros
  modulos antes de escribir codigo.
- Traducir la consigna a una estructura por capas compatible con Laravel.
- Proponer la entidad de dominio, los contratos y los casos de uso.
- Disenar las consultas de cruce de intervalos y de jornada medica.
- Ampliar la cobertura de pruebas y ordenar la evidencia.

## Prompts relevantes

1. Revisar como estructuraron su modulo los companeros que ya publicaron rama,
   e identificar las convenciones comunes del proyecto.
2. Determinar de que rama nacen las ramas nuevas y contra cual se abren los
   pull requests, contrastando la documentacion con el historial real.
3. Analizar la migracion existente de `appointments` y decidir si el modulo
   debe crear una tabla nueva o consumir la del scaffold.
4. Definir la entidad `Appointment` con los cinco estados del esquema y sus
   transiciones validas.
5. Disenar la consulta de cruce de intervalos aprovechando el indice
   `idx_appt_doctor_date`.
6. Escribir dobles en memoria que reproduzcan la regla de cruce para probar
   los casos de uso sin base de datos.
7. Escribir pruebas de integracion que ejecuten el SQL real contra las
   factories del proyecto.

## Verificacion previa a las decisiones

Antes de escribir codigo se revisaron las ramas `feat/mod09-dashboard-ocupacion`,
`feat/mod14-catalogo-medicamentos` y `feat/mod24-contratos-api` para adoptar
las convenciones ya establecidas: ubicacion de capas, registro de enlaces en
`AppServiceProvider`, agrupacion de rutas y declaracion del secreto JWT en
`phpunit.xml`.

Tambien se contrasto la instruccion de la consigna con el historial del
repositorio para determinar la rama base y el destino del pull request, ya que
el README del proyecto indica una rama que fue eliminada.

## Contenido aceptado

- La organizacion en cuatro capas con los contratos declarados en `Domain`.
- La separacion entre repositorio de citas y repositorio de disponibilidad.
- El uso de constructores nombrados `schedule()` y `restore()`.
- La resolucion de la expresion de fin de cita por driver de base de datos.
- La estructura de las tres suites de prueba.

## Contenido modificado o rechazado

- Se descarto modificar la tabla `appointments` del scaffold, porque pertenece
  al proyecto comun y otros modulos dependen de su estructura.
- Se descarto documentar el modulo con arquitectura federada e identificadores
  logicos, porque el repositorio implementa multi-tenant con claves foraneas
  reales.
- Se ajustaron los estados al enum en espanol que ya define la migracion, en
  lugar de introducir una nomenclatura propia.
- Se limito el alcance excluyendo lista de espera y notificaciones, que
  corresponden a otros modulos.

## Errores detectados y corregidos

| Hallazgo | Correccion |
|---|---|
| El modelo Eloquent quedo guardado con el namespace de la entidad de dominio, lo que impedia ejecutar las pruebas de integracion. | Se corrigio el namespace y se verifico con la suite completa. |
| La suite de integracion no estaba declarada en `phpunit.xml`, por lo que no se ejecutaba. | Se agrego la declaracion de la suite. |
| La prueba `ExampleTest` del scaffold fallaba por ausencia del manifiesto de Vite. | Se compilo el frontend; el fallo era previo y ajeno al modulo. |
| La migracion original fallaba en SQLite al declarar restricciones CHECK. | Se condiciono su aplicacion al motor activo. |

## Validacion humana

El estudiante realizo personalmente:

- La instalacion y configuracion del entorno de desarrollo.
- La verificacion de sintaxis de cada archivo con `php -l`.
- La ejecucion de la suite completa y la comprobacion del codigo de salida.
- La validacion de los diagramas con PlantUML y su revision visual.
- La revision de `git status` antes de cada confirmacion.
- La redaccion de los mensajes de commit y su publicacion.
- La lectura y aprobacion de cada documento antes de incorporarlo.

Ninguna afirmacion de esta entrega se incorporo sin comprobarse mediante
ejecucion.

## Responsabilidad academica

La inteligencia artificial se empleo como herramienta de apoyo. El diseno, las
decisiones arquitectonicas, la validacion y la preparacion para la defensa
oral corresponden al estudiante, quien asume la responsabilidad academica
sobre el contenido entregado.
