from PIL import Image, ImageDraw
from pytesseract import image_to_string
import pytesseract as tess
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# Set the path to the Tesseract executable
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Define your main directory containing the image folders
main_directory = "../data/output_cropage_Processed"
main_directory = os.getcwd()
#
# Define your output directory
output_directory = "../data/output_cropage_OCR"


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


# Loop through each sub-folder in the main directory
for folder_name in os.listdir(main_directory):
    folder_path = os.path.join(main_directory, folder_name)

    if os.path.isdir(folder_path):
        for image_file in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_file)

            # We assume that the files are named like 'BLS_4_header_processed.jpg' or 'BLS_4_table_processed.jpg'
            # We want to group both header and table under a folder named 'BLS_4_ocr'
            if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                # Extract the base name (e.g., 'BLS_4')
                base_name_parts = image_file.split('_')
                base_name = '_'.join(base_name_parts[:2])  # Adjust the slice accordingly

                # Define the path for the new folder to store the OCR results
                ocr_folder_path = os.path.join(output_directory, base_name + '__ocr')

                # Create the output directory if it doesn't exist
                if not os.path.exists(ocr_folder_path):
                    os.makedirs(ocr_folder_path)

                # Call process_image function with the OCR folder path and base name
                process_image(image_path, ocr_folder_path,
                              image_file.replace('.jpg', '').replace('.jpeg', '').replace('.png', ''))
                print(f"Processed OCR for image: {image_file}")

























# _____ODL ______

# #Reading the images Processed
# for i in range(4):
#
#     index = ["1", "3", "4" , "8"]
#
#     # Open the image
#     img_name = 'BLS_' + index[i] + '_croped_labels' + '_Processed'
#     image = Image.open('../output_models/' + img_name + '.jpg')
#     # img_name = 'BLS_' + str(i + 1)
#     # img_name = 'BLS_8_croped_Processed'
#     # image = Image.open('../output_models/' + img_name + '.jpg')
#     # image = Image.open('../data/models/' + img_name + '.jpg')
#
#     # Extract text from the image
#     text = image_to_string(image)
#
#     # Split the text by line breaks
#     text_lines = text.split('\n')
#
#     # Create an ImageDraw object
#     draw = ImageDraw.Draw(image)
#
#
#     # Create a PDF document
#     pdf_path = '../output_results_tesseract_testing/'+img_name+'______.pdf'
#     c = canvas.Canvas(pdf_path, pagesize=letter)
#
#     # Define font size and line height
#     font_size = 12
#     line_height = 1.5 * font_size
#
#     # Iterate over each line to draw bounding boxes and text, and add text to PDF
#     y_position = 700  # Starting y-position for text in PDF
#
#     # Track the current page
#     current_page = 0
#
#     # Print and write each line to a file with line breaks
#     with open('../output_results_tesseract_testing/'+img_name+'_text.txt', 'w') as file:
#         for line in text_lines:
#             print(line)
#             file.write(line + '\n')
#
#             # Add the text to the PDF document
#             c.setFont("Helvetica", font_size)
#             c.drawString(50, y_position, line )
#             y_position -= line_height
#
#     # Parse each line and draw bounding boxes
#     for line in text_lines:
#         # Skip empty lines
#         if not line.strip():
#             continue
#
#         if y_position <= 0:
#             # Add a new page
#             c.showPage()
#             current_page += 1
#             y_position = 700
#
#         # Split line into character, left, top, right, bottom
#         parts = line.split()
#         try:
#             character = parts[0]
#             left, top, right, bottom = map(int, parts[1:5])
#         except ValueError:
#             # Skip lines that don't contain valid bounding box information
#             continue
#
#         # Draw bounding box and text
#         draw.rectangle([(left, top), (right, bottom)], outline='red')
#         draw.text((left, top), character, fill='red')
#
#         y_position -= line_height
#
#
#
#     # Save the image with bounding boxes and text
#     image_with_boxes_path = '../output_results_tesseract_testing/'+img_name+'.jpg'
#     image.save(image_with_boxes_path)
#
#     # Save the PDF document
#     c.save()
#
#     # Display the image
#     # image.show()
#
#     # Print and write the recognized text to a file
#     text_path = '../output_results_tesseract_testing/'+img_name+'_text.txt'
#     # print("Bounding boxes and text drawn on the image. Image saved as:", image_with_boxes_path)
#     print("Recognized text saved as:", text_path)
