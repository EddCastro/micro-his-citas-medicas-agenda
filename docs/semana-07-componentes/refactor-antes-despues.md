# Refactorización — antes y después

Refactor **conceptual** del punto con mayor acoplamiento del flujo. No agrega
funcionalidades: el módulo sigue solicitando, validando, confirmando y
cancelando exactamente lo mismo.

## 1. Cómo se eligió el punto

Se revisó cada componente del flujo contando con cuántas responsabilidades y
con cuántos datos ajenos trabaja.

| Componente | Responsabilidades | Datos que toca | Acoplamiento |
|---|---|---|---|
| `ConfirmAppointment` | 1 (transición) | `appointments` | Bajo |
| `CancelAppointment` | 1 (transición) | `appointments` | Bajo |
| `Appointment` | Invariantes de estado | Ninguno externo | Bajo |
| `AppointmentController` | Traducir entrada | Ninguno | Bajo |
| **`AvailabilityRepository::isAvailable`** | **4** | **`doctor_availability` (de ASII-04) + `appointments`** | **Alto** |

El método `isAvailable()` es el único lugar donde se cruzan los seis conceptos
de la consigna: citas, agenda médica, disponibilidad, confirmación,
cancelación y concurrencia.

## 2. Antes

![Antes](refactor-antes.png)

Código real de `src/Persistence/PdoAvailabilityRepository.php`, resumido:

```php
public function isAvailable(int $doctorId, DateTimeImmutable $scheduledAt, int $durationMinutes): bool
{
    // 1. Jornada del médico: dato que pertenece a ASII-04
    SELECT COUNT(*) FROM doctor_availability WHERE doctor_id = ... AND weekday = ...
    if (0) return false;

    // 2. Regla de cruce y 3. regla de estado, escritas en SQL
    SELECT COUNT(*) FROM appointments
     WHERE doctor_id = ... AND status != 'cancelled'
       AND scheduled_at < :end AND datetime(scheduled_at, '+' || duration_minutes || ' minutes') > :start
    return count === 0;
}
```

Y en la versión Laravel (semana 6), la concurrencia depende de un estado
implícito:

```php
if (DB::transactionLevel() > 0) {   // 4. el bloqueo ocurre solo "si alguien abrió transacción"
    $this->lockDoctorAgenda($tenantId, $doctorId, $inicio);
}
```

### Problemas concretos

| # | Problema | Consecuencia observable |
|---|---|---|
| P1 | La regla de cruce vive en SQL, dentro de Persistence | No se puede probar sin base de datos; el doble en memoria la reimplementa distinta |
| P2 | Devuelve `bool` | "Fuera de jornada" y "horario ocupado" llegan como el mismo mensaje; el usuario no sabe si cambiar de hora o de médico |
| P3 | Jornada (ASII-04) y ocupación (ASII-05) en el mismo adaptador | Cuando ASII-04 publique su API hay que reescribir también la regla de cruce |
| P4 | Consulta y escritura son dos llamadas del caso de uso | Si nadie abre la transacción, la condición de carrera vuelve |
| P5 | La UI no tiene una fuente de horarios libres | Calcula la grilla por su cuenta y puede ofrecer un horario que el backend rechaza |

## 3. Después

![Después](refactor-despues.png)

```php
// Domain
final class SlotPolicy
{
    public function assertBookable(array $shifts, array $busy, TimeSlot $requested): void
    {
        if (!$this->insideAnyShift($shifts, $requested)) throw new OutsideWorkingHours();
        foreach ($busy as $slot) {
            if ($slot->overlaps($requested)) throw new SlotTaken();
        }
    }
}

// Application
public function execute(RequestAppointmentInput $in): AppointmentOutput
{
    return $this->tx->run(function () use ($in) {
        $this->lock->lockDoctorDay($in->doctorId, $in->date());
        $shifts = $this->schedule->shiftsOf($in->doctorId, $in->date());
        $busy   = $this->agenda->busySlotsOf($in->doctorId, $in->date());
        $this->policy->assertBookable($shifts, $busy, $in->slot());
        $id = $this->appointments->save(Appointment::schedule(...));
        return AppointmentOutput::from($id, ...);
    });
}
```

### Qué se separó y hacia dónde

| Responsabilidad | Antes | Después | Capa |
|---|---|---|---|
| Jornada del médico | `isAvailable()` | `DoctorScheduleProvider` | Puerto en Domain, adaptador en Persistence |
| Citas que ocupan agenda | `isAvailable()` | `AgendaReader::busySlotsOf` | Puerto en Domain, adaptador en Persistence |
| Regla de cruce y de jornada | SQL | `SlotPolicy` + `TimeSlot` | Domain |
| Qué estados ocupan agenda | `status != 'cancelled'` en SQL | `AppointmentStatus::occupiesAgenda()` | Domain |
| Atomicidad y bloqueo | Implícito (`transactionLevel()`) | `TransactionRunner` + `AgendaLock` | Application los invoca, Persistence los implementa |
| Mensaje al usuario | Uno solo | `ErrorMapper` → `DOCTOR_OUTSIDE_WORKING_HOURS` o `APPOINTMENT_SLOT_TAKEN` | Presentation |
| Horarios que ve la UI | Calculados en el cliente | `QueryAvailability` con la misma `SlotPolicy` | Application |

## 4. Justificación

| Problema | Cómo lo resuelve el refactor | Principio |
|---|---|---|
| P1 | La regla se prueba con objetos en memoria, sin base de datos | SRP, dominio independiente |
| P2 | Dos excepciones distintas, dos códigos, dos mensajes accionables | Contrato explícito |
| P3 | Cambiar la fuente de jornada es cambiar un adaptador | DIP, OCP |
| P4 | El caso de uso declara la transacción y el bloqueo; no depende del llamador | Atomicidad explícita |
| P5 | La consulta y la escritura usan la misma política | Una sola fuente de verdad |

## 5. Lo que no cambia

- Estados, transiciones y reglas de negocio del módulo.
- Endpoints y formato de errores del contrato de la semana 5.
- El índice único parcial `uq_appt_doctor_slot_active` como segunda defensa.
- El alcance: no se agregan reagendamiento, lista de espera ni notificaciones.

## 6. Cómo se verificaría

| Verificación | Criterio |
|---|---|
| Prueba unitaria de `SlotPolicy` | Intervalo fuera de jornada lanza `OutsideWorkingHours`; intervalo que cruza lanza `SlotTaken`; intervalo contiguo (10:30 tras 10:00–10:30) se acepta |
| Prueba de `TimeSlot` | `overlaps` es simétrico y no considera cruce a intervalos contiguos |
| Prueba de concurrencia existente (semana 6) | Dos solicitudes simultáneas siguen produciendo una sola cita |
| Prueba de contrato | Fuera de jornada → 422 `DOCTOR_OUTSIDE_WORKING_HOURS`; ocupado → 409 `APPOINTMENT_SLOT_TAKEN` |
| Consistencia UI/backend | Todo horario devuelto por `QueryAvailability` es aceptado por `RequestAppointment` si nadie lo toma antes |
