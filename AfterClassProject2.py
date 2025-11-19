import cv2
import numpy as np
import matplotlib as plt
def display_image(image, title):
    plt.figure(figsize=(8,8))
    if len(image.shape):
        plt.imshow(image, cmap = 'gray')
    else:
        plt.imshow(image, cv2.cvtColor(cv2, cv2.COLOR_BGR2GRAY))
    plt.title(title)
    plt.axis("off")
    plt.show()
def interactive_range_detection(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Image not found")
        return
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    display_image("original gray scale image", gray_image)
    print("select an option")
    print("1. Sobel Edge Detection")
    print("2. Canny Edge Detection")
    print("3. Laplacian Edge Detection")
    print("4. Gaussian Smoothing")
    print("5. Median Filtering")
    print("6. exit")
    while True:
        choice = input("Enter your choice (1-6): ")
        if choice == "1":
            sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
            combined_sobel = cv2.bitwise_or(sobelx.astype(np.uint8), sobely.astype(np.uint8))
            display_image("Sobel Edge Detection", combined_sobel)
        elif choice == "2":
            lower_threshold = int(input("Enter lower threshold"))
            upper_threshold = int(input("Enter higher threshold"))
            edges = cv2.Canny(gray_image, lower_threshold, upper_threshold)
            display_image("Canny Edge Detection", edges)
        elif choice == "3":
            laplacian = cv2.Laplacian(gray_image,cv2.CV_64F)
            display_image("Laplacian Edge Detection", np.abs(laplacian).astype(np.uint8))
        elif choice == "4":
            kernelsize = int(input("Enter Kernel Size (must be odd)"))
            blurred = cv2.GaussianBlur(image, (kernelsize,kernelsize), 0)
            display_image("Gaussian Smoothed Image", blurred)
        elif choice == "5":
            kernelsize = int(input("Enter Kernel Size (must be odd)"))
            medianfiltered = cv2.medianBlur(image, kernelsize)
            display_image("Median Filtered Image", medianfiltered)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid option, please choose among the options above.")

interactive_range_detection('example.jpg')

