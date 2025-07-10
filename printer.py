import socket
import sqlite3 as sql

class printer():
    fontsizes = {"00":b'\x1D\x21\x00', "01":b'\x1D\x21\x01', "10": b'\x1D\x21\x10', "11": b'\x1D\x21\x11', "02": b'\x1D\x21\x02', "12": b'\x1D\x21\x12', "22": b'\x1D\x21\x22', "20": b'\x1D\x21\x20', "21": b'\x1D\x21\x21'}
    actuallysize = "00"
    align = "left"
    limitchar = {"00":48, "01":48, "10":24, "11":24, "02":48, "12":24, "22":16, "20":16, "21":16}
    def __init__(self):
        self.connectprinter('')
    def connectprinter(self, ip):
        self.socketvar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketvar.connect(("192.168.0.202", 9100))
        mensagem = "12345678901234567890123456789"
        self.changesize(1)
        self.setalign("right")
        self.printtext("oi" * 25)
        self.cut()
    def desconnectprinter(self, ip):
        pass
    def cut(self):
        self.socketvar.sendall(b'\x1d\x56\x00')
    def printtext(self, text):
        limitchar = self.limitchar[self.actuallysize]
        for i in range(len(text) // limitchar + 1):
            textforprint = text[i * limitchar : (i+1) * limitchar]
            spaces = limitchar - len(textforprint)
            if self.align == "center":
                textforprint = (" " * (spaces//2) + textforprint)
                self.socketvar.sendall(textforprint.encode('utf-8'))
            elif self.align == "right":
                textforprint = (" " * spaces) + textforprint
                self.socketvar.sendall(textforprint.encode('utf-8'))
            else:
                self.socketvar.sendall(textforprint.encode('utf-8'))

        self.socketvar.sendall(b"\n" + b"\n" + b"\n"+ b"\n"+ b"\n"+ b"\n")
    def breakline(self):
        pass
    def changesize(self, sizex = 0, sizey = -1):
        if sizey == -1:
            sizey = sizex
        size = f"{sizex}{sizey}"
        self.actuallysize = str(size)
        hexsize = self.fontsizes[size]
        self.socketvar.sendall(hexsize)
    def changebold(self, bold = False):
        pass
    def setalign(self, align = "left"):
        if align == "left" or align == "center" or align == "right":
            self.align = align
            return "Sucess"
        raise AlignNotExist("This align not exist")
    def printsendproduct(self):
        pass
    def printexit(self, text):
        pass
if __name__ == "__main__":
    printervar = printer()