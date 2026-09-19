# Guía de defensa oral — Semana 8, Diseño de experiencia de usuario

## Datos generales

- **Módulo:** ASII-05 — Citas médicas y agenda
- **Estudiante:** Eddy Adolfo Castro Véliz
- **Proceso:** Solicitud, validación de disponibilidad y confirmación o cancelación de cita

## 1. ¿Qué se entregó?

Tres user flows (Recepcionista, Enfermera, Cancelación y Médico), seis
wireframes anotados (W1–W6) y un documento de reglas con estados, mensajes,
validaciones, ayuda contextual y protección de datos.

## 2. ¿Por qué el flujo por rol y no uno solo?

Porque cada rol tiene permisos distintos según la matriz de la semana 5. La
Recepción agenda y cancela, la Enfermera confirma y el Médico solo consulta.
Si un rol viera acciones que no puede ejecutar, el backend las rechazaría con
403 y el usuario quedaría confundido.

## 3. ¿Por qué cuatro pasos para agendar?

Cada paso corresponde a una validación del backend: paciente (ASII-03),
médico y especialidad (`DOCTOR_SPECIALTY_MISMATCH`), horario
(`DOCTOR_OUTSIDE_WORKING_HOURS`, `APPOINTMENT_SLOT_TAKEN`) y revisión final.
El motivo de la consulta es opcional porque así lo define
`StoreAppointmentRequest`; la interfaz no exige más que el servidor. Separarlos
permite prevenir el error en el paso donde ocurre en lugar de mostrarlo todo al
final.

## 4. ¿Qué estados de pantalla se diseñaron?

Carga (esqueleto), vacío (con una acción para salir de él), enviando (botón
deshabilitado), éxito (código de la cita) y error recuperable (con los datos
conservados).

## 5. ¿Cuál es el error más importante del flujo?

El 409 `APPOINTMENT_SLOT_TAKEN`: otro usuario reservó el horario entre la
consulta y el envío. Es la consecuencia visible del bloqueo de la semana 6.
La interfaz regresa a la grilla recargada y conserva paciente, médico y motivo.

## 6. ¿La grilla de horarios reserva el horario?

No. Consultar no reserva. La validación definitiva ocurre al agendar, dentro de
la transacción con bloqueo del médico y el día. Reservar al seleccionar
agregaría un estado nuevo al módulo, fuera del alcance.

## 7. ¿Cómo se evita una cita duplicada por doble clic?

El botón se deshabilita al enviar y el reintento usa la misma
`Idempotency-Key` definida en el contrato de la semana 5.

## 8. ¿Qué pasa si el paciente no contesta?

La cita permanece pendiente, igual que en la excepción EX-05 de la semana 1.

## 9. ¿Cómo se protegen los datos del paciente?

La agenda muestra nombre e iniciales de apellidos, sin DPI, teléfono ni motivo.
El DPI se enmascara salvo los 4 últimos dígitos. El motivo solo se ve en el
detalle. Una cita de otro hospital responde 404, igual que una inexistente.

## 10. ¿Por qué no se muestra un mensaje distinto para "no tiene permiso" y "no existe"?

Porque distinguirlos revelaría que la cita existe en otro hospital. Es la
misma decisión D-20 de la semana 6.

## 11. ¿Estos wireframes ya están implementados?

No. La implementación Laravel se entrega como API sin interfaz. Los wireframes
describen la interfaz que consumiría esos endpoints.

## Modificación práctica

Podrían pedir agregar al flujo de la Enfermera el caso "la cita ya fue
cancelada por Recepción mientras la llamaba". El bloque PlantUML sería:

    case (422 TRANSICION INVALIDA)
      :"Esta cita ya fue cancelada o confirmada por otra persona";
      :Se recarga el detalle con el estado actual;

Ya está incluido en `user-flow-enfermera.puml`; la modificación consistiría en
agregar un mensaje equivalente en el wireframe W6 y en el catálogo de
`reglas-interaccion.md`.

## Resumen para exposición

El flujo se diseñó por rol a partir de la matriz de permisos. Cada paso
previene un error concreto del contrato de API, y el error de concurrencia se
trata como recuperable: se informa qué horario se perdió y no se pierde lo
capturado. Los wireframes son la primera versión y se evalúan en la semana 9.
