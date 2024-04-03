import keras_ocr
import tensorflow as tf


# Print the version of keras_ocr
print("Keras-OCR Version:", keras_ocr.__version__)

# Print the version of TensorFlow
print("TensorFlow Version:", tf.__version__)
#

import glob
# import pandas as pd
import matplotlib.pyplot as plt

img = glob.glob('data/simple_test.jpg')

pipeline = keras_ocr.pipeline.Pipeline()
results = pipeline.recognize(
    [img[0]],
    # Uncomment the next lines to see messier results
    # detection_kwargs={
    #     'detection_threshold': 0.2,
    #     'text_threshold': 0,
    #     'link_threshold': 0,
    #     'size_threshold': 1,
    # },
)

df = pd.DataFrame(results[0], columns=['text', 'bbox'])
pd.set_option('display.max_columns', None)  # To display all columns
print(df.head())

# Code to display image with bounding boxes
fig, ax = plt.subplots(figsize=(10, 10))
keras_ocr.tools.drawAnnotations(plt.imread(img[0]), results[0], ax=ax)
ax.set_title('Keras OCR Result Example')
plt.show()