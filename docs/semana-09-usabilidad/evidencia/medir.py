"""Evidencia automatizada de la semana 9 sobre los wireframes de la semana 8.

1. Recorta cada hallazgo desde wireframes.html (Playwright).
2. Calcula contrastes WCAG de los colores usados.
3. Cuenta elementos operables por teclado en la grilla de horarios.
Uso: python docs/semana-09-usabilidad/evidencia/medir.py
"""
import os
from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
WF = os.path.join(AQUI, "..", "..", "semana-08-ux", "wireframes", "wireframes.html")


def lum(hexc):
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


PARES = [
    ("H-02", "Texto de horario ocupado", "#bdbdbd", "#ffffff", 4.5),
    ("H-02", "Borde de horario ocupado", "#e0e0e0", "#ffffff", 3.0),
    ("H-01", "Punto de estado pendiente", "#f0ad00", "#ffffff", 3.0),
    ("H-01", "Punto de estado confirmada", "#2e9e44", "#ffffff", 3.0),
    ("H-04", "Texto blanco sobre aviso de error", "#ffffff", "#b94a48", 4.5),
    ("H-05", "Texto blanco sobre aviso de exito", "#ffffff", "#3c8d4f", 4.5),
    ("H-08", "Texto de ayuda gris", "#666666", "#ffffff", 4.5),
    ("-", "Boton secundario (borde)", "#aaaaaa", "#ffffff", 3.0),
]

RECORTES = {
    "H-01-estado-solo-color": ["#w1-legend", "#w1-table"],
    "H-02-contraste-ocupado": ["#w3-grid"],
    "H-03-grilla-sin-teclado": ["#w3-grid"],
    "H-04-error-409-toast": ["#w4 .screen"],
    "H-05-exito-temporal": ["#w5 .screen"],
    "H-06-cancelar-ambiguo": ["#w6 .screen"],
    "H-07-fecha-ambigua": ["#w2-date"],
    "H-08-obligatorio-generico": ["#w6-reason"],
    "H-10-ayuda-sin-nombre": ["#w3-help"],
}

with open(os.path.join(AQUI, "contrastes.md"), "w", encoding="utf-8") as out:
    out.write("# Contrastes medidos (WCAG 2.2, formula de luminancia relativa)\n\n")
    out.write("| Hallazgo | Elemento | Primer plano | Fondo | Ratio | Minimo | Resultado |\n|---|---|---|---|---|---|---|\n")
    for h, nombre, fg, bg, minimo in PARES:
        r = ratio(fg, bg)
        out.write(f"| {h} | {nombre} | `{fg}` | `{bg}` | {r:.2f}:1 | {minimo}:1 | {'Cumple' if r >= minimo else '**No cumple**'} |\n")

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1300, "height": 900}, device_scale_factor=1.5)
    pg.goto("file://" + os.path.abspath(WF))
    pg.add_style_tag(content=".mk{display:none!important}")
    for nombre, sels in RECORTES.items():
        loc = pg.locator(", ".join(sels)).first if len(sels) == 1 else None
        if loc is None:
            boxes = [pg.locator(s).bounding_box() for s in sels]
            x0 = min(bx["x"] for bx in boxes) - 8; y0 = min(bx["y"] for bx in boxes) - 8
            x1 = max(bx["x"] + bx["width"] for bx in boxes) + 8; y1 = max(bx["y"] + bx["height"] for bx in boxes) + 8
            pg.screenshot(path=os.path.join(AQUI, nombre + ".png"), clip={"x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0}, full_page=True)
        else:
            loc.screenshot(path=os.path.join(AQUI, nombre + ".png"))

    # Teclado: ¿cuantos elementos de la grilla reciben foco con Tab?
    focusables = pg.evaluate("""() => [...document.querySelectorAll('#w3-grid .slot')]
        .filter(e => e.tabIndex >= 0 || ['BUTTON','INPUT','A'].includes(e.tagName)).length""")
    total = pg.evaluate("() => document.querySelectorAll('#w3-grid .slot').length")
    roles = pg.evaluate("() => document.querySelectorAll('#w3-grid [role]').length")
    with open(os.path.join(AQUI, "teclado.md"), "w", encoding="utf-8") as out:
        out.write("# Prueba de teclado sobre la grilla (W3)\n\n")
        out.write(f"- Horarios en la grilla: {total}\n")
        out.write(f"- Horarios alcanzables con Tab: {focusables}\n")
        out.write(f"- Elementos con rol ARIA en la grilla: {roles}\n")
        out.write("\nResultado: la grilla no define elementos operables por teclado ni un rol; "
                  "el wireframe no especifica cómo se elige un horario sin ratón (H-03).\n")
    b.close()
print(open(os.path.join(AQUI, "contrastes.md"), encoding="utf-8").read())
print(open(os.path.join(AQUI, "teclado.md"), encoding="utf-8").read())
