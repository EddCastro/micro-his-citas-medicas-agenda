# Declaración de uso de inteligencia artificial

## Datos de la actividad

- **Estudiante:** Eddy Adolfo Castro Véliz
- **GitHub:** EddCastro
- **Módulo:** ASII-05 - Citas médicas y agenda
- **Actividad:** Aplicación del principio SOLID DIP
- **Flujo analizado:** solicitud, validación de disponibilidad y confirmación o cancelación de cita
- **Issue relacionado:** #5
- **Fecha de elaboración:** 5 de agosto de 2026

## Herramienta utilizada

Se utilizó ChatGPT como herramienta de apoyo para organizar, redactar, revisar y validar parcialmente los artefactos de la actividad.

## Propósito del uso

La inteligencia artificial se utilizó para:

- organizar los requisitos funcionales y no funcionales;
- proponer criterios de aceptación trazables;
- analizar el problema de acoplamiento antes de aplicar DIP;
- proponer contratos, casos de uso y adaptadores para el diseño posterior;
- preparar diagramas editables en PlantUML;
- orientar la validación de archivos y comandos Git;
- mejorar la estructura de la evidencia y la guía de defensa oral.

## Prompts relevantes

Los siguientes son ejemplos representativos de las solicitudes realizadas durante el trabajo:

1. Organizar los requisitos funcionales y no funcionales del módulo de citas médicas y agenda.
2. Definir criterios de aceptación para solicitud, disponibilidad, confirmación y cancelación de citas.
3. Mostrar un diseño antes y después de aplicar el principio de inversión de dependencias.
4. Proponer responsabilidades, contratos y adaptadores para separar la lógica de negocio de Eloquent y Laravel.
5. Generar y corregir diagramas PlantUML que representen el diseño antes y después de DIP.
6. Preparar evidencia Git con commits, historial y archivos relacionados.
7. Elaborar una guía breve para explicar el diseño durante la defensa oral.

## Partes aceptadas

Después de revisar su relación con la consigna y el módulo, se aceptaron como apoyo:

- la estructura inicial de RF y RNF;
- la organización de los criterios de aceptación;
- la separación entre casos de uso, contratos y adaptadores;
- la comparación conceptual del diseño antes y después de DIP;
- la estructura de la matriz de responsabilidades;
- la organización de la evidencia Git y de la guía de defensa.

## Partes modificadas

Durante el proceso se realizaron ajustes sobre las propuestas iniciales:

- los diagramas PlantUML fueron simplificados para mejorar su legibilidad;
- la codificación de los archivos PlantUML se cambió a ASCII por incompatibilidad con UTF-8 con BOM;
- se corrigieron elementos de sintaxis que PlantUML rechazaba;
- el diagrama posterior a DIP se redujo a casos de uso, contratos y adaptadores para evitar líneas cruzadas;
- se aclaró que las clases e interfaces representan una propuesta arquitectónica y todavía no una implementación completa;
- se separaron los commits propios de los commits provenientes de la integración con origin/develop.

## Validación humana realizada

El estudiante realizó las siguientes verificaciones:

- revisó el contenido de los documentos creados;
- ejecutó personalmente los comandos en PowerShell;
- validó los diagramas con PlantUML mediante la opción -checkonly;
- confirmó que PlantUML devolviera el código de salida 0;
- abrió y revisó visualmente las imágenes PNG generadas;
- verificó los archivos con git status y git diff --cached --check;
- creó commits con propósito y los publicó en su rama de GitHub;
- comprobó que la rama quedara sincronizada y el árbol de trabajo limpio.

## Limitaciones

La inteligencia artificial no ejecutó comandos directamente en el equipo del estudiante ni sustituyó la validación del repositorio. Las decisiones propuestas deben ser comprendidas y defendidas por el estudiante. El diseño DIP documentado todavía requiere implementación y pruebas dentro del sistema hospitalario.

## Responsabilidad académica

La herramienta fue utilizada como apoyo. El estudiante conserva la responsabilidad sobre la revisión, comprensión, validación, defensa oral y entrega final de los artefactos.
