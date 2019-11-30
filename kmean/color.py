import random
from math import sqrt, floor

from PIL import Image

# IMAGE_LOCATION = "images.jpeg"
IMAGE_LOCATION = "banner-image-human-rights-pages-november-2018_8.jpg"
OUTPUT_IMAGE_NAME = "output_image.png"

colors = 'colors.txt'
OUTPUT_IMAGE = []
# change as per need
color_count = int(input("Enter Color Count: "))
MY_HASH_LIST = {}


COLOR_ARRAY = [0] * (256 ** 3)
skinCount = nonSkinCount = 0


def distance(point1, point2):
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)


def closestPoint(point, centers):
    min = 500
    closestPoint = ()
    for center in centers:
        dist = distance(point, center)
        if dist < min:
            min = dist
            closestPoint = center
    return closestPoint


def midPoint(points):
    x, y, z = 0, 0, 0
    for point in points:
        x += point[0]
        y += point[1]
        z += point[2]
    return floor(x / len(points)), floor(y / len(points)), floor(z / len(points))


def groupPoints(centers):
    groups = {}
    for point in list(MY_HASH_LIST.keys()):
        # print(point)
        if point is not None:
            key = closestPoint(point, centers)
            # print(key)
            if key in groups:
                groups[key].extend([point] * MY_HASH_LIST[point])
                # groups[key].append(point)
            else:
                groups[key] = [point] * MY_HASH_LIST[point]
            # print(groups)
    return groups


im = Image.open(IMAGE_LOCATION, "r")
image_rgb_list = list(im.getdata())
# print(image_rgb_list)
for j in range(len(image_rgb_list)):
    r, g, b = image_rgb_list[j]
    # idx = 255*255*r + 255*g + b
    if image_rgb_list[j] in MY_HASH_LIST:
        MY_HASH_LIST[image_rgb_list[j]] += 1
    else:
        MY_HASH_LIST[image_rgb_list[j]] = 1
# print(MY_HASH_LIST)
with open(colors, 'w') as f:
    f.write(str(MY_HASH_LIST))

centers = random.sample(list(MY_HASH_LIST.keys()), color_count)

print(centers)
groups = groupPoints(centers)
centersOld = centers
centers = []
for key in groups:
    centers.append(midPoint(groups[key]))
print(centers)
while distance(centers[0], centersOld[0]) > 1:
    groups = groupPoints(centers)
    centersOld = centers
    centers = []
    for key in groups:
        centers.append(midPoint(groups[key]))
        # print(key)
    print(centers)

for rgb in image_rgb_list:
    OUTPUT_IMAGE.append(closestPoint(rgb, centers))

im.putdata(OUTPUT_IMAGE)
im.save(OUTPUT_IMAGE_NAME)
