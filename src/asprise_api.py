# View complete code at: https://github.com/Asprise/receipt-ocr/tree/main/python-receipt-ocr
# import requests
#
# print("=== Python Receipt OCR Demo - Need help? Email support@asprise.com ===")
#
# receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt' # Receipt OCR API endpoint
# imageFile = "../data/new_bl.pdf" # // Modify this to use your own file if necessary
# r = requests.post(receiptOcrEndpoint, data = { \
#   'api_key': 'TEST',        # Use 'TEST' for testing purpose \
#   'recognizer': 'auto',       # can be 'US', 'CA', 'JP', 'SG' or 'auto' \
#   'ref_no': 'test', # optional caller provided ref code \
#   }, \
#   files = {"file": open(imageFile, "rb")})
#
# print(r.text) # result in JSON







# ---------------------------------------------------------------------------------------------------------------


# import os
# # os.environ["ASPRISE_OCR_DLL_PATH"] = r"C:\Users\abder\Downloads\asprise-ocr-csharp-vb.net-15.3.1-trail python"
# from asprise_ocr_api import *
# from asprise_ocr_api import *
# from asprise_ocr_api.ocr import Ocr, OCR_PAGES_ALL, OCR_RECOGNIZE_TYPE_TEXT, OCR_OUTPUT_FORMAT_PLAINTEXT
#
#
# os.environ["ASPRISE_OCR_DLL_PATH"] = r"C:\aocr_x64_dll"
# # print(os.environ.get('ASPRISE_OCR_DLL_PATH'))
#
# ocr = Ocr()
# ocr.start_engine("fra")  # deu, fra, por, spa - more than 30 languages are supported
#
# # ocr.recognize("../data/new_lb_rimini_croped.jpg", -1, -1, -1, -1, -1,
# #                     OCR_RECOGNIZE_TYPE_ALL, OCR_OUTPUT_FORMAT_PDF,
# #                     PROP_PDF_OUTPUT_FILE="ocr-result___new_lb_rimini_croped.jpg___.pdf",
# #                     PROP_PDF_OUTPUT_TEXT_VISIBLE=False)
#
# text = ocr.recognize(
#     "../data/new_bl.pdf",  # gif, jpg, pdf, png, tif, etc.
#     OCR_PAGES_ALL,  # the index of the selected page
#     -1, -1, -1, -1,  # you may optionally specify a region on the page instead of the whole page
#     # OCR_RECOGNIZE_TYPE_TEXT,  # recognize type: TEXT, BARCODES or ALL
#     OCR_RECOGNIZE_TYPE_ALL,  # recognize type: TEXT, BARCODES or ALL
#     OCR_OUTPUT_FORMAT_PLAINTEXT  # output format: TEXT, XML, or PDF
# )
# #
# # ocr.recognize("../data/new_bl.pdf", -1, -1, -1, -1, -1,
# #                     OCR_RECOGNIZE_TYPE_ALL, OCR_OUTPUT_FORMAT_PDF,
# #                     PROP_PDF_OUTPUT_FILE="ocr-result.pdf",
# #                     PROP_PDF_OUTPUT_TEXT_VISIBLE=True)
#
# # ocr.recognize("test-image.png", -1, -1, -1, -1, -1,
# #                     OCR_RECOGNIZE_TYPE_ALL, OCR_OUTPUT_FORMAT_RTF,
# #                     PROP_RTF_OUTPUT_FILE="ocr-result.pdf")
# print ("Result: " + text)
#
# # ocr.recognize("../data/new_bl.pdf", -1, -1, -1, -1, -1,
# #                     OCR_RECOGNIZE_TYPE_ALL, OCR_OUTPUT_FORMAT_PDF,
# #                     PROP_IMG_PREPROCESS_TYPE="custom",
# #                     PROP_IMG_PREPROCESS_CUSTOM_CMDS="scale(2);default()",
# #                     PROP_PDF_OUTPUT_FILE="ocr-result.pdf") # scale up
#
#
# # ocr.recognize("../data/new_bl_croped.jpg", -1, -1, -1, -1, -1,
# #                     OCR_RECOGNIZE_TYPE_ALL, OCR_OUTPUT_FORMAT_PDF,
# #                     PROP_IMG_PREPROCESS_TYPE="custom",
# #                     PROP_IMG_PREPROCESS_CUSTOM_CMDS="scale(2);default()", # invert();default() - invert color
# #                     PROP_PDF_OUTPUT_FILE="ocr-result.pdf") # scale up
#
#
#
# # ocr.recognize (more_images...)
#
# ocr.stop_engine()











import os
import json
import cv2
from asprise_ocr_api import Ocr, OCR_PAGES_ALL, OCR_RECOGNIZE_TYPE_TEXT, OCR_OUTPUT_FORMAT_PLAINTEXT
os.environ["ASPRISE_OCR_DLL_PATH"] = r"C:\aocr_x64_dll"
ocr = Ocr()
ocr.start_engine("fra")
image_path = "../data/new_bl.pdf"
# Preprocessing the image using OpenCV
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
scaled = cv2.resize(gray, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_LINEAR)
_, thresh = cv2.threshold(scaled, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
preprocessed_image_path = "preprocessed_image.jpg"
cv2.imwrite(preprocessed_image_path, thresh)
text = ocr.recognize(
    preprocessed_image_path,
    OCR_PAGES_ALL,
    -1, -1, -1, -1,
    OCR_RECOGNIZE_TYPE_TEXT,
    OCR_OUTPUT_FORMAT_PLAINTEXT
)
result_json = json.dumps({"ocr_text": text})
print("OCR Result in JSON: " + result_json)
ocr.stop_engine()




