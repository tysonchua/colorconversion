import cv2
import numpy as np
import math
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera")
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        print("Could not capture image")
        break
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0,20,70], dtype=np.uint8)
    upper_skin = np.array([20,255,255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    mask = cv2.GaussianBlur(mask, (9,9), 0)
    mask = cv2.erode(mask, np.ones((5,5), dtype=np.uint8), iterations=1)
    mask = cv2.dilate(mask, np.ones((5,5), dtype=np.uint8), iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    finger_count = 0
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(max_contour) > 1200:
            max_contour = cv2.approxPolyDP(max_contour,3, True)
            hull = cv2.convexHull(max_contour,returnPoints=False)
            defects = None
            if hull is not None and len(hull) > 3:
                try:
                    defects = cv2.convexityDefects(max_contour, hull)
                except:
                    defects = None
            if defects is not None:
                for i in range(defects.shape[0]):
                    s,e,f,d = defects[i, 0]
                    start = tuple(max_contour[s][0])
                    end = tuple(max_contour[e][0])
                    far = tuple(max_contour[f][0])
                    a = math.dist(start,end)
                    b = math.dist(start,far)
                    c = math.dist(end,far)

                    if b * c == 0:
                        continue
                    angle = math.degrees(math.acos((b*b + c*c - a*a) / (2*b*c)))
                    if angle < 80 and d > 9000:
                        finger_count += 1
                finger_count +=1
            x, y, w, h = cv2.boundingRect(max_contour)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
    cv2.putText(frame, f"Fingers: {finger_count}", (20,50), cv2.FONT_HERSHEY_COMPLEX, 1.2, (0,255,255), 3)
    cv2.imshow("Original Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()