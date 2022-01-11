from ServerWindow import ServerWindow
import sys
from PyQt5 import QtWidgets


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    a = ServerWindow()
    a.show()
    sys.exit(app.exec_())
    # server = socketserver.ThreadingTCPServer((IP, PORT), Server)
    # server.serve_forever()
