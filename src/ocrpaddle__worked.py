# !python3 -m pip install paddlepaddle-gpu
# !pip install "paddleocr>=2.0.1"

from paddleocr import PaddleOCR,draw_ocr
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.
ocr = PaddleOCR(use_angle_cls=True, lang='fr', use_gpu=False)  # need to run only once to download and load model into memory

from google.colab.patches import cv2_imshow
import cv2
import urllib.request  # Import the module for downloading files


# !https://rachidcosm.dorimy.com/public/uploads/all/bmISH4HLJMax2gDU07ZLzvyFtbZxhGJGNRM4SEX9.jpg -O /content/simple_test.jpg

# # URL of the image
# url = 'https://rachidcosm.dorimy.com/public/uploads/all/QU9asMLYL9lXRtYVB3DHxSOkOhrxxTIiLQVVx8P2.jpg'
#
# # Download the image from the URL and save it locally
# urllib.request.urlretrieve(url, 'image_test.jpg')


img_path = '../data/denoise_mod01_resized.jpg'

img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
cv2_imshow(img)

result = ocr.ocr(img_path, cls=True)
for line in result:
    print(line)

# draw result
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Load the input image
img_path = '../data/denoise_mod01_resized.jpg'
image = Image.open(img_path).convert('RGB')

# Extract bounding box coordinates, text, and confidence score from the result
boxes = [line[0] for line in result]
texts = [line[0][1][0] for line in result]  # Corrected line
scores = [line[0][1][1] for line in result]  # Corrected line

# Draw bounding boxes and texts on the image
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

for box, text, score in zip(boxes, texts, scores):
    # Extract x and y coordinates from the box
    xy = [(coord[0], coord[1]) for coord in box[0]]

    # Draw bounding box
    draw.polygon(xy, outline='red')

    # Draw text and confidence score
    draw.text((box[0][0][0], box[0][0][1] - 10), f"{text} ({score:.2f})", fill='red', font=font)

# Save the result image
output_path = '../output_results/result_orc_paddle.jpg'
image.save(output_path)

# Display the
result_path = '../output_results/result_orc_paddle.jpg'
result_img = cv2.imread(result_path, cv2.IMREAD_UNCHANGED)
cv2_imshow(result_img)