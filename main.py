from PIL import Image, ImageDraw, ImageFont
import numpy as np
from numpy import asarray
from fontTools.ttLib import ttFont

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # use a truetype font
    # font = ImageFont.truetype("arial.ttf", 15)
    # image = Image.new("RGB", (font.font.height,font.font.height), "black")
    # draw = ImageDraw.Draw(image)
    # draw.text((0, 0), "A", font=font)
    # image_sequence = image.getdata()
    # image_array = np.array(image_sequence)
    #
    # font2 = ttFont.TTFont("C:/Windows/Fonts/ariblk.ttf")
    # charar = font2.get(0)
    #
    # image.show()

    # image to hex array converter
    image = Image.open('datchik.bmp')  # download image
    numpydata = asarray(image)  # convert to array

    y = len(numpydata)  # get image height
    x = len(numpydata[1])  # get image width
    newy = 0  # newy is number of 8bit arrays in high
    if (y % 8 != 0):  # if the result of the division is not an integer, we round it up
        newy = y // 8 + 1
    else:
        newy = y // 8

    a = []  # final array
    for i in range(x):  # for every columns
        ay = []  # array for column arrays
        for j in range(newy):  # number of arrays in every column
            stroka = ""
            for k in range(8):  # for every 8 pixels
                val = j * 8 + k  # calculate pixel position in by total height
                if val < y:
                    stroka = stroka + str(numpydata[val][i])
                else:  # if position is out of array, when fill in with zero
                    stroka = stroka + "0"
            ay.append(format(int(stroka, 2), '#04x'))  # convert to 4 sign hex (0xXX)
            print(ay)
        a.append(ay)
    print(a)

    # array to string converter
    res = ""
    for i in range(newy):
        for j in range(x):
            res = res + "(tU8)" + str(a[j][i]) + ", "
        res = res + "\n"
    print(res)