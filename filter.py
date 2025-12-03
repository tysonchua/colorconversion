import cv2
import numpy as np

def apply_filter(image,type):
    image = image.copy()
    if type == "red_tint":
        image[:,:,1] = image[:,:,0] = 0
    elif type == "green_tint":
        image[:,:,0] = image[:,:,2] = 0
    elif type == "blue_tint":
        image[:,:,1] = image[:,:,2] = 0
    elif type == "sobel":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobel = cv2.bitwise_or(sobelx.astype("uint8"), sobely.astype("uint8"))
        image = cv2.cvtColor(sobel,cv2.COLOR_GRAY2BGR)
    elif type == "canny":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 100, 200)
        image = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
    elif type == "cartoon":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        colour = cv2.bilateralFilter(image,9,300,300)
        image = cv2.bitwise_and(colour, colour, mask=edges)
    elif type == "sketch":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        inv = cv2.bitwise_not(gray)
        blur = cv2.GaussianBlur(inv, (21,21), 0)
        blend = cv2.divide(gray,255 - blur, scale=256)
        image = cv2.cvtColor(blend, cv2.COLOR_GRAY2BGR)
    elif type == "sepia":
        kernel = np.array([[0.272, 0.534, 0.131],
        [0.349, 0.686, 0.168],
        [0.393, 0.769, 0.189]])
        image = cv2.transform(image, kernel)
        image = np.clip(image,0,255).astype(np.uint8)
    elif type == "hdr":
        image = cv2.detailEnhance(image, sigma_s=12, sigma_r=0.15)
    return image

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("cannot open camera")
        return
    ftype = "original"
    while True:
        ret,frame = cap.read()
        if not ret:
            print("can't recieve frame")
            break
        out = apply_filter(frame, ftype)
        cv2.imshow("Live Filters", out)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("r"): ftype = "red_tint"
        elif key == ord("g"): ftype = "green_tint"
        elif key == ord("b"): ftype = "blue_tint"
        elif key == ord("s"): ftype = "sobel"
        elif key == ord("c"): ftype = "canny"
        elif key == ord("t"): ftype = "cartoon"
        elif key == ord("k"): ftype = "sketch"
        elif key == ord("p"): ftype = "sepia"
        elif key == ord("h"): ftype = "hdr"
        elif key == ord("q"): break
    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()