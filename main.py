import sys
import io

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from numpy import asarray
from fontTools.ttLib import ttFont
from PyQt5.QtGui import QImage, QBitmap, QPixmap, QPainter, QPicture, QPen
from PyQt5.QtCore import QRect, QBitArray, QByteArray, QBuffer, QIODevice, Qt, QPoint, QSize
from PyQt5.QtWidgets import QWidget, QApplication, QGraphicsView, QGraphicsScene, QLabel, QPushButton

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Converter")
        self.openButton = QPushButton(self)
        self.openButton.setGeometry(0,430,200,20)
        self.openButton.setText("Open")
        self.openButton.clicked.connect(self.openEvent)

        self.drawing = False
        self.lastPoint = QPoint()

        self.image = QBitmap()
        self.image.load("datchik2.bmp")

        # self.graphicsView = QGraphicsView(self)
        # self.graphicsView.setGeometry(QRect(0, 0, 640, 430))

        # self.myScene = QGraphicsScene()
        # self.myScene.setSceneRect(0, 0, 640, 430)
        # self.myLable = QLabel()
        # self.myLable.setBaseSize(QSize(600,400))


        width = 640
        height = 450

        self.setGeometry(100, 100, width, height)



        # # From PIL Image to QImage
        # im = Image.open("datchik2.bmp")
        # im = im.convert("RGBA")
        # data = im.tobytes("raw", "RGBA")
        # qim = QImage(data, im.size[0], im.size[1], QImage.Format_ARGB32)
        # pix = QPixmap.fromImage(qim)
        #
        # # From QImage to PIL Image
        # buffer = QBuffer()
        # buffer.open(QBuffer.ReadWrite)
        # qim.save(buffer, "PNG")
        # pil_im = Image.open(io.BytesIO(buffer.data()))
        # pil_im.show()
        #
        # self.image = pix



    def mousePressEvent(self, event):
        painter = QPainter(self.image)
        if event.button() == Qt.LeftButton:
            painter.setPen(QPen(Qt.black, 1))
        if event.button() == Qt.RightButton:
            painter.setPen(QPen(Qt.white, 1))
        painter.drawPoint(event.pos() / 5)
        self.update()


    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        # canvasPainter.drawPixmap(self.rect(), self.image)
        canvasPainter.drawPixmap(QRect(0, 0, self.image.width() * 5, self.image.height() * 5), self.image)
        canvasPainter.drawRect(QRect(0, 0, 640, 430))
        # canvasPainter.drawPixmap(0, 0, self.image)

    def openEvent(self):
        print("HE")
        # self.image.load("datchik2.bmp")








def draw():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

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

    draw()

    #
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