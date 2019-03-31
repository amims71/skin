import os
from PIL import Image

#change as per need
UNMASK_DIR = 'H:/CSE/Python/HumanSkinDetection/unmask/'       # folder that contains all color images
MASK_DIR = 'H:/CSE/Python/HumanSkinDetection/mask/'         # folder that contains all mask images
TRAINING_SHEET = "training_sheet.txt"   # name of training sheet u want

THRESHOLD = 0.4

SKIN_ARRAY = [0] * (256 ** 3)              # initialize array with 256*256*256 length
NON_SKIN_ARRAY = [0] * (256 ** 3)
skinCount = nonSkinCount = 0

unmask_file_names = os.listdir(UNMASK_DIR)         # get all color images file names
mask_file_names = os.listdir(MASK_DIR)             # get all mask images file names

for i in range(len(mask_file_names)):              # loop through each image
    print(i * 100 / len(unmask_file_names), "%")   # print percentage done
    mask_image = list(Image.open(MASK_DIR + mask_file_names[i], "r").getdata())         # get mask image at i-th location
    unmask_image = list(Image.open(UNMASK_DIR + unmask_file_names[i], "r").getdata())   # get color image at i-th position

    for j in range(len(mask_image)):                                 # loop through each pixel of i-th position image
        r_mask, g_mask, b_mask = mask_image[j]                       # get rgb value of mask image at j-th pixel
        r_unmask, g_unmask, b_unmask = unmask_image[j]               # get rgb value of color image at j-th pixel
        idx = 255*255*r_unmask + 255*g_unmask + b_unmask             # get index using the rgb value of color image at j-th pixel
        if (r_mask < 250) and (g_mask < 250) and (b_mask < 250):     # if non-white
            SKIN_ARRAY[idx] += 1                                     # add 1 at the index position of SKIN_ARRAY
            skinCount += 1                                           # also increment total skin count
        else:                                                        # if white
            NON_SKIN_ARRAY[idx] += 1                                 # add 1 at the index position of NON_SKIN_ARRAY
            nonSkinCount += 1                                        # also increment total non skin count

print("Creating Training Sheet")
with open(TRAINING_SHEET, 'w') as f:                                 #open training sheet for writing
    for i in range(len(SKIN_ARRAY)):                                 # go through each value of the arrays
        skinValue = SKIN_ARRAY[i]/skinCount                          # get skin value by dividing the SKIN_ARRAY[i] with total skin count
        nonSkinValue = NON_SKIN_ARRAY[i]/nonSkinCount                # get non skin value by dividing NON_SKIN_ARRAY[i] with total non skin count

        ''' if nonSkinValue is 0, divide by zero occurs and if skinValue is 0, the threshold becomes 0... so no     
            need to check for those... we will be saving index values with threshold>0.4   
                                                                             '''
        if nonSkinValue != 0 and skinValue != 0:
            threshold = skinValue / nonSkinValue
            if threshold > THRESHOLD:
                f.write(str(i) + "\n")

print("Training Sheet Complete")
