# from imutils import paths
# import imutils
from PIL import ImageFilter
import numpy as np
import cv2
# import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import os

# ---------- Image preprocessing steps for many parts of image to a folder ----------

# Define your main directory containing subfolders of images
main_directory = "../data/output_cropage"

# Define your output directory
output_directory = "../data/output_cropage_Processed"

def display(im_path):
    dpi = 80
    im_data = plt.imread(im_path)

    height, width = im_data.shape[:2]

    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)

    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([1, 1, 0, 0])

    # Hide spines, ticks, etc.
    ax.axis('off')

    # Display the image.
    ax.imshow(im_data, cmap='gray')

    plt.show()

def deskew(image):
    # Find coordinates of non-zero pixels
    co_ords = np.where(image > 0)

    # Convert the row and column indices to a two-dimensional array
    co_ords = np.column_stack((co_ords[1], co_ords[0])).astype(np.float32)

    # Calculate the angle of rotation
    angle = cv2.minAreaRect(co_ords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # Get image dimensions
    (h, w) = image.shape[:2]

    # Calculate the center point
    center = (w // 2, h // 2)

    # Generate rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Apply rotation to the image
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated

def noise_removal(image):
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return (image)

def thin_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)  # should be (2,2)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)

def thick_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)

def processing_the_img(image):
    # -- - Skew Correction
    skew_correction = deskew(image)

    # 1 - Inverted Images
    inverted_image = cv2.bitwise_not(image)

    # 2 - Binarization - Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # cv2.COLOR_BGR2GRAY || cv2.COLOR_RGB2GRAY
    # plt.imshow(cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB))
    # plt.show()

    # Apply Gaussian blur to remove noise
    # blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)


    # 3 - Threshold - Apply thresholding to create a binary image
    _, binary_image = cv2.threshold(gray_image, 210, 255, cv2.THRESH_BINARY )  # cv2.THRESH_OTSU

    # 4 - Noise Removal
    no_noise = noise_removal(binary_image)

    # 5 - Dilation and Erosion
    eroded_image = thin_font(no_noise)

    # 6 - Thick Font
    dilated_image = thick_font(no_noise)

    # 7 - Removing Shadows
    rgb_planes = cv2.split(dilated_image)
    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        result_planes.append(diff_img)
    img = cv2.merge(result_planes)

    eroded_image = thin_font(img)

    return eroded_image
    # plt.imshow(cv2.cvtColor(eroded_image, cv2.COLOR_GRAY2RGB))
    # plt.show()


# Loop through each sub-folder in the main directory
for folder_name in os.listdir(main_directory):
    folder_path = os.path.join(main_directory, folder_name)

    # Make sure it's a directory
    if os.path.isdir(folder_path):

        # Create a corresponding output folder
        output_folder_path = os.path.join(output_directory, folder_name + '__Processed')
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        # Loop through each image in the sub-folder
        for image_name in os.listdir(folder_path):
            if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(folder_path, image_name)
                image = cv2.imread(image_path)

                # Apply the preprocessing functions to the image
                preprocessed_image = processing_the_img(image)

                # Save the processed image in the new folder with the modified name
                processed_image_path = os.path.join(output_folder_path, image_name.split('.')[0] + '__Processed.jpg')
                cv2.imwrite(processed_image_path, preprocessed_image)

                # Sshow the processed image
                # plt.imshow(cv2.cvtColor(preprocessed_image, cv2.COLOR_BGR2RGB))
                # plt.show()


















# ------------- Single Image --------------
# # Load the image
# image_nameimage_name = 'BLS_1_croped_labels'
# original_image = cv2.imread('../data/models/' + image_name + '.jpg')
#
#
# def display(im_path):
#     dpi = 80
#     im_data = plt.imread(im_path)
#
#     height, width = im_data.shape[:2]
#
#     # What size does the figure need to be in inches to fit the image?
#     figsize = width / float(dpi), height / float(dpi)
#
#     # Create a figure of the right size with one axes that takes up the full figure
#     fig = plt.figure(figsize=figsize)
#     ax = fig.add_axes([1, 1, 0, 0])
#
#     # Hide spines, ticks, etc.
#     ax.axis('off')
#
#     # Display the image.
#     ax.imshow(im_data, cmap='gray')
#
#     plt.show()
#
#
# def deskew(image):
#     # Find coordinates of non-zero pixels
#     co_ords = np.where(image > 0)
#
#     # Convert the row and column indices to a two-dimensional array
#     co_ords = np.column_stack((co_ords[1], co_ords[0])).astype(np.float32)
#
#     # Calculate the angle of rotation
#     angle = cv2.minAreaRect(co_ords)[-1]
#
#     if angle < -45:
#         angle = -(90 + angle)
#     else:
#         angle = -angle
#
#     # Get image dimensions
#     (h, w) = image.shape[:2]
#
#     # Calculate the center point
#     center = (w // 2, h // 2)
#
#     # Generate rotation matrix
#     M = cv2.getRotationMatrix2D(center, angle, 1.0)
#
#     # Apply rotation to the image
#     rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
#
#     return rotated
#
#
# def noise_removal(image):
#     import numpy as np
#     kernel = np.ones((1, 1), np.uint8)
#     image = cv2.dilate(image, kernel, iterations=1)
#     kernel = np.ones((1, 1), np.uint8)
#     image = cv2.erode(image, kernel, iterations=1)
#     image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
#     image = cv2.medianBlur(image, 3)
#     return (image)
#
#
# def thin_font(image):
#     import numpy as np
#     image = cv2.bitwise_not(image)
#     kernel = np.ones((2, 2), np.uint8)  # should be (2,2)
#     image = cv2.erode(image, kernel, iterations=1)
#     image = cv2.bitwise_not(image)
#     return (image)
#
#
# def thick_font(image):
#     import numpy as np
#     image = cv2.bitwise_not(image)
#     kernel = np.ones((2, 2), np.uint8)
#     image = cv2.dilate(image, kernel, iterations=1)
#     image = cv2.bitwise_not(image)
#     return (image)
#
#
# #
# # -- - Skew Correction
# skew_correction = deskew(original_image)
#
# # 1 - Inverted Images
# inverted_image = cv2.bitwise_not(original_image)
#
# # 2 - Binarization - Convert the image to grayscale
# gray_image = cv2.cvtColor(original_image, cv2.COLOR_RGB2GRAY)  # cv2.COLOR_BGR2GRAY || cv2.COLOR_RGB2GRAY
# # plt.imshow(cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB))
# # plt.show()
#
# # Apply Gaussian blur to remove noise
# # blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
#
#
# # 3 - Threshold - Apply thresholding to create a binary image
# _, binary_image = cv2.threshold(gray_image, 210, 255, cv2.THRESH_BINARY )  # cv2.THRESH_OTSU
#
# # 4 - Noise Removal
# no_noise = noise_removal(binary_image)
#
# # 5 - Dilation and Erosion
# eroded_image = thin_font(no_noise)
#
# # 6 - Thick Font
# dilated_image = thick_font(no_noise)
#
# # 7 - Removing Shadows
# rgb_planes = cv2.split(dilated_image)
# result_planes = []
# result_norm_planes = []
# for plane in rgb_planes:
#     dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
#     bg_img = cv2.medianBlur(dilated_img, 21)
#     diff_img = 255 - cv2.absdiff(plane, bg_img)
#     result_planes.append(diff_img)
# img = cv2.merge(result_planes)
#
# eroded_image = thin_font(img)
# plt.imshow(cv2.cvtColor(eroded_image, cv2.COLOR_GRAY2RGB))
# plt.show()
#
# # ---------------------------------------- Step 2 ----------------------------------------
#
# # Save the preprocessed image
# preprocessed_image_path = '../output_models/' + image_name + '_Processed' + '.jpg'
# cv2.imwrite(preprocessed_image_path, eroded_image)
# # cv2.imwrite(preprocessed_image_path, no_noise)














# ---------- Group Images -----------------

# #Reading the images
# for i in range(8):
#
#     # Load the image
#     image_name = 'BLS_' + str(i + 1)
#     original_image = cv2.imread('../data/models/' + image_name + '.jpg')
#
#
#
#     def display(im_path):
#         dpi = 80
#         im_data = plt.imread(im_path)
#
#         height, width  = im_data.shape[:2]
#
#         # What size does the figure need to be in inches to fit the image?
#         figsize = width / float(dpi), height / float(dpi)
#
#         # Create a figure of the right size with one axes that takes up the full figure
#         fig = plt.figure(figsize=figsize)
#         ax = fig.add_axes([1, 1, 0, 0])
#
#         # Hide spines, ticks, etc.
#         ax.axis('off')
#
#         # Display the image.
#         ax.imshow(im_data, cmap='gray')
#
#         plt.show()
#
#     def deskew(image):
#         # Find coordinates of non-zero pixels
#         co_ords = np.where(image > 0)
#
#         # Convert the row and column indices to a two-dimensional array
#         co_ords = np.column_stack((co_ords[1], co_ords[0])).astype(np.float32)
#
#         # Calculate the angle of rotation
#         angle = cv2.minAreaRect(co_ords)[-1]
#
#         if angle < -45:
#             angle = -(90 + angle)
#         else:
#             angle = -angle
#
#         # Get image dimensions
#         (h, w) = image.shape[:2]
#
#         # Calculate the center point
#         center = (w // 2, h // 2)
#
#         # Generate rotation matrix
#         M = cv2.getRotationMatrix2D(center, angle, 1.0)
#
#         # Apply rotation to the image
#         rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
#
#         return rotated
#
#     def noise_removal(image):
#         import numpy as np
#         kernel = np.ones((1, 1), np.uint8)
#         image = cv2.dilate(image, kernel, iterations=1)
#         kernel = np.ones((2, 2), np.uint8)
#         image = cv2.erode(image, kernel, iterations=1)
#         image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
#         image = cv2.medianBlur(image, 3)
#         return (image)
#
#     def thin_font(image):
#         import numpy as np
#         image = cv2.bitwise_not(image)
#         kernel = np.ones((2,2),np.uint8) # should be (2,2)
#         image = cv2.erode(image, kernel, iterations=1)
#         image = cv2.bitwise_not(image)
#         return (image)
#
#     def thick_font(image):
#         import numpy as np
#         image = cv2.bitwise_not(image)
#         kernel = np.ones((3,3),np.uint8)
#         image = cv2.dilate(image, kernel, iterations=1)
#         image = cv2.bitwise_not(image)
#         return (image)
#
#     #
#     # -- - Skew Correction
#     skew_correction = deskew(original_image)
#
#
#     # 1 - Inverted Images
#     inverted_image = cv2.bitwise_not(original_image)
#
#
#     # 2 - Binarization - Convert the image to grayscale
#     gray_image = cv2.cvtColor(original_image, cv2.COLOR_RGB2GRAY) # cv2.COLOR_BGR2GRAY || cv2.COLOR_RGB2GRAY
#     # plt.imshow(cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB))
#     # plt.show()
#
#     # Apply Gaussian blur to remove noise
#     # blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
#
#
#     # 3 - Threshold - Apply thresholding to create a binary image
#     _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU ) # cv2.THRESH_OTSU
#
#
#
#     # 4 - Noise Removal
#     no_noise = noise_removal(binary_image)
#
#
#     # 5 - Dilation and Erosion
#     eroded_image = thin_font(no_noise)
#
#
#     # 6 - Thick Font
#     dilated_image = thick_font(no_noise)
#
#
#
#     # 7 - Removing Shadows
#     rgb_planes = cv2.split(dilated_image)
#     result_planes = []
#     result_norm_planes = []
#     for plane in rgb_planes:
#         dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
#         bg_img = cv2.medianBlur(dilated_img, 21)
#         diff_img = 255 - cv2.absdiff(plane, bg_img)
#         result_planes.append(diff_img)
#     img = cv2.merge(result_planes)
#
#
#
#     eroded_image = thin_font(img)
#     # plt.imshow(cv2.cvtColor(no_noise, cv2.COLOR_GRAY2RGB))
#     # plt.show()
#
#     # ---------------------------------------- Step 2 ----------------------------------------
#
#     # Save the preprocessed image
#     preprocessed_image_path = '../output_models/' + image_name + '_Processed' + '.jpg'
#     cv2.imwrite(preprocessed_image_path, no_noise)
