# Evidencia Git - Semana 3

## Datos generales

- **MÃ³dulo:** ASII-05 - Citas mÃ©dicas y agenda
- **Estudiante:** Eddy Adolfo Castro VÃ©liz
- **GitHub:** EddCastro
- **Issue:** #5
- **Rama:** `feature/asii-05-citas-medicas-y-agenda-eddcastro`

## Entregable

La Semana 3 corresponde al diseÃ±o de la vista arquitectÃ³nica del mÃ³dulo ASII-05 y sus dependencias con el Sistema Hospitalario Integrado.

Los artefactos tÃ©cnicos principales son:

- `README.md`
- `vista-arquitectonica.puml`
- `vista-arquitectonica.png`

## Commit tÃ©cnico inicial

- **Commit:** `41b22ab7d57c32dfdc49a23e923ce5a0ec6f5934`
- **Mensaje:** `docs(module-05): add week 3 architectural view (#5)`
- **Enlace:** https://github.com/compilations-teams/sistema-hospitalario-integrado-SistenasII-2026/commit/41b22ab7d57c32dfdc49a23e923ce5a0ec6f5934

## Historial especÃ­fico

```powershell
git log --oneline --decorate -- docs/module-05/semana-03-arquitectura
```

Resultado inicial:

```text
41b22ab docs(module-05): add week 3 architectural view (#5)
```

## ValidaciÃ³n de PlantUML

La fuente editable del diagrama fue validada con:

```powershell
java -jar "$HOME\Tools\PlantUML\plantuml.jar" -checkonly ".\docs\module-05\semana-03-arquitectura\vista-arquitectonica.puml"
$LASTEXITCODE
```

El cÃ³digo de salida obtenido fue:

```text
0
```

Esto confirma que PlantUML no detectÃ³ errores de sintaxis.

## GeneraciÃ³n del diagrama

```powershell
java -jar "$HOME\Tools\PlantUML\plantuml.jar" -tpng ".\docs\module-05\semana-03-arquitectura\vista-arquitectonica.puml"
```

Se generÃ³ correctamente `vista-arquitectonica.png` y posteriormente se realizÃ³ una revisiÃ³n visual.

## SincronizaciÃ³n con develop

Antes de iniciar la Semana 3 se integraron los cambios mÃ¡s recientes de `origin/develop` en la rama del mÃ³dulo.

El commit de merge no se considera aporte funcional propio de la Semana 3.

## Estado de publicaciÃ³n

El commit tÃ©cnico inicial fue publicado en GitHub dentro de la rama del mÃ³dulo.
