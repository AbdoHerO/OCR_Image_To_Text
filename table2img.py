from img2table.document import PDF
from img2table.ocr import TesseractOCR

# Instantiation of the pdf
pdf = PDF(src="data/new_bl_croped.jpg")

# Instantiation of the OCR, Tesseract, which requires prior installation
ocr = TesseractOCR(lang="eng")

# Table identification and extraction
pdf_tables = pdf.extract_tables(ocr=ocr)

# We can also create an excel file with the tables
pdf.to_xlsx('output_results/tables__.xlsx',
            ocr=ocr)