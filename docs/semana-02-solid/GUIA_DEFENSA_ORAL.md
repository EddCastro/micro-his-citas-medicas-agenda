# Guía de defensa oral - Tarea 2 SOLID

## Datos generales

- **Módulo:** ASII-05 - Citas médicas y agenda
- **Principio asignado:** Dependency Inversion Principle (DIP)
- **Proceso:** solicitud, validación de disponibilidad, confirmación y cancelación de citas

## 1. ¿Qué significa DIP?

DIP significa Dependency Inversion Principle o principio de inversión de dependencias. Indica que la lógica de alto nivel no debe depender directamente de implementaciones concretas. Tanto la lógica principal como los detalles técnicos deben depender de abstracciones.

## 2. ¿Cuál es la lógica de alto nivel en ASII-05?

Los casos de uso RequestAppointment, ConfirmAppointment y CancelAppointment representan la lógica de alto nivel porque coordinan las reglas necesarias para solicitar, confirmar o cancelar una cita médica.

## 3. ¿Cuáles son los detalles de bajo nivel?

Los detalles de bajo nivel son Eloquent, SQL, la base de datos, Laravel Notification y los adaptadores utilizados para consultar pacientes, médicos, disponibilidad e historial.

## 4. ¿Qué problema existía antes de aplicar DIP?

El AppointmentController dependía directamente de modelos y servicios concretos. Esto producía alto acoplamiento, mezcla de responsabilidades y dificultad para realizar pruebas o sustituir tecnologías.

## 5. ¿Cómo se aplica DIP después del rediseño?

El controlador llama a casos de uso. Los casos de uso dependen de contratos como AppointmentRepository, PatientReader, DoctorAvailabilityChecker, AppointmentHistoryWriter y NotificationSender. Las implementaciones concretas cumplen esos contratos mediante adaptadores.

## 6. ¿Qué es una abstracción en este diseño?

Una abstracción es un contrato o interfaz que define lo que necesita la lógica principal sin indicar cómo se realizará técnicamente. Por ejemplo, NotificationSender define el envío de una notificación sin obligar a utilizar correo, SMS o una tecnología específica.

## 7. ¿Qué beneficio aporta AppointmentRepository?

Permite que los casos de uso consulten, guarden y actualicen citas sin depender directamente de Eloquent. En producción puede utilizarse EloquentAppointmentRepository y en pruebas una implementación en memoria.

## 8. ¿Cómo mejora la capacidad de realizar pruebas?

Las interfaces pueden sustituirse por implementaciones simuladas o en memoria. Esto permite probar casos como paciente inexistente, horario ocupado, error de persistencia o fallo de notificación sin utilizar servicios reales.

## 9. ¿Cómo se evita el cruce de horarios?

Debe comprobarse si existe una cita activa cuyo intervalo coincida con el nuevo horario. Los estados pendiente y confirmada bloquean el horario. La validación debe realizarse dentro de una operación controlada para reducir problemas de concurrencia.

## 10. ¿DIP elimina todas las dependencias?

No. DIP reorganiza la dirección de las dependencias. La lógica principal sigue necesitando persistencia, disponibilidad y notificaciones, pero accede a ellas mediante contratos en lugar de depender directamente de clases concretas.

## 11. ¿Qué muestra el diagrama antes de DIP?

Muestra al AppointmentController conectado directamente con Patient, Doctor, Appointment, AppointmentStatusHistory, LaravelNotification y la base de datos.

## 12. ¿Qué muestra el diagrama después de DIP?

Muestra al controlador conectado con los casos de uso. Los casos de uso dependen de contratos del módulo y los adaptadores de infraestructura implementan esos contratos.

## 13. Fuente utilizada

La fuente obligatoria fue el artículo Principios básicos del diseño de software, de Luis Miguel Rodríguez González, publicado en MVP Cluster.

## Resumen para exposición

Antes de aplicar DIP, el controlador de citas dependía directamente de modelos y servicios concretos. Después del rediseño, el controlador delega el proceso a casos de uso y estos dependen de interfaces. Las implementaciones de Laravel y Eloquent quedan como adaptadores reemplazables. Con esto disminuye el acoplamiento y mejora la mantenibilidad y la testabilidad.
