import os
from PIL import Image


TEST_IMAGE_LOCATION = "unmask/0006.jpg"
# TRAINING_FILE_LOCATION = "training_sheet.txt"
OUTPUT_IMAGE_NAME = "output_image2.png"

OUTPUT_IMAGE=[]
#change as per need
UNMASK_DIR = '/home/shan/Downloads/HumanSkinDetection-NaiveByes-Python/unmask/'
MASK_DIR = '/home/shan/Downloads/HumanSkinDetection-NaiveByes-Python/mask/'
TRAINING_SHEET = "training_sheet.txt"
skin='skin.txt'
noskin='noskin.txt'
THRESHOLD = float(input("Enter Threshold(0-1): "))
MY_HASH_LIST = {}

SKIN_ARRAY = [0] * (256 ** 3)
NON_SKIN_ARRAY = [0] * (256 ** 3)
skinCount = nonSkinCount = 0

unmask_file_names = os.listdir(UNMASK_DIR)
mask_file_names = os.listdir(MASK_DIR)
mask_file_names.sort()
unmask_file_names.sort()
for i in range(len(mask_file_names)):
    print(i * 100 / len(unmask_file_names), "%")
    mask_image = list(Image.open(MASK_DIR + mask_file_names[i], "r").getdata())
    unmask_image = list(Image.open(UNMASK_DIR + unmask_file_names[i], "r").getdata())
    for j in range(len(mask_image)):
        r_mask, g_mask, b_mask = mask_image[j]
        r_unmask, g_unmask, b_unmask = unmask_image[j]
        idx = 255*255*r_unmask + 255*g_unmask + b_unmask
        if (r_mask < 255) and (g_mask < 255) and (b_mask < 255):
            SKIN_ARRAY[idx] += 1
            skinCount += 1
        else:
            NON_SKIN_ARRAY[idx] += 1
            nonSkinCount += 1
# with open(skin, 'w') as f:
#     for item in SKIN_ARRAY:
#         if item!=0:
#             f.write("%s\n" % item)
# with open(noskin, 'w') as f:
#     for item in NON_SKIN_ARRAY:
#         if item!=0:
#             f.write("%s\n" % item)

print("Creating Training Sheet")
print(skinCount,nonSkinCount)

# with open(TRAINING_SHEET, 'w') as f:
for i in range(len(SKIN_ARRAY)):
    skinValue = SKIN_ARRAY[i]/skinCount
    nonSkinValue = NON_SKIN_ARRAY[i]/nonSkinCount
    if nonSkinValue != 0 and skinValue != 0:
        threshold = skinValue / nonSkinValue
        if threshold > THRESHOLD:
            MY_HASH_LIST[str(i)] = ""
            # f.write(str(i) + "\n")


im=Image.open(TEST_IMAGE_LOCATION, "r")
pix_val=list(im.getdata())

for rgb in pix_val:
    r_unmask, g_unmask, b_unmask = rgb
    key = str(255*255*r_unmask + 255*g_unmask + b_unmask)

    if key in MY_HASH_LIST:
        OUTPUT_IMAGE.append((r_unmask, g_unmask, b_unmask))
    else:
        OUTPUT_IMAGE.append((255, 255, 255))

im.putdata(OUTPUT_IMAGE)
im.save(OUTPUT_IMAGE_NAME)


print("Complete")
