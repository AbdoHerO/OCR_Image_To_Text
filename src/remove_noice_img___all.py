#Getting the imports
import cv2
import numpy as np

# *--------------------------------------------------------* Step 1 *--------------------------------------------------------*

#Reading the image
for i in range(8):
    
        img_name = 'BLS_' + str(i + 1)
        img = cv2.imread('../data/models/' + img_name + '.jpg')

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to smooth the image (reduce noise)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply adaptive thresholding to create a binary image
        # Adaptive thresholding calculates the threshold value for small regions of the image
        # This helps in handling varying lighting conditions across the image
        binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 17, 5)

        #Gaussian Kernal for sharpening
        gaussian_blur = cv2.GaussianBlur(img, (7,7), 2)

        #Sharpening using addWeighted()
        sharpened1 = cv2.addWeighted(img, 1.5, gaussian_blur, -0.5, 0)
        sharpened2 = cv2.addWeighted(img, 3.5, gaussian_blur, -2.5, 0)
        sharpened4 = cv2.addWeighted(img, 7.5, gaussian_blur, -6.5, 0)
        sharpened___ = cv2.addWeighted(img, 5.5, gaussian_blur, -4.5, 0)

        # Save the sharpened image
        cv2.imwrite('../output_models/binary_' + img_name + '.jpg', binary)
        cv2.imwrite('../output_models/sharpened_' + img_name + '.jpg', sharpened___)

        cv2.imwrite('../data/binary_' + img_name + '.jpg', binary)

        # *--------------------------------------------------------* Step 2 *--------------------------------------------------------*

        img_to_transformer_step_2 = cv2.imread('../data/binary_' + img_name + '.jpg')
        rows, cols = img_to_transformer_step_2.shape[:2]

        #Bilateral filtring (Reduction of noise + Preserving of edges)
        output_bil = cv2.bilateralFilter(img_to_transformer_step_2, 5,6,6)
        cv2.imwrite('../output_models/bilateral_' + img_name + '.jpg', output_bil)



        # *--------------------------------------------------------* Step 3 - Adaptive *--------------------------------------------------------*

        img_name = 'BLS_' + str(i + 1)
        img = cv2.imread('../data/models/' + img_name + '.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, result = cv2.threshold(img, 20, 255, cv2.THRESH_BINARY)
        adaptive_result = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 105, 5)

        cv2.imwrite('../output_models/adaptive_' + img_name + '.jpg', adaptive_result)
        # *--------------------------------------------------------* Show all Windows *--------------------------------------------------------*

        cv2.waitKey(0)
        cv2.destroyAllWindows()
