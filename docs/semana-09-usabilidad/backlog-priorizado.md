# Backlog priorizado de correcciones — Semana 9

## Criterio de prioridad

`Prioridad = Severidad (0–4) × Frecuencia (1–3) × Peso del concepto (1–2)`

- **Frecuencia:** 3 = en cada cita, 2 = en la mayoría, 1 = ocasional.
- **Peso del concepto:** 2 si el fallo puede producir una cita incorrecta,
  perdida o cancelada por error (concurrencia, cancelación, confirmación);
  1 en otro caso.

| Puntaje | Prioridad | Se corrige en |
|---|---|---|
| ≥ 16 | P1 — Crítica | Semana 10 (diseño móvil) y semana 11 (prototipo) |
| 8–15 | P2 — Alta | Semana 11 (prototipo) |
| < 8 | P3 — Media | Semana 11 si el tiempo lo permite |

## Backlog

| # | Hallazgo | S | F | P | Puntaje | Prioridad | Corrección propuesta | Criterio verificable |
|---|---|:-:|:-:|:-:|:-:|:-:|---|---|
| 1 | H-06 "Cancelar" ambiguo | 4 | 2 | 2 | **16** | P1 | Ficha: "Cancelar cita". Diálogo: "Volver sin cancelar" (secundario) y "Sí, cancelar cita" (destructivo, rojo oscuro). Nunca "Aceptar" ni "Cancelar" a secas | Ningún botón del flujo tiene el texto exacto "Cancelar" o "Aceptar" (búsqueda en el código del prototipo = 0 resultados) |
| 2 | H-04 409 genérico y lejano | 4 | 2 | 2 | **16** | P1 | Alerta en línea sobre la grilla con `role="alert"`: "Otro usuario acaba de reservar las 10:30. Elija otro horario; sus datos se conservaron." Foco al mensaje; horario marcado "Recién ocupado" | Al simular el 409: el foco queda en la alerta, el horario perdido aparece como ocupado y paciente/médico/motivo siguen llenos |
| 3 | H-03 grilla sin teclado | 4 | 3 | 1 | **12** | P2* | Grilla como `radiogroup`: una parada de Tab, flechas para moverse, Espacio/Enter para elegir, foco visible de 3 px | Completar el flujo W1→W5 solo con teclado; Tab entra a la grilla una sola vez |
| 4 | H-01 estado solo por color | 4 | 3 | 1 | **12** | P2* | Insignia con texto + ícono + color: "● Pendiente", "✓ Confirmada", "✕ Cancelada" | La agenda en escala de grises permite identificar los tres estados; contraste de la insignia ≥ 4.5:1 |
| 5 | H-05 éxito temporal | 3 | 3 | 1 | 9 | P2 | Panel de éxito persistente con el código y `role="status"`; se cierra solo con acción del usuario | El código sigue visible 60 s después de agendar |
| 6 | H-02 contraste ocupado | 3 | 3 | 1 | 9 | P2 | Ocupado: fondo `#eeeeee`, texto `#595959` (7.0:1) tachado + etiqueta "Ocupado" | Ratio medido ≥ 4.5:1 en texto y ≥ 3:1 en borde |
| 7 | H-09 foco del diálogo | 3 | 2 | 2 | **12** | P2 | Foco inicial en el motivo; Tab queda dentro; Escape = "Volver sin cancelar"; al cerrar, foco regresa a "Cancelar cita" | Abrir, recorrer con Tab (no sale del diálogo), Escape cierra y el foco vuelve al botón de origen |
| 8 | H-08 obligatorio y error | 2 | 3 | 1 | 6 | P3 | "(obligatorio)" en texto; mensaje específico asociado con `aria-describedby` y `aria-invalid` | El mensaje nombra el campo y el rango; axe-core sin infracciones en el formulario |
| 9 | H-07 fecha ambigua | 2 | 3 | 1 | 6 | P3 | Formato "lun 5 oct 2026, 10:30" en toda la interfaz | Toda fecha visible incluye día de la semana y mes en letras |
| 10 | H-10 ayuda sin nombre | 2 | 2 | 1 | 4 | P3 | Botón "¿Por qué no veo un horario?" con texto visible que abre la explicación | El control tiene nombre accesible y funciona con teclado |
| 11 | H-11 borde secundario | 1 | 3 | 1 | 3 | P3 | Borde `#6b6b6b` (5.3:1) | Ratio medido ≥ 3:1 |

\* H-03 y H-01 quedan en P2 por puntaje, pero se **promueven a P1** porque
bloquean por completo a usuarios de teclado o con daltonismo: un fallo que
impide terminar la tarea no se compensa con baja frecuencia de riesgo.

## Orden de trabajo resultante

1. **P1:** H-06, H-04, H-03, H-01 → se incorporan al diseño móvil (semana 10)
   y al prototipo (semana 11).
2. **P2:** H-09, H-05, H-02 → prototipo (semana 11).
3. **P3:** H-08, H-07, H-10, H-11 → prototipo (semana 11).

La semana 11 verifica cada criterio sobre el prototipo navegable.
