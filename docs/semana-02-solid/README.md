# Tarea 2 — Aplicación de SOLID

## Datos generales

- **Estudiante:** Eddy Adolfo Castro Véliz
- **GitHub:** EddCastro
- **Módulo:** ASII-05 — Citas médicas y agenda
- **Issue relacionado:** #5
- **Principio asignado:** DIP — Dependency Inversion Principle
- **Proceso:** Solicitud, validación de disponibilidad y confirmación o cancelación de cita

## Objetivo

Definir los requisitos del proceso de citas médicas y mejorar su diseño mediante el principio de inversión de dependencias.

La lógica principal de citas deberá depender de abstracciones y no quedar acoplada directamente a implementaciones concretas de persistencia, disponibilidad médica, pacientes, notificaciones o auditoría.

## Alcance funcional

El diseño cubrirá:

- solicitud de una cita médica;
- validación del paciente;
- validación del médico y la especialidad;
- consulta de disponibilidad;
- prevención de cruces de horario;
- registro inicial en estado pendiente;
- confirmación de la cita;
- cancelación con motivo;
- conservación del historial;
- notificación del resultado.

## Reglas transversales

- Todas las operaciones deben respetar el tenant activo.
- Solo usuarios autorizados pueden gestionar citas.
- No se utilizarán datos clínicos reales.
- Las citas canceladas no deben eliminarse.
- Los cambios de estado deben conservar trazabilidad.
- Los errores deben ser claros y reproducibles.
- El diseño debe permitir pruebas mediante dobles o implementaciones en memoria.

## Entregables técnicos previstos

- requisitos funcionales;
- requisitos no funcionales;
- criterios de aceptación;
- diseño antes de aplicar DIP;
- diseño después de aplicar DIP;
- justificación de responsabilidades y dependencias;
- diagramas editables PlantUML;
- matriz de trazabilidad;
- evidencia de validación;
- evidencia Git;
- declaración de uso de IA;
- guía de defensa oral.

## Fuente obligatoria

MVP Cluster. “Diseño de software 2”.

La fuente se utilizará exclusivamente para los principios SOLID cubiertos por la actividad, especialmente DIP. No se atribuirán a esa fuente principios distintos como DRY, KISS o YAGNI.

## Orden de trabajo

1. Definir requisitos funcionales y no funcionales.
2. Redactar criterios de aceptación.
3. Modelar el diseño con dependencias concretas.
4. Identificar problemas de acoplamiento.
5. Aplicar DIP mediante interfaces o puertos.
6. Elaborar los diagramas antes y después.
7. Documentar responsabilidades y dependencias.
8. Validar las fuentes editables.
9. Registrar evidencia Git y preparación de defensa.
10. Preparar el documento final.

## Referencia del equipo

El archivo general de Semana 2 incorporado desde `develop` corresponde al módulo RBAC. Se utilizará únicamente como referencia de organización y no como fuente de requisitos para ASII-05.
