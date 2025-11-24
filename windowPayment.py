from newWindow import newWindow
from tablesWindows import tablesWindows
from customtkinter import CTkLabel, CTkFrame, CTkButton
from table import table
class windowPayment():
    def __init__(self, master, command:int):
        self.master = master
        self.command = command
        self.rootpay = newWindow(self.master, "Pagamento", (500, 500), )
        #ctk.CTkToplevel(self.rootcommand)
        #self.rootpay.transient(self.rootcommand)

        self.scrollframepay = CTkScrollableFrame(self.rootpay)
        self.scrollframepay.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.75)
        
        self.table = tablesWindows(self.rootpay, (0.01, 0.01, 0.98, 0.75), "comandas", "Payments", ("cod", "number", "type", "quantity"), ("", "number"))
        self.table.create((("TIPO DE PAGAMENTO", "QUANTIDADE"), (2, 3)), (300, 100, 50), (50, 50, 50), deldata=(self.delete, "TABLE", 0))
        self.paytype = CTkLabel(self.scrollframepay, bg_color=self.colors[4], width=300, height=50, text="TIPO DE PAGAMENTO")
        self.paytype.grid(row=1, column=1, padx=1, pady=1)

        self.payment = CTkLabel(self.scrollframepay, bg_color=self.colors[4], width=100, height=50, text="QUANTIDADE")
        self.payment.grid(row=1, column=2, padx=1, pady=1)

        self.deletepay = CTkLabel(self.scrollframepay, bg_color=self.colors[4], width=50, height=50, text="Deletar")
        self.deletepay.grid(row=1, column=3, padx=1, pady=1)

        self.framepay = CTkFrame(self.rootpay)
        self.framepay.place(relx=0.01, rely=0.77, relwidth=0.98, relheight=0.22)

        self.confirmpay = CTkButton(self.framepay, text="CONFIRMAR", fg_color=self.colors[4], hover_color=self.colors[3], command=self.confirmpay)
        self.confirmpay.place(relx=0.61, rely=0.32, relwidth=0.38, relheight=0.67)

        self.addpay = CTkButton(self.framepay, text="ADICIONAR PAGAMENTO", fg_color=self.colors[4], hover_color=self.colors[3], command=addpay)
        self.addpay.place(relx=0.01, rely=0.32, relwidth=0.59, relheight=0.67)

        self.totalpricelbl = CTkLabel(self.framepay, text="TOTAL:", bg_color=self.colors[3])
        self.totalpricelbl.place(relx=0.01, rely=0.01, relwidth=0.2, relheight=0.3)

        self.totalprice = CTkLabel(self.framepay, text="", bg_color=self.colors[3])
        self.totalprice.place(relx=0.2, rely=0.01, relwidth=0.79, relheight=0.3)

        reloadpay()
    def delete(self, cod):
        table("comandas", "Payments").deleteData(("cod", ), (cod, ))
    def confirmpay(self):
        if self.totalprice.cget("text") >= 0:
            self.connectcommands()
            self.connecthistory()
            tableCommands = table("comandas", "CommandsActive")
            temp = tableCommands.getData(("number", ), where=("number", ), value=(self.command))[0][0]
            tableCommands.name = "Consumption"
            temp = tableCommands.getData(where=("number", ), value=(temp, ))
            totalprice = 0
            products = []
            for i in temp:
                products.append(i)
                totalprice = totalprice + float(i[5].replace(",", "."))
            tableCommands.name = "Payments"
            temp = tableCommands.getData()
            temp = self.commandscursor.execute("SELECT * FROM Payments WHERE number = ?", (commandactive[0], ))
            payments = []
            pay = 0
            for  i in temp:
                payments.append(i)
                pay = pay + float(i[3])
            date = str(datetime.datetime.now())[0:19]

            tim = self.historycursor.execute("""SELECT id FROM Cashdesk WHERE status = ?""", ("open", ))
            for i in tim:
                tim = i[0]
            self.historycursor.execute("INSERT INTO ClosedCommand (number, date, hour, nameclient, idclient, totalprice, datefinish, cashier, pay, cashdesk) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (commandactive[0], commandactive[1], commandactive[2], commandactive[3], commandactive[4], totalprice, date, self.namelogin, pay, tim))
            temp = self.historycursor.execute("SELECT cod FROM ClosedCommand WHERE number = ? AND nameclient = ? AND idclient = ? AND totalprice = ? AND datefinish = ?", (commandactive[0], commandactive[3], commandactive[4], totalprice, date))
            for i in temp:
                cod = i[0]
            for i in payments:
                self.historycursor.execute("INSERT INTO Payments (commandid, type, quantity) VALUES (?, ?, ?)", (cod, i[2], i[3]))
            self.connectprinter()
            self.printercursor.execute("INSERT INTO ClosedPrinter (command, date, permission, client) VALUES (?, ?, ?, ?)", (commandactive[0], commandactive[1] + " " + commandactive[2], "False", commandactive[3]))
            printertemp = self.printercursor.execute("SELECT id FROM ClosedPrinter WHERE command = ? AND date = ?", (commandactive[0], commandactive[1] + " " + commandactive[2]))
            for i in printertemp:
                idcom = i[0]
            for i in products:
                print(i)
                self.printercursor.execute("INSERT INTO ProductsClosed (id, product, type, qtd, unitprice) VALUES (?, ?, ?, ?, ?)", (idcom, i[8], i[9], i[7], i[6]))
                self.historycursor.execute("INSERT INTO Products (commandid, name, type, releasedate, releasehour, waiter, price, unitprice, quantity) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (cod, i[8], i[9], i[2], i[3], i[4], i[5], i[6], i[7]))
            self.printercursor.execute("UPDATE ClosedPrinter SET permission = ? WHERE command = ? AND date = ?", ("True", commandactive[0], commandactive[1] + " " + commandactive[2]))
            self.desconnectprinter()
            self.commandscursor.execute("DELETE FROM CommandsActive WHERE number = ?", (commandactive[0], ))
            for i in products:
                self.commandscursor.execute("DELETE FROM Consumption WHERE cod = ?", (i[0], ))
            for i in payments:
                self.commandscursor.execute("DELETE FROM Payments WHERE cod = ?", (i[0], ))
            self.desconnectcommands()
            self.desconnecthistory()
            closepay()
            self.on_closingcommandwindow()
            self.reloadcommands()
    def addpay(self):
        def closeadd():
            self.rootaddpay.destroy()
            self.rootpay.grab_set()
            self.root.bind_all("<KeyPress>", click)
        def clickpay(event):
            if event.keysym == "escape":
                closeadd()
        def addpayment():
            self.connectcommands()
            self.commandscursor.execute("INSERT INTO Payments (number, type, quantity) VALUES (?, ?, ?)", (self.currentcommandwindow, self.tipepayvar.get(), self.qtdpay.get()))
            self.desconnectcommands()
            closeadd()
            reloadpay()
        self.rootaddpay = ctk.CTkToplevel(self.rootpay)
        self.rootaddpay.geometry("400x150")
        self.rootaddpay.resizable(False, False)
        self.rootaddpay.title("Adicionar pagamento")
        self.rootaddpay.transient(self.rootpay)
        self.rootaddpay.grab_set()

        self.tipepayvar = StringVar(value="Dinheiro")

        self.confirmaddpay = ctk.CTkButton(self.rootaddpay, command=addpayment, text="CONFIRMAR", bg_color=self.colors[4], hover_color=self.colors[3])
        self.confirmaddpay.place(relx=0.01, rely=0.51, relwidth=0.98, relheight=0.48)

        self.tipepay = ctk.CTkComboBox(self.rootaddpay, width=196, height=73, variable=self.tipepayvar, values=["Dinheiro", "Débito", "Crédito"])
        self.tipepay.place(relx=0.01, rely=0.01, relwidth=0.49, relheight=0.49)

        self.qtdpay = ctk.CTkEntry(self.rootaddpay, placeholder_text="Quantidade")
        self.qtdpay.place(relx=0.51, rely=0.01, relwidth=0.48, relheight=0.49)

        self.root.bind_all("<KeyPress>", clickpay)
        self.rootaddpay.protocol("WM_DELETE_WINDOW", closeadd)
    
    def windowpay():
        def click(event):
            if event.keysym == "Escape":
                closepay()
        def closepay():
            self.root.bind_all("<KeyPress>", self.presskeycommandwindow)
            self.rootcommand.grab_set()
            self.rootpay.destroy()
        def delpay(cod):
            self.connectcommands()
            self.commandscursor.execute("DELETE FROM Payments WHERE cod = ?", (cod, ))
            self.desconnectcommands()
            reloadpay()
        
        def reloadpay():
            try:
                for i in self.currentpayments:
                    for j in i:
                        j.destroy()
            except:
                pass
            self.totalpricelbl.configure()
            self.connectcommands()
            temp = self.commandscursor.execute("SELECT * FROM Payments WHERE number = ?", (self.currentcommandwindow, ))
            self.currentpayments = []
            pay = 0.0
            for k, i in enumerate(temp):
                self.currentpayments.append([ctk.CTkLabel(self.scrollframepay, bg_color=self.colors[4], text=i[2], width=300, height=50), ctk.CTkLabel(self.scrollframepay, bg_color=self.colors[4], text=i[3], width=100, height=50), ctk.CTkButton(self.scrollframepay, text="", image=ctk.CTkImage(Image.open("./imgs/lixeira.png"), size=(35, 35)), fg_color=self.colors[4], hover=False, command=lambda y = i[0]:delpay(y), width=50, height=50)])
                n = k + 2
                self.currentpayments[k][0].grid(row=n, column=1, padx=1, pady=1)
                self.currentpayments[k][1].grid(row=n, column=2, padx=1, pady=1)
                self.currentpayments[k][2].grid(row=n, column=3, padx=1, pady=1)
                pay += float(i[3])
            temp = self.commandscursor.execute("SELECT price FROM Consumption WHERE number =?", (self.currentcommandwindow, ))
            for i in temp:
                pay -= float(i[0].replace(",", "."))
            if pay < 0:
                self.totalprice.configure(text=pay, text_color="#D81315")
            else:
                self.totalprice.configure(text=pay, text_color="#7CCD5C")
            self.desconnectcommands()
        