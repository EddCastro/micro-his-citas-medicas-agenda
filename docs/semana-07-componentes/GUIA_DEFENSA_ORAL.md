# Guía de defensa oral — Semana 7, Componentes y refactorización

## Datos generales

- **Módulo:** ASII-05 — Citas médicas y agenda
- **Estudiante:** Eddy Adolfo Castro Véliz
- **Código analizado:** rama `feature/asii-05-semana-06-parcial-eddcastro` del repositorio grupal

## 1. ¿Qué se entregó?

Un diagrama de componentes backend y frontend, los contratos de entrada,
salida y error de cada componente, y un refactor conceptual con el código
antes y después.

## 2. ¿Qué componentes existen y cuáles son propuestos?

Existen los del backend Laravel: `AppointmentController`, los `FormRequest`,
los casos de uso, la entidad `Appointment`, `AppointmentStatus`, los tres
puertos y sus adaptadores Eloquent. Son propuestos `AgendaLock`, `TimeSlot`,
`ErrorMapper` y todo el frontend, porque el módulo se entregó como API. En el
diagrama los propuestos tienen borde punteado.

## 3. ¿Cuál es el punto de mayor acoplamiento y por qué?

`EloquentAppointmentRepository::hasOverlap()`. Es el único componente que toca
los seis conceptos de la consigna: qué estados ocupan la agenda, cruce de
intervalos (disponibilidad) y, desde la semana 6, el bloqueo de concurrencia.

## 4. ¿Qué tiene de malo que `hasOverlap()` bloquee?

Que es una consulta con un efecto oculto, y que ese efecto depende de
`DB::transactionLevel() > 0`. Si alguien llama a `hasOverlap()` fuera de
`transaction()`, el bloqueo no ocurre y ninguna prueba falla. La protección de
la semana 6 depende de que todos recuerden una regla que no está escrita en el
caso de uso.

## 5. ¿Qué otro problema apareció al revisar el código?

Confirmar y cancelar hacen `findById → cambio de estado → update` sin
transacción. Si Enfermería confirma mientras Recepción cancela, ambas leen
`pendiente` y gana la última escritura: una de las dos cree que su acción quedó
registrada y no es así.

## 6. ¿Qué cambia con el refactor?

- El bloqueo pasa a un puerto propio, `AgendaLock`, que el caso de uso llama
  de forma explícita.
- `hasOverlap()` queda como consulta pura, conservando su SQL indexado.
- La regla de cruce se define una vez en `TimeSlot::overlaps()` y una prueba
  de contrato obliga al SQL y al doble de prueba a coincidir con ella.
- Confirmar y cancelar leen la cita con `findByIdForUpdate` dentro de una
  transacción.
- Cada regla incumplida tiene un código, y `ErrorMapper` responde 409 cuando
  el horario está ocupado.

## 7. ¿Eso no contradice la decisión D-14 de detectar cruces en la base?

No. El cruce se sigue calculando en SQL, con el índice. `TimeSlot` es la
definición de referencia que usan las pruebas; no reemplaza la consulta.

## 8. ¿Por qué no un bloqueo optimista con número de versión?

Para la cita nueva se descartó en la semana 6, porque no tiene versión previa.
Para confirmar y cancelar sería posible, pero obligaría a agregar una columna a
`appointments`, una tabla del andamiaje común que el módulo decidió no
modificar (D-13). `SELECT ... FOR UPDATE` no requiere cambios de esquema.

## 9. ¿Se amplió el módulo?

No. No hay endpoints, estados ni reglas nuevas. Los códigos de error ya
estaban en el contrato de la semana 5; el refactor solo hace que se emitan.

## 10. ¿Cómo se comprobaría que el refactor no rompe nada?

Las seis pruebas de concurrencia de la semana 6 deben seguir aprobando sin
cambiar sus aserciones, y se agregan cuatro: `hasOverlap()` sin `FOR UPDATE`,
la prueba de contrato del cruce, confirmar y cancelar en paralelo, y el código
HTTP de cada error.

## Modificación práctica

Podrían pedir aplicar el mismo patrón a `RescheduleAppointment`, que también
llama a `hasOverlap()`. El cambio en el caso de uso sería:

    return $this->appointments->transaction(function () use (...) {
        $this->lock->lockDoctorDay($tenantId, $doctorId, $fecha);
        if ($this->appointments->hasOverlap($tenantId, $doctorId, $fecha, $duracion, $appointmentId)) {
            throw AppointmentRuleViolation::horarioOcupado();
        }
        ...
    });

Luego se agrega `RescheduleAppointment ..> AgendaLock` en
`refactor-despues.puml`.

## Resumen para exposición

El acoplamiento más fuerte estaba en `hasOverlap()`: una consulta que también
bloqueaba, y solo si había una transacción abierta. El refactor hace explícito
el bloqueo, deja la consulta sin efectos, define el cruce una sola vez, protege
confirmar y cancelar ante concurrencia y tipa los errores, sin agregar
funciones al módulo.
