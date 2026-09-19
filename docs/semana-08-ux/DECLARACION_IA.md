# Declaración de uso de inteligencia artificial — Semana 8

## Identificación

| Dato | Información |
|---|---|
| Módulo | ASII-05 — Citas médicas y agenda |
| Estudiante | Eddy Adolfo Castro Véliz |
| Código | 1890-23-16857 |
| GitHub | EddCastro |
| Issue | #5 |
| Semana | 8 — Diseño de experiencia de usuario |
| Rama | `feature/week-08-ux` |

## Herramienta utilizada

Claude, de Anthropic, empleada como apoyo al análisis, al diseño, a la
redacción y a la generación de diagramas, maquetas y scripts de verificación.

La herramienta trabajó sobre una copia del repositorio en un entorno aislado.
La revisión, la publicación de las ramas y la apertura de los pull requests
corresponden al estudiante.

## Propósito del uso

- Estructurar el user flow de cada rol a partir de la matriz de permisos de la semana 5.
- Construir los seis wireframes de baja fidelidad en HTML y exportarlos a PNG.
- Redactar el catálogo de mensajes a partir de los códigos de error del contrato de API.

## Prompts relevantes

1. Diseñar el flujo UX de solicitud, validación de disponibilidad y confirmación o cancelación de cita para Recepcionista, Enfermera y Médico, respetando la matriz de roles de la semana 5.
2. Definir los estados vacío, carga, envío, éxito y error recuperable de cada pantalla.
3. Construir 6 wireframes anotados con marcadores numerados y notas de estados, mensajes, validaciones y reglas de interacción.
4. Asociar cada mensaje de error con su código simbólico del contrato de API.
5. Definir reglas de protección de datos del paciente para la agenda y el detalle de la cita.

## Contenido aceptado

- Flujo en cuatro pasos con indicador de progreso.
- Regla de conservar los datos capturados ante cualquier error recuperable.
- Ofrecer la siguiente fecha con horarios en el estado vacío de la grilla.
- Minimización de datos en la agenda y DPI enmascarado.

## Contenido modificado o rechazado

- Se descartó que el Médico pueda cancelar sus propias citas, para respetar la matriz de roles de la semana 5.
- Se descartó reservar temporalmente el horario al seleccionarlo: agregaría un estado nuevo al módulo, fuera del alcance.
- Se descartó guardar el borrador en almacenamiento persistente del navegador por contener datos de paciente.
- Se descartó que la Enfermera registre una nota cuando el paciente no asistirá: el módulo no tiene esa función; avisa a Recepción, que cancela con motivo.

## Errores detectados y corregidos

| Hallazgo | Corrección |
|---|---|
| El flujo de la Enfermera no contemplaba al paciente que no responde, previsto como EX-05 en la semana 1. | Se agregó la rama "No responde": la cita permanece pendiente. |
| Una sintaxis `backward` dentro de un `if` hacía fallar el user flow de Recepción en PlantUML. | Se reescribió con bloques `repeat`; `-checkonly` termina con código 0. |
| Los marcadores numerados tapaban la primera letra de las etiquetas en los wireframes. | Se desplazaron fuera del elemento y se regeneraron las capturas. |

## Validación humana

El estudiante verificó que cada acción mostrada corresponda a un endpoint existente, que los roles coincidan con la matriz de permisos, que los mensajes usen los códigos del contrato de API y que los diagramas se validen con `-checkonly` (código de salida `0`). Revisó visualmente cada wireframe.

## Responsabilidad académica

La inteligencia artificial se empleó como herramienta de apoyo. El diseño, las
decisiones, la validación y la preparación para la defensa oral corresponden
al estudiante, quien asume la responsabilidad académica sobre el contenido
entregado.
