from datetime import date, timedelta

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Paleta de colores profesional
COLOR_HEADER_BG = colors.HexColor('#2E8BC0')  # Azul encabezado
COLOR_HEADER_TEXT = colors.white
COLOR_CELL_BG = colors.HexColor('#F6FAFD')    # Fondo uniforme celdas
COLOR_CELL_BORDER = colors.HexColor('#A1C6EA')
COLOR_MARCO = colors.HexColor('#BFD7ED')      # Marco suave
COLOR_FECHA = colors.HexColor('#145DA0')      # Fecha
COLOR_HORARIO = colors.HexColor('#43A6C6')    # Horario
COLOR_PROFES = {
    "Claudia": colors.HexColor('#F18F01'),   # Naranja
    "Nadia":   colors.HexColor('#6DD47E'),   # Verde
    "Noelia":  colors.HexColor('#F6416C'),   # Rosa
    "Paula":   colors.HexColor('#845EC2'),   # Violeta
}

c = canvas.Canvas("calendario_pilates_julio_2025_completo.pdf", pagesize=A4)
width, height = A4

margin = 40
cell_height = 80
cell_padding = 10
start_y = height - margin

# Marco suave alrededor de todo el calendario
c.setStrokeColor(COLOR_MARCO)
c.setLineWidth(4)
c.roundRect(margin/2, margin/2, width - margin,
            height - margin, 18, fill=0, stroke=1)
c.setLineWidth(1)

# Título con fondo
c.setFillColor(COLOR_HEADER_BG)
c.rect(margin, start_y - 50, width - 2*margin, 50, fill=1, stroke=0)
c.setFillColor(COLOR_HEADER_TEXT)
c.setFont("Helvetica-Bold", 22)
c.drawCentredString(width / 2, start_y - 20, "Calendario Pilates Julio 2025")
start_y -= 70

day_width = (width - 2 * margin) / 5
weekdays = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
horario = {
    "Lunes":     {"mañana": "Claudia", "tarde": "Nadia"},
    "Martes":    {"mañana": "Noelia",  "tarde": "Claudia"},
    "Miércoles": {"mañana": "Claudia", "tarde": "Nadia"},
    "Jueves":    {"mañana": "Noelia",  "tarde": "Paula"},
    "Viernes":   {"mañana": "Claudia", "tarde": "Paula"},
}

# Encabezado de días con fondo uniforme
c.setFillColor(COLOR_HEADER_BG)
c.roundRect(margin, start_y - 30, width - 2 * margin, 30, 8, fill=1, stroke=0)
c.setFillColor(COLOR_HEADER_TEXT)
c.setFont("Helvetica-Bold", 13)
for i, dia in enumerate(weekdays):
    x = margin + i * day_width
    c.drawCentredString(x + day_width / 2, start_y - 12, dia)
start_y -= 40

current = date(2025, 7, 1)
end = date(2025, 7, 31)
row = 0
week = []

while current <= end:
    if current.weekday() < 5:
        week.append((current, weekdays[current.weekday()]))
    if len(week) == 5 or (current == end and week):
        y = start_y - row * cell_height
        for i, (fecha, dia_str) in enumerate(week):
            x = margin + i * day_width
            # Fondo uniforme de celda
            c.setFillColor(COLOR_CELL_BG)
            c.roundRect(x, y - cell_height + cell_padding, day_width -
                        4, cell_height - cell_padding, 8, fill=1, stroke=0)
            # Borde celda
            c.setStrokeColor(COLOR_CELL_BORDER)
            c.roundRect(x, y - cell_height + cell_padding, day_width -
                        4, cell_height - cell_padding, 8, fill=0, stroke=1)
            # Fecha
            c.setFont("Helvetica-Bold", 13)
            c.setFillColor(COLOR_FECHA)
            c.drawString(x + 12, y - 20, f"{fecha.day}/07")
            # Horario mañana
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(COLOR_HORARIO)
            c.drawString(x + 12, y - 38, "8 a 12:")
            c.setFont("Helvetica", 10)
            profe_manana = horario[dia_str]["mañana"]
            c.setFillColor(COLOR_PROFES[profe_manana])
            c.drawString(x + 70, y - 38, profe_manana)
            # Horario tarde
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(COLOR_HORARIO)
            c.drawString(x + 12, y - 56, "16 a 20:")
            c.setFont("Helvetica", 10)
            profe_tarde = horario[dia_str]["tarde"]
            c.setFillColor(COLOR_PROFES[profe_tarde])
            c.drawString(x + 70, y - 56, profe_tarde)
        row += 1
        # Separador visual entre semanas
        c.setStrokeColor(COLOR_HEADER_BG)
        c.setLineWidth(1.2)
        c.line(margin, y - cell_height + cell_padding - 6,
               width - margin, y - cell_height + cell_padding - 6)
        c.setLineWidth(1)
        # Salto de página si se llena
        if start_y - row * cell_height < margin + cell_height:
            c.showPage()
            start_y = height - margin
            # Marco en cada página
            c.setStrokeColor(COLOR_MARCO)
            c.setLineWidth(4)
            c.roundRect(margin/2, margin/2, width - margin,
                        height - margin, 18, fill=0, stroke=1)
            c.setLineWidth(1)
            # Repetir encabezado
            c.setFillColor(COLOR_HEADER_BG)
            c.rect(margin, start_y - 50, width -
                   2*margin, 50, fill=1, stroke=0)
            c.setFillColor(COLOR_HEADER_TEXT)
            c.setFont("Helvetica-Bold", 22)
            c.drawCentredString(width / 2, start_y - 20,
                                "Calendario Pilates Julio 2025 (cont.)")
            start_y -= 70
            c.setFillColor(COLOR_HEADER_BG)
            c.roundRect(margin, start_y - 30, width - 2 *
                        margin, 30, 8, fill=1, stroke=0)
            c.setFillColor(COLOR_HEADER_TEXT)
            c.setFont("Helvetica-Bold", 13)
            for i, dia in enumerate(weekdays):
                x = margin + i * day_width
                c.drawCentredString(x + day_width / 2, start_y - 12, dia)
            start_y -= 40
            row = 0
        week = []
    current += timedelta(days=1)

c.save()
print("✅ PDF generado: calendario_pilates_julio_2025_completo.pdf")
