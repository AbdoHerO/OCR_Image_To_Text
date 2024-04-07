from PyPDF2 import PdfReader
import pandas as pd
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io  # Add this import for the 'io' module

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# pytesseract.pytesseract.TESSDATA_PREFIX = r'C:\Program Files\Tesseract-OCR'

# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

def extract_data_under_column_head(text, column_head):
    index = [i for i, x in enumerate(text) if x == column_head]
    data = []
    for i in index:
        # Find the next column head or end of text
        next_index = index[index.index(i) + 1] if index.index(i) + 1 < len(index) else len(text)
        # Extract data under the current column head
        column_data = text[i+1:next_index]
        data.append(column_data)
    return data


def extract_text_from_image(image):
    # Use pytesseract to perform OCR on the image and return the extracted text
    return pytesseract.image_to_string(image)

def extract_text_from_pdf(file_path):
    text = ""
    # Open the PDF file
    with fitz.open(file_path) as pdf_document:
        # Iterate over each page
        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            # Extract images from the page
            images = page.get_images(full=True)
            # Iterate over each image on the page
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                # Convert the image bytes to a PIL Image object
                image = Image.open(io.BytesIO(image_bytes))
                # Perform OCR on the image and append the extracted text to the result
                text += extract_text_from_image(image)
    return text

column_names_target = ["Commandée", "Livrée", "Désignation", "P.P.M.", "LOT", "Date péremptic"]
column_names_excel = ["Quantité Commandée", "Quantité Livrée", "Désignation", "P.P.M.", "LOT", "Date péremptic"]
data_dict = {name: [] for name in column_names_excel}

# Read the file
# file_name = "../data/new_bl.pdf"
file_name = "C:\\Users\\abder\\Documents\\__GIT_Abdou\\OCR\\OCR_Image_To_Text\\data\\new_bl.pdf"
reader = PdfReader(file_name)
page = reader.pages[0]

# Get the text
# text = page.extract_text().split("\n")
text = extract_text_from_pdf(file_name)

print(text)

for column_name in column_names_target:
    data_dict[column_name].extend(extract_data_under_column_head(text, column_name))

data = pd.DataFrame(data_dict)
data.to_excel("data.xlsx", index=False)
















# from PyPDF2 import PdfReader
# import pandas as pd
#
# contract_no = []
# org_type = []
# org_ministry = []
# buyer_name = []
# buyer_address = []
#
# for pdf_no in range(1, 1):
#     # Read the file
#     file_name = f"{pdf_no}.pdf"
#     reader = PdfReader(file_name)
#     page = reader.pages[0]
#
#     # Get the text
#     text = page.extract_text().split("\n")
#
#     # Get Contract No.
#     index = [i + 2 for i, x in enumerate(text) if x == "Contract No:"]
#     contract_no.append(text[index[0]])
#
#     # Get Organisation type
#     index = [i + 1 for i, x in enumerate(text) if x == "Type:"]
#     org_type.append(text[index[0]])
#
#     # Get Organisation ministry
#     index = [i + 1 for i, x in enumerate(text) if x == "Ministry:"]
#     org_ministry.append(text[index[0]])
#
#     # Get Buyer Name
#     index = [i + 1 for i, x in enumerate(text) if x == "Name:"]
#     buyer_name.append(text[index[0]])
#
#     # Get Buyer Address
#     index = [i + 1 for i, x in enumerate(text) if x == "Address:"]
#     address = ""
#     blank_index = [i for i, x in enumerate(text[index[0]:]) if x == " "]
#
#     for item in text[index[0]:index[0] + blank_index[0]]:
#         address = address + item
#     buyer_address.append(address)
#
#
# data = pd.DataFrame({"contract_no": contract_no, "org_type": org_type, "org_ministry": org_ministry, "buyer_name": buyer_name, buyer_address: buyer_address })
# data.to_excel("data.xlsx", index=False)