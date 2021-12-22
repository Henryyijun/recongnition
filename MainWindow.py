from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QGraphicsPixmapItem, QGraphicsScene
from PyQt5.QtWidgets import QMainWindow

from Ui_mainwindow import Ui_MainWindow
from paddleocr import PaddleOCR
from PIL import ImageGrab
import screen_capture
import numpy
import cv2
import numpy as np


class MainWindow(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.bbox = None
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
        self.kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]], np.float32)
        self.image = None
        self.item = None
        self.scene = None


    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.capture = screen_capture.CaptureScreen()
        self.capture.signal_complete_capture.connect(self.get_box)
        print('选取')

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        result = self.recognition()
        str = ''
        for i in result:
            str += i

        self.ui.lineEdit.setText(str)
        self.show_image()

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        print('停止识别')


    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        print('send')

    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        print('返回')

    def get_box(self, begin, end):
        x1, y1 = begin.x(), begin.y()
        x2, y2 = end.x(), end.y()
        self.bbox = (x1, y1, x2, y2)

    def recognition(self):
        if self.bbox is not None:

            try:
                img = ImageGrab.grab(self.bbox)
                self.image = cv2.cvtColor(numpy.asarray(img))
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
            pass
            # need to complete
        return txts

    def show_image(self):
        height = self.image.shape[1]
        width = self.image.shape[0]
        frame = QImage(self.image, height, width, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.fitInView(QGraphicsPixmapItem(pix))
        self.graphicsView.show()
