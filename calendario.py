from datetime import date, timedelta

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Paleta de colores moderna
COLOR_HEADER_BG = colors.HexColor('#2E8BC0')  # Azul moderno
COLOR_HEADER_TEXT = colors.white
COLOR_CELL_BG_1 = colors.HexColor('#F1F6FB')  # Celda clara
COLOR_CELL_BG_2 = colors.HexColor('#D3EAF2')  # Celda alterna
COLOR_CELL_BORDER = colors.HexColor('#A1C6EA')
COLOR_FECHA = colors.HexColor('#2E8BC0')
COLOR_HORARIO = colors.HexColor('#145DA0')
COLOR_PROFE_MANANA = colors.HexColor('#F18F01')  # Naranja para mañana
COLOR_PROFE_TARDE = colors.HexColor('#6DD47E')   # Verde para tarde

c = canvas.Canvas("calendario_pilates_julio_2025_completo.pdf", pagesize=A4)
width, height = A4

margin = 40
cell_height = 80  # Más alto para separar renglones
cell_padding = 10
start_y = height - margin

# Título con fondo (más espacio arriba)
c.setFillColor(COLOR_HEADER_BG)
c.rect(0, start_y - 50, width, 50, fill=1, stroke=0)
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

# Encabezado de días con fondo
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
            # Alternar color de fondo
            cell_bg = COLOR_CELL_BG_1 if (row % 2 == 0) else COLOR_CELL_BG_2
            c.setFillColor(cell_bg)
            c.roundRect(x, y - cell_height + cell_padding, day_width -
                        4, cell_height - cell_padding, 8, fill=1, stroke=0)
            # Borde
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
            c.setFillColor(COLOR_PROFE_MANANA)
            c.drawString(x + 70, y - 38, horario[dia_str]["mañana"])
            # Horario tarde
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(COLOR_HORARIO)
            c.drawString(x + 12, y - 56, "16 a 20:")
            c.setFont("Helvetica", 10)
            c.setFillColor(COLOR_PROFE_TARDE)
            c.drawString(x + 70, y - 56, horario[dia_str]["tarde"])
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
            # Repetir encabezado
            c.setFillColor(COLOR_HEADER_BG)
            c.rect(0, start_y - 50, width, 50, fill=1, stroke=0)
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
