from datetime import date, timedelta

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Crear PDF
c = canvas.Canvas("calendario_pilates_julio_2025_completo.pdf", pagesize=A4)
width, height = A4

# Márgenes y espaciado
margin = 50
line_height = 30
start_y = height - margin
cell_height = 60
cell_padding = 8
day_width = (width - 2 * margin) / 5  # Solo lunes a viernes

# Título
c.setFont("Helvetica-Bold", 18)
c.drawCentredString(width / 2, start_y, "Calendario Pilates Julio 2025")
start_y -= 40

# Días laborales
weekdays = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

# Horario asignado
horario = {
    "Lunes":     {"mañana": "Claudia", "tarde": "Nadia"},
    "Martes":    {"mañana": "Noelia",  "tarde": "Claudia"},
    "Miércoles": {"mañana": "Claudia", "tarde": "Nadia"},
    "Jueves":    {"mañana": "Noelia",  "tarde": "Paula"},
    "Viernes":   {"mañana": "Claudia", "tarde": "Paula"},
}

# Encabezado de días
c.setFont("Helvetica-Bold", 12)
for i, dia in enumerate(weekdays):
    x = margin + i * day_width
    c.drawCentredString(x + day_width / 2, start_y, dia)

start_y -= 20

# Fechas del mes
current = date(2025, 7, 1)
end = date(2025, 7, 31)

row = 0
week = []

while current <= end:
    if current.weekday() < 5:
        week.append((current, weekdays[current.weekday()]))
    if len(week) == 5 or (current == end and week):
        y = start_y - row * cell_height
        # Dibujar celdas de la semana
        for i, (fecha, dia_str) in enumerate(week):
            x = margin + i * day_width
            # Fondo de celda
            c.setFillColor(colors.whitesmoke)
            c.rect(x, y - cell_height + cell_padding, day_width,
                   cell_height - cell_padding, fill=1, stroke=0)
            c.setFillColor(colors.black)
            # Fecha y horarios
            c.setFont("Helvetica-Bold", 10)
            c.drawString(x + 5, y - 18, f"{fecha.day}/07")
            c.setFont("Helvetica", 9)
            profe_manana = horario[dia_str]["mañana"]
            profe_tarde = horario[dia_str]["tarde"]
            c.drawString(x + 5, y - 33, f"8 a 12: {profe_manana}")
            c.drawString(x + 5, y - 48, f"16 a 20: {profe_tarde}")
            # Borde de celda
            c.setStrokeColor(colors.grey)
            c.rect(x, y - cell_height + cell_padding, day_width,
                   cell_height - cell_padding, fill=0, stroke=1)
        row += 1
        # Salto de página si se llena
        if start_y - row * cell_height < margin + cell_height:
            c.showPage()
            start_y = height - margin - 40
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString(width / 2, start_y,
                                "Calendario Pilates Julio 2025 (cont.)")
            start_y -= 40
            c.setFont("Helvetica-Bold", 12)
            for i, dia in enumerate(weekdays):
                x = margin + i * day_width
                c.drawCentredString(x + day_width / 2, start_y, dia)
            start_y -= 20
            row = 0
        week = []
    current += timedelta(days=1)

c.save()
print("✅ PDF generado: calendario_pilates_julio_2025_completo.pdf")
