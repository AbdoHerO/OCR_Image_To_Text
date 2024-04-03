import keras_ocr
import tensorflow as tf


# Print the version of keras_ocr
print("Keras-OCR Version:", keras_ocr.__version__)

# Print the version of TensorFlow
print("TensorFlow Version:", tf.__version__)
#

from matplotlib import pyplot as plt
import matplotlib.pyplot as plt

# keras-ocr will automatically download pretrained
# weights for the detector and recognizer.
pipeline = keras_ocr.pipeline.Pipeline()

# Get a set of three example images
images = [
    keras_ocr.tools.read(url) for url in [
        'data/simple_test.jpg'
    ]
]

# Each list of predictions in prediction_groups is a list of
# (word, box) tuples.
prediction_groups = pipeline.recognize(images)

# Plot the predictions
fig, axs = plt.subplots(nrows=len(images), figsize=(20, 20))
for ax, image, predictions in zip(axs, images, prediction_groups):
    keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)

