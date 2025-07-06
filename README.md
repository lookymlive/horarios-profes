# Guía para Actualizar el Calendario de Horarios

Este proyecto genera un archivo PDF con los horarios de las profesoras del estudio de Pilates. El script `calendario.py` está diseñado para que puedas actualizar los horarios fácilmente editando una sola sección.

## ¿Cómo actualizar el calendario?

Sigue estos 3 sencillos pasos:

### Paso 1: Abre el archivo de configuración

Abre el archivo `calendario.py` en un editor de texto. Toda la configuración que necesitas cambiar se encuentra al principio del archivo, en la sección llamada `CONFIGURACIÓN`.

### Paso 2: Edita los horarios

Puedes modificar varias cosas en la sección de `CONFIGURACIÓN`:

#### A. Para cambiar horarios de días específicos (excepciones o feriados)

Busca la sección `HORARIOS_ESPECIALES`. Aquí puedes:

* **Añadir un día especial:** Agrega una nueva línea con el formato `date(AÑO, MES, DIA): [("HORA_INICIO a HORA_FIN", "PROFESORA")]`.
* **Modificar un día existente:** Simplemente cambia las horas o la profesora en la línea correspondiente.
* **Marcar un feriado:** Añade una línea para el día festivo con el formato: `date(AÑO, MES, DIA): [("Feriado", "Cerrado")]`.

**Ejemplo:**

```python
HORARIOS_ESPECIALES = {
    # Feriado
    date(2025, 8, 18): [("Feriado", "Cerrado")], 
    # Horario especial para el 20 de agosto
    date(2025, 8, 20): [("8 a 12", "Silvia"), ("16 a 20", "Paula")],
}
```

#### B. Para cambiar el horario estándar de la semana

Busca la sección `HORARIO_SEMANA` y cambia el nombre de la profesora para el turno de `mañana` o `tarde` del día que necesites.

**Ejemplo:**

```python
HORARIO_SEMANA = {
    "Lunes":     {"mañana": "Claudia", "tarde": "Nadia"},
    "Martes":    {"mañana": "Noelia",  "tarde": "Silvia"}, # <-- Cambio de ejemplo
    # ... resto de los días
}
```

#### C. Para gestionar profesoras y colores

En la sección `COLOR_PROFES`, puedes añadir, eliminar o cambiar el nombre de una profesora y asignarle un color.

### Paso 3: Genera el nuevo PDF

Una vez que hayas guardado los cambios en `calendario.py`, abre una terminal o línea de comandos en la carpeta del proyecto y ejecuta el siguiente comando:

```bash
python calendario.py
```

El script creará un nuevo archivo PDF con el calendario actualizado (por ejemplo, `calendario_profes_julio_2025_actualizado.pdf`) y lo abrirá automáticamente.

¡Y eso es todo!
