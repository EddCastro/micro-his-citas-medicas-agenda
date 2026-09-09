# Generación y validación de diagramas UML

## Herramientas utilizadas

- Java: 21.0.5 LTS
- PlantUML: 1.2026.6
- Graphviz: 2.44.1
- Sistema operativo: Windows
- Consola: Windows PowerShell

## Archivos fuente

Los diagramas fueron elaborados mediante archivos editables PlantUML:

- casos-de-uso-solicitud-cita.puml
- actividad-solicitud-cita.puml
- secuencia-global-solicitud-cita.puml

## Imágenes generadas

Cada archivo PlantUML produce una imagen PNG con el mismo nombre:

- casos-de-uso-solicitud-cita.png
- actividad-solicitud-cita.png
- secuencia-global-solicitud-cita.png

## Ubicación de PlantUML

El archivo ejecutable de PlantUML se encuentra fuera del repositorio:

    C:\Users\eddya\Tools\PlantUML\plantuml.jar

El archivo plantuml.jar no se agrega al repositorio.

## Validación de sintaxis

Desde la raíz del repositorio se ejecutó:

    java -jar "$HOME\Tools\PlantUML\plantuml.jar" -checkonly ".\docs\module-05\tarea-01-uml\*.puml"

El código de salida obtenido fue:

    0

Esto indica que los archivos no contienen errores de sintaxis detectados por PlantUML.

## Generación de imágenes PNG

Desde la raíz del repositorio se ejecutó:

    java -jar "$HOME\Tools\PlantUML\plantuml.jar" -tpng ".\docs\module-05\tarea-01-uml\*.puml"

PlantUML generó automáticamente una imagen PNG por cada archivo fuente.

## Regeneración de un solo diagrama

Ejemplo para regenerar únicamente el diagrama de casos de uso:

    java -jar "$HOME\Tools\PlantUML\plantuml.jar" -tpng ".\docs\module-05\tarea-01-uml\casos-de-uso-solicitud-cita.puml"

## Verificación de archivos generados

Para consultar los PNG creados se utilizó:

    Get-ChildItem .\docs\module-05\tarea-01-uml -Filter *.png |
      Select-Object Name, Length, LastWriteTime

## Resultado

Se generaron y revisaron visualmente los tres diagramas. Las fuentes `.puml` permanecen dentro del repositorio para que el proceso sea editable y reproducible.
