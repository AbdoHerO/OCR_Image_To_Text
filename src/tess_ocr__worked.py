# from PIL import Image
# from pytesseract import image_to_string
# import pytesseract as tess
# tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#
#
# image=Image.open('data/mod01.jpg')
# text= image_to_string(image)
# print(text)
# file=open('output.txt','w')
# text=repr(text)
# file.write(text)
# file.close


from PIL import Image
from pytesseract import image_to_string
import pytesseract as tess

# Set the path to the Tesseract executable
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Open the image
image = Image.open('../data/denoise_mod02_resized.jpg')

# Extract text from the image
text = image_to_string(image)

# Split the text by line breaks
text_lines = text.split('\n')

# Print and write each line to a file with line breaks
with open('../output_results/output.txt', 'w') as file:
    for line in text_lines:
        print(line)
        file.write(line + '\n')