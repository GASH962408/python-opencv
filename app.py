from flask import Flask, Response, send_from_directory
import cv2
import torch
import numpy as np
import os

app = Flask(__name__, static_folder='build', static_url_path='/')

class VideoCamera:
    def __init__(self, video_file):
        self.video_file = video_file
        self.camera = cv2.VideoCapture(video_file)

    def get_frame(self):
        success, frame = self.camera.read()
        if not success:
            self.camera.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop video
            success, frame = self.camera.read()
        return frame

    def release(self):
        self.camera.release()

# Instantiate the video camera
video_file = 'video1.mp4'
camera = VideoCamera(video_file)

# Load the YOLOv5 model once
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def detect_objects(frame):
    """Detect objects in a frame using YOLOv5"""
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    results = model(frame_rgb)  # Perform detection

    for detection in results.xyxy[0]:
        xmin, ymin, xmax, ymax, confidence, class_id = detection
        label = f'{model.names[int(class_id)]} {confidence:.2f}'
        cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
        cv2.putText(frame, label, (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame

def generate_frames():
    """Generate frames from the video with object detection"""
    while True:
        frame = camera.get_frame()
        frame = detect_objects(frame)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    """Route to stream video"""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    """Serve the React application"""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    try:
        app.run(debug=True, port=5000)
    except Exception as e:
        print(f"Error occurred: {e}")
