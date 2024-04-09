import os
from asprise_ocr_api import *
import json
import cv2
import numpy as np
from asprise_ocr_api.ocr import Ocr, OCR_PAGES_ALL, OCR_RECOGNIZE_TYPE_TEXT, OCR_OUTPUT_FORMAT_PLAINTEXT


os.environ["ASPRISE_OCR_DLL_PATH"] = r"C:\aocr_x64_dll"

## __START__ Preprocessing for the image befor recognize the OCR

# Specify the path to the input image
image_path = "../data/new_bl.jpg"

# Read the input image using OpenCV
image = cv2.imread(image_path)

# Check if the image is loaded successfully
if image is None:
    print("Error: Unable to load the input image.")
    exit()

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Resize the grayscale image
scaled = cv2.resize(gray, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_LINEAR)

# Apply thresholding to the scaled image
_, thresh = cv2.threshold(scaled, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Save the preprocessed image
preprocessed_image_path = "preprocessed_image.jpg"
cv2.imwrite(preprocessed_image_path, thresh)
# cv2.imshow('Original Image', thresh)
# cv2.waitKey(0)  # Wait for any key press to close the window


## __END__ Preprocessing for the image befor recognize the OCR



ocr = Ocr()
ocr.start_engine("fra")  # deu, fra, por, spa - more than 30 languages are supported

# Export PLAINTEXT
text = ocr.recognize(
    "preprocessed_image.jpg",  # gif, jpg, pdf, png, tif, etc.
    OCR_PAGES_ALL,  # the index of the selected page
    -1, -1, -1, -1,  # you may optionally specify a region on the page instead of the whole page
    # OCR_RECOGNIZE_TYPE_TEXT,  # recognize type: TEXT, BARCODES or ALL
    OCR_RECOGNIZE_TYPE_ALL,  # recognize type: TEXT, BARCODES or ALL
    OCR_OUTPUT_FORMAT_PLAINTEXT  # output format: TEXT, XML, or PDF
)

# Export PDF
ocr.recognize("preprocessed_image.jpg", -1, -1, -1, -1, -1,
                    OCR_RECOGNIZE_TYPE_TEXT, OCR_OUTPUT_FORMAT_PDF,
                    PROP_PDF_OUTPUT_FILE="ocr-result___new_lb___.pdf")

print ("Result: " + text)
ocr.stop_engine()

