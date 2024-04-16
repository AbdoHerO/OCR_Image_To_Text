from PIL import Image, ImageDraw
from pytesseract import image_to_string
import pytesseract as tess
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Set the path to the Tesseract executable
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#Reading the images Processed
for i in range(4):

    index = ["1", "3", "4" , "8"]

    # Open the image
    img_name = 'BLS_' + index[i] + '_croped_labels' + '_Processed'
    image = Image.open('../output_models/' + img_name + '.jpg')
    # img_name = 'BLS_' + str(i + 1)
    # img_name = 'BLS_8_croped_Processed'
    # image = Image.open('../output_models/' + img_name + '.jpg')
    # image = Image.open('../data/models/' + img_name + '.jpg')

    # Extract text from the image
    text = image_to_string(image)

    # Split the text by line breaks
    text_lines = text.split('\n')

    # Create an ImageDraw object
    draw = ImageDraw.Draw(image)


    # Create a PDF document
    pdf_path = '../output_results_tesseract_testing/'+img_name+'______.pdf'
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Define font size and line height
    font_size = 12
    line_height = 1.5 * font_size

    # Iterate over each line to draw bounding boxes and text, and add text to PDF
    y_position = 700  # Starting y-position for text in PDF

    # Track the current page
    current_page = 0

    # Print and write each line to a file with line breaks
    with open('../output_results_tesseract_testing/'+img_name+'_text.txt', 'w') as file:
        for line in text_lines:
            print(line)
            file.write(line + '\n')

            # Add the text to the PDF document
            c.setFont("Helvetica", font_size)
            c.drawString(50, y_position, line )
            y_position -= line_height

    # Parse each line and draw bounding boxes
    for line in text_lines:
        # Skip empty lines
        if not line.strip():
            continue

        if y_position <= 0:
            # Add a new page
            c.showPage()
            current_page += 1
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



    # Save the image with bounding boxes and text
    image_with_boxes_path = '../output_results_tesseract_testing/'+img_name+'.jpg'
    image.save(image_with_boxes_path)

    # Save the PDF document
    c.save()

    # Display the image
    # image.show()

    # Print and write the recognized text to a file
    text_path = '../output_results_tesseract_testing/'+img_name+'_text.txt'
    # print("Bounding boxes and text drawn on the image. Image saved as:", image_with_boxes_path)
    print("Recognized text saved as:", text_path)
















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