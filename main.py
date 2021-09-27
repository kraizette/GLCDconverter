import sys
import io

from PIL import Image
from numpy import asarray
from PyQt5.QtGui import QImage, QBitmap, QPainter, QPen
from PyQt5.QtCore import QRect, QBuffer,  Qt, QPoint
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QFileDialog


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Converter")
        self.openButton = QPushButton(self)
        self.openButton.setGeometry(0, 430, 160, 20)
        self.openButton.setText("Open")
        self.openButton.clicked.connect(self.openEvent)

        self.newButton = QPushButton(self)
        self.newButton.setGeometry(160, 430, 160, 20)
        self.newButton.setText("New")
        self.newButton.clicked.connect(self.newEvent)

        self.saveHexButton = QPushButton(self)
        self.saveHexButton.setGeometry(320, 430, 160, 20)
        self.saveHexButton.setText("Save hex")
        self.saveHexButton.clicked.connect(self.saveHexEvent)

        self.saveImgButton = QPushButton(self)
        self.saveImgButton.setGeometry(480, 430, 160, 20)
        self.saveImgButton.setText("Save image")
        self.saveImgButton.clicked.connect(self.saveImgEvent)

        self.drawing = False
        self.lastPoint = QPoint()

        self.image = QBitmap(128, 86)

        self.hexStr = ''

        self.canvasWidth = 0
        self.canvasHeight = 0

        self.setGeometry(100, 100, 640, 450)

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
        canvasPainter.drawPixmap(QRect(0, 0, self.canvasWidth, self.canvasHeight), self.image)
        canvasPainter.drawRect(QRect(0, 0, self.canvasWidth, self.canvasHeight))

    def openEvent(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Image Files(*.png *.jpg *.bmp)')
        self.image.load(fileName)
        self.canvasWidth = self.image.width() * 5
        self.canvasHeight = self.image.height() * 5
        self.update()

    def newEvent(self):
        self.image = QBitmap(128, 86)
        self.canvasWidth = 640
        self.canvasHeight = 430
        self.image.clear()
        self.update()

    def saveHexEvent(self):
        fileName, _ = QFileDialog.getSaveFileName(self, 'QFileDialog.getSaveFileName()', 'hex',
                                                  'Text File(*.txt)')
        hex = self.convert()
        with open(fileName, 'w') as f:
            f.write(hex)

    def saveImgEvent(self):
        fileName, _ = QFileDialog.getSaveFileName(self, 'QFileDialog.getSaveFileName()', 'image',
                                                  'Bitmap File(*.bmp)')
        self.image.save(fileName, "bmp")

    def convert(self):
        img = QImage(self.image)
        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        img.save(buffer, "BMP")
        image = Image.open(io.BytesIO(buffer.data()))

        # image to hex array converter
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
            a.append(ay)

        # array to string converter
        res = ""
        for i in range(newy):
            for j in range(x):
                res = res + "(tU8)" + str(a[j][i]) + ", "
            res = res + "\n"

        return res

def draw():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    draw()