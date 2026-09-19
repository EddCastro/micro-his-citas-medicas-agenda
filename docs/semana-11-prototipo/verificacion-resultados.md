# Resultados de la verificación automatizada

Generado por `python prototipo/pruebas/verificar.py` (Playwright + axe-core).

**40 de 40 criterios cumplidos.**

| Referencia | Criterio | Resultado | Detalle |
|---|---|---|---|
| WCAG | axe-core sin infracciones A/AA: agenda, escritorio 1280 px | Cumple |  |
| WCAG | axe-core sin infracciones A/AA: paso 4 revisar, escritorio 1280 px | Cumple |  |
| WCAG | axe-core sin infracciones A/AA: paso 3 horarios, escritorio 1280 px | Cumple |  |
| WCAG | axe-core sin infracciones A/AA: diálogo de cancelación con error, escritorio 1280 px | Cumple |  |
| JS | Sin errores de JavaScript (escritorio 1280 px) | Cumple |  |
| WCAG | axe-core sin infracciones A/AA: agenda, móvil 375 px | Cumple |  |
| WCAG | axe-core sin infracciones A/AA: paso 4 revisar, móvil 375 px | Cumple |  |
| WCAG | axe-core sin infracciones A/AA: paso 3 horarios, móvil 375 px | Cumple |  |
| WCAG | axe-core sin infracciones A/AA: diálogo de cancelación con error, móvil 375 px | Cumple |  |
| JS | Sin errores de JavaScript (móvil 375 px) | Cumple |  |
| H-06 | Ningún botón dice solo "Cancelar" o "Aceptar" | Cumple | 0 coincidencias |
| H-04 | Tras 409 el foco queda en la alerta con role=alert | Cumple | foco=a409, role=alert |
| H-04 | El horario perdido figura como "Recién ocupado" | Cumple |  |
| H-04 | Paciente, médico y motivo se conservan tras el 409 | Cumple |  |
| H-05 | El código de la cita sigue visible 6 s después (el aviso de la semana 8 duraba 5 s) | Cumple |  |
| H-05 | Panel de éxito con role="status" | Cumple |  |
| H-01 | Cada estado de la agenda incluye texto | Cumple | ● Pendiente, ✓ Confirmada, ✕ Cancelada |
| H-03 | La grilla es un radiogroup con una sola parada de Tab | Cumple | paradas=1 |
| H-03 | Las flechas mueven la selección y saltan los ocupados | Cumple | 08:00 -> 09:00 |
| TECLADO | Flujo agenda → paso 1…4 → éxito completado solo con teclado | Cumple |  |
| H-09 | Foco inicial en el motivo | Cumple | reasonCancel |
| H-09 | Tab no sale del diálogo abierto | Cumple |  |
| H-09 | Escape cierra y el foco vuelve a "Cancelar cita" | Cumple | bCancelar |
| H-08 | El error del motivo está asociado (aria-describedby, aria-invalid) y dice qué falta | Cumple | Escriba el motivo de la cancelación: al menos 3 caracteres. |
| BACKEND | Cancelar con 2 caracteres se rechaza (CancelAppointmentRequest pide mínimo 3) | Cumple |  |
| BACKEND | El motivo de cancelación admite hasta 500 caracteres | Cumple |  |
| BACKEND | Cancelar con 3 caracteres se acepta | Cumple |  |
| BACKEND | El motivo de la consulta es opcional y admite hasta 500 caracteres (StoreAppointmentRequest) | Cumple |  |
| BACKEND | Se puede agendar sin motivo de consulta | Cumple |  |
| H-07 | La fecha visible incluye día de la semana y mes en letras | Cumple |  |
| H-07 | No aparecen fechas numéricas dd/mm/aaaa en el texto | Cumple |  |
| H-10 | La ayuda es un botón con texto y abre con teclado | Cumple |  |
| H-02 | Texto de horario ocupado ≥ 4.5:1 | Cumple | 6.07:1 |
| H-02 | Borde de horario ocupado ≥ 3:1 contra la tarjeta | Cumple | 4.69:1 |
| H-11 | Borde de botón secundario ≥ 3:1 | Cumple | 4.69:1 |
| ROLES | Médico: sin botones de agendar, confirmar ni cancelar | Cumple |  |
| ROLES | Enfermera: confirma, pero no agenda ni cancela | Cumple |  |
| 1.4.10 | Sin desplazamiento horizontal a 320 px (agenda, detalle, paso 4) | Cumple | anchos=[320, 320, 320] |
| RED | Sin conexión: botón "Reintentar" y motivo conservado | Cumple |  |
| RED | Al reconectar y reintentar se crea exactamente una cita | Cumple | citas de José R. L. a las 11:00: 1 |
