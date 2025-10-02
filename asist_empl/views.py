from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2

def home(request):
    return render(request, 'home.html')
def video_feed(request):
    """Vista que proporciona el streaming de video"""
    return StreamingHttpResponse(
        generate_frames(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )
    


def generate_frames():
    """Generador que captura frames de la cámara y detecta códigos QR"""
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Detectar código QR
        data, bbox, _ = detector.detectAndDecode(frame)
        
        # Si se detecta un QR, dibujar un recuadro
        if data:
            print(f"Código QR detectado: {data}")
            if bbox is not None:
                bbox_int = bbox[0].astype(int)
                cv2.polylines(frame, [bbox_int], True, (0, 255, 0), 2)
        
        # Convertir frame a formato JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        # Enviar frame en formato de streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

