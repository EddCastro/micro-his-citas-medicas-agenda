# Semana 3 - Vista arquitectónica del módulo ASII-05

## Datos del módulo

- **Módulo:** ASII-05 - Citas médicas y agenda
- **Estudiante:** Eddy Adolfo Castro Véliz
- **GitHub:** EddCastro
- **Issue:** #5
- **Rama:** `feature/asii-05-citas-medicas-y-agenda-eddcastro`

## Objetivo de la semana

Diseñar una vista arquitectónica de alto nivel del módulo Citas médicas y agenda, identificando sus principales componentes, límites y dependencias con otros módulos y servicios del Sistema Hospitalario Integrado (HIS).

## Alcance de la vista

La vista arquitectónica representa el módulo ASII-05 como parte del HIS y muestra cómo interactúa con la interfaz compartida, los servicios del backend y los módulos externos necesarios para ejecutar el flujo de citas.

En esta semana no se define todavía el diseño interno por capas ni el contrato detallado de la API, ya que esos elementos corresponden a semanas posteriores del plan del proyecto.

## Flujo arquitectónico principal

1. Un usuario autorizado utiliza la interfaz web del HIS.
2. La interfaz envía solicitudes al API del sistema.
3. El módulo ASII-05 procesa las operaciones relacionadas con citas y agenda.
4. ASII-05 consulta los módulos responsables de pacientes, médicos, especialidades y disponibilidad.
5. Las acciones son controladas mediante roles, permisos y tenant.
6. Los cambios relevantes generan trazabilidad mediante el módulo de auditoría.
7. Cuando corresponde, ASII-05 solicita el envío de avisos o recordatorios al módulo de alertas y notificaciones.

## Dependencias arquitectónicas

| Dependencia | Responsabilidad respecto a ASII-05 |
|---|---|
| **ASII-01 - Usuarios y tenants** | Proporciona el contexto del usuario autenticado y el tenant al que pertenece la operación. |
| **ASII-02 - RBAC** | Proporciona autorización mediante roles y permisos. |
| **ASII-03 - Pacientes** | Proporciona la referencia e información básica del paciente asociado a una cita. |
| **ASII-04 - Médicos, especialidades y disponibilidad** | Proporciona médicos, especialidades, horarios y validación de disponibilidad. |
| **ASII-21 - Alertas y notificaciones** | Gestiona recordatorios, confirmaciones y avisos relacionados con citas. |
| **ASII-22 - Gobernanza y auditoría** | Registra eventos y acciones relevantes para mantener trazabilidad. |
| **Frontend Vue compartido** | Presenta al usuario las funcionalidades de citas dentro de la interfaz general del HIS. |

## Dependencias transversales

- **Tenant:** toda operación debe mantenerse dentro del hospital correspondiente.
- **Autenticación y autorización:** el acceso depende de la identidad, rol y permisos del usuario.
- **Persistencia:** la estructura definitiva de base de datos será utilizada cuando sea confirmada para el proyecto; esta vista no define tablas ni migraciones.
- **ASII-25 - QA, pruebas E2E y CI:** participa posteriormente en la validación e integración del módulo, pero no forma parte del flujo operativo principal.

## Límites arquitectónicos

- ASII-05 no administra el registro maestro de pacientes.
- ASII-05 no administra el catálogo completo de médicos o especialidades.
- ASII-05 no define los horarios laborales, vacaciones o ausencias médicas.
- ASII-05 no implementa el sistema general de roles y permisos.
- ASII-05 no implementa el servicio general de notificaciones.
- ASII-05 consume las capacidades de esos módulos mediante sus integraciones dentro del HIS.

## Entregable principal

El entregable técnico de la Semana 3 será una vista arquitectónica de alto nivel documentada mediante PlantUML, acompañada de su versión exportada para revisión visual.
