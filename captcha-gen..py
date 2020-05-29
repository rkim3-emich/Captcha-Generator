import struct
from PIL import Image
import numpy as np
import random

idxImageReader = open("t10k-images.idx3-ubyte", "rb")
idxLabelReader = open("t10k-labels.idx1-ubyte", "rb")

imageContent = idxImageReader.read()
labels = idxLabelReader.read()

numberOfImages = struct.unpack(">i", imageContent[4:8])
current_byte = 8
numberOfRows = struct.unpack(">i", imageContent[current_byte:current_byte + 4])[0]
current_byte += 4
numberOfCols = struct.unpack(">i", imageContent[current_byte:current_byte + 4])[0]
current_byte += 4

image_arr = []
for images in range(numberOfImages[0]):
    imgData = []

    for i in range(numberOfRows*numberOfCols):
            imgData.append(255 - struct.unpack(">B", imageContent[current_byte:current_byte + 1])[0])
            current_byte += 1

    image_arr.append(imgData)

numberOfLabels = struct.unpack(">i", labels[4:8])
current_byte = 8

label_arr = []
for images in range(numberOfLabels[0]):
    label_arr.append(struct.unpack(">B", labels[current_byte:current_byte + 1])[0])
    current_byte += 1

answer = ""
rand_numbers = []
rand_images = []
for i in range(4):
    rand = random.randint(4999, len(image_arr)-1)
    rand_numbers.append(rand)
    answer = answer + str(label_arr[rand])
    rand_images.append(image_arr[rand])

captcha = []
for y in range(28):
    for i in range(4):
        for x in range(28):
            captcha.append(rand_images[i][x + 28*y])
    
image = Image.new("L", (numberOfCols*4, numberOfRows), None)
image.putdata(captcha)
                           
image.save(f"captcha.jpeg", "JPEG")

with open("answer.txt", "w") as writer:
    writer.write(answer)
