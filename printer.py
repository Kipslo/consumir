import socket
import sqlite3 as sql

class printer():
    def __init__(self):
        self.connectprinter('')
    def connectprinter(self, ip):
        self.socketvar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketvar.connect(("192.168.0.202", 9100))
        mensagem = "oi"
        self.changesize(1)
        self.socketvar.sendall(mensagem.encode('utf-8') + b'\n' + b'\n' + b'\n' + b'\n')
        self.cut()
    def desconnectprinter(self, ip):
        pass
    def cut(self):
        self.socketvar.sendall(b'\x1d\x56\x00')
    def printtext(self, text):
        pass
    def printtextl(self, text):
        pass
    def breakline(self):
        pass
    def changesize(self, size = 0):
        
        hexsize = f'\{hex(size)[1:]}'
        self.socketvar.sendall(b'\x1D\X21' + hexsize.encode())
    def changebold(self, bold = False):
        pass
    def setalign(self, align = "left"):
        pass
    def printsendproduct(self):
        pass
    def printexit(self):
        pass
if __name__ == "__main__":
    printervar = printer()