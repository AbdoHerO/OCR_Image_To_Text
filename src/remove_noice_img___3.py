import cv2
import matplotlib.pyplot as plt
from scipy.signal import convolve2d

# Load the noisy image
noisy_image = cv2.imread('../data/mod02.jpg', cv2.IMREAD_UNCHANGED)

# Convert the noisy image to grayscale
noisy_image_gray = cv2.cvtColor(noisy_image, cv2.COLOR_BGR2GRAY)

# Wiener filtering
wiener_image = cv2.medianBlur(noisy_image_gray, 5)
wiener_image = cv2.medianBlur(wiener_image, 5)
wiener_image = cv2.medianBlur(wiener_image, 5)
wiener_image = cv2.medianBlur(wiener_image, 5)
wiener_image = cv2.medianBlur(wiener_image, 5)
wiener_image = cv2.medianBlur(wiener_image, 5)
wiener_image = cv2.medianBlur(wiener_image, 5)

# Deconvolution
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
degraded_image = cv2.erode(noisy_image_gray, kernel, iterations=1)
deconv_image = convolve2d(degraded_image, kernel, mode='same')

# Non-Local Means Denoising
nlm_image = cv2.fastNlMeansDenoisingColored(noisy_image, None, 10, 10, 7, 21)

# Display the results
plt.figure(figsize=(10, 10))

plt.subplot(221)
plt.imshow(cv2.cvtColor(noisy_image, cv2.COLOR_BGR2RGB))
plt.title('Noisy Image')

plt.subplot(222)
plt.imshow(wiener_image, cmap='gray')
plt.title('Wiener Filter')

plt.subplot(223)
plt.imshow(deconv_image, cmap='gray')
plt.title('Deconvolution')

plt.subplot(224)
plt.imshow(cv2.cvtColor(nlm_image, cv2.COLOR_BGR2RGB))
plt.title('Non-Local Means Denoising')

plt.show()





# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
#
# # Load the image
# img = cv2.imread('../data/mod02.jpg')
#
# # Display the original image
# plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
# plt.title('Original Image')
# plt.show()
#
# # Add speckle noise
# speckle = np.random.randn(*img.shape) * 0.1
# noisy_img = np.clip(img + img * speckle, 0, 255).astype(np.uint8)
#
# # Display the image with added speckle noise
# plt.imshow(cv2.cvtColor(noisy_img, cv2.COLOR_BGR2RGB))
# plt.title('Speckle Noise')
# plt.show()



# from PIL import Image
# import numpy as np
# import matplotlib.pyplot as plt
# import random
#
# # Load the image
# image_path = '../data/mod02.jpg'
# original_image = Image.open(image_path)
#
# # Convert the image to a NumPy array
# image_array = np.array(original_image)
#
# # Function to add salt and pepper noise to the image
# def add_salt_and_pepper_noise(image, salt_prob, pepper_prob):
#     noisy_image = np.copy(image)
#     height, width, channels = noisy_image.shape
#     for i in range(height):
#         for j in range(width):
#             rand = random.random()
#             if rand < salt_prob:
#                 noisy_image[i, j] = [255, 255, 255]  # Add salt noise
#             elif rand > 1 - pepper_prob:
#                 noisy_image[i, j] = [0, 0, 0]  # Add pepper noise
#     return noisy_image
#
# # Add salt and pepper noise to the image
# noisy_image_salt_pepper = add_salt_and_pepper_noise(image_array, salt_prob=0.01, pepper_prob=0.01)
#
# noisy_image_salt_pepper = Image.fromarray(noisy_image_salt_pepper)
#
# # Display the original and corrupted images
# fig, axs = plt.subplots(1, 2, figsize=(12, 4))
# axs[0].imshow(original_image)
# axs[0].set_title('Original Image')
# axs[0].axis('off')
# axs[1].imshow(noisy_image_salt_pepper)
# axs[1].set_title('Salt and Pepper Noise')
# axs[1].axis('off')
# plt.tight_layout()
# plt.show()