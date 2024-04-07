# View complete code at: https://github.com/Asprise/receipt-ocr/tree/main/python-receipt-ocr
import requests

print("=== Python Receipt OCR Demo - Need help? Email support@asprise.com ===")

receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt' # Receipt OCR API endpoint
imageFile = "../data/mod01.pdf" # // Modify this to use your own file if necessary
r = requests.post(receiptOcrEndpoint, data = { \
  'api_key': 'TEST',        # Use 'TEST' for testing purpose \
  'recognizer': 'auto',       # can be 'US', 'CA', 'JP', 'SG' or 'auto' \
  'ref_no': 'ez', # optional caller provided ref code \
  }, \
  files = {"file": open(imageFile, "rb")})

print(r.text) # result in JSON


# import os
# os.environ["ASPRISE_OCR_DLL_PATH"] = r"C:\Users\abder\Downloads\asprise-ocr-csharp-vb.net-15.3.1-trail python"
# from asprise_ocr_api import *
# from asprise_ocr_api import *
# from asprise_ocr_api.ocr import Ocr, OCR_PAGES_ALL, OCR_RECOGNIZE_TYPE_TEXT, OCR_OUTPUT_FORMAT_PLAINTEXT

# ocr = Ocr()
# ocr.start_engine("eng")  # deu, fra, por, spa - more than 30 languages are supported
# text = ocr.recognize(
#     "../data/new_bl.pdf",  # gif, jpg, pdf, png, tif, etc.
#     OCR_PAGES_ALL,  # the index of the selected page
#     -1, -1, -1, -1,  # you may optionally specify a region on the page instead of the whole page
#     OCR_RECOGNIZE_TYPE_TEXT,  # recognize type: TEXT, BARCODES or ALL
#     OCR_OUTPUT_FORMAT_PLAINTEXT  # output format: TEXT, XML, or PDF
# )
# print ("Result: " + text)

# # ocr.recognize(more_images...)

# ocr.stop_engine()

