from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow
from Ui_serverwindow import Ui_ServerWindow
import threading
import socketserver
from MyLogger import MyLogger
from PyQt5.QtNetwork import QTcpServer, QHostAddress
import json
import requests

log = MyLogger('ServerWindowLog.txt')


# class Server(socketserver.BaseRequestHandler):
#
#     def add_obj(self, obj):
#         self.obj = obj
#
#     def handle(self):
#         try:
#             while True:
#                 self.data = self.request.recv(1024)
#                 self.obj.show_txt(self.data)
#                 print("{} send:".format(self.client_address), self.data)
#                 if not self.data:
#                     print('connection lost')
#                     break
#                 self.request.sendall(self.data.upper())
#         except Exception as e:
#             log.logger.info(str(self.client_address) + '连接断开')
#         finally:
#             self.request.close()
#
#     def setup(self):
#         log.logger.info("before handle,连接建立：" + str(self.client_address))
#
#     def finish(self):
#         log.logger.info("finish run  after handle")


class ServerWindow(QMainWindow):

    @pyqtSlot()
    def on_pushButton_clicked(self):
        print('建立连接')
        if not self.server.listen(QHostAddress.LocalHost, self.port):
            self.ui.textEdit.append(self.server.errorString())
        self.server.newConnection.connect(self.new_socket_slot)
    
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


    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_ServerWindow()
        self.ui.setupUi(self)
        self.ip = '0.0.0.0'
        self.port = 8080

        self.server = QTcpServer(self)


    def new_socket_slot(self):
        sock = self.server.nextPendingConnection()

        peer_address = sock.peerAddress().toString()
        peer_port = sock.peerPort()
        news = 'Connected with address {}, port {}'.format(peer_address, str(peer_port))
        self.ui.textEdit.append(news)

        sock.readyRead.connect(lambda: self.read_data_slot(sock))
        # sock.disconnected.connect(lambda: self.disconnected_slot(sock))

        # 3

    def read_data_slot(self, sock):
        while sock.bytesAvailable():
            try:
                datagram = sock.read(sock.bytesAvailable())
                message = datagram.decode()
                #answer = self.get_answer(message).replace('{br}', '\n')
            except Exception:
                log.logger.error("read_data_slot1: 寄")
            try:
                # new_datagram = answer.encode()
                #sock.write(new_datagram)
                print(message)
                self.ui.textEdit.append(message)
            except Exception:
                log.logger.error("read_data_slot2: 寄")


        # 4

    def disconnected_slot(self, sock):
        peer_address = sock.peerAddress().toString()
        peer_port = sock.peerPort()
        news = 'Disconnected with address {}, port {}'.format(peer_address, str(peer_port))
        self.ui.textEdit.append(news)

        sock.close()


    def show_txt(self):
        try:
            if self.ui.textEdit.toPlainText() is not None:
                self.ui.textEdit.setText(str(self.data))
            else:
                self.ui.textEdit.append(str(self.data))
        except Exception:
            log.logger.info(str(self.data) + '显示失败')

