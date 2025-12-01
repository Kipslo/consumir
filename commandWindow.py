from newWindow import newWindow 
from tablesWindows import tablesWindows
from customtkinter import CTkLabel
from priceClass import priceClass
class commandWindow():
    def __init__(self, master, number:int, closed=0):
        self.windowCommand = newWindow(master, "COMANDA " + str(number), (700, 800))
        if closed == 0:
            talbleconsume = tablesWindows(self.windowCommand.window, (0, 0, 1, 0.7), "comandas", "Consumption", ("cod", "number", "date", "hour", "waiter", "price", "unitprice", "quantity", "product", "type", "size"), ("number", ), (number, ))
            talbleconsume.create((("PRODUTO", "GARÇOM", "PREÇO UNIDADE", "QTD.", "PREÇO TOTAL"), (8, 4, 6, 7, 5)), (200, 200, 100, 50, 100, 100), (40, 40, 40, 40, 40, 40,), reloadfunc=(self.updateTotal, self))

        else:
            talbleconsume = tablesWindows(master, (0, 0.1, 1, 0.7), "historico", "Products", ("releasedate", "releasehour", "waiter", "price", "quantity", "name", "unitprice"), ("commandid", ), (closed, ))
            talbleconsume.create((("PRODUTO", "GARÇOM", "PREÇO UNIDADE", "QTD.", "PREÇO TOTAL"), (5, 2, 6, 4, 3)), (200, 200, 100, 50, 100, 100), (40, 40, 40, 40, 40, 40,))

        self.totalpricelabel = CTkLabel(self.frame_infocommand, text="TOTAL:", fg_color=self.colors[4])
        self.totalpricelabel.place(relx=0.31, rely=0.15, relwidth=0.06, relheight=0.3)
        
    def updateTotal(self, products):
        total = 0
        for i in products:
            total = total + (i[5] * 100)
        total = priceClass.getPrice(str(total/100))
        
        self.totalpricelabel.config(text=total)
        