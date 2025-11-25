from newWindow import newWindow
class addPay():
    def __init__(self, master):
        
        windowAddPay = newWindow(master, "Adicionar pagamento", (400, 150))
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