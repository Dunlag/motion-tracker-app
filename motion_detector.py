import cv2, time, pandas
from datetime import datetime

# Inicializa variables
first_frame = None  # Primer frame de referencia
status_list = [None, None]  # Lista para guardar el estado de movimiento (0 o 1)
times = []  # Lista para guardar los tiempos de inicio y fin de movimiento
df = pandas.DataFrame(columns=["Start", "End"])  # DataFrame para guardar los periodos de movimiento

video = cv2.VideoCapture(0)  # Inicia la captura de video desde la cámara

# Espera y descarta los primeros frames para evitar el frame negro inicial
for i in range(100):
    check, frame = video.read()

while True:
    check, frame = video.read()
    if not check or frame is None:
        break  # Sale del bucle si no hay más frames (fin del video o error)
    status = 0  # Por defecto, no hay movimiento

    # Convierte el frame a escala de grises y aplica desenfoque
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Toma el primer frame como referencia para detectar diferencias
    if first_frame is None:
        first_frame = gray
        continue

    # Calcula la diferencia absoluta entre el primer frame y el actual
    delta_frame = cv2.absdiff(first_frame, gray)
    # Aplica un umbral para resaltar las diferencias (zonas de movimiento)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    # Diluye la imagen para unir áreas blancas cercanas
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Encuentra los contornos de las zonas blancas (movimiento)
    (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue  # Ignora movimientos pequeños
        status = 1  # Se detecta movimiento

        # Dibuja un rectángulo alrededor del área de movimiento
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 140, 255), 3)
    status_list.append(status)

    # Mantiene solo los dos últimos estados
    status_list = status_list[-2:]

    # Guarda el tiempo cuando empieza el movimiento
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    # Guarda el tiempo cuando termina el movimiento
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    # Muestra las diferentes ventanas de procesamiento
    cv2.imshow("captura en gris", gray)
    cv2.imshow("diferencia", delta_frame)
    cv2.imshow("diferencia umbral", thresh_frame)
    cv2.imshow("Color frame", frame)

    # Lee la tecla presionada (1 ms de espera)
    key = cv2.waitKey(1)

    # Si se presiona 'q', sale del bucle y guarda el tiempo si hay movimiento
    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

# Imprime los estados y los tiempos detectados
print(status_list)
print(times)

# Construye la lista de periodos de movimiento a partir de los tiempos
periods = []
for i in range(0, len(times), 2):
    periods.append({"Start": times[i], "End": times[i+1]})

# Crea el DataFrame final y lo guarda en un archivo CSV
df = pandas.DataFrame(periods)
df.to_csv("times.csv")

# Libera la cámara y cierra todas las ventanas de OpenCV
video.release()
cv2.destroyAllWindows()