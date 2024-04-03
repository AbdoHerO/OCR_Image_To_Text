import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np

# read image
image_path = 'data/denoise_mod01.jpg'
img = cv2.imread(image_path)

# instance text detector
reader = easyocr.Reader(['fr'], gpu=False)

# detect text on imageS
text_ = reader.readtext(img)

threshold = 0.25

# store extracted text
extracted_text = []

# iterate through detected text
for t_, t in enumerate(text_):
    bbox, text, score = t

    # check if confidence score is above threshold
    if score > threshold:
        extracted_text.append(text)

# print the extracted text
for text in extracted_text:
    print(text)

# display the image with bounding boxes and text
for t_, t in enumerate(text_):
    bbox, text, score = t

    # check if confidence score is above threshold
    if score > threshold:
        cv2.rectangle(img, bbox[0], bbox[2], (0, 255, 0), 5)
        cv2.putText(img, text, bbox[0], cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()
