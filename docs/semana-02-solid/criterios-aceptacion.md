# Criterios de aceptación

## Módulo

**ASII-05 — Citas médicas y agenda**

## Proceso

Solicitud, validación de disponibilidad y confirmación o cancelación de una cita médica.

## Convenciones

Los escenarios se expresan con la estructura:

- **Dado:** condición inicial.
- **Cuando:** acción realizada.
- **Entonces:** resultado verificable.

Los datos utilizados son ficticios.

---

## CA-ASII05-01 — Registrar una cita válida

**Requisitos relacionados:** RF-ASII05-01, RF-ASII05-03, RF-ASII05-04, RF-ASII05-05, RF-ASII05-06, RF-ASII05-08 y RF-ASII05-09.

**Dado** que:

- el usuario posee un JWT válido;
- el usuario tiene permiso para crear citas;
- el tenant activo es válido;
- el paciente existe, está activo y pertenece al tenant;
- el médico existe, está activo y atiende la especialidad seleccionada;
- el horario se encuentra dentro de la disponibilidad del médico;
- no existen bloqueos ni cruces con citas activas;

**Cuando** el usuario registra la solicitud con paciente, médico, especialidad, fecha, hora, duración y motivo;

**Entonces**:

- se crea una sola cita;
- la cita pertenece al tenant activo;
- el estado inicial es `pendiente`;
- se devuelve un identificador de cita;
- se registra el cambio inicial de estado;
- se solicita el envío de una notificación;
- la respuesta indica que la operación fue exitosa.

---

## CA-ASII05-02 — Rechazar usuario no autenticado

**Requisitos relacionados:** RF-ASII05-02 y RNF-ASII05-01.

**Dado** que la solicitud no contiene un JWT válido;

**Cuando** se intenta crear, confirmar o cancelar una cita;

**Entonces**:

- la operación es rechazada;
- no se crea ni modifica ninguna cita;
- no se registra historial;
- la respuesta informa que el usuario no está autenticado.

---

## CA-ASII05-03 — Rechazar usuario sin permiso

**Requisitos relacionados:** RF-ASII05-02 y RNF-ASII05-01.

**Dado** que el usuario está autenticado, pero no posee el permiso requerido;

**Cuando** intenta crear, confirmar o cancelar una cita;

**Entonces**:

- la operación es rechazada;
- no se modifica información;
- la respuesta informa que el usuario no está autorizado.

---

## CA-ASII05-04 — Impedir acceso entre tenants

**Requisitos relacionados:** RF-ASII05-03, RNF-ASII05-01 y RNF-ASII05-02.

**Dado** que:

- el usuario pertenece al tenant A;
- el encabezado o recurso solicitado pertenece al tenant B;

**Cuando** el usuario intenta consultar o modificar una cita;

**Entonces**:

- la operación es rechazada;
- no se devuelve información de la cita del tenant B;
- no se modifica ningún registro;
- el intento puede registrarse para fines de auditoría.

---

## CA-ASII05-05 — Rechazar paciente inexistente o inactivo

**Requisitos relacionados:** RF-ASII05-04 y RF-ASII05-16.

**Dado** que el paciente no existe, está inactivo o pertenece a otro tenant;

**Cuando** se intenta registrar una cita;

**Entonces**:

- la cita no se crea;
- no se registra historial de cita;
- la respuesta identifica el problema relacionado con el paciente.

---

## CA-ASII05-06 — Rechazar médico o especialidad no válidos

**Requisitos relacionados:** RF-ASII05-05 y RF-ASII05-16.

**Dado** que:

- el médico no existe;
- el médico está inactivo;
- el médico pertenece a otro tenant;
- o el médico no atiende la especialidad seleccionada;

**Cuando** se intenta registrar una cita;

**Entonces**:

- la cita no se crea;
- no se reserva ningún horario;
- la respuesta identifica el dato inválido.

---

## CA-ASII05-07 — Rechazar horario fuera de disponibilidad

**Requisitos relacionados:** RF-ASII05-06 y RF-ASII05-16.

**Dado** que el horario solicitado se encuentra fuera de la jornada configurada para el médico;

**Cuando** se intenta registrar una cita;

**Entonces**:

- la cita no se crea;
- la respuesta informa que el médico no se encuentra disponible;
- se permite seleccionar otra fecha u hora.

---

## CA-ASII05-08 — Considerar una excepción de agenda

**Requisitos relacionados:** RF-ASII05-07 y RF-ASII05-16.

**Dado** que el médico tiene una ausencia, bloqueo, permiso o excepción registrada para el horario solicitado;

**Cuando** se intenta crear una cita dentro de ese intervalo;

**Entonces**:

- la cita no se crea;
- el intervalo se considera no disponible;
- la respuesta informa que existe una excepción de agenda.

---

## CA-ASII05-09 — Impedir cruce con otra cita

**Requisitos relacionados:** RF-ASII05-08 y RNF-ASII05-03.

**Dado** que el médico ya posee una cita pendiente o confirmada entre las 10:00 y las 10:30;

**Cuando** se solicita otra cita cuyo intervalo coincide total o parcialmente con ese horario;

**Entonces**:

- la nueva cita no se crea;
- la cita existente no se modifica;
- la respuesta informa que existe un cruce de horario.

---

## CA-ASII05-10 — Permitir horario ocupado únicamente por una cita cancelada

**Requisitos relacionados:** RF-ASII05-08.

**Dado** que el médico posee una cita cancelada en el horario solicitado y no existe otra cita activa;

**Cuando** se registra una nueva solicitud válida;

**Entonces**:

- el horario se considera disponible;
- la nueva cita se crea con estado `pendiente`;
- la cita cancelada permanece almacenada para trazabilidad.

---

## CA-ASII05-11 — Confirmar una cita pendiente

**Requisitos relacionados:** RF-ASII05-10, RF-ASII05-12, RF-ASII05-13 y RF-ASII05-14.

**Dado** que la cita pertenece al tenant activo y se encuentra en estado `pendiente`;

**Cuando** un usuario autorizado confirma la cita;

**Entonces**:

- el estado cambia a `confirmada`;
- se registra el estado anterior y el nuevo estado;
- se registra la fecha y el usuario responsable;
- se solicita el envío de una notificación de confirmación;
- la respuesta informa que la cita fue confirmada.

---

## CA-ASII05-12 — Cancelar una cita pendiente

**Requisitos relacionados:** RF-ASII05-11, RF-ASII05-12, RF-ASII05-13 y RF-ASII05-14.

**Dado** que la cita pertenece al tenant activo y se encuentra en estado `pendiente`;

**Cuando** un usuario autorizado la cancela indicando un motivo;

**Entonces**:

- el estado cambia a `cancelada`;
- se conserva el motivo;
- se registra la fecha y el usuario responsable;
- se registra el cambio en el historial;
- se solicita una notificación de cancelación;
- la cita no se elimina.

---

## CA-ASII05-13 — Cancelar una cita confirmada

**Requisitos relacionados:** RF-ASII05-11, RF-ASII05-12 y RF-ASII05-13.

**Dado** que una cita se encuentra en estado `confirmada`;

**Cuando** un usuario autorizado la cancela con un motivo válido;

**Entonces**:

- el estado cambia a `cancelada`;
- el historial conserva la transición de confirmada a cancelada;
- el motivo y el responsable quedan registrados;
- la cita continúa almacenada.

---

## CA-ASII05-14 — Exigir motivo de cancelación

**Requisitos relacionados:** RF-ASII05-11 y RNF-ASII05-09.

**Dado** que una cita pendiente o confirmada puede cancelarse;

**Cuando** el usuario intenta cancelarla sin proporcionar un motivo;

**Entonces**:

- la operación es rechazada;
- el estado de la cita no cambia;
- no se registra una transición de estado;
- la respuesta indica que el motivo es obligatorio.

---

## CA-ASII05-15 — Rechazar confirmación de cita cancelada

**Requisitos relacionados:** RF-ASII05-12 y RF-ASII05-16.

**Dado** que una cita se encuentra en estado `cancelada`;

**Cuando** se intenta confirmarla;

**Entonces**:

- la operación es rechazada;
- la cita permanece cancelada;
- no se agrega una transición inválida al historial;
- la respuesta explica que el estado actual no permite confirmar.

---

## CA-ASII05-16 — Evitar confirmación duplicada

**Requisitos relacionados:** RF-ASII05-12.

**Dado** que una cita ya se encuentra en estado `confirmada`;

**Cuando** se intenta confirmar nuevamente;

**Entonces**:

- no se crea una transición adicional;
- el estado permanece confirmado;
- la respuesta informa que la cita ya está confirmada.

---

## CA-ASII05-17 — Registrar historial de estados

**Requisitos relacionados:** RF-ASII05-13 y RNF-ASII05-09.

**Dado** que una cita cambia de estado;

**Cuando** la operación finaliza correctamente;

**Entonces** el historial registra:

- identificador de la cita;
- tenant;
- estado anterior;
- estado nuevo;
- fecha y hora;
- usuario responsable;
- motivo cuando corresponda.

---

## CA-ASII05-18 — Mantener integridad transaccional

**Requisitos relacionados:** RNF-ASII05-03.

**Dado** que la creación de la cita requiere guardar la cita y su historial inicial;

**Cuando** ocurre un error antes de completar ambas operaciones;

**Entonces**:

- la transacción se revierte;
- no queda una cita sin historial inicial;
- no queda un historial sin cita asociada;
- se devuelve un error controlado.

---

## CA-ASII05-19 — Controlar solicitudes simultáneas

**Requisitos relacionados:** RF-ASII05-08 y RNF-ASII05-04.

**Dado** que dos usuarios solicitan simultáneamente el mismo horario para el mismo médico;

**Cuando** ambas operaciones se procesan;

**Entonces**:

- solo una cita puede quedar registrada;
- la segunda operación debe detectar que el horario ya no está disponible;
- no deben existir citas activas superpuestas.

---

## CA-ASII05-20 — Conservar la cita ante fallo de notificación

**Requisitos relacionados:** RF-ASII05-14 y RNF-ASII05-08.

**Dado** que una cita fue registrada, confirmada o cancelada correctamente;

**Cuando** el servicio de notificaciones presenta un error;

**Entonces**:

- la operación principal conserva su resultado;
- la cita no se elimina ni revierte únicamente por el fallo de notificación;
- el fallo queda registrado;
- la notificación puede reintentarse posteriormente.

---

## CA-ASII05-21 — Consultar agenda con filtros

**Requisitos relacionados:** RF-ASII05-15 y RNF-ASII05-02.

**Dado** que existen citas de diferentes fechas, médicos, pacientes, especialidades y estados;

**Cuando** un usuario autorizado consulta la agenda utilizando uno o varios filtros;

**Entonces**:

- solo se devuelven citas del tenant activo;
- los resultados cumplen los filtros aplicados;
- no se muestran citas pertenecientes a otros tenants.

---

## CA-ASII05-22 — Mostrar errores comprensibles

**Requisitos relacionados:** RF-ASII05-16 y RNF-ASII05-10.

**Dado** que una validación impide completar la operación;

**Cuando** el sistema devuelve la respuesta;

**Entonces**:

- se identifica el campo o regla que falló;
- no se muestran detalles internos, consultas SQL ni rastros técnicos sensibles;
- el mensaje permite al usuario corregir la solicitud.

---

## CA-ASII05-23 — Probar los casos de uso sin base de datos real

**Requisitos relacionados:** RNF-ASII05-06 y RNF-ASII05-07.

**Dado** que los casos de uso dependen de interfaces;

**Cuando** se ejecutan pruebas con repositorios y servicios en memoria;

**Entonces**:

- las reglas de creación, confirmación y cancelación pueden probarse sin Eloquent ni PDO;
- los resultados son deterministas;
- pueden simularse disponibilidad, errores de persistencia y fallos de notificación.

---

## CA-ASII05-24 — Proteger datos ficticios y privacidad

**Requisitos relacionados:** RNF-ASII05-11.

**Dado** que se preparan pruebas, documentación o demostraciones;

**Cuando** se registran pacientes, médicos o citas de ejemplo;

**Entonces**:

- los datos utilizados son ficticios;
- no se incluye información clínica identificable;
- no se publican credenciales ni secretos del sistema.

---

## CA-ASII05-25 — Cumplir el tiempo de respuesta de disponibilidad

**Requisitos relacionados:** RNF-ASII05-05.

**Dado** que:

- el entorno de pruebas se encuentra disponible;
- existen datos ficticios representativos de médicos, horarios, excepciones y citas;
- el usuario está autenticado y autorizado;

**Cuando** se ejecutan veinte consultas consecutivas de disponibilidad;

**Entonces**:

- cada consulta responde en un máximo de dos segundos;
- ninguna consulta devuelve datos de otro tenant;
- no se producen errores inesperados;
- el tiempo obtenido queda registrado como evidencia de prueba.

---

## CA-ASII05-26 — Mantener compatibilidad con la arquitectura del proyecto

**Requisitos relacionados:** RNF-ASII05-12.

**Dado** que el proyecto utiliza Laravel, Vue y una arquitectura multitenant;

**Cuando** el diseño del módulo se integra con la aplicación;

**Entonces**:

- los casos de uso pueden registrarse mediante el contenedor de dependencias de Laravel;
- las implementaciones concretas pueden sustituirse sin modificar la lógica de alto nivel;
- las operaciones mantienen la validación de `X-Tenant-ID`;
- el Frontend consume el contrato de la API sin depender de clases internas del backend;
- el diseño no requiere modificar módulos ajenos sin coordinación.

---
## Matriz resumida de cobertura

| Grupo | Criterios |
|---|---|
| Seguridad y tenant | CA-ASII05-02 al CA-ASII05-04 |
| Paciente, médico y especialidad | CA-ASII05-05 y CA-ASII05-06 |
| Disponibilidad y cruces | CA-ASII05-07 al CA-ASII05-10 y CA-ASII05-19 |
| Creación de cita | CA-ASII05-01 y CA-ASII05-18 |
| Confirmación y cancelación | CA-ASII05-11 al CA-ASII05-16 |
| Historial y notificaciones | CA-ASII05-17 y CA-ASII05-20 |
| Consulta y errores | CA-ASII05-21 y CA-ASII05-22 |
| DIP y testabilidad | CA-ASII05-23 |
| Privacidad | CA-ASII05-24 |
| Rendimiento | CA-ASII05-25 |
| Compatibilidad arquitectónica | CA-ASII05-26 |

## Uso posterior

Estos criterios servirán como base para:

- pruebas unitarias de dominio y aplicación;
- pruebas de integración con persistencia;
- pruebas de API;
- pruebas de aislamiento por tenant;
- validación del diseño antes y después de aplicar DIP.
