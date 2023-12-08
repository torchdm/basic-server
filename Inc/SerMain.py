from threading import Thread
import pickle
import socket


class Kext:
    def __init__(self, controller) -> None:
        self.controller = controller

    def __call__(self, payload):
        if hasattr(self, "callback"):
            self.callback(payload)


class TSC:
    def __init__(self) -> None:
        self.kexts = []
        self.server = None

    def add_extension(self, kp):
        pth = __import__(kp)
        pth.setup(self)

    def hconn(self, conn):
        while True:
            payload = conn.recv(10240)
            self.hkext(pickle.loads(payload))

    def hkext(self, payload):
        for kext in self.kexts:
            try:
                kext(payload)
                return
            except:
                continue

    def connect(self, config):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((config["host"], config["port"]))

    def start(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            print(f"ACCEPT {addr} Torch1/1")
            Thread(target=lambda: self.hconn(conn)).start()

    def serve_forever(self, config):
        print(f"Connecting Server...")
        self.connect(config)
        print(f"Listening on torch:///{config['host']}:{config['port']}")
        self.start()
