import PyPDF2
import json
import re


def extract_text_from_pdf(pdf_file_path):
    # Open the PDF file
    with open(pdf_file_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)

        # Initialize an empty list to store extracted lines
        lines = []

        # Iterate through each page in the PDF
        for page_num in range(len(pdf_reader.pages)):
            # Get the text from the current page
            page_text = pdf_reader.pages[page_num].extract_text()

            # Split the text into lines and add them to the list
            lines.extend(page_text.split('\n'))

    return lines


def apply_filter(lines):
    filtered_lines = []
    for line in lines:
        if '|' in line:
            if ')' in line:
                parts = line.split('|')
                parts_2 = parts[0].split(')')
                filtered_lines.append(parts_2[1].strip())
                pushInObjectJSON(parts_2[1],parts[1], None)

            else:
                parts = line.split('|')
                filtered_lines.append(parts[1].strip())
                pushInObjectJSON(parts[1], parts[2], parts[0])

    return filtered_lines

def pushInObjectJSON(content_par1, content_par2, content_of_qty):

    # Define regular expression patterns
    price_pattern = r'\b\d+,\d{2}\b'
    remove_pattern = r'[.,]00\b'
    lot_pattern = r'\b([\w\s/]+)\s\d{2}/\d{2}/\d{4}$' # r'^([\w\s]+)\s'  # Matches the digits at the beginning of the string
    date_pattern = r'\d{2}/\d{2}/\d{4}$'  # Matches the date format dd/mm/yyyy

    row = {}

    if content_par1 is not None:
        # Find the price in the input string
        price_matches = re.findall(price_pattern, content_par1.strip())
        price_string = price_matches[0] if price_matches else "Price not found"

        # Remove the price from the input string
        product_name_string = re.sub(remove_pattern, '', content_par1.strip())

        row["product_name_string"] = product_name_string
        row["price"] = price_string

        #data.append({"product_name": product_name_string, "price": price_string})

    if content_par2 is not None:
        # Find the LOT and Date in the input string
        lot_match = re.search(lot_pattern, content_par2)
        date_match = re.search(date_pattern, content_par2)

        # Extract LOT and Date if found
        lot = lot_match.group(1) if lot_match else "Lot not found"
        date_peremption = date_match.group() if date_match else "Date not found"

        row["LOT"] = lot
        row["Date_peremption"] = date_peremption

        #data.append({"LOT": lot, "Date_peremption": date_peremption})

    if content_of_qty is not None:
        # Split the input string based on spaces
        parts = content_of_qty.split()

        if len(parts) > 1:
            row["Quantite Commande"] = parts[0]
            row["Quantite Livre"] = parts[1]
        elif len(parts) == 1:
            row["Quantite Livre"] = parts[0]


    data.append(row)



data = []
# Example usage
pdf_file_path = '../output_results/output_croped.pdf'  # Provide the path to your PDF file

lines_array = extract_text_from_pdf(pdf_file_path)
filtered_lines = apply_filter(lines_array)

for line in filtered_lines:
    print(line)


# Export to JSON
with open('../output_json/products.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(lines_array)



## Filter with removing the other lines like head of columns
# def apply_filter(lines):
#     filtered_lines = []
#     for line in lines:
#         if '|' in line:
#             if ')' in line:
#                 parts = line.split('|')
#                 parts_2 = parts[0].split(')')
#                 filtered_lines.append(parts_2[1].strip())
#             else:
#                 parts = line.split('|')
#                 filtered_lines.append(parts[1].strip())
#     return filtered_lines


## Filter without removing the other lines like head of columns
# def apply_filter(lines):
#     filtered_lines = []
#     for line in lines:
#         parts = line.split('|')
#         if len(parts) >= 2:
#             filtered_lines.append(parts[1].strip())
#         else:
#             alternative_parts = line.split(')')
#             filtered_lines.append(alternative_parts[-1].strip())
#     return filtered_lines
