from flask import Flask, Response
import cv2

app = Flask(__name__)

# Cambiar la fuente de video a un archivo local
video_file = './'  # Cambia esto al nombre de tu archivo de video
camera = cv2.VideoCapture(video_file)

# Verificar si el archivo de video se abrió correctamente
if not camera.isOpened():
    print(f"No se pudo abrir el archivo de video: {video_file}")
    exit()

def generate_frames():
    while True:
        # Leer el siguiente frame del archivo de video
        success, frame = camera.read()
        if not success:
            break  # Finaliza el bucle cuando se termine el video
        else:
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
    # Respuesta con el flujo de video
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
