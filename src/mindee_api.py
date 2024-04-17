import requests

url = "https://api.mindee.net/v1/products/mindee/invoices/v4/predict"

with open("../data/new_bl.jpg", "rb") as bl_doc:
    files = {"document": bl_doc}
    headers = {"Authorization": "Token 219a21488f05bbb3ebc1acd87b857e37"}
    response = requests.post(url, files=files, headers=headers)
    print(response.text)






from mindee import Client, PredictResponse, product
import json

# Init a new client
mindee_client = Client(api_key="219a21488f05bbb3ebc1acd87b857e37")

# Add your custom endpoint (document)
my_endpoint = mindee_client.create_endpoint(
    account_name="my-account",
    endpoint_name="my-endpoint",
)

# Load a file from disk
input_doc = mindee_client.source_from_path("../data/new_bl.jpg")


# Parse the file.
# The endpoint must be specified since it cannot be determined from the class.
result = mindee_client.parse(
    product.InvoiceV4,
    input_doc,
    # endpoint=my_endpoint
)


# Print a brief summary of the parsed data
# print(result.document)
print(result.document.inference.prediction)
for line_items_elem in result.document.inference.prediction.line_items:
    print(line_items_elem)
