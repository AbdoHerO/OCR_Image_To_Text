#Getting the imports
import cv2
import numpy as np

# *--------------------------------------------------------* Step 1 *--------------------------------------------------------*

#Reading the image
img = cv2.imread('../data/new_lb_rimini_croped_border.jpg')


        # //  -------------- binary image ------------------ *
# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to smooth the image (reduce noise)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply adaptive thresholding to create a binary image
# Adaptive thresholding calculates the threshold value for small regions of the image
# This helps in handling varying lighting conditions across the image
binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 17, 5)
        # //  -------------- binary image ------------------ *


#Gaussian Kernal for sharpening
gaussian_blur = cv2.GaussianBlur(img, (7,7), 2)

#Sharpening using addWeighted()
sharpened1 = cv2.addWeighted(img, 1.5, gaussian_blur, -0.5, 0)
sharpened2 = cv2.addWeighted(img, 3.5, gaussian_blur, -2.5, 0)
sharpened4 = cv2.addWeighted(img, 7.5, gaussian_blur, -6.5, 0)
sharpened___ = cv2.addWeighted(img, 5.5, gaussian_blur, -4.5, 0)

# Save the sharpened image
cv2.imwrite('../output_results/binary_remini_new_bl.jpg', binary)
cv2.imwrite('../output_results/sharpened__remini_new_bl.jpg', sharpened___)

#Showing the sharpened Images
# cv2.imshow('Sharpened 1', sharpened1)
# cv2.imshow('Sharpened 2', sharpened2)
# cv2.imshow('Sharpened 4', sharpened4)
cv2.imshow('Original Image', img)
cv2.imshow('Sharpened ___', sharpened___)
cv2.imshow('Processed Image', binary)

cv2.imwrite('../data/binary_new_bl.jpg', binary)



# *--------------------------------------------------------* Step 2 *--------------------------------------------------------*

img_to_transformer_step_2 = cv2.imread('../output_results/sharpened_image.jpg')
rows, cols = img_to_transformer_step_2.shape[:2]

#Bilateral filtring (Reduction of noise + Preserving of edges)
output_bil = cv2.bilateralFilter(img_to_transformer_step_2, 5,6,6)
cv2.imwrite('../output_results/Bilateral__remini_new_bl.jpg', output_bil)

cv2.imshow('Bilateral Filter', output_bil)




# *--------------------------------------------------------* Show all Windows *--------------------------------------------------------*


cv2.waitKey(0)
cv2.destroyAllWindows()
