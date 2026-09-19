# Guía de defensa oral — Semana 10, Diseño para movilidad

## Datos generales

- **Módulo:** ASII-05 — Citas médicas y agenda
- **Estudiante:** Eddy Adolfo Castro Véliz
- **Rango móvil:** 320 a 430 px

## 1. ¿Qué se entregó?

Cinco pantallas (agenda, médico y fecha, disponibilidad, revisar y agendar,
cancelar cita) mostradas a 320, 375 y 430 px; las reglas de breakpoint; y dos
escenarios móviles con sus decisiones de contenido y de error.

## 2. ¿Por qué los cortes en 600 y 1024 px?

Se definieron por contenido: en 600 px la tabla de agenda deja de caber sin
desplazamiento horizontal, y en 1024 px caben ocho horarios de 44 px. No se
eligieron por marcas de teléfono.

## 3. ¿Qué cambia en móvil?

La tabla pasa a tarjetas, los cuatro pasos pasan a "Paso N de 4" con barra,
la grilla pasa de 8 a 3 columnas agrupadas en Mañana y Tarde, los diálogos se
vuelven hojas inferiores y la acción principal queda fija abajo.

## 4. ¿Cómo se redujo la carga cognitiva?

Una decisión por pantalla, una sola línea de contexto con lo ya elegido, un
solo botón con color de relleno y ninguna acción que el rol no pueda usar.

## 5. ¿Por qué 44 px si WCAG pide 24?

WCAG 2.5.8 fija 24 px como mínimo. Con 44 px se reduce el error al tocar con
el pulgar, sobre todo en la grilla de horarios, donde tocar el horario vecino
agenda la cita a otra hora.

## 6. ¿Qué pasa si se pierde la conexión?

Se muestra un aviso con lo que se puede y no se puede hacer. La agenda cargada
se sigue viendo. Al enviar sin red aparece "No pudimos confirmar el registro"
y el botón pasa a Reintentar, con la misma `Idempotency-Key`: si la primera
solicitud sí llegó, no se crea otra cita.

## 7. ¿Por qué no un modo sin conexión que guarde la cita y la envíe después?

Porque dos recepcionistas podrían agendar el mismo horario sin red y el
conflicto aparecería más tarde, sin el paciente enfrente. Además obligaría a
guardar datos de paciente en el teléfono.

## 8. ¿Cómo se ve el conflicto 409 en el teléfono?

Regresa al paso 3 con la grilla recargada. La alerta dice qué horario se
perdió, ese horario queda marcado "Recién ocupado" y paciente, médico y motivo
se conservan.

## 9. ¿Qué correcciones de la semana 9 se aplicaron aquí?

Las cuatro P1: estado con texto (H-01), grilla operable con teclado (H-03),
alerta del 409 en línea con foco (H-04) y botones de cancelación inequívocos
(H-06).

## 10. ¿De dónde salen las pantallas?

Son capturas automáticas del prototipo HTML, tomadas con
`prototipo/pruebas/recorrido.py`. Así las pantallas del documento y el
prototipo de la semana 11 son la misma cosa.

## Modificación práctica

Podrían pedir que en móvil la grilla muestre 4 columnas en vez de 3. En
`prototipo/index.html`, dentro de `@media (max-width: 599px)`:

    .slots { grid-template-columns: repeat(4, minmax(0, 1fr)); }

Luego se ejecuta `python prototipo/pruebas/recorrido.py movil` y se revisa que
a 320 px cada horario siga midiendo al menos 44 px de ancho.

## Resumen para exposición

La versión móvil prioriza una decisión por pantalla y deja la acción principal
al alcance del pulgar. Los cortes se definieron por contenido. Los dos
escenarios, conflicto en ventanilla y red débil en el pasillo, muestran que el
usuario nunca pierde lo capturado ni termina con una cita duplicada.
