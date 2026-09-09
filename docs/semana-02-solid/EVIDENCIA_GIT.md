# Evidencia de Git - Tarea 2 SOLID

## Datos generales

- **Estudiante:** Eddy Adolfo Castro Véliz
- **GitHub:** EddCastro
- **Módulo:** ASII-05 - Citas médicas y agenda
- **Issue relacionado:** #5
- **Principio aplicado:** Dependency Inversion Principle (DIP)
- **Repositorio:** https://github.com/compilations-teams/sistema-hospitalario-integrado-SistenasII-2026
- **Rama:** feature/asii-05-citas-medicas-y-agenda-eddcastro
- **Etiqueta de entrega:** solid-dip-asii-05-v1.0

## Enlace verificable a un commit

El siguiente commit contiene la declaración ampliada del uso de inteligencia artificial y forma parte de la evidencia de la actividad:

https://github.com/compilations-teams/sistema-hospitalario-integrado-SistenasII-2026/commit/1cee9ac9a4adc4eb05feff9c8c6d0fb9f7570381

## Commits propios relacionados con la Tarea 2

| Commit | Propósito |
|---|---|
| `982a183` | Definir RF, RNF y criterios de aceptación. |
| `d255fab` | Modelar el flujo de citas antes y después de aplicar DIP. |
| `bf56199` | Documentar la fuente obligatoria de DIP. |
| `b64962d` | Agregar evidencia Git de la Tarea 2. |
| `79da60d` | Agregar la declaración inicial de uso de IA. |
| `d9bf583` | Agregar la guía para la defensa oral. |
| `1cee9ac` | Ampliar la declaración de IA con prompts, cambios y validación humana. |

## Aclaración sobre commits integrados

El commit `a938bc1` corresponde a la integración de cambios de `origin/develop` en la rama del módulo. No se contabiliza como aporte propio.

## Comando para consultar el historial

```powershell
git log --oneline --decorate -10
```

## Árbol técnico de la Tarea 2

```text
docs/module-05/tarea-02-solid/DECLARACION_IA.md
docs/module-05/tarea-02-solid/EVIDENCIA_GIT.md
docs/module-05/tarea-02-solid/GUIA_DEFENSA_ORAL.md
docs/module-05/tarea-02-solid/README.md
docs/module-05/tarea-02-solid/criterios-aceptacion.md
docs/module-05/tarea-02-solid/diseno-antes-dip.png
docs/module-05/tarea-02-solid/diseno-antes-dip.puml
docs/module-05/tarea-02-solid/diseno-despues-dip.png
docs/module-05/tarea-02-solid/diseno-despues-dip.puml
docs/module-05/tarea-02-solid/diseno-dip-antes-despues.md
docs/module-05/tarea-02-solid/fuente-dip.md
docs/module-05/tarea-02-solid/requisitos-rf-rnf.md
```

## Comando para obtener el árbol

```powershell
git ls-tree -r --name-only HEAD docs/module-05/tarea-02-solid
```

## Evidencia de validación de PlantUML

Los diagramas editables fueron validados con el siguiente comando:

```powershell
java -jar "$HOME\Tools\PlantUML\plantuml.jar" -checkonly archivo.puml
$LASTEXITCODE
```

El código de salida obtenido para ambos diagramas fue `0`, lo cual indica que PlantUML no encontró errores.

## Validaciones de Git realizadas

```powershell
git diff --cached --check
git status
```

El comando `git diff --cached --check` no mostró errores. Después de cada publicación, `git status` confirmó que la rama estaba sincronizada y que el árbol de trabajo estaba limpio.

## Fuentes editables y exportadas

Los archivos `.puml` son las fuentes editables de los diagramas. Los archivos `.png` corresponden a las versiones exportadas y revisadas visualmente.

## Estado de publicación

Los commits fueron enviados a GitHub en la rama `feature/asii-05-citas-medicas-y-agenda-eddcastro`. La etiqueta `solid-dip-asii-05-v1.0` se publicará cuando se complete la entrega final.
