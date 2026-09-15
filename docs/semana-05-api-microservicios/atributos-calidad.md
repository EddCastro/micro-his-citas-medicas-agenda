# Atributos de calidad del diseño cliente-servidor

Definición de propiedad de datos, comunicación, seguridad, resiliencia,
observabilidad y consistencia para el módulo ASII-05.

## Propiedad de datos

Cada dato tiene un único módulo propietario, que es el que puede escribirlo.
Los demás lo consultan a través de su interfaz.

| Dato | Propietario | ASII-05 |
|---|---|---|
| Citas médicas | ASII-05 | Escribe y lee |
| Disponibilidad médica | ASII-04 | Lee; hoy replicada localmente |
| Pacientes | ASII-03 | Solo lee la referencia |
| Médicos y especialidades | ASII-04 | Solo lee la referencia |
| Usuarios y hospital | ASII-01 | Recibe el contexto |
| Permisos | ASII-02 | Consulta autorización |

### Situación de la disponibilidad

El módulo ASII-04 desarrolló su disponibilidad en un proyecto independiente,
fuera del backend. Mientras no la publique, ASII-05 mantiene la tabla
`doctor_availabilities` aislada tras su propio contrato.

Es una excepción declarada, no una apropiación: el contrato permite sustituir
la fuente sin modificar los casos de uso, y la reconciliación está planteada
como punto de coordinación en el pull request del módulo.

## Comunicación

### Cliente y servidor

Síncrona sobre HTTP con JSON. El cliente es la interfaz web del sistema; el
servidor expone el contrato documentado.

Se elige síncrona porque el usuario necesita saber de inmediato si su cita
quedó registrada. Una respuesta diferida obligaría al personal administrativo
a consultar después si el horario se reservó, lo que empeora el flujo de
recepción.

### Entre módulos

Hoy la comunicación es una llamada de método dentro del mismo proceso, a través
de los contratos del dominio. Si se ejecutara la etapa 2 de la migración,
pasaría a HTTP síncrono con tiempo de espera y reintento.

### Notificaciones

El aviso al paciente es la única operación que conviene tratar de forma
asíncrona: no debe bloquear el registro de la cita ni revertirlo si falla. Se
modela como consecuencia posterior a la operación principal, con reintento
independiente.

## Seguridad

| Control | Mecanismo | Dónde se aplica |
|---|---|---|
| Autenticación | Token JWT firmado | Middleware `jwt.auth` |
| Aislamiento por hospital | Cabecera validada contra la tabla de hospitales | Middleware `tenant` |
| Autorización | Permisos por operación | Módulo ASII-02 |
| Transporte | HTTPS obligatorio | Servidor web |
| Inyección | Sentencias preparadas con parámetros nombrados | Capa de persistencia |
| Fuga entre hospitales | 404 indistinguible para cita ajena o inexistente | Repositorio |
| Abuso | Límite de solicitudes por usuario | Middleware de límite |

### El hospital no viaja en el cuerpo

El identificador del hospital nunca se acepta como parámetro de la petición. Lo
resuelve el middleware a partir de una cabecera ya validada y los casos de uso
lo reciben mediante un contrato.

Aceptarlo del cliente permitiría que una petición manipulada consultara o
modificara citas de otro hospital.

### Datos sensibles fuera del registro

El motivo de la cita y las notas pueden contener información clínica. No se
escriben en los registros de la aplicación ni en las trazas; solo se
almacenan en la base.

## Resiliencia

| Riesgo | Mitigación |
|---|---|
| Dependencia lenta | Tiempo de espera de 2 segundos por llamada |
| Fallo transitorio | Hasta 2 reintentos con espera creciente |
| Dependencia caída | Interruptor que abre tras 5 fallos consecutivos |
| Reintento del cliente | Cabecera de idempotencia en la creación |
| Ráfaga de solicitudes | Límite por usuario |
| Fallo de notificación | No revierte la cita; se reintenta aparte |

### Reintento solo donde es seguro

Un reintento automático solo se aplica a operaciones de lectura y a las
escrituras que llevan clave de idempotencia. Reintentar una creación sin esa
clave produciría citas duplicadas.

### Degradación

Si la fuente de disponibilidad no responde, el módulo **rechaza** la solicitud
en lugar de aceptarla sin validar. Agendar sin verificar la jornada
incumpliría la regla central del módulo y produciría citas en horarios en que
el médico no atiende.

Es una degradación hacia el rechazo, no hacia el permiso.

## Observabilidad

| Señal | Qué se registra |
|---|---|
| Identificador de correlación | `X-Request-Id` en cada entrada de registro y en la respuesta de error |
| Registro estructurado | Operación, hospital, usuario, resultado y duración |
| Métrica de latencia | Percentiles 50, 95 y 99 por ruta |
| Métrica de negocio | Citas creadas, confirmadas, canceladas y rechazadas por regla |
| Tasa de rechazo | Proporción de rechazos por cada código de negocio |

### La métrica de negocio importa

La tasa de rechazo por cruce de horario revela si la agenda está saturada. La
tasa de rechazo por jornada revela si la disponibilidad declarada no coincide
con la realidad del hospital.

Ambas son señales operativas que ninguna métrica técnica aporta.

### Sin datos clínicos en las señales

Los registros identifican al paciente por su identificador, nunca por su
nombre, y no incluyen el motivo de la cita.

## Consistencia

### Dentro del módulo

La verificación de cruce y la escritura de la cita ocurren en la misma
transacción de base de datos. Eso reduce la ventana en que dos solicitudes
simultáneas podrían reservar el mismo intervalo.

No la elimina por completo: sin un bloqueo explícito sobre las filas del
médico, dos transacciones concurrentes pueden leer el mismo estado antes de
que cualquiera escriba.

### Mitigación adicional propuesta

| Opción | Efecto | Costo |
|---|---|---|
| Bloqueo pesimista sobre las citas del médico y día | Elimina la condición de carrera | Reduce la concurrencia en esa agenda |
| Restricción de exclusión en la base | La base rechaza el solape | Depende del motor |
| Revalidación antes de confirmar la escritura | Reduce la ventana | No la elimina |

La opción recomendada es la restricción a nivel de base, porque hace imposible
el estado inválido con independencia del código que escriba.

### Si el módulo se separara

Con bases distintas, la validación de paciente y médico dejaría de ser
transaccional. La cita se crearía con los datos verificados en ese instante, y
una baja posterior del paciente no la invalidaría automáticamente.

Ese escenario exigiría una compensación: un proceso que detecte citas cuyas
referencias dejaron de ser válidas y las marque para revisión. Es otro costo
que hoy no existe y que refuerza la decisión de no extraer el módulo.

### Consistencia de lectura

La consulta de agenda se sirve de la misma base que las escrituras, por lo que
es inmediatamente consistente. Si más adelante se introdujera una réplica de
lectura, la agenda del día debería seguir leyéndose de la fuente principal:
mostrar un horario como libre cuando acaba de ocuparse induciría al personal a
intentar una reserva que fallará.
