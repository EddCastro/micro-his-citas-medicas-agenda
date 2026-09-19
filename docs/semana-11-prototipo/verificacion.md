# Verificación de roles, estados y accesibilidad — Semana 11

El prototipo se verificó con un script automatizado
([`prototipo/pruebas/verificar.py`](../../prototipo/pruebas/verificar.py)) que
usa Playwright para recorrerlo y axe-core para auditar WCAG. Cada criterio
verificable del backlog de la semana 9 tiene al menos una comprobación.

**Resultado: 40 de 40 criterios cumplidos.** El detalle generado por el script
está en [`verificacion-resultados.md`](verificacion-resultados.md).

## 1. Cierre del backlog de la semana 9

| Hallazgo | Prioridad | Corrección aplicada | Verificación | Estado |
|---|:-:|---|---|:-:|
| H-06 "Cancelar" ambiguo | P1 | "Cancelar cita" / "Volver sin cancelar" / "Sí, cancelar cita" | 0 botones con el texto "Cancelar" o "Aceptar" a secas | Cerrado |
| H-04 409 genérico | P1 | Alerta en línea sobre la grilla, foco, horario "Recién ocupado", datos conservados | Foco en `#a409`, `role="alert"`, motivo intacto | Cerrado |
| H-03 grilla sin teclado | P1 | `radiogroup` con tabindex móvil y flechas | 1 parada de Tab; flechas saltan ocupados; flujo completo solo con teclado | Cerrado |
| H-01 estado solo color | P1 | Insignia con texto + ícono + color | Todas las insignias contienen Pendiente/Confirmada/Cancelada | Cerrado |
| H-09 foco del diálogo | P2 | Foco inicial en el motivo, trampa de Tab, Escape, retorno del foco | Foco inicial, 8 Tab dentro, Escape devuelve el foco a "Cancelar cita" | Cerrado |
| H-05 éxito temporal | P2 | Panel persistente con código y `role="status"` | Visible 6 s después (antes duraba 5 s) | Cerrado |
| H-02 contraste ocupado | P2 | Texto `#595959` sobre `#eceff2`, borde punteado, palabra "Ocupado" | Texto 6.07:1, borde 4.69:1 | Cerrado |
| H-08 obligatorio genérico | P3 | "(obligatorio)" u "(opcional)" en texto; error específico con `aria-describedby` y `aria-invalid` | Mensaje "…al menos 3 caracteres", asociado al campo | Cerrado |
| H-07 fecha ambigua | P3 | "martes 6 de octubre de 2026" / "mar 6 oct 2026" | Ninguna fecha dd/mm/aaaa en el texto | Cerrado |
| H-10 ayuda sin nombre | P3 | Botón "¿Por qué no veo un horario?" | Abre con Enter | Cerrado |
| H-11 borde secundario | P3 | Borde `#6b7580` | 4.69:1 | Cerrado |

**Límite conocido de H-07:** el control nativo `<input type="date">` muestra la
fecha con el formato del sistema operativo. Por eso debajo de cada control de
fecha se escribe la fecha completa en letras.

## 2. Consistencia de roles

| Rol | Inicio | Agendar | Confirmar | Cancelar | Verificado |
|---|---|:-:|:-:|:-:|:-:|
| Recepcionista | Agenda del día | Sí | Sí | Sí | Recorrido completo |
| Enfermera | Agenda filtrada en Pendientes | No | Sí | No | Sin "Nueva cita" ni "Cancelar cita"; sí "Confirmar asistencia" |
| Médico | "Mi agenda", solo lectura | No | No | No | Sin botones de acción |

Coincide con la matriz de permisos del contrato de API (semana 5) y con los
user flows (semana 8).

## 3. Consistencia con las reglas del backend

La interfaz no pide más ni menos que el servidor. Las reglas se tomaron de los
`FormRequest` de la rama `feature/asii-05-semana-06-parcial-eddcastro`.

| Regla del backend | Comportamiento del prototipo | Verificado |
|---|---|:-:|
| Motivo de cancelación obligatorio, 3 a 500 caracteres (`CancelAppointmentRequest`) | Rechaza 2 caracteres, acepta 3, límite 500 | Sí |
| Motivo de consulta opcional, máximo 500 (`StoreAppointmentRequest`) | Se agenda sin motivo; límite 500 con contador | Sí |
| Duración de 5 a 480 minutos | Ofrece 15, 30, 45 y 60 | Por diseño |
| Fecha futura (RN-01) | El calendario no admite fechas pasadas | Por diseño |
| Horario ocupado | Muestra el conflicto como 409 `APPOINTMENT_SLOT_TAKEN` | Ver nota |

**Nota sobre el 409.** Hoy el backend responde **422** con solo `message`
cuando el horario está ocupado. El prototipo muestra el comportamiento del
diseño propuesto en la semana 7 (`ErrorMapper` con los códigos del contrato de
la semana 5). La experiencia del usuario sería la misma con el 422 actual si
la interfaz reconoce el mensaje, pero el diseño no depende del texto.

## 4. Consistencia de estados

| Estado | Se ve igual en | Transiciones permitidas |
|---|---|---|
| Pendiente (● amarillo) | Agenda, tarjeta móvil, detalle | → Confirmada, → Cancelada |
| Confirmada (✓ verde) | Agenda, tarjeta móvil, detalle | → Cancelada |
| Cancelada (✕ rojo) | Agenda, tarjeta móvil, detalle | Ninguna; no muestra acciones |

Las reglas son las del dominio (`Appointment::confirm()` y `cancel()`): una
cita cancelada no se confirma ni se cancela de nuevo, y una confirmada no se
confirma otra vez.

## 5. Accesibilidad

| Verificación | Resultado |
|---|---|
| axe-core, reglas WCAG 2.0/2.1/2.2 A y AA, en agenda, paso 3, paso 4 y diálogo de cancelación con error, a 1280 y 375 px | 0 infracciones en los 8 casos |
| Flujo completo solo con teclado | Completado |
| Reflow a 320 px (WCAG 1.4.10) | Ancho del documento = 320 px en agenda, detalle y paso 4 |
| Objetivos táctiles | 44 px de alto mínimo |
| Enlace "Saltar al contenido" | Presente |
| Foco al cambiar de pantalla | Va al título `h1` de la nueva pantalla |
| Movimiento reducido | Animación del esqueleto desactivada con `prefers-reduced-motion` |
| Errores de JavaScript durante el recorrido | 0 en escritorio y móvil |

## 6. Conexión limitada

| Verificación | Resultado |
|---|---|
| Sin conexión: botón "Reintentar" y motivo conservado | Cumple |
| Al reconectar y reintentar se crea exactamente una cita | Cumple (1 cita) |

## 7. Mejores prácticas aplicadas

| Práctica | Aplicación |
|---|---|
| Diseño a partir del contenido | Cortes en 600 y 1024 px donde el contenido deja de caber |
| Prevención antes que corrección | Calendario sin fechas pasadas, médico filtrado por especialidad, solo horarios libres seleccionables |
| Acción principal única y al alcance | Un botón con relleno por pantalla; barra fija inferior en móvil |
| Estado del sistema visible | Esqueletos de carga, "Agendando…", panel de éxito persistente |
| Mensajes accionables | Qué pasó + qué hacer, sin códigos técnicos |
| Datos mínimos | Nombre abreviado en listas; DPI enmascarado; motivo solo en detalle |
| Navegación predecible | Direcciones por paso y botón atrás funcional |
| Sin dependencias | Un solo archivo HTML; funciona sin conexión a Internet |
