from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QGraphicsPixmapItem, QGraphicsScene
from PyQt5.QtWidgets import QMainWindow
from Ui_mainwindow import Ui_MainWindow
from paddleocr import PaddleOCR
from PIL import ImageGrab, Image
import screen_capture
import numpy
import cv2
import numpy as np
from MyLogger import MyLogger
from PyQt5.QtNetwork import QTcpServer, QHostAddress
from LoginWindow import LoginWindow

class MainWindow(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)
        self.IP = '0.0.0.0'     #监听所有ip
        self.PORT = 60000       #监听来自60000端口的请求
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.bbox = None
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en',
                             det_model_dir=r'.\2.3.0.2\ocr\det',
                             rec_model_dir=r'.\2.3.0.2\ocr\rec\en',
                             cls_model_dir=r'.\2.3.0.2\ocr\cls'
                             )
        self.kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]], np.float32)
        self.item = None
        self.scene = QGraphicsScene(self)
        self.log = MyLogger('MainWindowLog.txt')
        self.show()
        # self.sock.connectToHost(QHostAddress.LocalHost, self.PORT)
        # 建立服务器
        self.server = QTcpServer(self)
        # 建立连接
        if not self.server.listen(QHostAddress(self.IP), self.PORT):
            self.ui.textEdit.append(self.server.errorString())
        self.server.newConnection.connect(self.new_socket_slot)



    def write_data_slot(self):

        message = self.ui.lineEdit.text()
        if message == '':
            message = "识别错误，识别区域中未识别出内容"
            self.log.logger.error(message)
        print('Client: {}'.format(message))
        datagram = message.encode()
        try:
            self.sock.write(datagram)
        except Exception:
            self.log.logger.error("write_data_slot：寄")


    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.capture = screen_capture.CaptureScreen()
        self.capture.signal_complete_capture.connect(self.get_box)
        print('选取')

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        '''
        识别按钮
        :return:
        '''
        result, img = self.recognition()
        if result is not None and img is not None:
            str = ''
            for i in result:
                str += i
            self.ui.lineEdit.setText(str)
            self.show_image(img)
        else:
            self.log.logger.info('识别错误，用户未框选')

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        '''
        停止识别按钮
        :return:
        '''
        self.bbox = None


    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        '''
        发送按钮
        :return:
        '''
        # txt = self.ui.lineEdit.text()
        # self.send_texts(txt)
        self.write_data_slot()

    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        '''
        返回登录按钮
        :return:
        '''
        self.Login_window.show()
        self.close()


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
        im = Image.fromarray(image)
        pix = im.toqpixmap()
        #pix = QPixmap(frame)
        self.item = QGraphicsPixmapItem(pix)
        self.scene.addItem(self.item)
        self.ui.graphicsView.setScene(self.scene)
        self.scene.update()
        # self.ui.graphicsView.fitInView(QGraphicsPixmapItem(pix))
        # self.ui.graphicsView.show()

    def new_socket_slot(self):
        self.sock = self.server.nextPendingConnection()

        peer_address = self.sock.peerAddress().toString()
        peer_port = self.sock.peerPort()
        news = 'Connected with address {}, port {}'.format(peer_address, str(peer_port))
        self.log.logger.info(news)

        self.sock.readyRead.connect(lambda: self.read_data_slot(self.sock))
        # sock.disconnected.connect(lambda: self.disconnected_slot(sock))

        # 3
    def read_data_slot(self, sock):
        while sock.bytesAvailable():
            try:
                datagram = sock.read(sock.bytesAvailable())
                message = datagram.decode()
                #answer = self.get_answer(message).replace('{br}', '\n')
            except Exception:
                self.log.logger.error("read_data_slot1: error")
            try:
                # new_datagram = answer.encode()
                #sock.write(new_datagram)
                self.log.logger.info("[receive message]:"+message)
                if message == "recognition":
                    result, img = self.recognition()
                    if result is not None and img is not None:
                        str = ''
                        for i in result:
                            str += i
                        self.ui.lineEdit.setText(str)
                        self.show_image(img)
                    else:
                        self.log.logger.info('识别错误，用户未框选')
                    self.write_data_slot()
            except Exception:
                self.log.logger.error("receive message error")