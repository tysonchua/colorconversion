import cv2
import numpy as np
import matplotlib.pyplot as plt
def display_image(title, image):
    plt.figure(figsize=(8,8))
    if len(image.shape) == 2:
        plt.imshow(image, cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis("off")
    plt.show()
def interactive_range_detection(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("image not found")
        return
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    display_image("original gray scale image", gray_image)
    print("select an option")
    print("1. sobel edge detection")
    print("2. canny edge detection")
    print("3. laplacian edge detection")
    print("4. gaussian smoothing")
    print("5. median filtering")
    print("6. exit")
    while True:
        choice = input("Enter your choice (1-6): ")
        if choice == "1":
            sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
            combined_sobel = cv2.bitwise_or(sobelx.astype(np.uint8), sobely.astype(np.uint8))
            display_image("sobel edge detection", combined_sobel)
        elif choice == "2":
            lower_threshold = int(input("Enter lower threshold"))
            upper_threshold = int(input("Enter higher threshold"))
            edges = cv2.Canny(gray_image, lower_threshold, upper_threshold)
            display_image("canny edge detection", edges)
        elif choice == "3":
            laplacian = cv2.Laplacian(gray_image,cv2.CV_64F)
            display_image("Laplacian edge detection", np.abs(laplacian).astype(np.uint8))
        elif choice == "4":
            kernelsize = int(input("enter kernel size (must be odd)"))
            blurred = cv2.GaussianBlur(image, (kernelsize,kernelsize), 0)
            display_image("Gaussian Smoothed Image", blurred)
        elif choice == "5":
            kernelsize = int(input("enter kernel size (must be odd)"))
            medianfiltered = cv2.medianBlur(image, kernelsize)
            display_image("Median Filtered Image", medianfiltered)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("invalid option")

interactive_range_detection('example.jpg')