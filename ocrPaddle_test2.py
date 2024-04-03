# ---------- Showing the image with the text above ---------------

# from paddleocr import PaddleOCR, draw_ocr
# import cv2
#
# # Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# # You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# # to switch the language model in order.
# ocr = PaddleOCR(use_angle_cls=True, lang='fr')  # need to run only once to download and load model into memory
#
# img_path = 'data/mod01.jpg'
#
# img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
# cv2.imshow('Image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# result = ocr.ocr(img_path, cls=True)
# for line in result:
#     print(line)
#
# # draw result
# from PIL import Image, ImageDraw, ImageFont
#
# image = Image.open(img_path).convert('RGB')
#
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
# font = ImageFont.load_default()
#
# # Modify the font path according to your Arial font location
# im_show = draw_ocr(image, boxes, txts, scores, font_path='C:/Windows/Fonts/arial.ttf')
# im_show.save('result.jpg')


# ---------- Extract just the text above ---------------


from paddleocr import PaddleOCR, draw_ocr
import cv2

# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.
ocr = PaddleOCR(use_angle_cls=True, lang='fr')  # need to run only once to download and load model into memory

img_path = 'data/mod01.jpg'

# img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
# cv2.imshow('Image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

print("Result ---------------------------------------------------")

result = ocr.ocr(img_path, cls=True)
for line in result:
    print(line)

# # draw result
# from PIL import Image, ImageDraw, ImageFont
#
# image = Image.open(img_path).convert('RGB')
#
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
# font = ImageFont.load_default()
#
# # Modify the font path according to your Arial font location
# im_show = draw_ocr(image, boxes, txts, scores, font_path='C:/Windows/Fonts/arial.ttf')
# im_show.save('result.jpg')

