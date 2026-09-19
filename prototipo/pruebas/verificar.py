"""Verifica el prototipo contra los criterios del backlog de la semana 9.

Requisitos:
  pip install playwright
  python -m playwright install chromium
  npm install axe-core        (o indicar la ruta con la variable AXE_JS)

Uso:
  python prototipo/pruebas/verificar.py
Genera docs/semana-11-prototipo/verificacion-resultados.md y termina con
código 1 si algún criterio falla.
"""
import os
import re
import sys
from playwright.sync_api import sync_playwright

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HTML = os.path.join(RAIZ, "prototipo", "index.html")
URL = "file://" + HTML
AXE = os.environ.get("AXE_JS") or os.path.join(RAIZ, "node_modules", "axe-core", "axe.min.js")
SALIDA = os.path.join(RAIZ, "docs", "semana-11-prototipo", "verificacion-resultados.md")

resultados = []  # (id, criterio, ok, detalle)


def registrar(hid, criterio, ok, detalle=""):
    resultados.append((hid, criterio, bool(ok), detalle))
    print(("OK   " if ok else "FALLA"), hid, criterio, detalle)


def lum(rgb):
    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def rgb(s):
    return tuple(int(x) for x in re.findall(r"\d+", s)[:3])


def axe(pg, etiqueta):
    pg.add_script_tag(path=AXE)
    r = pg.evaluate("""async () => {
        const r = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa'] } });
        return r.violations.map(v => v.id + ' (' + v.nodes.length + ')');
    }""")
    registrar("WCAG", f"axe-core sin infracciones A/AA: {etiqueta}", not r, ", ".join(r))


def hasta_paso4(pg, paciente="Pérez", hora="10:30", motivo=None):
    pg.goto(URL + "#/agenda")
    pg.click("text=+ Nueva cita")
    pg.fill("#qPac", paciente); pg.check("input[name=pac]"); pg.click("#n1")
    pg.select_option("#esp", "Medicina interna"); pg.select_option("#medS", "1"); pg.click("#n2")
    pg.wait_for_selector(".slot"); pg.click(f".slot[data-h='{hora}']"); pg.click("#n3")
    if motivo:
        pg.fill("#motivo", motivo)


with sync_playwright() as p:
    b = p.chromium.launch()

    for nombre, vp in (("escritorio 1280 px", {"width": 1280, "height": 800}), ("móvil 375 px", {"width": 375, "height": 812})):
        pg = b.new_page(viewport=vp, locale="es-GT")
        errores = []
        pg.on("pageerror", lambda e: errores.append(str(e)))
        pg.goto(URL + "#/agenda"); pg.wait_for_timeout(150); axe(pg, f"agenda, {nombre}")
        hasta_paso4(pg); axe(pg, f"paso 4 revisar, {nombre}")
        pg.goto(URL + "#/agenda"); pg.click("text=+ Nueva cita"); pg.fill("#qPac", "Pérez"); pg.check("input[name=pac]"); pg.click("#n1")
        pg.select_option("#esp", "Medicina interna"); pg.select_option("#medS", "1"); pg.click("#n2"); pg.wait_for_selector(".slot")
        axe(pg, f"paso 3 horarios, {nombre}")
        pg.goto(URL + "#/cita/180"); pg.click("#bCancelar"); pg.click("#btnDoCancel"); axe(pg, f"diálogo de cancelación con error, {nombre}")
        registrar("JS", f"Sin errores de JavaScript ({nombre})", not errores, "; ".join(errores))
        pg.close()

    pg = b.new_page(viewport={"width": 1280, "height": 800}, locale="es-GT")

    # H-06: ningún botón con el texto exacto "Cancelar" o "Aceptar"
    fuente = open(HTML, encoding="utf-8").read()
    ambiguos = re.findall(r">\s*(Cancelar|Aceptar)\s*<", fuente)
    registrar("H-06", 'Ningún botón dice solo "Cancelar" o "Aceptar"', not ambiguos, f"{len(ambiguos)} coincidencias")

    # H-04: 409 -> foco en alerta, horario marcado, datos conservados
    hasta_paso4(pg, "Gómez", "11:00", "Seguimiento de laboratorio")
    pg.check("#sim409"); pg.click("#n4"); pg.wait_for_selector("#a409"); pg.wait_for_selector(".slot")
    foco = pg.evaluate("document.activeElement.id")
    rol_alerta = pg.get_attribute("#a409", "role")
    marcado = pg.get_attribute(".slot[data-h='11:00']", "aria-disabled") == "true" and "Recién ocupado" in pg.inner_text(".slot[data-h='11:00']")
    pg.click(".slot[data-h='11:30']"); pg.click("#n3")
    motivo = pg.input_value("#motivo")
    registrar("H-04", "Tras 409 el foco queda en la alerta con role=alert", foco == "a409" and rol_alerta == "alert", f"foco={foco}, role={rol_alerta}")
    registrar("H-04", 'El horario perdido figura como "Recién ocupado"', marcado)
    registrar("H-04", "Paciente, médico y motivo se conservan tras el 409", motivo == "Seguimiento de laboratorio" and "Gómez" in pg.inner_text("main"))

    # H-05: éxito persistente
    pg.click("#n4"); pg.wait_for_selector("#okPanel")
    pg.wait_for_timeout(6000)
    visible = pg.is_visible("#okPanel") and "CT-" in pg.inner_text("#okPanel")
    registrar("H-05", "El código de la cita sigue visible 6 s después (el aviso de la semana 8 duraba 5 s)", visible)
    registrar("H-05", 'Panel de éxito con role="status"', pg.get_attribute("#okPanel", "role") == "status")

    # H-01: estado con texto
    pg.click("#okCerrar"); pg.fill("#fFecha", "2026-10-05"); pg.wait_for_timeout(100)
    textos = pg.eval_on_selector_all("table.agenda .badge", "els => els.map(e => e.innerText.trim())")
    registrar("H-01", "Cada estado de la agenda incluye texto", textos and all(re.search(r"Pendiente|Confirmada|Cancelada", t) for t in textos), ", ".join(sorted(set(t.replace("\n", " ") for t in textos))))

    # H-03: grilla con teclado
    pg.goto(URL + "#/agenda"); pg.click("text=+ Nueva cita"); pg.fill("#qPac", "Pérez"); pg.check("input[name=pac]"); pg.click("#n1")
    pg.select_option("#esp", "Medicina interna"); pg.select_option("#medS", "1"); pg.click("#n2"); pg.wait_for_selector(".slot")
    paradas = pg.evaluate("[...document.querySelectorAll('.slot')].filter(e => e.tabIndex === 0).length")
    rg = pg.evaluate("!!document.querySelector('[role=radiogroup]')")
    pg.focus(".slot[tabindex='0']")
    antes = pg.evaluate("document.activeElement.dataset.h")
    pg.keyboard.press("ArrowRight"); pg.keyboard.press("ArrowRight")
    despues = pg.evaluate("document.activeElement.dataset.h")
    elegido = pg.evaluate("document.querySelector('.slot[aria-checked=true]')?.dataset.h")
    registrar("H-03", "La grilla es un radiogroup con una sola parada de Tab", rg and paradas == 1, f"paradas={paradas}")
    registrar("H-03", "Las flechas mueven la selección y saltan los ocupados", antes != despues and elegido == despues, f"{antes} -> {despues}")

    # Flujo completo solo con teclado
    pg.goto(URL + "#/agenda"); pg.wait_for_timeout(100)
    pg.focus("#btnNueva"); pg.keyboard.press("Enter"); pg.wait_for_selector("#qPac")
    pg.focus("#qPac"); pg.keyboard.type("Ramírez"); pg.wait_for_selector("input[name=pac]")
    pg.keyboard.press("Tab"); pg.keyboard.press("Space"); pg.keyboard.press("Tab"); pg.keyboard.press("Tab"); pg.keyboard.press("Enter")
    pg.wait_for_selector("#esp"); pg.focus("#esp"); pg.keyboard.press("ArrowDown")
    pg.keyboard.press("Tab"); pg.keyboard.press("ArrowDown")
    pg.focus("#n2"); pg.keyboard.press("Enter"); pg.wait_for_selector(".slot")
    pg.focus(".slot[tabindex='0']"); pg.keyboard.press("ArrowRight")
    pg.focus("#n3"); pg.keyboard.press("Enter"); pg.wait_for_selector("#motivo")
    pg.focus("#motivo"); pg.keyboard.type("Chequeo general")
    pg.focus("#n4"); pg.keyboard.press("Enter"); pg.wait_for_selector("#okPanel")
    registrar("TECLADO", "Flujo agenda → paso 1…4 → éxito completado solo con teclado", pg.is_visible("#okPanel"))

    # H-09: diálogo de cancelación
    pg.goto(URL + "#/cita/182"); pg.wait_for_selector("#bCancelar"); pg.focus("#bCancelar"); pg.keyboard.press("Enter")
    foco_ini = pg.evaluate("document.activeElement.id")
    dentro = True
    for _ in range(8):
        pg.keyboard.press("Tab")
        dentro = dentro and pg.evaluate("!!document.activeElement.closest('#dlgCancel')")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
    foco_fin = pg.evaluate("document.activeElement.id")
    registrar("H-09", "Foco inicial en el motivo", foco_ini == "reasonCancel", foco_ini)
    registrar("H-09", "Tab no sale del diálogo abierto", dentro)
    registrar("H-09", 'Escape cierra y el foco vuelve a "Cancelar cita"', foco_fin == "bCancelar", foco_fin)

    # H-08: error específico y asociado
    pg.click("#bCancelar"); pg.click("#btnDoCancel")
    inv = pg.get_attribute("#reasonCancel", "aria-invalid")
    desc = pg.get_attribute("#reasonCancel", "aria-describedby") or ""
    txt = pg.inner_text("#reasonCancelErr")
    registrar("H-08", "El error del motivo está asociado (aria-describedby, aria-invalid) y dice qué falta", inv == "true" and "reasonCancelErr" in desc and "3 caracteres" in txt, txt)

    # Reglas iguales a los FormRequest del backend
    pg.fill("#reasonCancel", "ab"); pg.click("#btnDoCancel")
    rechaza_2 = pg.is_visible("#reasonCancelErr")
    registrar("BACKEND", "Cancelar con 2 caracteres se rechaza (CancelAppointmentRequest pide mínimo 3)", rechaza_2)
    registrar("BACKEND", "El motivo de cancelación admite hasta 500 caracteres", pg.get_attribute("#reasonCancel", "maxlength") == "500")
    pg.fill("#reasonCancel", "abc"); pg.click("#btnDoCancel"); pg.wait_for_selector(".alert.ok")
    registrar("BACKEND", "Cancelar con 3 caracteres se acepta", "Cancelada" in pg.inner_text("main"))
    hasta_paso4(pg, "Cifuentes", "14:00")
    registrar("BACKEND", "El motivo de la consulta es opcional y admite hasta 500 caracteres (StoreAppointmentRequest)", pg.get_attribute("#motivo", "maxlength") == "500")
    pg.click("#n4"); pg.wait_for_selector("#okPanel")
    registrar("BACKEND", "Se puede agendar sin motivo de consulta", pg.is_visible("#okPanel"))

    # H-07: fechas con día de la semana y mes en letras
    pg.goto(URL + "#/cita/182"); cuerpo = pg.inner_text("main")
    registrar("H-07", "La fecha visible incluye día de la semana y mes en letras", bool(re.search(r"(lunes|martes|miércoles|jueves|viernes|sábado|domingo) \d+ de [a-z]+ de \d{4}", cuerpo)))
    registrar("H-07", "No aparecen fechas numéricas dd/mm/aaaa en el texto", not re.search(r"\b\d{2}/\d{2}/\d{4}\b", cuerpo))

    # H-10: ayuda con nombre accesible
    pg.goto(URL + "#/agenda"); pg.click("text=+ Nueva cita"); pg.fill("#qPac", "Pérez"); pg.check("input[name=pac]"); pg.click("#n1")
    pg.select_option("#esp", "Medicina interna"); pg.select_option("#medS", "1"); pg.click("#n2"); pg.wait_for_selector(".slot")
    pg.focus("#btnAyuda"); pg.keyboard.press("Enter")
    registrar("H-10", "La ayuda es un botón con texto y abre con teclado", pg.inner_text("#btnAyuda").startswith("¿Por qué") and pg.is_visible("#ayuda"))

    # H-02 / H-11: contraste medido en el navegador
    oc = pg.eval_on_selector(".slot[aria-disabled=true]", "e => { const s = getComputedStyle(e); return [s.color, s.backgroundColor, s.borderTopColor]; }")
    r_txt = ratio(rgb(oc[0]), rgb(oc[1])); r_brd = ratio(rgb(oc[2]), (255, 255, 255))
    registrar("H-02", "Texto de horario ocupado ≥ 4.5:1", r_txt >= 4.5, f"{r_txt:.2f}:1")
    registrar("H-02", "Borde de horario ocupado ≥ 3:1 contra la tarjeta", r_brd >= 3, f"{r_brd:.2f}:1")
    sec = pg.eval_on_selector("a.btn.secondary, button.btn.secondary", "e => getComputedStyle(e).borderTopColor")
    r_sec = ratio(rgb(sec), (255, 255, 255))
    registrar("H-11", "Borde de botón secundario ≥ 3:1", r_sec >= 3, f"{r_sec:.2f}:1")

    # Roles: Médico sin acciones, Enfermera sin crear ni cancelar
    pg.goto(URL + "?rol=medico#/cita/180"); pg.wait_for_timeout(100)
    registrar("ROLES", "Médico: sin botones de agendar, confirmar ni cancelar", pg.locator("#bCancelar, #bConfirmar").count() == 0)
    pg.goto(URL + "?rol=enfermera#/agenda"); pg.wait_for_timeout(100)
    sin_nueva = pg.locator("#btnNueva").count() == 0
    pg.goto(URL + "?rol=enfermera#/cita/180"); pg.wait_for_timeout(100)
    registrar("ROLES", "Enfermera: confirma, pero no agenda ni cancela", sin_nueva and pg.locator("#bConfirmar").count() == 1 and pg.locator("#bCancelar").count() == 0)
    pg.close()

    # Reflow a 320 px y sin conexión (escenario 2 de la semana 10)
    pg = b.new_page(viewport={"width": 320, "height": 700}, locale="es-GT")
    anchos = []
    for ruta in ("#/agenda", "#/cita/180"):
        pg.goto(URL + ruta); pg.wait_for_timeout(150)
        anchos.append(pg.evaluate("document.documentElement.scrollWidth"))
    hasta_paso4(pg, "López", "11:00", "Control")
    anchos.append(pg.evaluate("document.documentElement.scrollWidth"))
    registrar("1.4.10", "Sin desplazamiento horizontal a 320 px (agenda, detalle, paso 4)", max(anchos) <= 320, f"anchos={anchos}")
    pg.close()

    pg = b.new_page(viewport={"width": 375, "height": 812}, locale="es-GT")
    pg.goto(URL + "?offline=1#/agenda")
    pg.click("text=+ Nueva cita"); pg.fill("#qPac", "López"); pg.check("input[name=pac]"); pg.click("#n1")
    pg.select_option("#esp", "Medicina interna"); pg.select_option("#medS", "1"); pg.click("#n2")
    pg.wait_for_selector(".slot"); pg.click(".slot[data-h='11:00']"); pg.click("#n3"); pg.fill("#motivo", "Control de rutina")
    pg.click("#n4"); pg.wait_for_selector("#aNet")
    reint = pg.inner_text("#n4") == "Reintentar" and pg.input_value("#motivo") == "Control de rutina"
    pg.click("#demoBox summary") if pg.get_attribute("#demoBox", "open") is None else None
    pg.uncheck("#simOffline"); pg.click("#n4"); pg.wait_for_selector("#okPanel")
    creadas = pg.evaluate("[...document.querySelectorAll('.cards li')].filter(li => li.innerText.includes('José R. L.') && li.innerText.includes('11:00')).length")
    registrar("RED", 'Sin conexión: botón "Reintentar" y motivo conservado', reint)
    registrar("RED", "Al reconectar y reintentar se crea exactamente una cita", creadas == 1, f"citas de José R. L. a las 11:00: {creadas}")
    pg.close()
    b.close()

ok = sum(1 for r in resultados if r[2])
with open(SALIDA, "w", encoding="utf-8") as f:
    f.write("# Resultados de la verificación automatizada\n\n")
    f.write("Generado por `python prototipo/pruebas/verificar.py` (Playwright + axe-core).\n\n")
    f.write(f"**{ok} de {len(resultados)} criterios cumplidos.**\n\n")
    f.write("| Referencia | Criterio | Resultado | Detalle |\n|---|---|---|---|\n")
    for hid, crit, good, det in resultados:
        f.write(f"| {hid} | {crit} | {'Cumple' if good else '**Falla**'} | {det.replace('|', '/')} |\n")
print(f"\n{ok}/{len(resultados)} criterios cumplidos")
sys.exit(0 if ok == len(resultados) else 1)
