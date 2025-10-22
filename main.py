import cv2
import matplotlib.pyplot as plt
image = cv2.imread('Pencils.jpg')

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.imshow(image_rgb)
plt.title("RGB Image")
plt.show()
 
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
plt.imshow(image_gray, cmap="gray")
plt.title("Gray Image")
plt.show()

height, width = image.shape[:2]
y_start = height - 200
y_end = height
x_start = width // 3
x_end = 2 * width // 3
cropped_image = image[y_start:y_end, x_start:x_end]
cropped_rgb = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
plt.imshow(cropped_rgb)
plt.title("Cropped Region")
plt.show()