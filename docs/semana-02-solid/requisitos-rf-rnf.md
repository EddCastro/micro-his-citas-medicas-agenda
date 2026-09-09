# Requisitos funcionales y no funcionales

## Módulo

**ASII-05 — Citas médicas y agenda**

## Proceso analizado

Solicitud, validación de disponibilidad y confirmación o cancelación de una cita médica.

## Estado del documento

Los siguientes requisitos representan el diseño funcional previsto para el módulo. Su inclusión en este documento no implica que ya estén implementados.

---

## 1. Supuestos

- El usuario se encuentra autenticado mediante JWT.
- El hospital activo se identifica mediante `X-Tenant-ID`.
- Los pacientes, médicos y especialidades pertenecen a un tenant.
- La información básica de pacientes y médicos es proporcionada por sus respectivos módulos.
- La duración de la cita se expresa en minutos.
- Los estados principales utilizados en este alcance son:
  - pendiente;
  - confirmada;
  - cancelada.
- Las citas canceladas se conservan para fines de auditoría.
- Los datos utilizados en pruebas y documentación son ficticios.

---

## 2. Requisitos funcionales

| Código | Requisito | Descripción | Prioridad |
|---|---|---|---|
| RF-ASII05-01 | Registrar solicitud de cita | El sistema debe permitir registrar una solicitud indicando paciente, médico, especialidad, fecha, hora, duración y motivo de consulta. | Alta |
| RF-ASII05-02 | Validar autorización | El sistema debe comprobar que el usuario esté autenticado y posea permiso para crear, confirmar o cancelar citas. | Alta |
| RF-ASII05-03 | Validar tenant | El sistema debe comprobar que la operación, el usuario, el paciente, el médico y la cita correspondan al tenant activo. | Alta |
| RF-ASII05-04 | Validar paciente | El sistema debe comprobar que el paciente exista, se encuentre activo y pertenezca al tenant de la solicitud. | Alta |
| RF-ASII05-05 | Validar médico y especialidad | El sistema debe comprobar que el médico exista, esté activo, atienda la especialidad seleccionada y pertenezca al tenant. | Alta |
| RF-ASII05-06 | Consultar disponibilidad | El sistema debe verificar que la fecha y hora solicitadas se encuentren dentro de la disponibilidad configurada para el médico. | Alta |
| RF-ASII05-07 | Considerar excepciones de agenda | El sistema debe considerar bloqueos, ausencias, permisos u otras excepciones que impidan atender en el horario solicitado. | Alta |
| RF-ASII05-08 | Evitar cruces de horario | El sistema debe impedir que un médico tenga dos citas activas cuyos intervalos de tiempo se superpongan. | Alta |
| RF-ASII05-09 | Crear cita pendiente | Cuando todas las validaciones sean satisfactorias, el sistema debe registrar la cita inicialmente con estado `pendiente`. | Alta |
| RF-ASII05-10 | Confirmar cita | El sistema debe permitir confirmar una cita pendiente y cambiar su estado a `confirmada`. | Alta |
| RF-ASII05-11 | Cancelar cita | El sistema debe permitir cancelar una cita pendiente o confirmada, conservando la fecha, el usuario responsable y el motivo de cancelación. | Alta |
| RF-ASII05-12 | Controlar transiciones de estado | El sistema debe rechazar cambios de estado inválidos, por ejemplo confirmar una cita que ya se encuentra cancelada. | Alta |
| RF-ASII05-13 | Registrar historial | El sistema debe conservar un historial por cada cambio de estado, incluyendo estado anterior, estado nuevo, fecha, usuario y motivo cuando corresponda. | Alta |
| RF-ASII05-14 | Notificar resultado | El sistema debe solicitar el envío de una notificación cuando una cita sea registrada, confirmada o cancelada. | Media |
| RF-ASII05-15 | Consultar agenda | El sistema debe permitir consultar citas por fecha, médico, paciente, especialidad y estado, respetando el tenant activo. | Media |
| RF-ASII05-16 | Informar errores | El sistema debe devolver mensajes comprensibles cuando una validación impida registrar o modificar una cita. | Alta |

---

## 3. Regla de cruce de horarios

Una nueva cita presenta cruce cuando su intervalo coincide total o parcialmente con una cita activa del mismo médico.

La comprobación conceptual es:

    inicio_nueva < fin_existente
    y
    fin_nueva > inicio_existente

Para esta validación se consideran activas las citas con estado:

- pendiente;
- confirmada.

Las citas canceladas no bloquean disponibilidad.

---

## 4. Reglas de transición de estado

| Estado actual | Acción | Nuevo estado | Permitido |
|---|---|---|---|
| pendiente | Confirmar | confirmada | Sí |
| pendiente | Cancelar | cancelada | Sí |
| confirmada | Cancelar | cancelada | Sí |
| confirmada | Confirmar nuevamente | confirmada | No |
| cancelada | Confirmar | confirmada | No |
| cancelada | Cancelar nuevamente | cancelada | No |

Las transiciones adicionales que puedan surgir en fases posteriores deberán documentarse antes de implementarse.

---

## 5. Requisitos no funcionales

| Código | Categoría | Requisito verificable | Prioridad |
|---|---|---|---|
| RNF-ASII05-01 | Seguridad | Todas las operaciones protegidas deben requerir JWT válido, permiso correspondiente y `X-Tenant-ID`. | Alta |
| RNF-ASII05-02 | Aislamiento | Ninguna consulta o modificación debe devolver o afectar citas pertenecientes a otro tenant. | Alta |
| RNF-ASII05-03 | Integridad | La creación de la cita y el registro inicial de historial deben ejecutarse de forma atómica. | Alta |
| RNF-ASII05-04 | Concurrencia | Dos solicitudes simultáneas no deben generar citas superpuestas para el mismo médico y horario. | Alta |
| RNF-ASII05-05 | Rendimiento | La consulta de disponibilidad deberá responder en un máximo de dos segundos bajo el entorno de pruebas definido por el equipo. | Media |
| RNF-ASII05-06 | Mantenibilidad | La lógica de aplicación debe depender de interfaces para persistencia, disponibilidad, pacientes, notificaciones y auditoría. | Alta |
| RNF-ASII05-07 | Testabilidad | Los casos de uso deben poder probarse utilizando implementaciones en memoria o dobles de prueba sin requerir una base de datos real. | Alta |
| RNF-ASII05-08 | Fiabilidad | Un fallo en el envío de una notificación no debe provocar la pérdida de una cita registrada correctamente. | Alta |
| RNF-ASII05-09 | Trazabilidad | Cada cambio de estado debe permitir identificar fecha, usuario responsable y motivo cuando corresponda. | Alta |
| RNF-ASII05-10 | Usabilidad | Los errores de validación deben indicar el dato o regla que impidió completar la operación. | Media |
| RNF-ASII05-11 | Privacidad | La documentación, pruebas y demostraciones no deben contener información clínica real ni datos personales identificables. | Alta |
| RNF-ASII05-12 | Compatibilidad | El diseño debe ser compatible con la arquitectura Laravel, Vue y multitenancy utilizada por el proyecto. | Alta |

---

## 6. Aplicación prevista de DIP

La lógica de alto nivel para gestionar citas no debe depender directamente de:

- modelos Eloquent;
- consultas SQL concretas;
- servicios externos de notificación;
- implementaciones específicas de disponibilidad;
- clases concretas de pacientes;
- mecanismos específicos de auditoría.

En su lugar, los casos de uso dependerán de contratos o interfaces como:

- `AppointmentRepository`;
- `PatientReader`;
- `DoctorAvailabilityChecker`;
- `NotificationSender`;
- `AppointmentAuditWriter`.

Las implementaciones concretas se conectarán mediante inyección de dependencias.

---

## 7. Fuera del alcance inmediato

Los siguientes elementos se consideran para fases posteriores y no forman parte obligatoria de este flujo inicial:

- lista de espera;
- ofertas automáticas de espacios;
- recordatorios programados;
- teleconsulta;
- pagos;
- recetas médicas;
- reprogramación automática;
- integración con calendarios externos.

Su incorporación futura deberá respetar los requisitos de tenant, trazabilidad y prevención de cruces definidos en este documento.
