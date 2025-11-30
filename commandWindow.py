from newWindow import newWindow 
from tablesWindows import tablesWindows
from customtkinter import CTkLabel
class commandWindow():
    def __init__(self, master, number, closed=0):
        self.windowCommand = newWindow(master, "COMANDA " + number, (500, 800))
        if closed == 0:
            talbleconsume = tablesWindows(master, (0, 0.1, 1, 0.7), "comandas", "Consumption", ("cod", "number", "date", "hour", "waiter", "price", "unitprice", "quantity", "product", "type", "size"), ("number", ), (number, ))
            talbleconsume.create((("PRODUTO", "GARÇOM", "PREÇO UNIDADE", "QTD.", "PREÇO TOTAL"), (8, 4, 6, 7, 5)), (200, 200, 100, 50, 100, 100), (40, 40, 40, 40, 40, 40,), reloadfunc=())

        else:
            talbleconsume = tablesWindows(master, (0, 0.1, 1, 0.7), "historico", "Products", ("releasedate", "releasehour", "waiter", "price", "quantity", "name", "unitprice"), ("commandid", ), (closed, ))
            talbleconsume.create((("PRODUTO", "GARÇOM", "PREÇO UNIDADE", "QTD.", "PREÇO TOTAL"), (5, 2, 6, 4, 3)), (200, 200, 100, 50, 100, 100), (40, 40, 40, 40, 40, 40,))

        self.totalpricelabel = CTkLabel(self.frame_infocommand, text="TOTAL:", fg_color=self.colors[4])
        self.totalpricelabel.place(relx=0.31, rely=0.15, relwidth=0.06, relheight=0.3)
        
    def updateTotal():
        