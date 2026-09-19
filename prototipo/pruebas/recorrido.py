"""Recorre el prototipo con Playwright y guarda capturas.

Uso:
  python prototipo/pruebas/recorrido.py movil     -> docs/semana-10-movil/pantallas
  python prototipo/pruebas/recorrido.py desktop   -> docs/semana-11-prototipo/capturas (desktop)
  python prototipo/pruebas/recorrido.py todo      -> ambos tamaños en semana 11
"""
import os, sys
from playwright.sync_api import sync_playwright

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
URL = "file://" + os.path.join(RAIZ, "prototipo", "index.html")
TAM = {"desktop": {"width": 1280, "height": 800}, "movil": {"width": 375, "height": 812}}


def flujo(pg, out, pref, full=False):
    errores = []
    pg.on("pageerror", lambda e: errores.append(str(e)))
    shot = lambda n: pg.screenshot(path=os.path.join(out, f"{pref}{n}.png"), full_page=full)
    pg.goto(URL + "#/agenda"); pg.wait_for_timeout(200)
    shot("01-agenda")
    pg.click("text=+ Nueva cita")
    pg.fill("#qPac", "Pérez"); pg.check("input[name=pac]"); shot("02-paciente")
    pg.click("#n1")
    pg.select_option("#esp", "Medicina interna"); pg.select_option("#medS", "1"); shot("03-medico-fecha")
    pg.click("#n2"); pg.wait_for_timeout(100); shot("04-horarios-cargando")
    pg.wait_for_selector(".slot"); pg.click(".slot[data-h='10:30']"); shot("05-horario-elegido")
    pg.click("#n3"); pg.fill("#motivo", "Control de presión arterial"); shot("06-revisar")
    pg.click("#n4"); pg.wait_for_selector("#okPanel"); pg.wait_for_timeout(100); shot("07-exito")
    # Error crítico: concurrencia 409
    pg.click("#okOtra"); pg.fill("#qPac", "Gómez"); pg.check("input[name=pac]"); pg.click("#n1")
    pg.select_option("#esp", "Medicina interna"); pg.select_option("#medS", "1"); pg.click("#n2")
    pg.wait_for_selector(".slot"); pg.click(".slot[data-h='11:00']"); pg.click("#n3")
    pg.fill("#motivo", "Seguimiento de laboratorio")
    if pg.locator("#demoBox").get_attribute("open") is None: pg.click("#demoBox summary")
    pg.check("#sim409"); shot("08-antes-del-conflicto")
    pg.click("#n4"); pg.wait_for_selector("#a409"); pg.wait_for_selector(".slot"); pg.wait_for_timeout(100)
    shot("09-error-409-horario-tomado")
    pg.click(".slot[data-h='11:30']"); pg.click("#n3"); pg.click("#n4"); pg.wait_for_selector("#okPanel"); shot("10-recuperado-exito")
    # Cancelación
    pg.click("#okVer"); pg.wait_for_selector("#bCancelar"); shot("11-detalle")
    pg.click("#bCancelar"); pg.click("#btnDoCancel"); shot("12-cancelar-validacion")
    pg.fill("#reasonCancel", "Paciente reprogramará por viaje"); pg.click("#btnDoCancel")
    pg.wait_for_selector(".alert.ok"); shot("13-cancelada")
    # Sin conexión
    pg.goto(URL + "?offline=1#/agenda"); pg.click("text=+ Nueva cita"); pg.fill("#qPac", "López"); pg.check("input[name=pac]")
    pg.click("#n1"); pg.select_option("#esp", "Pediatría"); pg.select_option("#medS", "2"); pg.click("#n2")
    pg.wait_for_selector(".slot"); pg.click(".slot:not([aria-disabled])"); pg.click("#n3"); pg.fill("#motivo", "Control de niño sano")
    pg.click("#n4"); pg.wait_for_selector("#aNet"); shot("14-sin-conexion")
    # Enfermera
    pg.goto(URL + "?rol=enfermera#/agenda"); pg.wait_for_timeout(100); shot("15-enfermera-pendientes")
    return errores


def tableros(out):
    """Une 320, 375 y 430 px de cada pantalla elegida en un solo PNG."""
    import glob
    from PIL import Image, ImageDraw, ImageFont
    try:
        fuente = ImageFont.truetype("DejaVuSans-Bold.ttf", 30)
    except OSError:
        fuente = ImageFont.load_default()
    sets = {"P1-agenda": "01-agenda", "P2-medico-fecha": "03-medico-fecha", "P3-disponibilidad": "05-horario-elegido",
            "P4-revisar-agendar": "06-revisar", "P5-cancelar-cita": "12-cancelar-validacion",
            "E1-conflicto-409": "09-error-409-horario-tomado", "E2-sin-conexion": "14-sin-conexion"}
    for nombre, suf in sets.items():
        ims = [(w, Image.open(os.path.join(out, f"m{w}-{suf}.png"))) for w in (320, 375, 430)]
        W = sum(i.width for _, i in ims) + 160; H = max(i.height for _, i in ims) + 70
        c = Image.new("RGB", (W, H), "#e9ecef"); d = ImageDraw.Draw(c); x = 40
        for w, i in ims:
            d.text((x, 18), f"{w} px", fill="#1b1f24", font=fuente); c.paste(i, (x, 60)); x += i.width + 40
        c.save(os.path.join(out, nombre + ".png"), optimize=True)
    for f in glob.glob(os.path.join(out, "m*.png")):
        os.remove(f)


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "todo"
    with sync_playwright() as p:
        b = p.chromium.launch()
        if modo == "movil":
            out = os.path.join(RAIZ, "docs", "semana-10-movil", "pantallas"); os.makedirs(out, exist_ok=True)
            for w in (375, 320, 430):
                pg = b.new_page(viewport={"width": w, "height": 812}, device_scale_factor=2, locale="es-GT")
                print(w, flujo(pg, out, f"m{w}-"))
                pg.close()
            tableros(out)
        else:
            out = os.path.join(RAIZ, "docs", "semana-11-prototipo", "capturas"); os.makedirs(out, exist_ok=True)
            for nombre in (["desktop", "movil"] if modo == "todo" else [modo]):
                pg = b.new_page(viewport=TAM[nombre], device_scale_factor=1 if nombre == "desktop" else 2, locale="es-GT")
                print(nombre, flujo(pg, out, nombre + "-", full=(nombre == "desktop")))
                pg.close()
        b.close()
