import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time
from datetime import datetime
cap = cv2.VideoCapture(0)
capture_time = 0
ftype = "original"
detector = HandDetector(maxHands=1,detectionCon=0.8)
palm_opened = False
capture_pending = False
def ApplyColourFilter(image, filter_type):
    filtered_image = image.copy()
    if filter_type == "red_tint":
        filtered_image[:,:,1] = 0
        filtered_image[:,:,0] = 0
    elif filter_type == "green_tint":
        filtered_image[:,:,2] = 0
        filtered_image[:,:,0] = 0
    elif filter_type == "blue_tint":
        filtered_image[:,:,2] = 0
        filtered_image[:,:,1] = 0
    elif filter_type == "sobel":
        gray = cv2.cvtColor(filtered_image,cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1,0,ksize=3)
        sobely = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=3)
        sobel = cv2.bitwise_or(sobelx.astype("uint8"),sobely.astype("uint8"))
        filtered_image=cv2.cvtColor(sobel,cv2.COLOR_GRAY2BGR)
    elif filter_type == "canny":
        gray = cv2.cvtColor(filtered_image,cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray,100,200)
        filtered_image = cv2.cvtColor(canny,cv2.COLOR_GRAY2BGR)
    elif filter_type == "cartoon":
        gray = cv2.cvtColor(filtered_image,cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray,5)
        edges = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,9)
        colour = cv2.bilateralFilter(filtered_image,9,300,300)
        filtered_image = cv2.bitwise_and(colour,colour,mask=edges)
    return filtered_image
while True:
    success, frame = cap.read()
    if not success:
        break
    hands,frame = detector.findHands(frame,draw=True)
    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        if fingers.count(1) >= 4 and not palm_opened:
            palm_opened = True
        if fingers.count(1) == 0 and not capture_pending:
            palm_opened = False
            capture_time = time.time() + 3
    if capture_pending:
        remaining = int(capture_time - time.time())
        if remaining <=0:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"IMG_{timestamp}.jpg"
            cv2.imwrite(file_name,frame)
            capture_pending = False
            palm_opened = False
        else:
            cv2.putText(
                frame,
                f"Capturing in {remaining}...",
                (30,60),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (0,255,255),
                2
                )
    key = cv2.waitKey(1) & 0xFF
    if key == ord("o"):
        ftype = "original"
        print(ftype)
    elif key == ord("r"):
        ftype = "red_tint"
        print(ftype)
    elif key == ord("g"):
        ftype = "green_tint"
        print(ftype)
    elif key == ord("b"):
        ftype = "blue_tint"
        print(ftype)
    elif key == ord("s"):
        ftype = "sobel"
        print(ftype)
    elif key == ord("c"):
        ftype = "canny"
        print(ftype)
    elif key == ord("t"):
        ftype = "cartoon"
        print(ftype)
    elif key == ord("q"):
        print("Exiting...")
        break
    filter_image = ApplyColourFilter(frame,ftype)
    cv2.imshow("Gesture Controlled Photo App With Filters", filter_image)
cap.release()
cv2.destroyAllWindows()       