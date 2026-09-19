# Semana 9 — Evaluación del diseño, usabilidad y accesibilidad

Módulo **ASII-05 — Citas médicas y agenda**.

| Dato | Información |
|---|---|
| Estudiante | Eddy Adolfo Castro Véliz |
| Código | 1890-23-16857 |
| GitHub | EddCastro |
| Correo | ecastrov5@miumg.edu.gt |
| Issue | #5 |
| Rama | `feature/week-09-usabilidad` |

## Tarea

Evaluar el flujo UX de la semana 8 con heurísticas de usabilidad y WCAG
(teclado, foco, contraste, etiquetas, mensajes y prevención de errores) y
priorizar las correcciones según su impacto en citas, agenda médica,
disponibilidad, confirmación, cancelación y concurrencia.

## Resultado

**11 hallazgos**, cuatro de severidad 4. Los dos más graves tocan
directamente el núcleo del módulo:

- **H-06** — en el diálogo de cancelación, "Cancelar" no cancela y "Aceptar"
  sí: una acción destructiva con etiquetas invertidas.
- **H-04** — el conflicto de concurrencia (409) se informa con un aviso que
  dice solo "Error", lejos del botón y sin mover el foco.

## Entregables

| Evidencia pedida | Archivo |
|---|---|
| Checklist completado | [`checklist.md`](checklist.md) — 10 heurísticas + 19 criterios WCAG 2.2 |
| Evidencia de al menos 6 hallazgos | [`hallazgos.md`](hallazgos.md) + capturas en [`evidencia/`](evidencia) |
| Backlog priorizado con corrección y criterio verificable | [`backlog-priorizado.md`](backlog-priorizado.md) |
| Mediciones reproducibles | [`evidencia/medir.py`](evidencia/medir.py) → `contrastes.md`, `teclado.md` |
| Guía de defensa oral | [`GUIA_DEFENSA_ORAL.md`](GUIA_DEFENSA_ORAL.md) |
| Declaración de IA | [`DECLARACION_IA.md`](DECLARACION_IA.md) |

## Método

1. Recorrido del flujo por rol (Recepcionista, Enfermera, Médico) sobre W1–W6.
2. Inspección con las 10 heurísticas de Nielsen, severidad 0–4.
3. Revisión contra WCAG 2.2 AA en los temas que pide la consigna.
4. Medición automatizada: contraste con la fórmula de luminancia relativa y
   conteo de elementos operables por teclado en la grilla.
5. Priorización por severidad × frecuencia × peso del concepto.

## Alcance de la entrega

Incluye:

- Evaluación del user flow y de los seis wireframes de la semana 8.
- Inspección con las 10 heurísticas de Nielsen y 19 criterios de WCAG 2.2.
- Once hallazgos con captura y, cuando aplica, medición.
- Backlog priorizado con corrección propuesta y criterio verificable.

No incluye:

- Pruebas con usuarios reales: el módulo no tiene todavía interfaz
  implementada ni usuarios del hospital disponibles.
- Evaluación con lectores de pantalla reales; se evalúa la especificación.
- Aplicación de las correcciones, que corresponde a las semanas 10 y 11.

## Validación

El script de evidencia se ejecutó sin errores:

```powershell
python docs/semana-09-usabilidad/evidencia/medir.py
```

Terminó con código de salida `0` y regeneró `contrastes.md`, `teclado.md` y
las nueve capturas de `evidencia/`.

## Reproducir la evidencia

```powershell
pip install playwright
python -m playwright install chromium
python docs/semana-09-usabilidad/evidencia/medir.py
```

El script lee `docs/semana-08-ux/wireframes/wireframes.html`, recorta cada
hallazgo y regenera `contrastes.md` y `teclado.md`.

## Continuidad

Las correcciones P1 se aplican en el diseño móvil (semana 10) y todas se
verifican sobre el prototipo navegable (semana 11).
