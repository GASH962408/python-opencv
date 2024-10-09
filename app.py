from flask import Flask, Response
import cv2
import torch
import numpy as np

app = Flask(__name__)

# Ruta al archivo de video
video_file = 'video1.mp4'
camera = cv2.VideoCapture(video_file)

# Verificar si el archivo de video se abrió correctamente
if not camera.isOpened():
    print(f"No se pudo abrir el archivo de video: {video_file}")
    exit()

# Cargar el modelo YOLOv5 preentrenado desde PyTorch Hub
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Función para procesar y detectar objetos en el frame
def detect_objects(frame):
    """Detectar objetos en un frame usando YOLOv5"""
    # Convertir el frame de OpenCV (BGR) a formato RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(frame_rgb)  # Realizar la detección con YOLOv5

    # Dibujar las cajas y etiquetas en el frame
    for detection in results.xyxy[0]:  # Obtener las detecciones
        xmin, ymin, xmax, ymax, confidence, class_id = detection
        label = f'{model.names[int(class_id)]} {confidence:.2f}'
        # Dibujar rectángulo alrededor del objeto detectado
        cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
        # Añadir la etiqueta del objeto detectado
        cv2.putText(frame, label, (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame

def generate_frames():
    while True:
        success, frame = camera.read()

        if not success:
            # Reiniciar el video al llegar al final
            camera.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue  # Seguir el bucle para leer desde el inicio

        # Detectar objetos en el frame usando YOLOv5
        frame = detect_objects(frame)

        # Codificar el frame en formato JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Enviar el frame con el formato adecuado para el navegador
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return "¡Bienvenido al Sistema de Vigilancia Inteligente con Video de Archivo!"

@app.route('/video_feed')
def video_feed():
    global camera
    # Cerrar y reabrir el archivo de video al recargar la página
    camera.release()
    camera = cv2.VideoCapture(video_file)
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
