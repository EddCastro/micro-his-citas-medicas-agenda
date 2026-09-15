# Evaluación de la frontera de microservicio

Análisis de si el módulo ASII-05 debe extraerse como servicio independiente y,
en caso contrario, bajo qué condiciones convendría hacerlo.

## Situación actual

El Sistema Hospitalario Integrado es un monolito modular sobre Laravel. El
módulo de citas ya está aislado en su interior mediante la arquitectura por
capas y los contratos Repository declarados en el dominio: los casos de uso no
conocen Eloquent ni la base de datos.

Ese aislamiento lógico es el requisito previo de cualquier extracción. Sin él,
separar el módulo obligaría a rediseñarlo primero.

## Frontera candidata

La frontera natural es un servicio de **Agenda** que agrupe:

| Elemento | Naturaleza |
|---|---|
| Citas médicas | Propiedad exclusiva del módulo |
| Disponibilidad médica | Consumida; hoy replicada localmente |
| Reglas de cruce y transición de estado | Propiedad exclusiva |

Fuera de la frontera quedarían pacientes, médicos, especialidades, usuarios y
permisos, que pertenecen a otros módulos.

## Acoplamiento actual

| Dependencia | Tipo de uso | Frecuencia por operación |
|---|---|---|
| Usuarios y hospital activo | Lectura de contexto | 1 por solicitud |
| Permisos | Verificación | 1 por solicitud |
| Pacientes | Validación de existencia | 1 al solicitar cita |
| Médicos y especialidades | Validación de correspondencia | 1 al solicitar cita |
| Disponibilidad médica | Consulta de jornada | 1 al solicitar o reagendar |

Cada operación de escritura consulta hoy entre tres y cuatro entidades ajenas
al módulo. En el monolito esas consultas son uniones dentro de la misma base y
cuestan microsegundos.

Al extraerlo, cada una se convertiría en una llamada de red con su latencia,
su modo de fallo y su necesidad de reintento. Una solicitud de cita pasaría de
una transacción local a una secuencia de llamadas remotas coordinadas.

## Criterios medibles

La extracción se justifica cuando el costo de mantener el módulo dentro del
monolito supera el costo operativo de mantenerlo aparte. Se definen cinco
umbrales observables:

| Criterio | Umbral de activación | Cómo se mide |
|---|---|---|
| Volumen | Más de 50 solicitudes por segundo sostenidas en el módulo | Métrica de peticiones por ruta |
| Escalado diferencial | El módulo consume más del 40 % de los recursos del sistema | Uso de CPU y memoria atribuido por ruta |
| Conflicto de despliegue | Más de 4 despliegues mensuales bloqueados por cambios de otros módulos | Registro de publicaciones |
| Aislamiento de fallos | Más de 2 incidentes trimestrales en que un fallo ajeno deja la agenda inoperante | Bitácora de incidentes |
| Autonomía de equipo | Un equipo dedicado de 3 personas o más con cadencia propia | Estructura organizacional |

## Situación medida

| Criterio | Valor actual | ¿Supera el umbral? |
|---|---|---|
| Volumen | Entorno académico, sin carga real | No |
| Escalado diferencial | Sin medición diferenciada | No |
| Conflicto de despliegue | Ninguno registrado | No |
| Aislamiento de fallos | Ninguno registrado | No |
| Autonomía de equipo | Un estudiante responsable del módulo | No |

## Decisión

**No se extrae el módulo.** Ninguno de los cinco criterios alcanza su umbral.

La separación introduciría latencia de red en cada validación, exigiría
coordinar consistencia entre bases distintas, obligaría a operar y observar dos
despliegues, y multiplicaría los modos de fallo. A cambio no resolvería ningún
problema que hoy exista de forma medible.

La decisión sigue la advertencia de la consigna: no dividir el sistema sin una
justificación medible.

## Costo evitado

| Costo que la extracción habría introducido | Estimación |
|---|---|
| Latencia adicional por operación de escritura | 3 a 4 llamadas de red |
| Consistencia entre bases | Requiere saga o compensación |
| Observabilidad | Trazado distribuido obligatorio |
| Despliegue | Dos artefactos en lugar de uno |
| Pruebas de integración | Dependen de otro servicio en ejecución |

## Migración razonada

Si en el futuro algún umbral se alcanza, la extracción sigue cuatro etapas
ordenadas de menor a mayor riesgo. Cada una deja el sistema en un estado
funcional y reversible.

### Etapa 1 — Aislar la propiedad de datos

Las tablas del módulo dejan de ser consultadas por otros módulos mediante
uniones directas. Todo acceso pasa por los contratos del módulo.

Condición de salida: ninguna consulta ajena referencia las tablas de citas.
Se verifica revisando las consultas del sistema.

### Etapa 2 — Reemplazar las dependencias por contratos remotos

Las implementaciones de `PatientReader` y `DoctorAvailabilityRepository` pasan
a consumir la interfaz HTTP de los módulos propietarios, aunque sigan
desplegados juntos. Aparecen así los tiempos de espera y reintentos reales.

Condición de salida: el módulo funciona con las dependencias detrás de red,
con latencia y tasa de error medidas.

### Etapa 3 — Separar el almacenamiento

Las tablas de citas y disponibilidad migran a su propia base. Las referencias a
pacientes y médicos se conservan como identificadores sin clave foránea.

Condición de salida: la base propia opera sin claves foráneas hacia tablas
ajenas y las pruebas de integración siguen aprobando.

### Etapa 4 — Desplegar de forma independiente

El módulo se publica como servicio propio. La aplicación anterior lo consume
por red.

Condición de salida: el servicio se despliega sin coordinar con el resto y
los umbrales que motivaron la extracción se reducen de forma observable.

### Punto de retorno

Las tres primeras etapas son reversibles con bajo costo. La cuarta no lo es en
la práctica, porque introduce operación independiente. Por eso las tres
primeras pueden ejecutarse de forma preventiva y la cuarta solo cuando un
umbral esté efectivamente superado.

## Consecuencia para el diseño actual

La decisión de no extraer no significa no prepararse. El módulo mantiene:

- Contratos declarados en el dominio, sustituibles por implementaciones remotas.
- Ausencia de consultas ajenas hacia sus tablas.
- Un contrato de API estable y versionado.
- Identificadores de correlación en cada solicitud.

Con eso, la etapa 1 está cumplida y la etapa 2 requiere escribir
implementaciones alternativas de contratos que ya existen, sin tocar los casos
de uso.
