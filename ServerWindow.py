from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow
from Ui_serverwindow import Ui_ServerWindow
from MyLogger import MyLogger
from PyQt5.QtNetwork import QTcpSocket, QHostAddress
import datetime
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

    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        print('识别')
        self.write_data_slot()
        self.sock.readyRead.connect(lambda: self.read_data_slot(self.sock))


    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        print('建立连接')
        ip = self.ui.ip_text.text()
        port = self.ui.port_text.text()
        port = int(port)
        print(ip,port)
        try:
            self.connect_to_host(ip, port)
        except Exception:
            print("connect failed!")




    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_ServerWindow()
        self.ui.setupUi(self)
        self.IP = '0.0.0.0'
        self.PORT = 60000
        self.message = None

        self.sock = QTcpSocket(self)


    def connect_to_host(self, ip, port):
        print('connect to host')
        self.IP = ip
        self.PORT = port
        try:
            self.sock.connectToHost(QHostAddress.LocalHost, self.PORT)
        except Exception:
            self.log.logger.error("连接失败")
            print('xiao ji')

    def write_data_slot(self):

        message = "recognition"
        print('Client: {}'.format(message))
        datagram = message.encode()
        try:
            self.sock.write(datagram)
        except Exception:
            self.log.logger.error("write_data_slot：寄")


    def read_data_slot(self, sock):
        while sock.bytesAvailable():
            try:
                datagram = sock.read(sock.bytesAvailable())
                self.message = datagram.decode()
                self.View_message()
                break
                #answer = self.get_answer(message).replace('{br}', '\n')
            except Exception:
                log.logger.error("read_data_slot1: error")


        # 4
    def View_message(self):
        try:
            # new_datagram = answer.encode()
            # sock.write(new_datagram)
            if self.message is not None:
                print(self.message)
                dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.ui.textEdit.append('[' + dt + ']: ' + self.message)
                log.logger.info("[receive message]:" + self.message)
                self.message=None
        except Exception:
            log.logger.error("receive message error")

    def disconnected_slot(self, sock):
        peer_address = sock.peerAddress().toString()
        peer_port = sock.peerPort()
        news = 'Disconnected with address {}, port {}'.format(peer_address, str(peer_port))
        log.logger.info(news)
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

