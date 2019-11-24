from PIL import Image
import os
import numpy as np

skinArray = np.zeros((256, 256, 256))
nonSkinArray = np.zeros((256, 256, 256))
bayes = np.zeros((256, 256, 256))
white_pixel = (250, 250, 250)
skinCount = 0
nonSkinCount = 0
maskPath = '/home/shan/Downloads/HumanSkinDetection-NaiveByes-Python/mask'
unMaskPath = '/home/shan/Downloads/HumanSkinDetection-NaiveByes-Python/unmask'
mask = os.listdir(maskPath)
unMask = os.listdir(unMaskPath)
print("Training Started....\n Preparing Data........")
for i in range(len(mask)):
    print(i * 100 / len(mask), "%")   # print percentage done
    xpathMask = os.path.join(maskPath, mask[i])
    xpathUnMask = os.path.join(unMaskPath, unMask[i])
    imgMask = Image.open(xpathMask)
    imgUnMask = Image.open(xpathUnMask)
    pixelsMask = imgMask.load()
    pixelsUnMask = imgUnMask.load()
    width, height = imgMask.size
    for x in range(width):
        for y in range(height):
            c = pixelsMask[x, y]
            c2 = pixelsUnMask[x, y]
            if c < white_pixel:
                skinArray[c2[0], c2[1], c2[2]] += 1
                skinCount += 1
            else:
                nonSkinArray[c2[0], c2[1], c2[2]] += 1
                nonSkinCount += 1
with open("training_sheet.txt", "w") as text_file:
    for r in range(256):
        for g in range(256):
            for b in range(256):
                skinArray[r][g][b] /= skinCount
                nonSkinArray[r][g][b] /= nonSkinCount
                val = 0
                if nonSkinArray[r][g][b] != 0 and skinArray[r][g][b] != 0:
                    val = skinArray[r][g][b] / nonSkinArray[r][g][b]
                else:
                    val = 0.0000
                bayes[r][g][b] = val
                if val > 0.4:
                    # print(r, "-", g, "-", b, "-", bayes[r][g][b], file=text_file)
                    print(str(r)+str(g)+str(b), file=text_file)
print("Training Sheet Complete")
# imgTest = Image.open("H:\\CSE\\Python\\Demo\\test.jpg")
# pixelsTest = imgTest.load()
# testWidth, testHeight = imgTest.size
# img = Image.new('RGB', (testWidth, testHeight))
# for x in range(testWidth):
#     for y in range(testHeight):
#         c = pixelsTest[x, y]
#         if bayes[c[0], c[1], c[2]] > 0.4:
#             img.putpixel((x, y), white_pixel)
#         else:
#             img.putpixel((x, y), (0, 0, 0))
# img.save('output.jpg')
