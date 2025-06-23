# Calendario Profes Junio y Julio 2025 - SILVIA FERNANDEZ PILATES REFORMER

Este proyecto genera un calendario profesional en PDF para los días del 23 al 30 de junio y todo julio de 2025, con los horarios y profesoras de Pilates Reformer. El PDF resultante es limpio, sin secciones innecesarias, y con una cabecera clara en dos líneas.

## ¿Qué hace el script?

- Genera un único archivo PDF: `calendario_profes_junio_julio_2025.pdf`.
- Incluye solo los días hábiles (lunes a viernes) del 23/06 al 30/06 y todo julio 2025.
- Muestra los horarios especiales y estándar para cada día.
- Elimina cualquier sección de anotaciones o elementos innecesarios.
- El diseño es profesional, claro y fácil de imprimir.

## Requisitos

- Python 3.8 o superior
- Paquete `reportlab`

Instala la dependencia ejecutando:

```sh
pip install reportlab
```

## Cómo usar

1. Descarga o clona este repositorio.
2. Abre una terminal en la carpeta del proyecto.
3. Ejecuta:

   ```sh
   python calendario.py
   ```

4. El PDF se generará en la misma carpeta y se abrirá automáticamente (si tu sistema lo permite).

## Buenas prácticas y recomendaciones (Product Manager)

- **Automatización**: El script está listo para integrarse en flujos de trabajo automatizados (por ejemplo, tareas programadas o integración con sistemas de reservas).
- **Escalabilidad**: Si en el futuro necesitas agregar más meses, profesoras o tipos de horarios, la estructura del script permite hacerlo fácilmente añadiendo nuevas reglas o ampliando los diccionarios de horarios.
- **Mantenibilidad**: El código está limpio, con variables y funciones bien nombradas. Si necesitas modificar los colores, profesoras o cabecera, puedes hacerlo fácilmente en la parte superior del script.
- **Personalización**: Puedes adaptar el diseño visual (colores, fuentes, cabecera) para alinearlo con la identidad visual de tu estudio.
- **Control de versiones**: Guarda los PDFs generados con nombres que incluyan la fecha de generación para mantener un historial de calendarios.

## Sugerencias de mejora futura

- Permitir la generación de calendarios para cualquier rango de fechas mediante argumentos de línea de comandos.
- Exportar también a otros formatos (por ejemplo, imagen PNG o Excel).
- Añadir tests automáticos para validar la generación del PDF.
- Integrar con una interfaz web para que los usuarios puedan descargar el calendario personalizado.

---

¿Tienes sugerencias o necesitas una funcionalidad extra? ¡No dudes en abrir un issue o contactarme!
