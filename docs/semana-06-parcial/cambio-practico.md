# Registro del cambio práctico

Cambio implementado y defendido en la primera evaluación parcial del módulo
ASII-05, Citas médicas y agenda.

| Dato | Información |
|---|---|
| Estudiante | Eddy Adolfo Castro Véliz |
| Código | 1890-23-16857 |
| Rama | `feature/asii-05-semana-06-parcial-eddcastro` |
| Commits | `4bb4082`, `bf5a554`, `38dfd61` |

## El problema

Desde la semana 3 el módulo declaraba una limitación conocida:

> La validación de disponibilidad y la escritura de la cita no se ejecutan
> dentro de una transacción, por lo que una condición de carrera entre dos
> solicitudes simultáneas no queda descartada.

En la semana 4 se introdujo la transacción, lo que redujo la ventana pero no
la cerró. El texto de la limitación se ajustó, sin desaparecer:

> La transacción reduce la ventana de condición de carrera, pero no la elimina
> sin un bloqueo explícito sobre las filas del médico.

Este cambio cierra esa limitación.

## Por qué la transacción no bastaba

El método `hasOverlap()` ejecutaba una consulta de solo lectura:

```php
return $query->exists();
```

En el nivel de aislamiento por defecto, una lectura no bloquea las filas que
examina. Dos transacciones concurrentes que soliciten el mismo horario siguen
esta secuencia:

| Momento | Transacción A | Transacción B |
|---|---|---|
| 1 | `BEGIN` | |
| 2 | | `BEGIN` |
| 3 | `hasOverlap` → libre | |
| 4 | | `hasOverlap` → libre |
| 5 | `INSERT` cita | |
| 6 | | `INSERT` cita |
| 7 | `COMMIT` | |
| 8 | | `COMMIT` |

Ambas leyeron el mismo estado antes de que cualquiera escribiera. El resultado
son dos citas activas del mismo médico en el mismo intervalo: exactamente el
estado que la regla central del módulo prohíbe.

## La solución

Dos capas de defensa independientes.

### Primera capa: bloqueo pesimista

Cuando la consulta de cruce corre dentro de una transacción, bloquea las filas
de la agenda del médico para ese día antes de examinarlas.

```php
if (DB::transactionLevel() > 0) {
    $this->lockDoctorAgenda($tenantId, $doctorId, $inicio);
}
```

La transacción B queda en espera en el paso 4 hasta que A confirme o revierta.
Cuando B continúa, ya ve la cita de A y la detecta como cruce.

### Alcance del bloqueo

Se bloquea un médico y un día, no la tabla ni toda la agenda del médico:

```php
AppointmentModel::query()
    ->where('tenant_id', $tenantId)
    ->where('doctor_id', $doctorId)
    ->whereDate('scheduled_at', $inicio->format('Y-m-d'))
    ->lockForUpdate()
    ->get(['id']);
```

Dos citas de días distintos nunca se cruzan, y dos médicos distintos tampoco.
Un bloqueo más amplio serializaría operaciones que no compiten entre sí y
reduciría la capacidad del sistema sin ganar nada.

### Segunda capa: índice único parcial

El bloqueo protege mientras la escritura pase por el módulo. El índice protege
el mismo invariante a nivel de base de datos:

```sql
CREATE UNIQUE INDEX uq_appt_doctor_slot_active
ON appointments (tenant_id, doctor_id, scheduled_at)
WHERE status IN ('pendiente', 'confirmada');
```

Es parcial a propósito. Si cubriera todos los estados, una cita cancelada
seguiría ocupando su horario y sería imposible reutilizarlo, lo que
contradiría la regla de que cancelar libera el intervalo.

### Por qué dos capas

| Vía de escritura | Bloqueo | Índice |
|---|:---:|:---:|
| Caso de uso del módulo | Protege | Protege |
| Carga masiva o migración | No protege | Protege |
| Consulta manual en la base | No protege | Protege |
| Otro módulo que escriba directo | No protege | Protege |

El bloqueo resuelve la concurrencia; el índice hace imposible el estado
inválido con independencia de quién escriba.

## Alcance y límite

El índice cubre el **inicio exacto** de la cita. Un solape parcial —una cita de
10:00 a 10:30 y otra de 10:15 a 10:45— no viola el índice, pero sí lo detecta
la consulta de cruce bajo bloqueo.

Cerrar también ese caso a nivel de base requeriría una restricción de exclusión
por rango, que en PostgreSQL necesita la extensión `btree_gist`. Queda
documentado como mejora futura y no como algo implementado.

## Alternativas evaluadas

| Alternativa | Efecto | Por qué se descartó |
|---|---|---|
| Bloqueo optimista con número de versión | Detecta el conflicto al escribir | La cita nueva no tiene versión previa que comparar |
| Serializar toda la tabla | Elimina el conflicto | Reduce la concurrencia del sistema entero |
| Revalidar antes de confirmar la escritura | Reduce la ventana | No la elimina; el problema se repite a menor escala |
| Restricción de exclusión por rango | Cubre también el solape parcial | Requiere una extensión no disponible por defecto |

## Evidencia

Seis pruebas de integración sobre base de datos real:

| Prueba | Qué verifica |
|---|---|
| `la verificacion de cruce ocurre dentro de transaccion` | Condición previa del bloqueo |
| `dos solicitudes al mismo horario no producen dos citas` | El invariante se sostiene |
| `un solape parcial tampoco produce dos citas` | Cubre el caso que el índice no alcanza |
| `el bloqueo no impide agendar en otro dia` | El alcance no es excesivo |
| `el bloqueo no impide agendar con otro medico` | El alcance no es excesivo |
| `cancelar libera el horario bajo el indice parcial` | El índice parcial se comporta como se diseñó |

Las dos últimas importan tanto como las primeras: una corrección de
concurrencia que bloquee de más resuelve un problema creando otro.

### Ejecución

```
Tests:    148 passed (208 assertions)
```

Código de salida: `0`. El total incluye las pruebas de los módulos 03 y 20,
lo que confirma que el cambio no altera el comportamiento de los demás.

## Trazabilidad

| Elemento | Referencia |
|---|---|
| Requisito no funcional | RNF-03, atomicidad entre validación y escritura |
| Regla de negocio | RN-07, sin cruce con cita que bloquee el horario |
| Criterio de aceptación | CA-05, solicitud que se cruza con una cita activa |
| Limitación declarada | Semana 3 y semana 4, sección Limitaciones |
| Decisiones | D-28 a D-32 de la matriz decisión → evidencia |

## Qué no resuelve

- No cubre el solape parcial a nivel de base de datos.
- No aplica en SQLite, que serializa las escrituras a nivel de conexión; las
  pruebas verifican el invariante a nivel de aplicación.
- Introduce espera entre solicitudes que compiten por la misma agenda. Es el
  costo deliberado de garantizar el invariante.
