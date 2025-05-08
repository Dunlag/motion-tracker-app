from motion_detector import df  # Importa el DataFrame con los periodos de movimiento

from bokeh.plotting import figure, show, output_file  # Funciones principales de Bokeh para graficar
from bokeh.models import HoverTool, ColumnDataSource   # Herramientas para interacción y fuente de datos

# Formatea las columnas de fecha/hora para mostrarlas como texto en el hover
df["Start_string"] = df["Start"].dt.strftime("%H:%m:%S %d-%m-%Y")
df["End_string"] = df["End"].dt.strftime("%H:%m:%S %d-%m-%Y")

# Convierte el DataFrame en una fuente de datos para Bokeh
cds = ColumnDataSource(df)

# Crea la figura principal del gráfico, con eje X de tipo fecha/hora
p = figure(
    x_axis_type='datetime',
    height=500,
    width=500,
    sizing_mode="stretch_width",
    title="Grafico de movimiento"
)

# Quita las marcas menores del eje Y
p.yaxis.minor_tick_line_color = None
# Limita el número de ticks principales en el eje Y a 1
p.yaxis[0].ticker.desired_num_ticks = 1

# Configura la herramienta de hover para mostrar los datos de inicio y fin
hover = HoverTool(tooltips=[("Start ", "@Start_string"), ("End ", "@End_string")])
p.add_tools(hover)

# Dibuja los intervalos de movimiento como barras (quads) naranjas
q = p.quad(left="Start", right="End", bottom=0, top=1, color="orange", source=cds)

# Define el archivo de salida HTML
output_file("Grafico.html")

# Muestra el gráfico en el navegador
show(p)