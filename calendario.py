import os
from datetime import date

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Paleta de colores profesional
COLOR_HEADER_BG = colors.HexColor('#2E8BC0')
COLOR_HEADER_TEXT = colors.white
COLOR_CELL_BG = colors.HexColor('#D0E6F6')
COLOR_CELL_BORDER = colors.HexColor('#5B9BD5')
COLOR_MARCO = colors.HexColor('#BFD7ED')
COLOR_FECHA = colors.HexColor('#145DA0')
COLOR_HORARIO = colors.HexColor('#43A6C6')
FERIADO_COLOR = colors.HexColor('#FFD700')
COLOR_PROFES = {
    "Claudia": colors.HexColor('#F18F01'),
    "Nadia":   colors.HexColor('#6DD47E'),
    "Noelia":  colors.HexColor('#0074D9'),
    "Paula":   colors.HexColor('#845EC2'),
    "Silvia":  colors.HexColor('#FF007F'),
    "3 libre": colors.HexColor('#888888'),
    "Cerrado": colors.HexColor('#B0B0B0'),
}

# Horarios especiales para días concretos de junio y julio
horarios_especiales_junio = {
    date(2025, 6, 23): [("8 a 12", "Silvia"), ("14 a 15", "Silvia"), ("17 a 21", "Claudia")],
    date(2025, 6, 24): [("8 a 12", "Noelia"), ("14 a 15", "Cerrado"), ("16 a 21", "Claudia")],
    date(2025, 6, 25): [("8 a 12", "Claudia"), ("14 a 15", "Cerrado"), ("16 a 21", "Claudia")],
    date(2025, 6, 26): [("8 a 12", "Noelia"), ("16 a 17", "Paula"), ("18 a 21", "Paula")],
    date(2025, 6, 27): [("8 a 12", "Claudia"), ("16 a 21", "Paula")],
    date(2025, 6, 30): [("8 a 12", "Claudia"), ("14 a 15", "Cerrado"), ("17 a 21", "Nadia")],
}

horarios_especiales_julio = {
    date(2025, 7, 3): [("8 a 12", "Noelia"), ("16 a 17", "Paula"), ("18 a 21", "Paula")],
    date(2025, 7, 7): [("8 a 12", "Claudia"), ("17 a 21", "Nadia")],
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

# Horario estándar por día de la semana
HORARIO_SEMANA = {
    "Lunes":     {"mañana": "Claudia", "tarde": "Nadia"},
    "Martes":    {"mañana": "Noelia",  "tarde": "Claudia"},
    "Miércoles": {"mañana": "Claudia", "tarde": "Nadia"},
    "Jueves":    {"mañana": "Noelia",  "tarde": "Paula"},
    "Viernes":   {"mañana": "Claudia", "tarde": "Paula"},
}
HORARIO_TARDE = "16 a 21"

WEEKDAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]


def generar_calendario_combinado(nombre_pdf):
    c = canvas.Canvas(nombre_pdf, pagesize=A4)
    width, height = A4
    margin = 40
    cell_height = 80
    cell_padding = 10
    start_y = height - margin

    # Marco y cabecera
    c.setStrokeColor(COLOR_MARCO)
    c.setLineWidth(4)
    c.roundRect(margin/2, margin/2, width - margin,
                height - margin, 30, fill=0, stroke=1)
    c.setLineWidth(1)
    titulo = "Calendario Profes Junio y Julio 2025"
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
    # Encabezado de días
    c.setFillColor(COLOR_HEADER_BG)
    c.roundRect(margin, start_y - 30, width - 2 *
                margin, 30, 12, fill=1, stroke=0)
    c.setFillColor(COLOR_HEADER_TEXT)
    c.setFont("Helvetica-Bold", 13)
    for i, dia in enumerate(WEEKDAYS):
        x = margin + i * day_width
        c.drawCentredString(x + day_width / 2, start_y - 12, dia)
    start_y -= 40

    # Fechas: 23/06 al 30/06 y todo julio (lunes a viernes)
    fechas = [date(2025, 6, d)
              for d in range(23, 31) if date(2025, 6, d).weekday() < 5]
    fechas += [date(2025, 7, d)
               for d in range(1, 32) if date(2025, 7, d).weekday() < 5]
    semanas = [fechas[i:i+5] for i in range(0, len(fechas), 5)]

    for row, week in enumerate(semanas):
        y = start_y - row * cell_height
        for i, fecha in enumerate(week):
            x = margin + i * day_width
            # Fondo de celda y feriados
            if fecha == date(2025, 6, 20) or fecha == date(2025, 7, 9):
                c.setFillColor(FERIADO_COLOR)
            else:
                c.setFillColor(COLOR_CELL_BG)
            c.roundRect(x, y - cell_height + cell_padding, day_width - 4,
                        cell_height - cell_padding, 12, fill=1, stroke=0)
            c.setStrokeColor(COLOR_CELL_BORDER)
            c.setLineWidth(2)
            c.roundRect(x, y - cell_height + cell_padding, day_width - 4,
                        cell_height - cell_padding, 12, fill=0, stroke=1)
            c.setLineWidth(1)
            center_x = x + (day_width - 4) / 2
            # Fecha
            c.setFont("Helvetica-Bold", 13)
            c.setFillColor(COLOR_FECHA)
            c.drawCentredString(
                center_x, y - 20, f"{fecha.day:02d}/{fecha.month:02d}")
            # Horarios especiales o estándar
            if fecha in horarios_especiales_junio:
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
                        c.drawRightString(x + day_width - 14, y_horario, profe)
                    y_horario -= 14
            elif fecha in horarios_especiales_julio:
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
                        c.drawRightString(x + day_width - 14, y_horario, profe)
                    y_horario -= 14
            else:
                dia_str = WEEKDAYS[i]
                c.setFont("Helvetica-Bold", 10)
                c.setFillColor(COLOR_HORARIO)
                c.drawString(x + 14, y - 38, "8 a 12:")
                profe_manana = HORARIO_SEMANA[dia_str]["mañana"]
                font_size_manana = 11
                while c.stringWidth(profe_manana, "Helvetica-Bold", font_size_manana) > (day_width/2 - 20) and font_size_manana > 7:
                    font_size_manana -= 1
                c.setFont("Helvetica-Bold", font_size_manana)
                c.setFillColor(COLOR_PROFES[profe_manana])
                c.drawRightString(x + day_width - 14, y - 38, profe_manana)
                c.setFont("Helvetica-Bold", 10)
                c.setFillColor(COLOR_HORARIO)
                c.drawString(x + 14, y - 62, HORARIO_TARDE + ":")
                profe_tarde = HORARIO_SEMANA[dia_str]["tarde"]
                font_size_tarde = 11
                while c.stringWidth(profe_tarde, "Helvetica-Bold", font_size_tarde) > (day_width/2 - 20) and font_size_tarde > 7:
                    font_size_tarde -= 1
                c.setFont("Helvetica-Bold", font_size_tarde)
                c.setFillColor(COLOR_PROFES[profe_tarde])
                c.drawRightString(x + day_width - 14, y - 62, profe_tarde)
    c.save()
    print(f"✅ PDF generado: {nombre_pdf}")
    try:
        os.startfile(nombre_pdf)
        print(f"Abriendo {nombre_pdf}...")
    except Exception as e:
        print(f"No se pudo abrir el PDF automáticamente: {e}")


if __name__ == "__main__":
    generar_calendario_combinado("calendario_profes_junio_julio_2025.pdf")
