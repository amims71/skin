from PIL import Image

# change as per need
TEST_IMAGE_LOCATION = "test.jpg"
TRAINING_FILE_LOCATION = "training_sheet.txt"
OUTPUT_IMAGE_NAME = "output_image.png"

OUTPUT_IMAGE=[]
MY_HASH_LIST = {}

im=Image.open(TEST_IMAGE_LOCATION, "r")                    # read image from image location
pix_val=list(im.getdata())                                 # get all pixel values from image

for line in open(TRAINING_FILE_LOCATION).readlines():      # read each line from training sheet
    MY_HASH_LIST[line.strip()] = ""                        # add that value to dictionary so that searching is easy

for rgb in pix_val:                                        # search for every pixel of the test image
    r_unmask, g_unmask, b_unmask = rgb                     # get rgb value of that pixel
    key = str(255*255*r_unmask + 255*g_unmask + b_unmask)  # get index position of that rgb value

    if key in MY_HASH_LIST:                                # if that index in present in dictionary, it means it is a skin
        OUTPUT_IMAGE.append((255, 255, 255))               # add pixel as white
    else:                                                  # else non skin
        OUTPUT_IMAGE.append((0, 0, 0))                     # add pixel as black


im.putdata(OUTPUT_IMAGE)
im.save(OUTPUT_IMAGE_NAME)                                 # save image