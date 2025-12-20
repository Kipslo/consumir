from newWindow import newWindow
from tablesWindows import tablesWindows
from customtkinter import CTkLabel, CTkFrame, CTkButton
from table import table
from datetime import datetime
from addPay import addPay
class windowPayment():
    def __init__(self, master, command:int):
        def addpay():
            addPay(self, self.command)
        self.master = master
        self.command = command
        self.rootpay = newWindow(self.master, "Pagamento", (500, 500), )
        #ctk.CTkToplevel(self.rootcommand)
        #self.rootpay.transient(self.rootcommand)
        
        self.table = tablesWindows(self.rootpay, (0.01, 0.01, 0.98, 0.75), "comandas", "Payments", ("cod", "number", "type", "quantity"), ("", "number"))
        self.table.create((("TIPO DE PAGAMENTO", "QUANTIDADE"), (2, 3)), (300, 100, 50), (50, 50, 50), deldata=(self.delete, "TABLE", 0))

        self.framepay = CTkFrame(self.rootpay)
        self.framepay.place(relx=0.01, rely=0.77, relwidth=0.98, relheight=0.22)

        self.confirmpay_button = CTkButton(self.framepay, text="CONFIRMAR", fg_color=self.colors[4], hover_color=self.colors[3], command=self.confirmpay)
        self.confirmpay_button.place(relx=0.61, rely=0.32, relwidth=0.38, relheight=0.67)

        self.addpay = CTkButton(self.framepay, text="ADICIONAR PAGAMENTO", fg_color=self.colors[4], hover_color=self.colors[3], command=addpay)
        self.addpay.place(relx=0.01, rely=0.32, relwidth=0.59, relheight=0.67)

        self.totalpricelbl = CTkLabel(self.framepay, text="TOTAL:", bg_color=self.colors[3])
        self.totalpricelbl.place(relx=0.01, rely=0.01, relwidth=0.2, relheight=0.3)

        self.totalprice = CTkLabel(self.framepay, text="", bg_color=self.colors[3])
        self.totalprice.place(relx=0.2, rely=0.01, relwidth=0.79, relheight=0.3)

    def delete(self, cod):
        table("comandas", "Payments").deleteData(("cod", ), (cod, ))
    def confirmpay(self):
        if self.totalprice.cget("text") >= 0:
            tableCommands = table("comandas", "CommandsActive")
            commandactive = tableCommands.getData(where=("number", ), value=(self.command))[0][0]
            tableCommands.name = "Consumption"
            temp = tableCommands.getData(where=("number", ), value=(commandactive[0], ))
            totalprice = 0
            products = []
            for i in temp:
                products.append(i)
                totalprice = totalprice + float(i[5].replace(",", "."))
            tableCommands.name = "Payments"
            temp = tableCommands.getData(where=("number", ), value=(commandactive[0]))
            payments = []
            pay = 0
            for  i in temp:
                payments.append(i)
                pay = pay + float(i[3])
            date = str(datetime.now())[0:19]
            tableHistory = table("historico", "Cashdesk")
            tim = tableHistory.getData(("id", ), ("status",) , ("open", ))
            for i in tim:
                tim = i[0]
            tableHistory.name = "ClosedCommand"
            tableHistory.insertData(("number", "date", "hour", "nameclient", "idclient", "totalprice", "datefinish", "cashier", "pay", "cashdesk"), (commandactive[0], commandactive[1], commandactive[2], commandactive[3], commandactive[4], totalprice, date, self.namelogin, pay, tim))
            temp = tableHistory.getData(("cod", ), ("number", "nameclient", "idclient", "totalprice", "datefinish"), (commandactive[0], commandactive[3], commandactive[4], totalprice, date))
            for i in temp:
                cod = i[0]
            for i in payments:
                tableHistory.name = "Payments"
                tableHistory.insertData(("commandid", "type", "quantity"), (cod, i[2], i[3]))
            tablePrinter = table("impressoras", "ClosedPrinter")
            self.connectprinter()
            tablePrinter.insertData(("command", "date", "permission", "client"), (commandactive[0], commandactive[1] + " " + commandactive[2], "False", commandactive[3]))
            printertemp = tablePrinter.getData(("id", ), ("command", "date"), (commandactive[0], commandactive[1] + " " + commandactive[2]))
            for i in printertemp:
                idcom = i[0]
            tablePrinter.name = "ProductsClosed"
            tableHistory.name = "Products"
            for i in products:
                print(i)
                tablePrinter.insertData(("id", "product", "type", "qtd", "unitprice"), (idcom, i[8], i[9], i[7], i[6]))
                tableHistory.insertData(("commandid", "name", "type", "releasedate", "releasehour", "waiter", "price", "unitprice", "quantity"), (cod, i[8], i[9], i[2], i[3], i[4], i[5], i[6], i[7]))
            tablePrinter.name = "ClosedPrinter"
            tablePrinter.updateData(("permission", ), ("True"), ("command", "date"), (commandactive[0], commandactive[1] + " " + commandactive[2]))
            tableCommands.name = "CommandsActive"
            tableCommands.deleteData(("number", ), (commandactive[0], ))
            tableCommands.name = "Consumption"
            for i in products:
                tableCommands.deleteData(("cod", ), (i[0], ))
            tableCommands.name = "Payments"
            for i in payments:
                tableCommands.deleteData(("Payments", ), (i[0], ))
            self.rootpay.deleteWindow()
            self.reloadcommands()
    def reload(self, ):
        
        pay = 0.0
        temp = table("comandas", "Payments").getData(("price", ), ("number", ), (self.command, )) 
        for i in temp:
            pay += float(i[0])
        temp = table("comandas", ("Consumption")).getData(("price", ), ("number", ), (self.command))
        for i in temp:
            pay -= float(i[0].replace(",", "."))
        if pay < 0:
            self.totalprice.configure(text=pay, text_color="#D81315")
        else:
            self.totalprice.configure(text=pay, text_color="#7CCD5C")
        self.desconnectcommands()
    
