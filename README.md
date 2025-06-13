# Calendario Pilates Julio 2025

Este proyecto genera un calendario en PDF para las clases de Pilates del mes de julio de 2025, con los horarios y profesores asignados.

## Requisitos

- Python 3.13.3 o superior
- reportlab

## Instalación

1. Clona este repositorio o descarga los archivos.
2. Instala la librería necesaria:

   ```bash
   pip install reportlab
   ```

## Uso

1. Ejecuta el script para generar el PDF:

   ```bash
   python calendario.py
   ```

2. Se creará el archivo `calendario_pilates_julio_2025_completo.pdf` en la misma carpeta.
3. Abre el PDF y usa la opción de imprimir desde tu lector de PDF favorito.

## Subir a GitHub

1. Crea un repositorio en GitHub (por ejemplo: `calendario-pilates-julio-2025`).
2. Abre una terminal en la carpeta del proyecto y ejecuta:

   ```bash
   git init
   git add .
   git commit -m "Calendario Pilates Julio 2025"
   git branch -M main
   git remote add origin https://github.com/tu-usuario/calendario-pilates-julio-2025.git
   git push -u origin main
   ```

   Cambia `tu-usuario` por tu nombre de usuario de GitHub.

## Notas para futuros desarrolladores y UI/UX

- El script principal es `calendario.py`. Puedes modificar los horarios, nombres de profesores o el diseño del PDF editando este archivo.
- Si necesitas cambiar el mes o el año, ajusta las variables `current = date(2025, 7, 1)` y `end = date(2025, 7, 31)`.
- Para personalizar la estética (colores, tipografía, logos), edita las secciones donde se usan las funciones de `reportlab`.
- Si agregas nuevas dependencias, recuerda actualizar esta guía.
- Si tienes problemas con la importación de librerías, asegúrate de estar usando el mismo intérprete de Python donde instalaste los paquetes.

---

¡Listo! Este README está preparado para que cualquier persona (IA, dev o UI/UX) pueda entender, ejecutar y mantener el proyecto fácilmente.
