# Semana 7 — Diseño de componentes y refactorización

Módulo **ASII-05 — Citas médicas y agenda**.

| Dato | Información |
|---|---|
| Estudiante | Eddy Adolfo Castro Véliz |
| Código | 1890-23-16857 |
| GitHub | EddCastro |
| Correo | ecastrov5@miumg.edu.gt |
| Issue | #5 |
| Rama | `feature/week-07-componentes` |
| Código analizado | Repositorio grupal, rama `feature/asii-05-semana-06-parcial-eddcastro` |

## Tarea

Diseñar los componentes backend y frontend propios del flujo **solicitud,
validación de disponibilidad y confirmación o cancelación de cita**, y
refactorizar conceptualmente el punto con mayor acoplamiento entre citas,
agenda médica, disponibilidad, confirmación, cancelación y concurrencia,
separando UI, aplicación, dominio y persistencia sin ampliar el módulo.

## Estado del diseño

El backend del diagrama de componentes **existe**: son las clases de la
implementación Laravel de las semanas 4 a 6. Lo marcado como
`<<propuesto>>` es el diseño de esta semana y todavía no está implementado:
`AgendaLock`, `TimeSlot`, `ErrorMapper` y todo el frontend, porque el módulo
se entregó como API sin interfaz.

## Resultado principal

El punto de mayor acoplamiento es
`EloquentAppointmentRepository::hasOverlap()`. Es el único componente que toca
los seis conceptos de la consigna: decide qué estados ocupan la agenda, calcula
el cruce de intervalos en SQL y, desde la semana 6, bloquea la agenda del
médico como efecto oculto, **solo si** detecta una transacción abierta.

El análisis también encontró que confirmar y cancelar se ejecutan sin
transacción: si Enfermería confirma mientras Recepción cancela, gana la última
escritura.

El refactor separa el bloqueo en un puerto explícito (`AgendaLock`), deja
`hasOverlap()` como consulta pura, define el cruce una sola vez (`TimeSlot`),
protege confirmar y cancelar con `findByIdForUpdate` y tipa los errores para
emitir los códigos del contrato de la semana 5.

## Entregables

| Evidencia pedida | Archivo |
|---|---|
| Diagrama de componentes | [`componentes.png`](componentes.png) — fuente [`componentes.puml`](componentes.puml) |
| Contratos de entrada/salida | [`contratos-entrada-salida.md`](contratos-entrada-salida.md) |
| Comparación antes/después con justificación | [`refactor-antes-despues.md`](refactor-antes-despues.md) |
| Diagrama antes | [`refactor-antes.png`](refactor-antes.png) — fuente `.puml` |
| Diagrama después | [`refactor-despues.png`](refactor-despues.png) — fuente `.puml` |
| Guía de defensa oral | [`GUIA_DEFENSA_ORAL.md`](GUIA_DEFENSA_ORAL.md) |
| Declaración de IA | [`DECLARACION_IA.md`](DECLARACION_IA.md) |

![Componentes](componentes.png)

## Coherencia con semanas anteriores

| Decisión previa | Se conserva así |
|---|---|
| DIP y contratos en Domain (semanas 2 y 4) | Los puertos nuevos también se declaran en Domain |
| Dos contratos separados, citas y disponibilidad (D-11) | Se mantienen; se agrega un tercero para el bloqueo |
| Detección de cruces en la base con índice (D-14) | `hasOverlap()` conserva su SQL; solo pierde el efecto secundario |
| Bloqueo por médico y día (D-28, D-29) | Mismo alcance, ahora explícito |
| Índice único parcial (D-30, D-31) | Se conserva y su violación se traduce a "horario ocupado" |
| Códigos simbólicos y 409 (contrato semana 5) | Pasan de propuesta a diseño concreto mediante `code()` y `ErrorMapper` |

## Alcance de la entrega

Incluye:

- Componentes backend existentes y propuestos del flujo asignado.
- Componentes frontend propuestos para ese flujo.
- Contratos de entrada, salida y error de cada componente.
- Un refactor conceptual con código antes y después y su justificación.

No incluye:

- Implementación del refactor en el repositorio grupal.
- Reagendamiento (CU-04): existe en el código y usa `hasOverlap()`, así que
  se beneficia del refactor, pero no pertenece al flujo asignado.
- Lista de espera, notificaciones ni registro de pacientes.

## Validación

```powershell
java -jar "$HOME\Tools\PlantUML\plantuml.jar" -checkonly ".\docs\semana-07-componentes\*.puml"
```

El comando finalizó con código de salida `0`. Cada fragmento de código del
"antes" se copió de la rama indicada y se comparó con el archivo original.

## Datos

Todos los datos de ejemplo son ficticios.
