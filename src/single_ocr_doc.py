import cv2
import numpy as np
from pathlib import Path
from PIL import ImageFilter
import cv2
from matplotlib import pyplot as plt
import os
from PIL import Image, ImageDraw
from pytesseract import image_to_string
import pytesseract as tess
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path

# Set the path to the Tesseract executable
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Directory containing the images
image_file ="../data/image2.jpg"
output_dir_path = Path("../data/complete_ocr_output")
output_ocr_final_path = Path("../data/complete_ocr_output/OCR output final")


# ---------------------------------------- Crop the Image --------------------------------------------

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


    # Save the header and table images
    if largest_contour is not None:
        x, y, w, h = cv2.boundingRect(largest_contour)
        header_image = image[0:y, 0:image.shape[1]]
        table_image = image[y:y + h, x:x + w]
        header_image_path = output_dir_path / f"BL_header_croped.jpg"
        table_image_path = output_dir_path / f"BL_table_croped.jpg"
        cv2.imwrite(str(header_image_path), header_image)
        cv2.imwrite(str(table_image_path), table_image)
        return header_image_path, table_image_path
    return None, None

# Process the jpg image in the directory
process_image(image_file)

# ---------------------------------- Pre Processing the Image -----------------------------------------

def display(im_path):
    dpi = 80
    im_data = plt.imread(im_path)

    height, width = im_data.shape[:2]

    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)

    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([1, 1, 0, 0])

    # Hide spines, ticks, etc.
    ax.axis('off')

    # Display the image.
    ax.imshow(im_data, cmap='gray')

    plt.show()
def deskew(image):
    # Find coordinates of non-zero pixels
    co_ords = np.where(image > 0)

    # Convert the row and column indices to a two-dimensional array
    co_ords = np.column_stack((co_ords[1], co_ords[0])).astype(np.float32)

    # Calculate the angle of rotation
    angle = cv2.minAreaRect(co_ords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # Get image dimensions
    (h, w) = image.shape[:2]

    # Calculate the center point
    center = (w // 2, h // 2)

    # Generate rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Apply rotation to the image
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated
def noise_removal(image):
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return (image)
def thin_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)  # should be (2,2)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)
def thick_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)
def processing_the_img(image):
    # -- - Skew Correction
    skew_correction = deskew(image)

    # 1 - Inverted Images
    inverted_image = cv2.bitwise_not(image)

    # 2 - Binarization - Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # cv2.COLOR_BGR2GRAY || cv2.COLOR_RGB2GRAY
    # plt.imshow(cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB))
    # plt.show()

    # Apply Gaussian blur to remove noise
    # blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)


    # 3 - Threshold - Apply thresholding to create a binary image
    _, binary_image = cv2.threshold(gray_image, 180, 255, cv2.THRESH_BINARY )  # cv2.THRESH_OTSU

    # 4 - Noise Removal
    no_noise = noise_removal(binary_image)

    # 5 - Dilation and Erosion
    eroded_image = thin_font(no_noise)

    # 6 - Thick Font
    dilated_image = thick_font(no_noise)

    # 7 - Removing Shadows
    rgb_planes = cv2.split(dilated_image)
    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        result_planes.append(diff_img)
    img = cv2.merge(result_planes)

    eroded_image = thin_font(img)

    return no_noise
    # plt.imshow(cv2.cvtColor(eroded_image, cv2.COLOR_GRAY2RGB))
    # plt.show()

# Loop through each image in the sub-folder
for image_name in os.listdir(output_dir_path):
    if image_name.lower().endswith(('_croped.png', '_croped.jpg', '_croped.jpeg')):
        image_path = os.path.join(output_dir_path, image_name)
        image = cv2.imread(image_path)

        # Apply the preprocessing functions to the image
        preprocessed_image = processing_the_img(image)

        # Save the processed image in the new folder with the modified name
        processed_image_path = os.path.join(output_dir_path, image_name.split('.')[0] + '_processed.jpg')
        cv2.imwrite(processed_image_path, preprocessed_image)

        # Show the processed image
        # print(image_name)
        plt.imshow(cv2.cvtColor(preprocessed_image, cv2.COLOR_BGR2RGB))
        plt.show()


# ---------------------------------- OCR Tesseract Processing -----------------------------------------

def process_image(image_path, ocr_folder_path, base_name):
    image = Image.open(image_path)
    text = image_to_string(image)

    text_lines = text.split('\n')
    draw = ImageDraw.Draw(image)

    # pdf_path = output_base_path + '__OCR.pdf'
    pdf_file_path = os.path.join(ocr_folder_path, base_name + '_ocr.pdf')
    c = canvas.Canvas(pdf_file_path, pagesize=letter)
    font_size = 12
    line_height = font_size * 1.5
    y_position = letter[1] - 2 * line_height  # Start below the top of the page

    # text_file_path = output_base_path + '__OCR.txt'
    text_file_path = os.path.join(ocr_folder_path, base_name + '_ocr.txt')
    with open(text_file_path, 'w') as text_file:
        for line in text_lines:

            # Optional
            if 'table' in  base_name:
                print(line)

            text_file.write(line + '\n')
            c.setFont("Helvetica", font_size)
            c.drawString(50, y_position, line)
            y_position -= line_height
            if y_position < line_height:  # Margin at the bottom
                c.showPage()
                y_position = letter[1] - 2 * line_height

    # Parse each line and draw bounding boxes
    for line in text_lines:
        # Skip empty lines
        if not line.strip():
            continue

        if y_position <= 0:
            # Add a new page
            c.showPage()
            y_position = 700

        # Split line into character, left, top, right, bottom
        parts = line.split()
        try:
            character = parts[0]
            left, top, right, bottom = map(int, parts[1:5])
        except ValueError:
            # Skip lines that don't contain valid bounding box information
            continue

        # Draw bounding box and text
        draw.rectangle([(left, top), (right, bottom)], outline='red')
        draw.text((left, top), character, fill='red')

        y_position -= line_height

    # image_with_boxes_path = output_base_path + '__OCR.jpg'
    image_with_boxes_path = os.path.join(ocr_folder_path, base_name + '_ocr.jpg')

    image.save(image_with_boxes_path)
    c.save()

for image_file in os.listdir(output_dir_path):
    image_path = os.path.join(output_dir_path, image_file)

    # We assume that the files are named like 'BLS_4_header_processed.jpg' or 'BLS_4_table_processed.jpg'
    # We want to group both header and table under a folder named 'BLS_4_ocr'
    if image_file.lower().endswith(('_processed.jpg', '_processed.jpeg', '_processed.png')):
        # Extract the base name
        base_name_parts = image_file.split('_')
        base_name = '_'.join(base_name_parts[:2])  # Adjust the slice accordingly

        # Define the path for the new folder to store the OCR results
        ocr_folder_path = os.path.join(output_ocr_final_path, base_name + '__ocr')

        # Create the output directory if it doesn't exist
        if not os.path.exists(ocr_folder_path):
            os.makedirs(ocr_folder_path)

        # Call process_image function with the OCR folder path and base name
        process_image(image_path, ocr_folder_path,
                      image_file.replace('.jpg', '').replace('.jpeg', '').replace('.png', ''))
        # print(f"Processed OCR for image: {image_file}")
