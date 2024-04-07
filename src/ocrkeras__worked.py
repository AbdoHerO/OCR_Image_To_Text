# pip install keras-ocr
# pip install glob2

import matplotlib.pyplot as plt
import glob
import keras_ocr

import urllib.request  # Import the module for downloading files

# Print the version of keras_ocr
print("Keras-OCR Version:", keras_ocr.__version__)



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