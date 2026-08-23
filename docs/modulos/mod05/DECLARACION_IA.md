# Declaracion de uso de inteligencia artificial

## Identificacion

| Dato | Informacion |
|---|---|
| Modulo | ASII-05 - Citas medicas y agenda |
| Estudiante | Eddy Adolfo Castro Veliz |
| GitHub | EddCastro |
| Actividad | Tarea 3 - Micro-monolito en PHP vanilla |

## Herramientas utilizadas

| Herramienta | Etapa | Uso |
|---|---|---|
| ChatGPT (OpenAI) | Construccion inicial | Estructura de capas, borradores de clases, esquema SQL y primeras pruebas. |
| Claude (Anthropic) | Revision y correccion | Auditoria del codigo contra la consigna, deteccion de inconsistencias, ampliacion de pruebas y correccion documental. |

Ambas herramientas se emplearon como apoyo. Ninguna ejecuto comandos en el
equipo ni publico cambios en el repositorio: toda ejecucion y toda decision
final corresponden al estudiante.

## Proposito del uso

- Analizar la consigna y traducirla a una estructura por capas.
- Proponer borradores de entidad, contratos, casos de uso y adaptadores.
- Revisar la correspondencia entre la documentacion y el codigo.
- Ampliar la cobertura de pruebas.
- Ordenar la evidencia de validacion.

## Prompts relevantes

### Etapa de construccion

1. Estructurar un micro-monolito en PHP 8.2 vanilla con las capas
   Presentation, Application, Domain y Persistence, sin framework.
2. Definir la entidad `Appointment` con los estados pendiente, confirmada y
   cancelada, y sus reglas de transicion.
3. Escribir el esquema SQLite para citas y disponibilidad medica, con
   restricciones e indices.
4. Implementar repositorios PDO con sentencias preparadas para guardar,
   recuperar y actualizar citas.
5. Construir dobles en memoria que implementen los mismos contratos para
   pruebas sin base de datos.

### Etapa de revision

6. Revisar el proyecto completo contra los requisitos tecnicos de la consigna e
   indicar que falta.
7. Comparar la especificacion con el codigo y senalar donde no coinciden.
8. Ampliar las pruebas para cubrir la persistencia real y no solo los dobles.
9. Reescribir la evidencia usando salidas reales de la terminal en lugar de
   descripciones.

## Contenido aceptado

- La organizacion en cuatro capas con los contratos declarados en `Domain`.
- La separacion entre `AppointmentRepository` y `AvailabilityRepository`.
- El uso de constructores nombrados `schedule()` y `restore()`.
- El esquema SQLite con restricciones `CHECK` e indices por medico.
- La estructura de la suite de pruebas.

## Contenido modificado o rechazado

- Se ajustaron los mensajes de error al dominio de citas medicas.
- Se unificaron los identificadores ficticios usados en las pruebas.
- Se descarto agregar dependencias externas para mantener el proyecto en PHP
  vanilla, conforme a la prohibicion expresa de la consigna.
- Se descarto documentar la propiedad de datos mediante UUID logicos, porque
  ese modelo corresponde a una actividad distinta y no esta implementado en
  este codigo.

## Errores detectados durante la revision

La revision asistida permitio identificar defectos reales que fueron
corregidos y verificados:

| Hallazgo | Correccion aplicada |
|---|---|
| `Appointment::confirm()` permitia confirmar una cita ya confirmada. | Se agrego la validacion de transicion y una prueba que la cubre. |
| Las clases PDO y el esquema SQL nunca se habian ejecutado: las pruebas solo usaban dobles en memoria. | Se creo `tests/integration.php` con seis pruebas sobre una base SQLite real. |
| La especificacion afirmaba reglas que el codigo no implementaba. | Se reescribio la especificacion vinculando cada regla al metodo que la verifica. |
| `EVIDENCIA.md` y `DECLARACION_IA.md` existian duplicados en la raiz y en `docs/modulos/mod05/`. | Se eliminaron las copias de la raiz. |
| La evidencia describia resultados en lugar de mostrarlos. | Se reemplazo por salidas literales de la terminal. |

Tambien se corrigieron dos errores introducidos por sugerencias de la
herramienta durante la sesion de trabajo: un caracter de escape invalido en un
script de PowerShell y un archivo PHP escrito con marca BOM que impedia su
ejecucion. Ambos fueron detectados al ejecutar el codigo y corregidos antes de
confirmar los cambios.

## Validacion humana

El estudiante realizo personalmente:

- La ejecucion de `php -l` sobre los archivos modificados.
- La ejecucion de la suite completa mediante `php tests/all.php`.
- La verificacion del codigo de salida del runner.
- La revision de `git status` antes de cada confirmacion.
- La redaccion de los mensajes de commit y su publicacion.
- La lectura y aprobacion de cada documento antes de incorporarlo.

Ninguna afirmacion de este repositorio se incorporo sin comprobarse mediante
ejecucion.

## Responsabilidad academica

La inteligencia artificial se utilizo como herramienta de apoyo al analisis y a
la redaccion. El diseno, las decisiones arquitectonicas, la validacion y la
preparacion para la defensa oral corresponden al estudiante, quien asume la
responsabilidad academica sobre el contenido entregado.
