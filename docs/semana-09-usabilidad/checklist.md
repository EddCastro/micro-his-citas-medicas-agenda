# Checklist de evaluación — Semana 9

Objeto evaluado: user flow y wireframes W1–W6 de la semana 8
(`docs/semana-08-ux`), flujo **solicitud, validación de disponibilidad y
confirmación o cancelación de cita**.

Método: inspección heurística (10 heurísticas de Nielsen) + revisión contra
WCAG 2.2 nivel AA, apoyada en mediciones automatizadas
([`evidencia/medir.py`](evidencia/medir.py)): contraste por fórmula de
luminancia relativa y conteo de elementos operables por teclado.

Escala de severidad (Nielsen): 0 no es problema · 1 cosmético · 2 menor ·
3 mayor · 4 catastrófico.

## A. Heurísticas de Nielsen

| # | Heurística | Resultado | Hallazgos |
|---|---|---|---|
| 1 | Visibilidad del estado del sistema | Parcial | H-05 (éxito que desaparece) |
| 2 | Relación con el mundo real | No cumple | H-07 (fecha ambigua) |
| 3 | Control y libertad del usuario | Cumple | Pasos reabribles, datos conservados |
| 4 | Consistencia y estándares | No cumple | H-06 ("Cancelar" con dos significados) |
| 5 | Prevención de errores | Parcial | H-06; a favor: calendario sin fechas pasadas, médico filtrado |
| 6 | Reconocer antes que recordar | No cumple | H-01 (estado codificado solo en color) |
| 7 | Flexibilidad y eficiencia | Parcial | H-03 (sin atajo de teclado en la grilla) |
| 8 | Diseño estético y minimalista | Cumple | — |
| 9 | Reconocer, diagnosticar y recuperarse de errores | No cumple | H-04 ("Error" genérico en aviso lejano), H-08 |
| 10 | Ayuda y documentación | Parcial | H-10 (ayuda solo en ícono sin nombre) |

## B. WCAG 2.2 AA — criterios pedidos por la consigna

| Tema | Criterio | Resultado | Hallazgos / evidencia |
|---|---|---|---|
| Teclado | 2.1.1 Teclado | No cumple | H-03: 0 de 16 horarios alcanzables con Tab ([teclado.md](evidencia/teclado.md)) |
| Teclado | 2.1.2 Sin trampas de teclado | No definido | H-09: diálogo sin comportamiento de foco especificado |
| Foco | 2.4.3 Orden del foco | No definido | H-03, H-09 |
| Foco | 2.4.7 Foco visible | No definido | H-03: la grilla no especifica indicador de foco |
| Foco | 2.4.11 Foco no oculto | No cumple | H-04: el aviso flotante puede tapar el indicador de pasos |
| Contraste | 1.4.3 Contraste mínimo (texto) | No cumple | H-02: 1.88:1; H-05: 4.11:1 ([contrastes.md](evidencia/contrastes.md)) |
| Contraste | 1.4.11 Contraste no textual | No cumple | H-01: 1.97:1; H-02: 1.32:1; H-11: 2.32:1 |
| Color | 1.4.1 Uso del color | No cumple | H-01: estado solo por color |
| Etiquetas | 1.3.1 Información y relaciones | Parcial | H-08: error no asociado al campo |
| Etiquetas | 2.4.6 Encabezados y etiquetas | No cumple | H-06: botones "Cancelar" / "Aceptar" |
| Etiquetas | 3.3.2 Etiquetas o instrucciones | Parcial | H-08: obligatorio solo con asterisco rojo; H-07 |
| Etiquetas | 1.1.1 Contenido no textual | No cumple | H-10: ícono ⓘ sin nombre accesible |
| Mensajes | 3.3.1 Identificación de errores | Parcial | H-04: "Error" sin causa en el título |
| Mensajes | 3.3.3 Sugerencia ante errores | Parcial | H-08: "Campo requerido" no indica cómo corregir |
| Mensajes | 4.1.3 Mensajes de estado | No definido | H-04, H-05: avisos no anunciados a lectores |
| Tiempo | 2.2.1 Tiempo ajustable | No cumple | H-05: código de cita visible 5 s |
| Prevención | 3.3.4 Prevención de errores (datos) | Parcial | H-06: el diálogo existe, pero sus botones confunden |
| Tamaño | 2.5.8 Tamaño del objetivo (mínimo) | Cumple | Horarios de 34 px de alto, sobre el mínimo de 24 px |
| Autenticación | 3.3.8 Autenticación accesible | N/A | Lo resuelve ASII-01 |

## C. Resumen

| Resultado | Heurísticas | Criterios WCAG |
|---|---:|---:|
| Cumple | 2 | 1 |
| Parcial | 4 | 5 |
| No cumple / No definido | 4 | 12 |
| N/A | 0 | 1 |

Se registran **11 hallazgos** (mínimo pedido: 6), detallados en
[`hallazgos.md`](hallazgos.md) y priorizados en
[`backlog-priorizado.md`](backlog-priorizado.md).
