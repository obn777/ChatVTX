import cv2
import base64
import requests
import time

def capture_and_recognize():
    # 1. Подключение к камере Nitro
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Камера не найдена")
        return

    print("📸 Малыш открывает глаза... (3 сек)")
    time.sleep(1) # Даем камере настроить экспозицию
    
    ret, frame = cap.read()
    if ret:
        # 2. Кодируем изображение в Base64 для передачи на сервер
        _, buffer = cv2.imencode('.jpg', frame)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # 3. Отправляем запрос на наш сервер NovBase
        try:
            response = requests.post(
                "http://0.0.0.0:8080/chat",
                json={"image": img_base64}
            )
            print(f"🤖 Ответ Малыша: {response.json().get('response')}")
        except Exception as e:
            print(f"⚠️ Ошибка связи с сервером: {e}")
            
    cap.release()

if __name__ == "__main__":
    capture_and_recognize()
