# Guía de defensa oral — Semana 11, Prototipo navegable

## Datos generales

- **Módulo:** ASII-05 — Citas médicas y agenda
- **Estudiante:** Eddy Adolfo Castro Véliz
- **Prototipo:** `prototipo/index.html`

## 1. ¿Qué se entregó?

Un prototipo navegable en HTML que funciona en escritorio y en teléfono, su
mapa de navegación, capturas de cada paso del camino feliz y del error
crítico, y una verificación automatizada con 40 criterios.

## 2. ¿Por qué HTML y no Figma?

La consigna del proyecto acepta "Figma, Canva, Excalidraw o equivalente". Un
prototipo HTML se abre sin cuenta, funciona en el teléfono real, tiene
navegación y teclado reales y se puede verificar de forma automática. Figma no
permite comprobar con un script que el foco o el contraste sean correctos.

## 3. ¿Cuál es el camino feliz?

Agenda → Nueva cita → paciente → médico y fecha → horario → revisar →
Agendar → panel de éxito con el código de la cita en estado pendiente.

## 4. ¿Cuál es el error crítico y por qué ese?

Que otro usuario reserve el mismo horario entre la consulta y el envío. Es el
error que el módulo previene en el backend con el bloqueo y el índice de la
semana 6; si la interfaz lo muestra mal, el usuario no se entera o repite el
intento sobre un horario que ya no existe.

## 5. ¿Cómo se simula?

Con la casilla "Otro usuario toma el horario (409)" de la franja de controles
del prototipo. Al pulsar Agendar, el prototipo registra una cita ajena en ese
horario y responde con el conflicto.

## 6. ¿El backend responde 409 hoy?

No. Hoy responde 422 con un mensaje. El prototipo muestra el diseño propuesto
en la semana 7, donde `ErrorMapper` emite 409 `APPOINTMENT_SLOT_TAKEN` según el
contrato de la semana 5. Se declara en `verificacion.md` para no presentarlo
como implementado.

## 7. ¿Cómo se mantiene la consistencia de roles?

El selector de rol cambia lo que se ve: la Recepcionista agenda, confirma y
cancela; la Enfermera solo confirma y entra con el filtro "Pendientes"; el
Médico ve su agenda en solo lectura. Es la matriz de la semana 5 y la
verificación lo comprueba.

## 8. ¿Cómo se comprobó la accesibilidad?

Con axe-core en ocho pantallas (cuatro por tamaño), 0 infracciones A y AA;
recorriendo el flujo completo solo con teclado; midiendo el contraste en el
navegador; y comprobando que a 320 px no haya desplazamiento horizontal.

## 9. ¿Qué pasó con los once hallazgos de la semana 9?

Los once quedaron cerrados y cada uno tiene al menos una comprobación
automática. Uno de ellos, la trampa de foco del diálogo (H-09), falló en la
primera verificación y se corrigió antes de entregar.

## 10. ¿Las reglas de los campos son las del backend?

Sí. El motivo de cancelación pide de 3 a 500 caracteres, como
`CancelAppointmentRequest`, y el motivo de la consulta es opcional hasta 500,
como `StoreAppointmentRequest`. La verificación incluye cinco comprobaciones
de esas reglas.

## Modificación práctica

Podrían pedir agregar el rol Admin al selector. En `prototipo/index.html`:

    <option value="admin">Admin</option>

y en el objeto de permisos:

    admin: { crear: true, confirmar: true, cancelar: true },

Luego se agrega una comprobación en `prototipo/pruebas/verificar.py`
(sección ROLES) y se ejecuta la verificación.

## Resumen para exposición

El prototipo recorre el flujo completo en escritorio y móvil con los tres
roles. El error crítico es el conflicto de concurrencia, y la interfaz dice
qué horario se perdió sin perder lo capturado. Cada corrección de la semana 9
y cada regla de los formularios del backend tiene una comprobación automática:
40 de 40 cumplidas.
