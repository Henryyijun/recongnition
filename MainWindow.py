from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QGraphicsPixmapItem, QGraphicsScene, QMainWindow, QApplication, QDialog, QMessageBox
from PyQt5.QtGui import QGuiApplication
from Ui_mainwindow import Ui_MainWindow
from paddleocr import PaddleOCR
from PIL import Image, ImageQt
import screen_capture
import cv2
import numpy
import numpy as np
from MyLogger import MyLogger
from PyQt5.QtNetwork import QTcpServer, QHostAddress


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
        self.screen = QGuiApplication.screens()[-1]
        self.item = None
        self.scene = QGraphicsScene(self)
        self.log = MyLogger('MainWindowLog.txt')
        self.show()
        self.server = QTcpServer(self)
        # 建立连接
        if not self.server.listen(QHostAddress(self.IP), self.PORT):
            self.log.logger.info(self.server.errorString())
        self.log.logger.info("正在监听端口：%d" % (self.PORT))
        self.server.newConnection.connect(self.new_socket_slot)
        self.resize(QGuiApplication.primaryScreen().size()*2/5)
        # self.ui.graphicsView.setGeometry(self.geometry())
        # print(self.ui.graphicsView.x())
        # print(self.ui.graphicsView.y())
        # print(self.ui.graphicsView.width())
        # print(self.ui.graphicsView.height())

    def closeEvent(self, event) -> None:
        dialog = QMessageBox.question(self, '提示信息',
                                            "是否要退出程序？",
                                            QMessageBox.Yes | QMessageBox.No,
                                            QMessageBox.No)

        if dialog == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

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
        self.log.logger.info("选取区域中")

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
                pscreen = QGuiApplication.primaryScreen()
                screen = QGuiApplication.screens()[-1]
                dialog = QDialog()
                dialog.setGeometry(screen.availableGeometry())
                pix_img = screen.grabWindow(QApplication.desktop().winId(), self.bbox[0]+dialog.x(), self.bbox[1],
                                                 self.bbox[2]-self.bbox[0], self.bbox[3]-self.bbox[1])
                qimg = pix_img.toImage()
                img = ImageQt.fromqimage(qimg)
                img_rbg = numpy.asarray(img)
                img = cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2GRAY)
                img = cv2.medianBlur(img, 3)
                img = cv2.filter2D(img, -1, kernel=self.kernel)
                result = self.ocr.ocr(img, cls=True)
                txts = [line[1][0] for line in result]
                print(txts)
            except Exception as e:
                self.log.logger.error("识别失败")
        else:
            print('未框选')
        return txts, img_rbg

    def show_image(self, image):

        width = image.shape[1]
        height = image.shape[0]
        if width > self.ui.graphicsView.width() or height > self.ui.graphicsView.height():
            self.log.logger.error("显示图片失败")
        else:
            self.scene.clear()
            self.ui.graphicsView.clearFocus()
            im = Image.fromarray(image)
            pix = im.toqpixmap()
            self.item = QGraphicsPixmapItem(pix)
            self.scene.addItem(self.item)
            self.ui.graphicsView.setScene(self.scene)
            self.scene.update()



    def new_socket_slot(self):
        self.sock = self.server.nextPendingConnection()
        peer_address = self.sock.peerAddress().toString()
        peer_port = self.sock.peerPort()
        news = 'Connected with address {}, port {}'.format(peer_address, str(peer_port))
        self.log.logger.info(news)
        self.sock.readyRead.connect(lambda: self.read_data_slot(self.sock))

    def read_data_slot(self, sock):
        while sock.bytesAvailable():
            try:
                datagram = sock.read(sock.bytesAvailable())
                message = datagram.decode()
            except Exception:
                self.log.logger.error("read_data_slot1: error")
            try:
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