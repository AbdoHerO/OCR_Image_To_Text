import cv2
import numpy as np

# Load the image
image_path = "../data/models/with_camscanner/BLS_1.jpg"
image = cv2.imread(image_path)

# Convert the image to gray scale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use a threshold to create a binary image
_, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# Use dilation to connect the table lines
kernel = np.ones((1,1),np.uint8)
dilated = cv2.dilate(binary, kernel, iterations=1)

# Find contours
contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Sort the contours by area and then by the position
contours = sorted(contours, key=cv2.contourArea, reverse=True)
contours = sorted(contours, key=lambda cont: cv2.boundingRect(cont)[1])

# Initialize variables for the largest contour (which should be the table)
largest_contour = None
largest_area = 0

# Go through the contours and find the largest rectangle (which should be the table)
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    area = w * h
    if area > largest_area:
        largest_area = area
        largest_contour = contour

# If we have found the largest contour, we crop the image around it
header_image_path = "../data/header_image.jpg"
table_image_path = "../data/table_image.jpg"
if largest_contour is not None:
    x, y, w, h = cv2.boundingRect(largest_contour)
    # Crop the table part and save
    table_image = image[y:y+h, x:x+w]
    cv2.imwrite(table_image_path, table_image)
    # Crop the header part (everything above the table) and save
    header_image = image[0:y, 0:image.shape[1]]
    cv2.imwrite(header_image_path, header_image)

