# Guía de defensa oral — Tarea 1 UML

## Datos generales

- Estudiante: Eddy Adolfo Castro Véliz
- Módulo: ASII-05 — Citas médicas y agenda
- Proceso: Solicitud, validación de disponibilidad y confirmación o cancelación de cita

## Resumen del trabajo

Se elaboraron tres diagramas UML sobre el mismo proceso:

1. Casos de uso.
2. Actividad.
3. Secuencia global.

Los diagramas utilizan los mismos actores, validaciones, excepciones y estados.

## Diagrama de casos de uso

Muestra quién participa y qué función realiza.

Actores:

- Paciente.
- Recepcionista.
- Módulo de Médicos y Disponibilidad.
- Sistema de Notificaciones.

Casos de uso principales:

- Solicitar cita.
- Consultar disponibilidad médica.
- Confirmar cita.
- Cancelar cita.
- Validar paciente y datos.
- Registrar cambio de estado.
- Notificar resultado.

La relación include indica que una función necesita ejecutar obligatoriamente otra. Por ejemplo, solicitar una cita incluye validar al paciente y consultar disponibilidad.

## Diagrama de actividad

Representa los pasos, decisiones y resultados del proceso.

Flujo principal:

1. El paciente solicita una cita.
2. Recepción registra los datos.
3. Se valida al paciente.
4. Se valida al médico y la especialidad.
5. Se consulta la disponibilidad.
6. Se registra la cita como pendiente.
7. El paciente confirma, cancela o no responde.

Resultados:

- Si confirma, la cita queda confirmada.
- Si cancela, queda cancelada y se conserva el motivo.
- Si no responde, permanece pendiente.

Excepciones:

- Paciente inexistente o inactivo.
- Médico o especialidad no válidos.
- Horario no disponible.
- Cruce con otra cita activa.

## Diagrama de secuencia global

Muestra los mensajes intercambiados entre:

- Paciente.
- Recepcionista.
- Frontend Vue 3.
- API Laravel.
- Servicio de Pacientes.
- Servicio de Médicos y Disponibilidad.
- Servicio de Citas.
- Base de Datos del Tenant.
- Servicio de Notificaciones.

La API valida JWT, permisos y X-Tenant-ID antes de consultar pacientes, disponibilidad y citas.

## Decisiones importantes

### Estado pendiente

La cita se registra inicialmente como pendiente porque todavía puede requerir confirmación.

### Cancelación

Una cita cancelada no se elimina. Se conserva el motivo y el historial de la operación.

### Historial de estados

Cada cambio debe registrar:

- estado anterior;
- estado nuevo;
- fecha;
- usuario responsable;
- motivo.

### Tenant

X-Tenant-ID identifica el hospital al que pertenece la operación y evita mezclar información entre hospitales.

## Preguntas posibles

### ¿Por qué se usaron tres diagramas?

Porque muestran perspectivas distintas:

- casos de uso: actores y funciones;
- actividad: pasos y decisiones;
- secuencia: mensajes entre componentes.

### ¿Qué ocurre cuando no hay disponibilidad?

La cita no se registra y debe elegirse otro horario.

### ¿Por qué una cita cancelada no se elimina?

Para conservar trazabilidad y evidencia de la operación.

### ¿Cómo se evita un cruce de horario?

Se comparan la fecha de inicio y final de la nueva cita con las citas activas existentes.

### ¿Qué estados se utilizaron?

- pendiente;
- confirmada;
- cancelada.

### ¿Qué ocurre si el paciente no responde?

La cita permanece en estado pendiente.

### ¿Para qué sirve appointment_status_history?

Permite reconstruir todos los cambios realizados sobre una cita.

## Modificación práctica

Durante la defensa podrían solicitar agregar una excepción de autenticación al diagrama de secuencia.

El bloque PlantUML sería:

    alt Usuario no autenticado o sin permiso
        API --> Frontend: Error de autenticación o autorización
        Frontend --> Recepcionista: Mostrar acceso denegado
    else Usuario autorizado
        API -> Pacientes: Validar paciente
    end

Después de modificar un diagrama también debe revisarse la matriz de trazabilidad.

## Comandos utilizados

Validación:

    java -jar "$HOME\Tools\PlantUML\plantuml.jar" -checkonly ".\docs\module-05\tarea-01-uml\*.puml"

Generación de PNG:

    java -jar "$HOME\Tools\PlantUML\plantuml.jar" -tpng ".\docs\module-05\tarea-01-uml\*.puml"

## Conclusión para la defensa

Los tres diagramas representan el mismo proceso desde las perspectivas funcional, de flujo y técnica. La decisión principal fue conservar la trazabilidad mediante estados e historial. La implementación del módulo aún está pendiente, pero las fuentes PlantUML, imágenes y matriz de trazabilidad permiten verificar el diseño.
