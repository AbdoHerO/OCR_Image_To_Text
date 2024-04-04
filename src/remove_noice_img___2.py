from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import random

# Load the image
image_path = '../data/mod02.jpg'
original_image = Image.open(image_path)

# Convert the image to a NumPy array
image_array = np.array(original_image)

# Function to add Gaussian noise to the image
def add_gaussian_noise(image, mean, std_dev):
    noise = np.random.normal(mean, std_dev, image.shape).astype(np.uint8)
    noisy_image = np.clip(image + noise, 0, 255)
    return noisy_image


# Add Gaussian noise to the image
noisy_image_gaussian = add_gaussian_noise(image_array, mean=0, std_dev=30)


# Convert the NumPy arrays back to images
noisy_image_gaussian = Image.fromarray(noisy_image_gaussian)

# Display the original and corrupted images
fig, axs = plt.subplots(1, 2, figsize=(12, 4))
axs[0].imshow(original_image)
axs[0].set_title('Original Image')
axs[0].axis('off')
axs[1].imshow(noisy_image_gaussian)
axs[1].set_title('Gaussian Noise')
axs[1].axis('off')


plt.tight_layout()
plt.show()



# --------------------------------------------------------------------

# from skimage import io
# from skimage.filters import gaussian
# from skimage.util import img_as_float64
# import cv2
#
# # Load the image with OpenCV
# img_bgr = cv2.imread('../data/mod02.jpg')
# # Convert from BGR to RGB
# img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
#
# # Convert the image to float64
# img_float64 = img_as_float64(img_rgb)
#
# # Choose one of the noisy images
# img = img_float64
#
# # Apply Gaussian blur using cv2
# gaussian_using_cv2 = cv2.GaussianBlur(img_bgr, (3,3), 0, borderType=cv2.BORDER_CONSTANT)
#
# # Apply Gaussian blur using skimage
# gaussian_using_skimage = gaussian(img, sigma=1, mode='constant', cval=0.0)
#
# # Display the images
# cv2.imshow("Original", img)
# cv2.imshow("Using cv2 Gaussian", gaussian_using_cv2)
# cv2.imshow("Using Skimage", gaussian_using_skimage)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# -------------------------------------------------------------------------------

# from skimage import io
# from skimage.filters import gaussian
# from skimage.util import img_as_float64
# import cv2
#
# img_gaussian_noice = img_as_float64(io.imread('../data/mod02.jpg', as_gray=False))
# img_salt_papper_noice = img_as_float64(io.imread('../data/mod02.jpg', as_gray=False))
#
# img = img_salt_papper_noice
#
# gaussian_using_cv2 = cv2.GaussianBlur(img, (3,3), 0, borderType= cv2.BORDER_CONSTANT)
# gaussian_using_skimage = gaussian(img, sigma=1, mode='constant', cval=0.0)
#
# cv2.imshow("Original", img)
# cv2.imshow("Using cv2 Gaussian", gaussian_using_cv2)
# cv2.imshow("Using Skimage", gaussian_using_skimage)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
