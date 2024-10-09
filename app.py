from flask import Flask, Response
import cv2

app = Flask(__name__)

# Ruta al archivo de video
video_file = 'video1.mp4'
camera = cv2.VideoCapture(video_file)

# Verificar si el archivo de video se abrió correctamente
if not camera.isOpened():
    print(f"No se pudo abrir el archivo de video: {video_file}")
    exit()

def generate_frames():
    while True:
        success, frame = camera.read()

        if not success:
            # Reiniciar el video al llegar al final
            camera.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue  # Seguir el bucle para leer desde el inicio

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
