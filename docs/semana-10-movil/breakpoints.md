# Reglas de breakpoint — Semana 10

## Rangos

| Rango | Nombre | Dispositivos típicos | Diseño |
|---|---|---|---|
| 320–599 px | Móvil | Teléfonos de 320 (SE) a 430 (Pro Max) | Una columna, tarjetas, barra de acción fija |
| 600–1023 px | Tableta | Tabletas en vertical, ventanas angostas | Tabla, 2 columnas de campos, grilla de 6 |
| ≥ 1024 px | Escritorio | Estaciones de Recepción y Enfermería | Tabla, 3 columnas de campos, grilla de 8 |

Los cortes se definieron por **contenido, no por dispositivo**: 600 px es donde
la tabla de agenda deja de caber sin desplazamiento horizontal; 1024 px es donde
caben 8 horarios de 44 px con separación.

## Qué cambia en cada corte

| Componente | ≥ 1024 | 600–1023 | ≤ 599 |
|---|---|---|---|
| Agenda | Tabla | Tabla | Tarjetas |
| Filtros | En fila | En fila | Apilados, ancho completo |
| Indicador de pasos | 4 pestañas | 4 pestañas | "Paso N de 4" + barra |
| Campos de Médico y fecha | 3 columnas | 2 columnas | 1 columna |
| Grilla de horarios | 8 columnas | 6 columnas | 3 columnas |
| Resumen | Etiqueta y valor en fila | Igual | Etiqueta sobre valor |
| Botones de acción | Al final del contenido | Igual | Barra fija inferior; primario ocupa 2/3 |
| Diálogos | Centrados, 520 px | Centrados | Hoja inferior a ancho completo |
| Subtítulo del hospital | Visible | Visible | Oculto |
| Controles del prototipo | Desplegados | Desplegados | Plegados |

## Reglas que no cambian con el ancho

- Objetivos táctiles de al menos 44 × 44 px (supera WCAG 2.5.8, que pide 24).
- Texto base de 16 px; nada por debajo de 12 px.
- Indicador de foco de 3 px en todos los tamaños.
- El estado de la cita siempre lleva texto.
- Contraste ≥ 4.5:1 en texto y ≥ 3:1 en bordes de controles.
- Sin desplazamiento horizontal a 320 px (WCAG 1.4.10 Reflow).
- Animación del esqueleto desactivada con `prefers-reduced-motion`.
- La barra fija respeta `env(safe-area-inset-bottom)` en teléfonos con muesca.

## Implementación

```css
/* Escritorio es la base; se ajusta hacia abajo */
@media (max-width: 1023px) { /* tableta */ }
@media (max-width: 599px)  { /* móvil 320–430 */ }
```

El código completo está en `prototipo/index.html`, sección `<style>`.

## Verificación

`prototipo/pruebas/recorrido.py movil` recorre el flujo completo a 320, 375 y
430 px y genera los tableros de [`pantallas/`](pantallas). En los tres anchos
el recorrido termina sin errores de JavaScript.
