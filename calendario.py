import os
from datetime import date, timedelta

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ==============================================================================
# CONFIGURACIÓN
# ==============================================================================

# --- Paleta de Colores ---
COLOR_HEADER_BG = colors.HexColor('#2E8BC0')
COLOR_HEADER_TEXT = colors.white
COLOR_CELL_BG = colors.HexColor('#D0E6F6')
COLOR_CELL_BORDER = colors.HexColor('#5B9BD5')
COLOR_MARCO = colors.HexColor('#BFD7ED')
COLOR_FECHA = colors.HexColor('#145DA0')
COLOR_HORARIO = colors.HexColor('#43A6C6')
FERIADO_COLOR = colors.HexColor('#FFD700')

# --- Colores de Profesoras ---
COLOR_PROFES = {
    "Claudia": colors.HexColor('#F18F01'),
    "Nadia":   colors.HexColor('#6DD47E'),
    "Noelia":  colors.HexColor('#0074D9'),
    "Paula":   colors.HexColor('#845EC2'),
    "Silvia":  colors.HexColor('#FF007F'),
    "3 libre": colors.HexColor('#888888'),
    "Cerrado": colors.HexColor('#B0B0B0'),
}

# --- Horario Estándar (Lunes a Viernes) ---
# Mañana: 8 a 12 hs
# Tarde: 16 a 21 hs
HORARIO_SEMANA = {
    "Lunes":     {"mañana": "Claudia", "tarde": "Nadia"},
    "Martes":    {"mañana": "Noelia",  "tarde": "Claudia"},
    "Miércoles": {"mañana": "Claudia", "tarde": "Nadia"},
    "Jueves":    {"mañana": "Noelia",  "tarde": "Paula"},
    "Viernes":   {"mañana": "Claudia", "tarde": "Paula"},
}
HORARIO_TARDE_DEFAULT = "16 a 21"

# --- Horarios Especiales ---
# Aquí puedes añadir o modificar fechas con horarios que no siguen el estándar.
# Formato: date(AÑO, MES, DIA): [("HORA_INICIO a HORA_FIN", "PROFESORA"), ...]
HORARIOS_ESPECIALES = {
    date(2025, 7, 7): [("8 a 12", "Claudia"), ("17 a 21", "Nadia")],
    date(2025, 7, 9): [("Feriado", "Cerrado")], # Feriado 9 de Julio
    date(2025, 7, 10): [("8 a 12", "Noelia"), ("16 a 17", "Paula"), ("18 a 21", "Paula")],
    date(2025, 7, 14): [("8 a 12", "Claudia"), ("17 a 21", "Nadia")],
    date(2025, 7, 17): [("8 a 12", "Noelia"), ("16 a 17", "Paula"), ("18 a 21", "Paula")],
    date(2025, 7, 21): [("8 a 12", "Claudia"), ("17 a 21", "Nadia")],
    date(2025, 7, 22): [("8 a 12", "Noelia"), ("14 a 15", "Silvia"), ("16 a 21", "Silvia")],
    date(2025, 7, 23): [("8 a 12", "Silvia"), ("14 a 15", "Silvia"), ("16 a 21", "Silvia")],
    date(2025, 7, 24): [("8 a 12", "Noelia"), ("16 a 17", "Paula"), ("18 a 21", "Paula")],
    date(2025, 7, 25): [("8 a 12", "Claudia"), ("16 a 20", "Paula"), ("20 a 21", "Silvia")],
    date(2025, 7, 28): [("8 a 12", "Silvia"), ("14 a 15", "Silvia"), ("17 a 21", "Nadia")],
    date(2025, 7, 29): [("8 a 12", "Noelia"), ("14 a 15", "Silvia"), ("16 a 21", "Silvia")],
    date(2025, 7, 30): [("8 a 12", "Silvia"), ("14 a 15", "Silvia"), ("16 a 21", "Silvia")],
    date(2025, 7, 31): [("8 a 12", "Noelia"), ("16 a 17", "Paula"), ("18 a 21", "Paula")],
}

# --- Constantes del Calendario ---
WEEKDAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
NOMBRE_PDF_SALIDA = "calendario_profes_julio_2025_actualizado.pdf"

# ==============================================================================
# LÓGICA DE GENERACIÓN DEL PDF
# ==============================================================================

def draw_centered_text(c, text, center_x, y, font_name, font_size, color):
    """Dibuja texto centrado horizontalmente."""
    c.setFont(font_name, font_size)
    c.setFillColor(color)
    c.drawCentredString(center_x, y, text)

def draw_schedule(c, x, y, day_width, horarios):
    """Dibuja los horarios para un día específico."""
    y_horario = y - 38
    for hora, profe in horarios:
        # Dibuja la hora
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(COLOR_HORARIO)
        c.drawString(x + 14, y_horario, hora + ":")

        # Dibuja el nombre de la profesora
        if profe:
            font_size = 11
            # Ajusta el tamaño de la fuente si el nombre es muy largo
            while c.stringWidth(profe, "Helvetica-Bold", font_size) > (day_width / 2 - 10) and font_size > 7:
                font_size -= 1
            c.setFont("Helvetica-Bold", font_size)
            color_profe = COLOR_PROFES.get(profe, colors.black)
            c.setFillColor(color_profe)
            c.drawRightString(x + day_width - 14, y_horario, profe)
        y_horario -= 14


def generar_calendario(nombre_pdf):
    """Genera el calendario en formato PDF."""
    c = canvas.Canvas(nombre_pdf, pagesize=A4)
    width, height = A4
    margin = 40
    cell_height = 80
    cell_padding = 10
    start_y = height - margin

    # --- Dibuja el Marco y la Cabecera ---
    c.setStrokeColor(COLOR_MARCO)
    c.setLineWidth(4)
    c.roundRect(margin / 2, margin / 2, width - margin, height - margin, 30, fill=0, stroke=1)
    c.setLineWidth(1)

    titulo = "Calendario Profes - Julio 2025"
    titulo_y = start_y - 60
    c.setFillColor(COLOR_HEADER_BG)
    c.roundRect(margin, titulo_y, width - 2 * margin, 60, 20, fill=1, stroke=0)
    draw_centered_text(c, titulo, width / 2, start_y - 22, "Helvetica-Bold", 22, COLOR_HEADER_TEXT)
    draw_centered_text(c, "SILVIA FERNANDEZ Pilates Reformer", width / 2, start_y - 42, "Helvetica", 13, COLOR_HEADER_TEXT)
    start_y -= 80

    # --- Dibuja los Nombres de los Días ---
    day_width = (width - 2 * margin) / 5
    c.setFillColor(COLOR_HEADER_BG)
    c.roundRect(margin, start_y - 30, width - 2 * margin, 30, 12, fill=1, stroke=0)
    c.setFillColor(COLOR_HEADER_TEXT)
    for i, dia in enumerate(WEEKDAYS):
        x = margin + i * day_width
        draw_centered_text(c, dia, x + day_width / 2, start_y - 12, "Helvetica-Bold", 13, COLOR_HEADER_TEXT)
    start_y -= 40

    # --- Genera las Fechas para el Calendario ---
    # Empezamos desde el 7 de julio y continuamos hasta fin de mes
    fechas = []
    d = date(2025, 7, 7)
    while d.month == 7:
        if d.weekday() < 5: # Lunes a Viernes
            fechas.append(d)
        d += timedelta(days=1)

    semanas = [fechas[i:i + 5] for i in range(0, len(fechas), 5)]

    # --- Dibuja las Celdas del Calendario ---
    for row, week in enumerate(semanas):
        y = start_y - row * cell_height
        for i, fecha in enumerate(week):
            x = margin + i * day_width
            center_x = x + (day_width - 4) / 2

            # --- Fondo de la Celda ---
            is_feriado = fecha in HORARIOS_ESPECIALES and HORARIOS_ESPECIALES[fecha][0][0] == "Feriado"
            cell_color = FERIADO_COLOR if is_feriado else COLOR_CELL_BG
            c.setFillColor(cell_color)
            c.roundRect(x, y - cell_height + cell_padding, day_width - 4, cell_height - cell_padding, 12, fill=1, stroke=0)
            c.setStrokeColor(COLOR_CELL_BORDER)
            c.setLineWidth(2)
            c.roundRect(x, y - cell_height + cell_padding, day_width - 4, cell_height - cell_padding, 12, fill=0, stroke=1)
            c.setLineWidth(1)

            # --- Dibuja la Fecha ---
            draw_centered_text(c, f"{fecha.day:02d}/{fecha.month:02d}", center_x, y - 20, "Helvetica-Bold", 13, COLOR_FECHA)

            # --- Dibuja los Horarios ---
            if fecha in HORARIOS_ESPECIALES:
                horarios_dia = HORARIOS_ESPECIALES[fecha]
                # Si es feriado, solo muestra "Cerrado"
                if is_feriado:
                     draw_centered_text(c, "Cerrado", center_x, y - 45, "Helvetica-Bold", 14, COLOR_PROFES["Cerrado"])
                else:
                    draw_schedule(c, x, y, day_width, horarios_dia)
            else:
                dia_semana_str = WEEKDAYS[fecha.weekday()]
                horario_estandar = [
                    ("8 a 12", HORARIO_SEMANA[dia_semana_str]["mañana"]),
                    (HORARIO_TARDE_DEFAULT, HORARIO_SEMANA[dia_semana_str]["tarde"])
                ]
                draw_schedule(c, x, y, day_width, horario_estandar)

    c.save()
    print(f"✅ PDF generado: {nombre_pdf}")
    try:
        os.startfile(nombre_pdf)
        print(f"Abriendo {nombre_pdf}...")
    except Exception as e:
        print(f"No se pudo abrir el PDF automáticamente: {e}")


if __name__ == "__main__":
    generar_calendario(NOMBRE_PDF_SALIDA)