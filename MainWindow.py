from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import pyqtSlot, QRectF,Qt
from PyQt5.QtWidgets import QWidget, QGraphicsPixmapItem, QGraphicsScene
from PyQt5.QtWidgets import QMainWindow
from Ui_mainwindow import Ui_MainWindow
from paddleocr import PaddleOCR
from PIL import ImageGrab,Image
import screen_capture
import numpy
import cv2
import numpy as np
import socket
import threading

class MainWindow(QMainWindow):
    def __init__(self):
        self.IP = '127.0.0.1'
        self.PORT = 8080
        QWidget.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.bbox = None
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
        self.kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]], np.float32)
        self.item = None
        self.scene = QGraphicsScene(self)

        self.client = socket.socket()
        self.client.connect(('localhost', 8080))

    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.capture = screen_capture.CaptureScreen()
        self.capture.signal_complete_capture.connect(self.get_box)
        print('选取')

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        result, img = self.recognition()
        if result is not None and img is not None:
            str = ''
            for i in result:
                str += i
            self.ui.lineEdit.setText(str)
            self.show_image(img)
        else:
            print('还未框选')

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        self.bbox = None


    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        txt = self.ui.lineEdit.text()
        print(txt)
        self.send_texts(txt)


    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        pass

    def get_box(self, begin, end):
        x1, y1 = begin.x(), begin.y()
        x2, y2 = end.x(), end.y()
        self.bbox = (x1, y1, x2, y2)

    def recognition(self):
        txts = None
        img_rbg = None
        if self.bbox is not None:
            try:
                img = ImageGrab.grab(self.bbox)
                img_rbg = numpy.asarray(img)
                img = cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2GRAY)
                img = cv2.medianBlur(img, 3)
                img = cv2.filter2D(img, -1, kernel=self.kernel)
                # # ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
                # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                #                   cv2.THRESH_BINARY_INV, 11, 2)
                # cv2.erode(img, None, iterations=5)
                # cv2.imshow('median', img)
                # cv2.waitKey(0)
                result = self.ocr.ocr(img, cls=True)
                txts = [line[1][0] for line in result]
                print(txts)
            except Exception as e:
                print(e)
        else:
            print('未框选')

            # need to complete
        return txts, img_rbg

    def show_image(self, image):
        width = image.shape[1]
        height = image.shape[0]
        self.scene.clear()
        self.ui.graphicsView.clearFocus()
        # width = 400
        # height = 200
        print(type(image))
        print(image.shape)
        
        #frame = QImage(image, width, height, QImage.Format.Format_RGB666)
        im = Image.fromarray(image)
        pix = im.toqpixmap()
        #pix = QPixmap(frame)
        self.item = QGraphicsPixmapItem(pix)
        self.scene.addItem(self.item)
        self.ui.graphicsView.setScene(self.scene)
        self.scene.update()
        # self.ui.graphicsView.fitInView(QGraphicsPixmapItem(pix))
        # self.ui.graphicsView.show()

    def send_texts(self, text):
        self.client.send(text.encode())
        cmd_res = self.client.recv(1024)
        print(cmd_res.decode())
