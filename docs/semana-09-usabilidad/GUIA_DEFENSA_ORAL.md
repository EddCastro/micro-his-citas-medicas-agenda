# Guía de defensa oral — Semana 9, Usabilidad y accesibilidad

## Datos generales

- **Módulo:** ASII-05 — Citas médicas y agenda
- **Estudiante:** Eddy Adolfo Castro Véliz
- **Objeto evaluado:** user flow y wireframes W1–W6 de la semana 8

## 1. ¿Qué se evaluó y con qué?

El flujo de la semana 8 con las 10 heurísticas de Nielsen y 19 criterios de
WCAG 2.2 nivel AA, en los temas que pide la consigna: teclado, foco,
contraste, etiquetas, mensajes y prevención de errores.

## 2. ¿Cómo se obtuvo la evidencia?

Con el script `evidencia/medir.py`: recorta cada hallazgo desde los
wireframes, calcula el contraste con la fórmula de luminancia relativa de WCAG
y cuenta cuántos horarios de la grilla se alcanzan con Tab. Cualquiera puede
volver a ejecutarlo y obtener los mismos números.

## 3. ¿Cuál es el hallazgo más grave?

H-06: en el diálogo de cancelación, "Cancelar" cierra sin cancelar y "Aceptar"
cancela la cita. Es una acción destructiva con etiquetas que dicen lo contrario
de lo que hacen.

## 4. ¿Y el más relacionado con el núcleo del módulo?

H-04: el conflicto de concurrencia (409) se mostraba con un aviso que decía
solo "Error", lejos del botón y sin mover el foco. Es el error que produce el
bloqueo de la semana 6 y el usuario podía no enterarse.

## 5. ¿Qué es la severidad de Nielsen?

Una escala de 0 a 4: 0 no es problema, 1 cosmético, 2 menor, 3 mayor y 4
catastrófico. Se asigna por la frecuencia, el impacto y la persistencia del
problema.

## 6. ¿Cómo se priorizó el backlog?

Severidad × frecuencia × peso del concepto. El peso es 2 cuando el fallo puede
producir una cita incorrecta, perdida o cancelada por error. Con 16 puntos o
más es P1.

## 7. ¿Por qué H-01 y H-03 subieron a P1 si su puntaje era 12?

Porque bloquean por completo a un grupo de usuarios: sin teclado no se puede
elegir horario, y con daltonismo no se distingue una cita confirmada de una
cancelada. Un fallo que impide terminar la tarea no se compensa con baja
frecuencia.

## 8. ¿Qué significa 1.88:1?

Es la relación de contraste entre el texto de un horario ocupado (`#bdbdbd`) y
el fondo blanco. WCAG exige 4.5:1 para texto normal. El 1:1 es sin contraste y
el 21:1 es negro sobre blanco.

## 9. ¿Qué es un criterio verificable?

Una condición que se puede comprobar con sí o no, sin opinión. Por ejemplo:
"Tab entra a la grilla una sola vez" o "el código de la cita sigue visible 60 s
después". La semana 11 comprueba cada uno sobre el prototipo.

## 10. ¿Por qué no hubo pruebas con usuarios?

El módulo no tiene interfaz implementada ni acceso a personal del hospital. La
evaluación heurística es el método indicado para una etapa de diseño y se
declara esa limitación en el README.

## Modificación práctica

Podrían pedir agregar un hallazgo nuevo. Se agrega su bloque en
`hallazgos.md`, su recorte en `evidencia/medir.py` dentro del diccionario
`RECORTES` y su fila en el backlog:

    "H-12-nuevo-hallazgo": ["#w2-patient"],

Después se ejecuta `python docs/semana-09-usabilidad/evidencia/medir.py` y se
actualizan los totales del checklist.

## Resumen para exposición

Se evaluaron los wireframes con heurísticas y WCAG, apoyando cada hallazgo con
capturas y mediciones reproducibles. De once hallazgos, cuatro son de
severidad máxima y dos tocan directamente la cancelación y la concurrencia.
Cada corrección tiene un criterio verificable que la semana 11 comprueba sobre
el prototipo.
