import cv2
import numpy as np
import os
from pathlib import Path

# Directory containing the images
input_dir_path = Path("../data/models/with_camscanner")
output_dir_path = Path("../data/output_cropage")


# Function to process an image and extract the header and table
def process_image(image_path):
    image = cv2.imread(str(image_path))

    # Convert to grayscale, threshold, and dilate to find contours
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((1, 1), np.uint8)
    dilated = cv2.dilate(binary, kernel, iterations=1)
    contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour
    largest_area = 0
    largest_contour = None
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        if area > largest_area:
            largest_area = area
            largest_contour = contour

    # Create a directory named after the image to store the output
    image_name = image_path.stem
    custom_output_dir = output_dir_path / image_name
    custom_output_dir.mkdir(parents=True, exist_ok=True)

    # Save the header and table images
    if largest_contour is not None:
        x, y, w, h = cv2.boundingRect(largest_contour)
        header_image = image[0:y, 0:image.shape[1]]
        table_image = image[y:y + h, x:x + w]
        header_image_path = custom_output_dir / f"{image_name}_header.jpg"
        table_image_path = custom_output_dir / f"{image_name}_table.jpg"
        cv2.imwrite(str(header_image_path), header_image)
        cv2.imwrite(str(table_image_path), table_image)
        return header_image_path, table_image_path
    return None, None


# Process all jpg images in the directory
for image_file in input_dir_path.glob('*.jpg'):
    process_image(image_file)
