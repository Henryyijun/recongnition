from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtWidgets import QMainWindow
from Ui_serverwindow import Ui_ServerWindow
from MyLogger import MyLogger
from PyQt5.QtNetwork import QTcpSocket, QHostAddress
import datetime
log = MyLogger('Client.log')


class ServerWindow(QMainWindow):

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_ServerWindow()
        self.ui.setupUi(self)
        self.message = None
        self.sock = QTcpSocket(self)
        self.msg_box1 = QMessageBox(QMessageBox.Warning, "错误", "请输入服务器IP或者端口号")
        self.msg_box2 = QMessageBox(QMessageBox.Warning, "错误", "连接超时！")
        self.msg_box3 = QMessageBox(QMessageBox.Information, "消息", "连接成功！")
        self.msg_box4 = QMessageBox(QMessageBox.Warning, "错误", "服务未连接，不可识别")
        self.msg_box5 = QMessageBox(QMessageBox.Warning, "错误", "不可重复连接")
        self.connected = False

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        if self.connected:
            self.write_data_slot()
            self.sock.readyRead.connect(lambda: self.read_data_slot(self.sock))
        else:
            self.msg_box4.show()

    @pyqtSlot()
    def on_pushButton_3_clicked(self):

        ip = self.ui.ip_text.text()
        port = self.ui.port_text.text()
        if ip == '' or port == '':
            self.msg_box1.show()
            log.logger.info("没有输入ip或者端口号")
        else:
            if not self.connected:
                port = int(port)
                self.connect_to_host(ip, port)
            else:
                self.msg_box5.show()

    def connect_to_host(self, ip, port):
        try:
            self.sock.connectToHost(QHostAddress(ip), port)
            if not self.sock.waitForConnected(80000):
                self.msg_box2.show()
                self.connected = False

                log.logger.error("连接超时")
            else:
                self.msg_box3.show()
                self.connected = True

        except Exception:
            self.log.logger.error("连接失败")

    def write_data_slot(self):
        message = "recognition"
        print('Client: {}'.format(message))
        datagram = message.encode()
        try:
            self.sock.write(datagram)
        except Exception:
            self.log.logger.error("write_data_slot：error")

    def read_data_slot(self, sock):
        while sock.bytesAvailable():
            try:
                datagram = sock.read(sock.bytesAvailable())
                self.message = datagram.decode()
                self.view_message()
                break
            except Exception:
                log.logger.error("read_data_slot1: error")

    def view_message(self):
        try:
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

