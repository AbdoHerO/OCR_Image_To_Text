# pip install keras-ocr
# pip install glob2

import matplotlib.pyplot as plt
import glob
import keras
import keras_ocr
import tensorflow as tf
import json
import os

import urllib.request  # Import the module for downloading files

# Print the version of keras_ocr
print("Keras-OCR Version:", keras.__version__)



# # URL of the image
# url = 'https://rachidcosm.dorimy.com/public/uploads/all/8YveznMtmVQdT9J3WB9BymsPbM58qEpcfWH5OEHq.jpg'
#
# # Download the image from the URL and save it locally
# urllib.request.urlretrieve(url, 'image.jpg')


# Pass the local path of the image to the pipeline
pipeline = keras_ocr.pipeline.Pipeline()
results = pipeline.recognize(
    ['../data/denoise_mod01_resized.jpg'],  # Pass the local path here
    # ['image.jpg'],  # Pass the local path here
    # Uncomment the next lines to see messier results
    # detection_kwargs={
    #     'detection_threshold': 0.2,
    #     'text_threshold': 0,
    #     'link_threshold': 0,
    #     'size_threshold': 1,
    # },
)

import pandas as pd
df = pd.DataFrame(results[0], columns=['text', 'bbox'])
pd.set_option('display.max_columns', None)  # To display all columns
print(df.head())

# Check if results are not empty before drawing bounding boxes
if results:
    # Code to display image with bounding boxes
    fig, ax = plt.subplots(figsize=(10, 10))
    keras_ocr.tools.drawAnnotations(plt.imread('../data/denoise_mod01_resized.jpg'), results[0], ax=ax)
    ax.set_title('Keras OCR Result Example')
    plt.show()
else:
    print("No text detected in the image.")


# __START__ Export the text extracted from OCR to a text file (output.txt) and a JSON file (output.json) --- **Words**

# Convert numpy arrays in results to lists
results_serializable = []
for entry in results[0]:
    text = entry[0]
    bbox = entry[1].tolist()  # Convert bounding box ndarray to list
    entry_serializable = {'text': text, 'bbox': bbox}
    results_serializable.append(entry_serializable)

# Convert the OCR results to JSON
json_results = json.dumps(results_serializable)





# Export the JSON results to a file
with open('output.json', 'w') as json_file:
    json_file.write(json_results)
#
# # Extract text from OCR results
# text = '\n'.join([entry[0] for entry in results[0]])
#
# # Export the extracted text to a text file
# with open('output.txt', 'w') as text_file:
#     text_file.write(text)


# Extract text from OCR results and concatenate into sentences
sentences = []
current_sentence = ''
for entry in results[0]:
    word = entry[0]
    # Check if the word is a space
    if word == ' ':
        current_sentence += word
    else:
        current_sentence += word + ' '
    # If the word ends with a punctuation mark, add the current sentence to the list and reset it
    if word.endswith(('.', ',', '!', '?')):
        sentences.append(current_sentence.strip())
        current_sentence = ''

# Export the extracted sentences to a text file
with open('output.txt', 'w') as text_file:
    for sentence in sentences:
        text_file.write(sentence + '\n')


# Additional information for confirmation
print("Text extracted from OCR has been exported to output.txt and output.json files.")

# __END__ Export the text extracted from OCR to a text file (output.txt) and a JSON file (output.json) --- **Words**




# __START__ Export the text extracted from OCR to a text file (output.txt) and a JSON file (output.json) --- **Sentences**

# # Combine words into sentences
# sentences = []
# current_sentence = ''
# for entry in results[0]:
#     word = entry[0]
#     if word.endswith(('.', '!', '?')):  # Check if the word ends with punctuation indicating end of sentence
#         current_sentence += word + ' '  # Add word to current sentence
#         sentences.append(current_sentence.strip())  # Add complete sentence to list
#         current_sentence = ''  # Reset current sentence
#     else:
#         current_sentence += word + ' '  # Add word to current sentence
#
# # If there's any remaining text in current sentence, add it as well
# if current_sentence:
#     sentences.append(current_sentence.strip())
#
# # Combine sentences into a single string
# text = '\n'.join(sentences)
#
# # Export the extracted text to a text file
# with open('output_sentences.txt', 'w') as text_file:
#     text_file.write(text)
#
# # Additional information for confirmation
# print("Text extracted from OCR has been exported to output_sentences.txt file.")

# __END__ Export the text extracted from OCR to a text file (output.txt) and a JSON file (output.json) --- **Sentences**


# # Download the files to local machine
# from google.colab import files
# files.download('output.json')
# files.download('output.txt')