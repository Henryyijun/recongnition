from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow
from Ui_serverwindow import Ui_ServerWindow
import threading
import socketserver
from MyLogger import MyLogger

log = MyLogger('ServerWindowLog.txt')


class ServerWindow(QMainWindow):
    class Server(socketserver.BaseRequestHandler):
        def handle(self):
            try:
                while True:
                    self.data = self.request.recv(1024)
                    ServerWindow.show_txt(self.data)
                    print("{} send:".format(self.client_address), self.data)
                    if not self.data:
                        print('connection lost')
                        break
                    self.request.sendall(self.data.upper())
            except Exception as e:
                log.logger.info(str(self.client_address) + '连接断开')
            finally:
                self.request.close()

        def setup(self):
            log.logger.info("before handle,连接建立：" + str(self.client_address))

        def finish(self):
            log.logger.info("finish run  after handle")

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_ServerWindow()
        self.ui.setupUi(self)
        self.ip = '0.0.0.0'
        self.port = 8080

    def create_server(self):
        self.server = socketserver.ThreadingTCPServer((self.ip, self.port), self.Server)
        self.server.serve_forever()

    @classmethod
    def show_txt(self, data):
        try:
            self.ui.textEdit.setText(str(data))
        except Exception:
            log.logger.info(str(data) + '显示失败')


    @pyqtSlot()
    def on_pushButton_clicked(self):
        print('建立连接')
        thread = threading.Thread(target=self.create_server)
        thread.start()
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        print('开始接收')

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        print('停止接收')

    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        print('设定ip与端口')

    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        print('确定ip与端口')