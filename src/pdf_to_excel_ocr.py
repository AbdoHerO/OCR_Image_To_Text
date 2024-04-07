from PyPDF2 import PdfReader
import pandas as pd

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

column_names = ["Quantité Commandée", "Quantité Livrée", "Désignation", "P.P.M.", "LOT", "Date péremptic"]
data_dict = {name: [] for name in column_names}

# Read the file
file_name = "../data/new_lb.pdf"
reader = PdfReader(file_name)
page = reader.pages[0]

# Get the text
text = page.extract_text().split("\n")

for column_name in column_names:
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