from newWindow import newWindow 
from tablesWindows import tablesWindows
from customtkinter import CTkLabel, StringVar, CTkComboBox, CTkFrame, CTkButton
from priceClass import priceClass
from table import table
from windowPayment import windowPayment
from colorsList import getColors
class commandWindow():
    def __init__(self, master, number:int, reloadFunc = None, closed=0):
        def selectid(id):
            temp = table("clientes", "Clients").getData(("name", ), ("id", ), (id, ))  
            self.nameclient.set(temp[0][0])
        def selectname(name):
            self.nameclient.set(name.split("- ")[1])
            self.idclient.set(name.split(" -")[0])
        self.number = number
        self.reloadFunc = reloadFunc
        self.colors = getColors()
        self.windowCommand = newWindow(master, "COMANDA " + str(number), (900, 800))
        self.frame_infocommand = CTkFrame(self.windowCommand.window, fg_color=self.colors[2])
        self.frame_infocommand.place(relx=0,rely=0.8,relwidth=1,relheight=0.2)

        self.totalpricelabel = CTkLabel(self.frame_infocommand, text="TOTAL:", fg_color=self.colors[4])
        self.totalpricelabel.place(relx=0.31, rely=0.15, relwidth=0.37, relheight=0.3)
        if closed == 0:
            tableconsume = tablesWindows(self.windowCommand.window, (0, 0, 1, 0.7), "comandas", "Consumption", ("cod", "number", "date", "hour", "waiter", "price", "unitprice", "quantity", "product", "type", "size"), ("number", ), (number, ))
            tableconsume.create((("PRODUTO", "GARÇOM", "PREÇO UNIDADE", "QTD.", "PREÇO TOTAL"), (8, 4, 6, 7, 5)), (200, 200, 100, 50, 100, 100), (40, 40, 40, 40, 40, 40,), reloadfunc=(self.updateTotal, self))
            tmp = table("comandas", "CommandsActive").getData(("idclient", "nameclient"), ("number", ), (number, ))
            idclient, self.actuallyname = "", ""
            for i in tmp:
                idclient, self.actuallyname = i
            temp = table("clientes", "Clients").getData(("id", "name"), )
            ids = []
            names = []
            for i in temp:
                ids.append(str(i[0]))
                names.append(f"{str(i[0])} - {i[1]}")

            self.idclient = StringVar(value=idclient)
            self.nameclient = StringVar(value=self.actuallyname)

            self.clientid = CTkComboBox(self.frame_infocommand, width=100, height=50, values=ids, command=selectid, font=("Arial", 15), variable=self.idclient)
            self.clientid.place(relx=0.31, rely=0.51)

            self.clientname = CTkComboBox(self.frame_infocommand, width=235, height=50, values=names, command=selectname, font=("Arial", 15), variable=self.nameclient)
            self.clientname.place(relx=0.43, rely=0.51)

            self.button_delcommand = CTkButton(self.frame_infocommand, fg_color=self.colors[4], text="EXCLUIR COMANDA", hover_color=self.colors[5], command=self.delete)
            self.button_delcommand.place(relx=0.01, rely=0.15, relwidth=0.29, relheight=0.7)

            self.button_finishcommand = CTkButton(self.frame_infocommand, fg_color=self.colors[4], text="PAGAMENTO", hover_color=self.colors[5], command=self.windowPay)
            self.button_finishcommand.place(relx=0.7, rely=0.15, relwidth=0.29, relheight=0.7)
        else:
            tableconsume = tablesWindows(self.windowCommand.window, (0, 0.1, 1, 0.7), "historico", "Products", ("releasedate", "releasehour", "waiter", "price", "quantity", "name", "unitprice",""), ("commandid", ), (closed, ))
            tableconsume.create((("PRODUTO", "GARÇOM", "PREÇO UNIDADE", "QTD.", "PREÇO TOTAL"), (5, 2, 6, 4, 3)), (200, 200, 100, 50, 100, 100), (40, 40, 40, 40, 40, 40,))
            self.time_heading = CTkLabel(self.rootcommand, text="TEMPO", fg_color=self.colors[4], width=150, height=30)
            self.time_heading.grid(row=1, column=6, padx=1, pady=50)
            self.button_finishcommand = CTkButton(self.frame_infocommand, fg_color=self.colors[4], text="Reimprimir", hover_color=self.colors[5], command=lambda x = closed:"reprint(x)")
            self.button_finishcommand.place(relx=0.7, rely=0.15, relwidth=0.29, relheight=0.7)
        
    def updateTotal(self, products, data):
        total = 0
        for i in products:
            total = total + (float(i[5]) * 100)
        total = priceClass.getPrice(str(total/100))
        print(total)
        self.totalpricelabel.configure(text="TOTAL: " + total)
        

    def delete(self, ):
        def delete():
            commandTable = table("comandas", "CommandsActive")
            commandTable.deleteData(("number", ), (self.number, ))
            commandTable.name = "Consumption"
            commandTable.deleteData(("number", ), (self.number, ))
            commandTable.name = "Payments"
            commandTable.deleteData(("number", ), (self.number, ))
            self.windowCommand.deleteWindow()
            if self.reloadFunc:
                self.reloadFunc()
        windowdel = newWindow(self.windowCommand.window, "Excluir comanda", (300, 200), )
        self.button_confirmdelete = CTkButton(windowdel.window, fg_color=self.colors[4], hover_color=self.colors[5], text="CONFIRMAR", command= delete)
        self.button_confirmdelete.place(relx=0.01, rely=0.01, relwidth=1, relheight=0.48)

        self.button_canceldelete = CTkButton(windowdel.window, fg_color=self.colors[4], hover_color=self.colors[5], text="CANCELAR", command= windowdel.deleteWindow,)
        self.button_canceldelete.place(relx=0.01, rely=0.51, relwidth=1, relheight=0.48)

    def windowPay(self, ):
        windowPayment(self.windowCommand.window, self.number)