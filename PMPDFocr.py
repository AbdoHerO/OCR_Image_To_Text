import fitz

input_pdf_path = "data/mod02.pdf"
output_text_path = "output.txt"

try:
    # Open the PDF file
    doc = fitz.open(input_pdf_path)

    # Create a text output file
    with open(output_text_path, "w", encoding="utf-8") as out:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)

            # Extract text from the page
            text = page.get_text()

            # Write text to the output file
            out.write(text + "\n\n")  # Add newlines between pages

    print("Text extraction completed successfully.")

except Exception as e:
    print("Error:", e)
