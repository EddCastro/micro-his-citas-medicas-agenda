# Diseño antes y después de aplicar DIP

## Módulo

**ASII-05 — Citas médicas y agenda**

## Proceso analizado

Solicitud, validación de disponibilidad y confirmación o cancelación de una cita médica.

## Estado del diseño

Este documento representa una propuesta arquitectónica. Las clases e interfaces mencionadas todavía no están implementadas.

---

## 1. Principio aplicado

DIP significa **Dependency Inversion Principle** o principio de inversión de dependencias.

Este principio indica que:

- la lógica de alto nivel no debe depender directamente de detalles de infraestructura;
- tanto la lógica principal como la infraestructura deben depender de abstracciones;
- las implementaciones concretas deben poder sustituirse sin modificar los casos de uso.

En ASII-05, la creación, confirmación y cancelación de citas representan la lógica de alto nivel. Eloquent, SQL, notificaciones y otros servicios son detalles de infraestructura.

## 2. Diseño antes de aplicar DIP

En un diseño fuertemente acoplado, el controlador de citas podría encargarse directamente de:

- consultar pacientes con Eloquent;
- consultar médicos y especialidades;
- revisar la disponibilidad;
- buscar cruces de horario;
- crear la cita;
- registrar el historial;
- enviar la notificación;
- manejar la respuesta HTTP.

En este diseño, el controlador depende directamente de clases concretas como:

- `Patient`;
- `Doctor`;
- `Appointment`;
- `AppointmentStatusHistory`;
- `Notification`.

Esto provoca un alto acoplamiento entre la lógica del módulo y la infraestructura.

## 3. Problemas del diseño antes de DIP

### 3.1. Alto acoplamiento

El controlador depende directamente de modelos, consultas y servicios concretos.

### 3.2. Baja testabilidad

Para probar el proceso sería necesario utilizar Laravel, una base de datos y servicios reales o configurados.

### 3.3. Mezcla de responsabilidades

El controlador estaría realizando al mismo tiempo:

- validaciones;
- reglas de negocio;
- consultas;
- persistencia;
- historial;
- notificaciones;
- respuestas HTTP.

### 3.4. Dificultad para sustituir implementaciones

Cambiar Eloquent por PDO, correo por SMS o disponibilidad local por una API requeriría modificar la lógica principal.

### 3.5. Mayor riesgo de errores

Un cambio en persistencia, notificaciones o disponibilidad podría afectar directamente la creación, confirmación o cancelación de citas.

### 3.6. Dificultad para simular fallos

Sería más difícil probar de forma controlada:

- paciente inexistente;
- médico no válido;
- horario ocupado;
- error de persistencia;
- fallo de notificación;
- acceso entre tenants.

## 4. Diseño después de aplicar DIP

El diseño mejorado separa la lógica principal de los detalles técnicos.

Los casos de uso de citas dependerán de interfaces y no directamente de Eloquent, SQL o servicios concretos.

### Casos de uso principales

- `RequestAppointment`
- `ConfirmAppointment`
- `CancelAppointment`

### Interfaces propuestas

- `AppointmentRepository`
- `PatientReader`
- `DoctorEligibilityChecker`
- `DoctorAvailabilityChecker`
- `AppointmentHistoryWriter`
- `NotificationSender`
- `TransactionManager`
- `Clock`
- `TenantContext`

Las implementaciones concretas se conectarán mediante inyección de dependencias.

Por ejemplo:

- `AppointmentRepository` podrá ser implementado por `EloquentAppointmentRepository`;
- `NotificationSender` podrá ser implementado por `LaravelNotificationSender`;
- `Clock` podrá ser implementado por `SystemClock`;
- en pruebas podrán utilizarse implementaciones en memoria o simuladas.

## 5. Responsabilidades y dependencias

| Elemento | Responsabilidad | Dependencia |
|---|---|---|
| `RequestAppointment` | Coordinar la solicitud y creación de una cita pendiente. | Interfaces del módulo. |
| `ConfirmAppointment` | Validar y confirmar una cita pendiente. | Repositorio, historial y notificaciones. |
| `CancelAppointment` | Cancelar una cita válida y conservar el motivo. | Repositorio, historial y notificaciones. |
| `AppointmentRepository` | Guardar, consultar y actualizar citas. | No depende de Eloquent en su contrato. |
| `PatientReader` | Validar existencia, estado y tenant del paciente. | Implementación del módulo de pacientes. |
| `DoctorEligibilityChecker` | Validar médico, especialidad y tenant. | Implementación del módulo de médicos. |
| `DoctorAvailabilityChecker` | Comprobar jornada, excepciones y cruces. | Adaptador de disponibilidad. |
| `AppointmentHistoryWriter` | Registrar cambios de estado y responsables. | Implementación de persistencia. |
| `NotificationSender` | Solicitar notificaciones sin definir el canal. | Correo, SMS, cola u otro adaptador. |
| `TransactionManager` | Ejecutar operaciones de forma atómica. | Transacciones de Laravel o PDO. |
| `Clock` | Proporcionar fecha y hora controlables. | Reloj real o fijo para pruebas. |
| `TenantContext` | Proporcionar el tenant activo validado. | Middleware e infraestructura HTTP. |

La lógica de alto nivel dependerá únicamente de contratos. Las implementaciones concretas dependerán de esos contratos y se conectarán mediante inyección de dependencias.
