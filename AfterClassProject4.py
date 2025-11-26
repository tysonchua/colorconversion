import cv2
import time
from fer import FER
detector = FER()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam")
    exit(0)

while True:
    ret,frame = cap.open()
    if not ret:
        print("Error: Failed to capture image")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30))
        for (x,y,w,h) in faces:
            cv2.rectangle(cv2,(x,y),(x+w,y+h), (255,0,0), 2)
            face_region = frame[y:y+h, x:x+w]
            emotion = detector.top_emotion(face_region)
            if emotion is not None:
                emotion_name, emotion_score = emotion
                cv2.putText(frame, f"{emotion_name} ({emotion_score:.2f})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 255, 0), 2)
        cv2.imshow(f"Facial Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()