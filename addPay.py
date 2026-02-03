from customtkinter import StringVar, CTkButton, CTkComboBox, CTkEntry
from newWindow import newWindow
from table import table
from colorsList import getColors
class addPay():
    def __init__(self, master, command):
        self.colors = getColors()
        self.command = command
        self.master = master
        self.windowAddPay = newWindow(master.rootpay.window, "Adicionar pagamento", (400, 150))
        
        self.tipepayvar = StringVar(value="Dinheiro")

        self.confirmaddpay = CTkButton(self.windowAddPay.window, command=self.addpayment, text="CONFIRMAR", bg_color=self.colors[4], hover_color=self.colors[3])
        self.confirmaddpay.place(relx=0.01, rely=0.51, relwidth=0.98, relheight=0.48)

        self.tipepay = CTkComboBox(self.windowAddPay.window, width=196, height=73, variable=self.tipepayvar, values=["Dinheiro", "Débito", "Crédito"])
        self.tipepay.place(relx=0.01, rely=0.01, relwidth=0.49, relheight=0.49)

        self.qtdpay = CTkEntry(self.windowAddPay.window, placeholder_text="Quantidade")
        self.qtdpay.place(relx=0.51, rely=0.01, relwidth=0.48, relheight=0.49)

    def addpayment(self,):
        table("comandas", "Payments").insertData(("number", "type", "quantity"), (self.command, self.tipepayvar.get(), self.qtdpay.get()))
        self.windowAddPay.deleteWindow()
        self.master.table.reload()