import threading
import socketserver

IP = '127.0.0.1'
PORT = 8080


class Server(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            while True:
                self.data = self.request.recv(1024)
                print("{} send:".format(self.client_address), self.data)
                if not self.data:
                    print('connection lost')
                    break
                self.request.sendall(self.data.upper())
        except Exception as e:
            print(self.client_address, '连接断开')
        finally:
            self.request.close()

    def setup(self):
        print("before handle,连接建立：", self.client_address)

    def finish(self):
        print("finish run  after handle")

if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer((IP, PORT), Server)
    server.serve_forever()
