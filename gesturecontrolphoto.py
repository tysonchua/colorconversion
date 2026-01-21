import cv2
from cvzone.HandTrackingModule import HandDetector
import time
from datetime import datetime
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)
palm_opened = False
capture_pending = False
capture_time = 0
while True:
    success, frame = cap.read()
    if not success:
        break
    
    hands, frame = detector.findHands(frame, draw=True)
    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        if fingers.count(1) >= 4 and not palm_opened:
            palm_opened = True
        if fingers.count(1) == 0 and not capture_pending:
            capture_pending = True
            capture_time = time.time() + 3
    if capture_pending:
        remaining = int(capture_time - time.time())
        if remaining <= 0:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"IMG_{timestamp}.jpg"
            cv2.imwrite(filename,frame)
            capture_pending = False
            palm_opened = False
        else:
            cv2.putText(
                frame,
                f"Capturing in {remaining}...",
                (30,60),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (0,0,255),
                2
            )
    cv2.imshow("Gestur Controlled Photo App", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()