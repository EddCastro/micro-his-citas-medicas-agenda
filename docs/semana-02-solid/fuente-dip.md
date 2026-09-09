# Fuente obligatoria sobre DIP

## Datos de la fuente

- **Título:** Principios básicos del diseño de software
- **Autor:** Luis Miguel Rodríguez González
- **Sitio web:** MVP Cluster
- **Fecha indicada en la página:** 10 de octubre, sin año visible
- **URL:** https://mvpcluster.com/diseno-de-software-2/
- **Fecha de consulta:** 5 de agosto de 2026

## Principio estudiado

**Dependency Inversion Principle (DIP)** o principio de inversión de dependencias.

## Cita textual breve

> "Las clases de alto nivel no tienen que depender de otras de bajo nivel, sino que ambas dependan de abstracciones."

## Interpretación

El principio DIP busca disminuir el acoplamiento entre la lógica principal de una aplicación y sus detalles técnicos. Las reglas de negocio no deben depender directamente de bases de datos, frameworks, modelos concretos o servicios externos. Tanto la lógica de alto nivel como las implementaciones de bajo nivel deben relacionarse mediante abstracciones.

## Aplicación en ASII-05

En el módulo de citas médicas y agenda, los casos de uso RequestAppointment, ConfirmAppointment y CancelAppointment representan la lógica de alto nivel.

Estos casos de uso dependerán de contratos como AppointmentRepository, PatientReader, DoctorAvailabilityChecker, AppointmentHistoryWriter y NotificationSender.

Las implementaciones concretas, como EloquentAppointmentRepository y LaravelNotificationSender, se conectarán mediante inyección de dependencias. De esta forma, la lógica de citas no dependerá directamente de Eloquent, SQL o del mecanismo utilizado para enviar notificaciones.

## Referencia

Rodríguez González, L. M. (s. f.). *Principios básicos del diseño de software*. MVP Cluster. https://mvpcluster.com/diseno-de-software-2/

## Alcance

La fuente se utiliza para fundamentar el principio DIP. El diseño presentado para ASII-05 es una propuesta arquitectónica y no representa todavía una implementación completa en el sistema.
