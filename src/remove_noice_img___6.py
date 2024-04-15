#Getting the imports
import cv2

#Reading the image
img = cv2.imread('../data/bw_image_new_bl___.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img = cv2.resize(img, (20, 900))

_, result = cv2.threshold(img, 20, 255, cv2.THRESH_BINARY)

adaptive_result = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 105, 5)

cv2.imshow("Original", img)
cv2.imshow("Adaptive", adaptive_result)

cv2.imwrite('../output_results/Adaptive_ORG_bw_image_new_bl___.jpg', adaptive_result)

cv2.waitKey(0)
cv2.destroyAllWindows()
