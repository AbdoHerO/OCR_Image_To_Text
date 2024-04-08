import cv2
import numpy as np

#Reading a image from computer and taking dimensions
img = cv2.imread('../data/new_lb_rimini_croped_border.jpg')
rows, cols = img.shape[:2]

#Kernel Bluerring using filter2D()
kernel = np.ones((7, 2), np.float32) / 12.0
output_kernel = cv2.filter2D(img, -1, kernel)

#boxFilter and Blur fucntion blurring
output_blur = cv2.blur(img, (25,25))
output_box = cv2.boxFilter(img, -1, (5,5), normalize=False)

#Gaussian Blur
output_gaussian = cv2.GaussianBlur(img, (5,5) , 0)

#Median Blur (reduction the noise)
output_med = cv2.medianBlur(img, 5)

#Bilateral filtring (Reduction of noise + Preserving of edges)
output_bil = cv2.bilateralFilter(img, 5,6,6)

# cv2.imshow('Kernel Blur', output_kernel)
# cv2.imshow('Blur() output', output_blur)
# cv2.imshow('Gaussian Blur' , output_gaussian)
# cv2.imshow('Box Filter', output_box)
# cv2.imshow('Median Filter', output_med)
cv2.imshow('Bilateral Filter', output_bil)
cv2.imshow('Original Image', img)


cv2.waitKey(0)
cv2.destroyAllWindows()

