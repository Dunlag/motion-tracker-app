# 📹 Motion Detector con Gráfico de Movimiento

Este proyecto en Python utiliza **OpenCV** para detectar movimiento en tiempo real desde una camara, y **Bokeh** para generar un gráfico interactivo que muestra los intervalos de tiempo en los que hubo movimiento detectado.

## 🚀 ¿Cómo funciona?

1. **Detección de movimiento**  
   Usando la webcam, se analiza el vídeo en directo comparando cada frame con uno de referencia. Si se detecta un cambio significativo (es decir, algo se mueve), se dibuja un rectángulo alrededor del área en movimiento y se registra el momento.

2. **Registro de tiempos**  
   Cada inicio y fin de movimiento se guarda en una lista y luego se exporta como un archivo `times.csv`.

3. **Visualización interactiva**  
   El archivo `plotting.py` genera un gráfico HTML con los periodos de movimiento usando Bokeh. El gráfico incluye un **hover interactivo** que muestra las marcas de tiempo de cada evento.

## 🧠 Tecnologías usadas

- [`OpenCV`](https://opencv.org/) para la captura y análisis de video.
- [`Pandas`](https://pandas.pydata.org/) para el manejo de datos.
- [`Bokeh`](https://docs.bokeh.org/en/latest/) para la visualización interactiva.
- [`Python`](https://www.python.org/) 3.x

## 📸 Importante

Cuando ejecutas directamente `plotting.py`, **automáticamente también se ejecuta el detector de movimiento** gracias a cómo está estructurado el código. Esto es **intencional**: así puedes registrar los eventos y ver el gráfico generado en un solo paso.


## ▶️ Cómo ejecutarlo

Abre una terminal y ejecuta:

```bash
python plotting.py
````

Esto **lanzará la cámara**, detectará movimiento, guardará los intervalos en `times.csv` y generará el archivo `Grafico.html` con la visualización interactiva de los eventos detectados. ¡Todo en un solo paso!

## 💡 Ideas para expandir el proyecto

Este proyecto es perfectamente adaptable para funcionar como una **cámara de seguridad en una Raspberry Pi** conectada a una cámara. Sería un sistema ligero, de bajo consumo y de bajo coste con visualización remota desde el navegador, ideal para monitoreo en tiempo real o grabación de eventos importantes.

## 📁 Archivos principales

* `motion_detector.py`: Código de detección de movimiento y registro de tiempos.
* `plotting.py`: Generador de gráfico HTML basado en los eventos detectados.
* `times.csv`: Archivo con los periodos de movimiento detectados.
* `Grafico.html`: Visualización generada con Bokeh.

📝 Notas
El script descarta los primeros 100 frames para evitar errores al iniciar la webcam.

Solo se considera movimiento si el área detectada es mayor a 10,000 píxeles, lo cual filtra cambios leves como iluminación o sombras.
