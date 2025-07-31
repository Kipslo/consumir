import socket
import sqlite3 as sql

fonte_padrao = b'\x1b!\x00'  # Fonte padrão
fonte_negrito = b'\x1b!\x08'  # Fonte em negrito
fonte_dobrada = b'\x1b!\x10'  # Fonte com largura dobrada
class printer():
    fontsizes = {"00":b'\x1D\x21\x00', "01":b'\x1D\x21\x01', "10": b'\x1D\x21\x10', "11": b'\x1D\x21\x11', "02": b'\x1D\x21\x02', "12": b'\x1D\x21\x12', "22": b'\x1D\x21\x22', "20": b'\x1D\x21\x20', "21": b'\x1D\x21\x21'}
    actuallysize = "00"
    align = "left"
    actuallyfont = "A"
    limitchar = {"A00":48, "A01":48, "A10":24, "A11":24, "A02":48, "A12":24, "A22":16, "A20":16, "A21":16, 
                 "B00":48, "B01":48, "B10":32, "B11":32, "B02":48, "B12":32, "B22":16, "B20":16, "B21":16}
    def connect(self, ip):
        print(ip)
        self.socketvar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketvar.connect((ip, 9100))
    def desconnectprinter(self):
        self.socketvar.close()
    def cut(self):
        self.socketvar.sendall(b"\n" + b"\n" + b"\n"+ b"\n"+ b"\n"+ b"\n")
        self.socketvar.sendall(b'\x1d\x56\x00')
    def printtext(self, text, isStrip = False):
        if isStrip:
            text = text.strip()
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
        self.breakline
    def breakline(self):
        self.socketvar.sendall(b"\n")
    def changesize(self, sizex = 0, sizey = -1):
        if sizey == -1:
            sizey = sizex
        size = f"{sizex}{sizey}"
        self.actuallysize = self.actuallyfont + str(size)
        hexsize = self.fontsizes[size]
        self.socketvar.sendall(hexsize)
    def changesmooth(self, smooth = False):
        if smooth:
            self.socketvar.sendall(b"\x1d\x62\x01")
            return
        self.socketvar.sendall(b"\x1d\x62\x00")
    def changefont(self, font = "a"):
        self.actuallyfont = font.upper()
        if self.actuallyfont == "B":
            self.socketvar.sendall(b'\x1B\x4D\x01')
        elif self.actuallyfont == "A":
            self.socketvar.sendall(b'\x1B\x4D\x00')
        self.changesize(self.actuallysize[1], self.actuallysize[2])
    def changebold(self, bold = False):
        if bold:
            self.socketvar.sendall(b"\x1b\x45\x01")
            return
        self.socketvar.sendall(b"\x1b\x45\x00")
    def changeitalic(self, italic = False):
        if italic:
            self.socketvar.sendall(b"\x1b\x34\x01")
            return
        self.socketvar.sendall(b"\x1b\x34\x00")
    def changeunderline(self, underline = False):
        if underline:
            self.socketvar.sendall(b"\x1b\x2d\x01")
            return
        self.socketvar.sendall(b"\x1b\x2d\x00")
    def setalign(self, align = "left"):
        if align == "left" or align == "center" or align == "right":
            self.align = align
            return "Sucess"
        raise AlignNotExist("This align not exist")
if __name__ == "__main__":
    printervar = printer()
    printervar.connect("192.168.0.202")
    printervar.changesize(1)
    printervar.changefont("b")
    printervar.printtext("oioioioioioi")
    printervar.cut()
    printervar.desconnectprinter()