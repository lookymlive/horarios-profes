import os
from calendar import monthrange
from datetime import date, timedelta

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Paleta de colores profesional
COLOR_HEADER_BG = colors.HexColor('#2E8BC0')  # Azul encabezado
COLOR_HEADER_TEXT = colors.white
COLOR_CELL_BG = colors.HexColor('#D0E6F6')    # Fondo celda menos claro
COLOR_CELL_BORDER = colors.HexColor('#5B9BD5')  # Borde celda más visible
COLOR_MARCO = colors.HexColor('#BFD7ED')      # Marco suave
COLOR_FECHA = colors.HexColor('#145DA0')      # Fecha
COLOR_HORARIO = colors.HexColor('#43A6C6')    # Horario
COLOR_SEP_SEMANA = colors.HexColor('#2E8BC0')  # Separador semana
COLOR_PROFES = {
    "Claudia": colors.HexColor('#F18F01'),   # Naranja
    "Nadia":   colors.HexColor('#6DD47E'),   # Verde
    "Noelia":  colors.HexColor('#0074D9'),   # Azul diferente
    "Paula":   colors.HexColor('#845EC2'),   # Violeta
    "Silvia":  colors.HexColor('#FF007F'),   # Fucsia llamativo
    "3 libre": colors.HexColor('#888888'),   # Gris para libre
}
COLOR_PROFES["Cerrado"] = colors.HexColor('#B0B0B0')
FERIADO_COLOR = colors.HexColor('#FFD700')  # Amarillo para feriado

# Horarios especiales para la semana del 21 al 25 de julio 2025 (de la imagen)
horarios_especiales = {
    date(2025, 7, 21): [
        ("8 a 12", "3 libre"),
        ("14 a 15", "3 libre"),
        ("16 a 20", "Nadia"),
    ],
    date(2025, 7, 22): [
        ("8 a 12", "Noelia"),
        ("14 a 15", ""),
        ("16 a 20", "Silvia"),
    ],
    date(2025, 7, 23): [
        ("8 a 12", "Silvia"),
        ("14 a 15", "Silvia"),
        ("16 a 20", "Silvia"),
    ],
    date(2025, 7, 24): [
        ("8 a 12", "Noelia"),
        ("14 a 15", ""),
        ("16 a 20", "Paula"),
    ],
    date(2025, 7, 25): [
        ("8 a 12", "Claudia"),
        ("16 a 20", "Paula"),
        ("20 a 21", "Silvia"),
    ],
}

# Horarios especiales para la segunda quincena de junio y la última semana de julio (de las imágenes)
horarios_especiales_junio = {
    date(2025, 6, 16): [("8 a 12", "Silvia"), ("14 a 15", "Silvia"), ("17 a 21", "Nadia")],
    date(2025, 6, 17): [("8 a 12", "Noelia"), ("14 a 15", "Silvia"), ("16 a 21", "Silvia")],
    date(2025, 6, 18): [("8 a 12", "Silvia"), ("14 a 15", "Silvia"), ("16 a 21", "Silvia")],
    date(2025, 6, 19): [("8 a 12", "Noelia"), ("14 a 15", "Silvia"), ("16 a 21", "Paula")],
    date(2025, 6, 20): [("8 a 12", "Claudia"), ("16 a 21", "Paula")],
    date(2025, 6, 23): [("8 a 12", "Silvia"), ("14 a 15", "Silvia"), ("17 a 21", "Nadia")],
    date(2025, 6, 24): [("8 a 12", "Noelia"), ("14 a 15", "Cerrado"), ("16 a 21", "Claudia")],
    date(2025, 6, 25): [("8 a 12", "Claudia"), ("14 a 15", "Cerrado"), ("16 a 21", "Nadia")],
    date(2025, 6, 26): [("8 a 12", "Noelia"), ("14 a 15", "Cerrado"), ("16 a 21", "Paula")],
    date(2025, 6, 27): [("8 a 12", "Claudia"), ("16 a 21", "Paula")],
    date(2025, 6, 30): [("8 a 12", "Claudia"), ("14 a 15", "Cerrado"), ("17 a 21", "Nadia")],
}

horarios_especiales_julio = {
    date(2025, 7, 7): [("8 a 12", "Claudia"), ("17 a 21", "Nadia")],
    date(2025, 7, 14): [("8 a 12", "Claudia"), ("17 a 21", "Nadia")],
    date(2025, 7, 21): [("8 a 12", "Claudia"), ("17 a 21", "Nadia")],
    date(2025, 7, 22): [("8 a 12", "Noelia"), ("14 a 15", "Silvia"), ("16 a 21", "Silvia")],
    date(2025, 7, 23): [("8 a 12", "Silvia"), ("14 a 15", "Silvia"), ("16 a 21", "Silvia")],
    date(2025, 7, 24): [("8 a 12", "Noelia"), ("14 a 15", "Silvia"), ("16 a 21", "Paula")],
    date(2025, 7, 25): [("8 a 12", "Claudia"), ("16 a 20", "Paula"), ("20 a 21", "Silvia")],
    date(2025, 7, 28): [("8 a 12", "Silvia"), ("14 a 15", "Silvia"), ("17 a 21", "Nadia")],
    date(2025, 7, 29): [("8 a 12", "Noelia"), ("14 a 15", "Silvia"), ("16 a 21", "Silvia")],
    date(2025, 7, 30): [("8 a 12", "Silvia"), ("14 a 15", "Silvia"), ("16 a 21", "Silvia")],
    date(2025, 7, 31): [("8 a 12", "Claudia"), ("16 a 21", "Paula")],
}

# --- GENERADOR DE CALENDARIO ---


def generar_calendario(nombre_pdf, mes, anio, titulo):
    c = canvas.Canvas(nombre_pdf, pagesize=A4)
    width, height = A4
    margin = 40
    cell_height = 80
    cell_padding = 10
    start_y = height - margin

    # Marco suave alrededor de todo el calendario (más redondeado)
    c.setStrokeColor(COLOR_MARCO)
    c.setLineWidth(4)
    c.roundRect(margin/2, margin/2, width - margin,
                height - margin, 30, fill=0, stroke=1)
    c.setLineWidth(1)

    # Título con fondo y marco redondeado
    titulo_y = start_y - 60
    c.setFillColor(COLOR_HEADER_BG)
    c.roundRect(margin, titulo_y, width - 2*margin, 60, 20, fill=1, stroke=0)
    c.setFillColor(COLOR_HEADER_TEXT)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2, start_y - 22, titulo)
    c.setFont("Helvetica", 13)
    c.drawCentredString(width / 2, start_y - 42,
                        "SILVIA FERNANDEZ Pilates Reformer")
    start_y -= 80

    day_width = (width - 2 * margin) / 5
    weekdays = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    horario = {
        "Lunes":     {"mañana": "Claudia", "tarde": "Nadia"},
        "Martes":    {"mañana": "Noelia",  "tarde": "Claudia"},
        "Miércoles": {"mañana": "Claudia", "tarde": "Nadia"},
        "Jueves":    {"mañana": "Noelia",  "tarde": "Paula"},
        "Viernes":   {"mañana": "Claudia", "tarde": "Paula"},
    }
    horario_tarde = "16 a 21"

    # Encabezado de días con fondo uniforme y marco redondeado
    c.setFillColor(COLOR_HEADER_BG)
    c.roundRect(margin, start_y - 30, width - 2 *
                margin, 30, 12, fill=1, stroke=0)
    c.setFillColor(COLOR_HEADER_TEXT)
    c.setFont("Helvetica-Bold", 13)
    for i, dia in enumerate(weekdays):
        x = margin + i * day_width
        c.drawCentredString(x + day_width / 2, start_y - 12, dia)
    start_y -= 40

    # Generar la matriz de semanas (lunes a viernes) para el mes
    first_day = date(anio, mes, 1)
    last_day = date(anio, mes, monthrange(anio, mes)[1])
    # Buscar el primer lunes antes o igual al primer día del mes
    first_monday = first_day
    while first_monday.weekday() != 0:
        first_monday -= timedelta(days=1)
    # Si es junio, empezar desde el 16/06
    if mes == 6:
        first_monday = date(anio, mes, 16)
        while first_monday.weekday() != 0:
            first_monday -= timedelta(days=1)
    # Construir la matriz de semanas
    weeks = []
    week = []
    current = first_monday
    while True:
        if current >= first_day and current <= last_day and current.weekday() < 5:
            week.append(current)
        elif current < first_day and current.weekday() < 5:
            week.append(None)
        elif current > last_day and current.weekday() < 5:
            week.append(None)
        if len(week) == 5:
            weeks.append(week)
            week = []
        # Condición de corte: si ya pasamos el último viernes del mes
        if current > last_day and current.weekday() == 4:
            break
        current += timedelta(days=1)
    # Dibujar las semanas
    for row, week in enumerate(weeks):
        y = start_y - row * cell_height
        for i, fecha in enumerate(week):
            x = margin + i * day_width
            # Fondo de celda menos claro y marco redondeado
            if mes == 6 and (fecha == date(2025, 6, 16) or fecha == date(2025, 6, 20)):
                c.setFillColor(FERIADO_COLOR)
            else:
                c.setFillColor(COLOR_CELL_BG)
            c.roundRect(x, y - cell_height + cell_padding, day_width - 4,
                        cell_height - cell_padding, 12, fill=1, stroke=0)
            # Marco/borde de cada día
            c.setStrokeColor(COLOR_CELL_BORDER)
            c.setLineWidth(2)
            c.roundRect(x, y - cell_height + cell_padding, day_width - 4,
                        cell_height - cell_padding, 12, fill=0, stroke=1)
            c.setLineWidth(1)
            center_x = x + (day_width - 4) / 2
            if fecha:
                # Fecha centrada
                c.setFont("Helvetica-Bold", 13)
                c.setFillColor(COLOR_FECHA)
                c.drawCentredString(
                    center_x, y - 20, f"{fecha.day:02d}/{mes:02d}")
                # Si es semana especial, usar los horarios de la imagen
                if mes == 6 and fecha in horarios_especiales_junio:
                    horarios_dia = horarios_especiales_junio[fecha]
                    y_horario = y - 38
                    for hora, profe in horarios_dia:
                        c.setFont("Helvetica-Bold", 10)
                        c.setFillColor(COLOR_HORARIO)
                        c.drawString(x + 14, y_horario, hora + ":")
                        if profe:
                            font_size = 11
                            while c.stringWidth(profe, "Helvetica-Bold", font_size) > (day_width/2 - 20) and font_size > 7:
                                font_size -= 1
                            c.setFont("Helvetica-Bold", font_size)
                            color = COLOR_PROFES.get(profe, colors.black)
                            c.setFillColor(color)
                            c.drawRightString(
                                x + day_width - 14, y_horario, profe)
                        y_horario -= 14
                elif mes == 7 and fecha in horarios_especiales_julio:
                    horarios_dia = horarios_especiales_julio[fecha]
                    y_horario = y - 38
                    for hora, profe in horarios_dia:
                        c.setFont("Helvetica-Bold", 10)
                        c.setFillColor(COLOR_HORARIO)
                        c.drawString(x + 14, y_horario, hora + ":")
                        if profe:
                            font_size = 11
                            while c.stringWidth(profe, "Helvetica-Bold", font_size) > (day_width/2 - 20) and font_size > 7:
                                font_size -= 1
                            c.setFont("Helvetica-Bold", font_size)
                            color = COLOR_PROFES.get(profe, colors.black)
                            c.setFillColor(color)
                            c.drawRightString(
                                x + day_width - 14, y_horario, profe)
                        y_horario -= 14
                else:
                    dia_str = weekdays[i]
                    # Horario mañana a la izquierda, nombre a la derecha
                    c.setFont("Helvetica-Bold", 10)
                    c.setFillColor(COLOR_HORARIO)
                    c.drawString(x + 14, y - 38, "8 a 12:")
                    profe_manana = horario[dia_str]["mañana"]
                    font_size_manana = 11
                    while c.stringWidth(profe_manana, "Helvetica-Bold", font_size_manana) > (day_width/2 - 20) and font_size_manana > 7:
                        font_size_manana -= 1
                    c.setFont("Helvetica-Bold", font_size_manana)
                    c.setFillColor(COLOR_PROFES[profe_manana])
                    c.drawRightString(x + day_width - 14, y - 38, profe_manana)
                    # Horario tarde a la izquierda, nombre a la derecha
                    c.setFont("Helvetica-Bold", 10)
                    c.setFillColor(COLOR_HORARIO)
                    c.drawString(x + 14, y - 62, horario_tarde + ":")
                    profe_tarde = horario[dia_str]["tarde"]
                    font_size_tarde = 11
                    while c.stringWidth(profe_tarde, "Helvetica-Bold", font_size_tarde) > (day_width/2 - 20) and font_size_tarde > 7:
                        font_size_tarde -= 1
                    c.setFont("Helvetica-Bold", font_size_tarde)
                    c.setFillColor(COLOR_PROFES[profe_tarde])
                    c.drawRightString(x + day_width - 14, y - 62, profe_tarde)
            else:
                # Celda vacía
                pass
    # Sección de anotaciones si hay espacio
    anotaciones_y = start_y - len(weeks) * cell_height - 30
    if anotaciones_y > margin + 100:
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(COLOR_HEADER_BG)
        c.drawString(margin, anotaciones_y, "Anotaciones:")
        c.setStrokeColor(COLOR_CELL_BORDER)
        c.setLineWidth(1)
        for i in range(7):
            y_line = anotaciones_y - 18 - i*18
            c.line(margin, y_line, width - margin, y_line)
    c.save()
    print(f"✅ PDF generado: {nombre_pdf}")
    try:
        os.startfile(nombre_pdf)
        print(f"Abriendo {nombre_pdf}...")
    except Exception as e:
        print(f"No se pudo abrir el PDF automáticamente: {e}")


# Generar calendario de JUNIO y JULIO 2025 correctamente
generar_calendario(
    "calendario_pilates_junio_2025_completo.pdf",
    6, 2025,
    "Calendario Pilates Junio 2025"
)
generar_calendario(
    "calendario_pilates_julio_2025_completo.pdf",
    7, 2025,
    "Calendario Pilates Julio 2025"
)
