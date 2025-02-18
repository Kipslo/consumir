import tkinter as tk
from tkinter import ttk
import socket
import customtkinter as ctk
import sqlite3 as sql
from PIL import Image
import threading
import pyautogui as pa
import datetime
from unidecode import unidecode
from escpos.printer import Network
from multiprocessing import Process
from tkcalendar import DateEntry
from time import sleep
from CTkSpinbox import CTkSpinbox
class application():
    def __init__(self):
        def close():
            self.root.destroy()
            aserver.close()
            aprinter.printervar.terminate()
        self.insertproductlist = []
        self.createtables()
        self.desconnecthistory()
        self.positionp = True
        self.cod, self.stylemode, self.maxcommands = "", "", ""
        mod, up = False, False
        self.connectconfig()
        self.currentconfig = self.configcursor.execute("""SELECT cod, stylemode, maxcommands FROM Config WHERE cod = 1""") 
        for i in self.currentconfig:
            self.cod, self.stylemode, self.maxcommands = i
        if self.cod == "":
            self.cod = 1
            mod = True
        if self.stylemode == "":
            self.stylemode = "ESCURO"
            up = True
        if self.maxcommands == "":
            self.maxcommands = 400
            up = True
        if mod:
            self.configcursor.execute("""INSERT INTO Config (stylemode, maxcommands, cnpj, housename, adress, fone, male, female) VALUES (?, ?, '', '', '', '', '', '')""", (self.stylemode, self.maxcommands))
        elif mod == False and up == True:
            self.configcursor.execute("""UPDATE Config SET stylemode = ?, maxcommands = ? WHERE cod = 1""", (self.stylemode, self.maxcommands))
        if self.stylemode == "ESCURO":
            ctk.set_appearance_mode("dark")
            self.colors = ["#1f1f1f", "#2f2f2f", "#383838", "#3f3f3f", "#484848", "#4f4f4f", "#585858", "#5f5f5f", "#6f6f6f", "#7f7f7f"]
        elif self.stylemode == "CLARO":
            ctk.set_appearance_mode("light")
            self.colors = ["#ffffff", "#efefef", "#c8c8c8", "#bfbfbf", "#a8a8a8", "#9f9f9f", "#888888", "#8f8f8f", "#8f8f8f", "#7f7f7f"]
        self.desconnectconfig()
        
        self.root = ctk.CTk()
        self.loginwindow()
        self.root.protocol("WM_DELETE_WINDOW", close)
        self.root.after(3000, self.insertcurrentproduct)
        self.root.after(3000, self.printerexecute)
        self.root.mainloop()
    def printerexecute(self):
        aprinter.init()
    def loginwindow(self):
        self.currentwindow = "LOGIN"
        self.root.attributes("-fullscreen", True)
        self.root.update()
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()

        self.entry_name = ctk.CTkEntry(self.root, bg_color=self.colors[9], placeholder_text="NOME", font=("Arial", 20))
        self.entry_name.place(relx=0.4, rely=0.45, relwidth=0.2, relheight=0.05)

        self.entry_password = ctk.CTkEntry(self.root, bg_color=self.colors[9], placeholder_text="SENHA", show="*", font=("Arial", 20))
        self.entry_password.place(relx=0.4, rely=0.55, relwidth=0.2, relheight=0.05)
        
        self.button_login = ctk.CTkButton(self.root, fg_color=self.colors[9], text="LOGIN", hover_color=self.colors[8], command=self.login, font=("Arial", 20))
        self.button_login.place(relx=0.4, rely=0.65, relwidth=0.2, relheight=0.05)
        

        self.personimg = ctk.CTkImage(Image.open("./imgs/person.png"), size=(self.height//3.6,self.height//3.6))
        self.label_person = ctk.CTkLabel(self.root, image = self.personimg, bg_color="#242424", text="")
        self.label_person.place(relx=0.423, rely=0.15)
        temp = ""
        self.connectconts()
        tmp = self.contscursor.execute("SELECT * FROM Conts")
        for i in tmp:
            temp = i[0]
            break
        if temp == "":
            self.contscursor.execute("INSERT INTO Conts (username, name, password, permissionmaster, permissionrelease, permissionentry) VALUES (?, ?, ?, ?, ?, ?)",("ADMIN", "Admin", "ADMIN", "Y", "Y", "Y"))
        self.desconnectconts()
        self.root.bind_all("<KeyPress>", self.keypresslogin)
    def keypresslogin(self, event):
        n = event.keysym
        if n == "Return":
            self.login()
    def on_closingcommandwindow(self):
        self.root.bind_all("<KeyPress>", self.presskey)
        self.connectcommands()
        self.connectclients()
        try:
            temp = self.clientscursor.execute("SELECT name FROM Clients WHERE id = ?", (self.idclient.get(), ))
            for i in temp:
                temp = i[0]
        except:
            temp = ""
        self.desconnectclients()
        if self.nameclient.get() != self.actuallyname:
            print(self.nameclient.get())
            print(temp)
            if temp == self.nameclient.get():
                self.commandscursor.execute("UPDATE CommandsActive SET idclient = ?, nameclient = ? WHERE number = ?", (self.idclient.get(), self.nameclient.get(), self.currentcommandwindow))
            else:
                self.commandscursor.execute("UPDATE CommandsActive SET idclient = ?, nameclient = ? WHERE number = ?", ("", self.nameclient.get(), self.currentcommandwindow))
        self.desconnectcommands()
            
        
        self.rootcommand.destroy()
    def window(self):
        self.entry_name.destroy(); self.entry_password.destroy(); self.button_login.destroy(); self.label_person.destroy()
        del self.personimg
        try:
            self.label_failedlogin.destroy()
        except:
            pass
        self.frame_tab = ctk.CTkFrame(self.root, fg_color=self.colors[7], border_color=self.colors[0])
        self.frame_tab.place(relx=0, rely=0, relwidth=1, relheight=0.14)


        self.label_none = ctk.CTkLabel(self.frame_tab, fg_color=self.colors[6], text="")
        self.label_none.place(relx=0.2, rely=0, relwidth=0.8, relheight=0.285)

        self.button_main = ctk.CTkButton(self.frame_tab, text="PRINCIPAL", hover_color=self.colors[4], fg_color=self.colors[5], command=lambda:self.changemainbuttons(self.button_main))
        self.button_main.place(relx=0, rely=0, relwidth=0.1, relheight=0.285)

        self.button_product = ctk.CTkButton(self.frame_tab, text="PRODUTO", hover_color=self.colors[4], fg_color=self.colors[5], command=lambda:self.changemainbuttons(self.button_product))
        self.button_product.place(relx=0.1, rely=0, relwidth=0.1, relheight=0.285)

        self.button_config = ctk.CTkButton(self.frame_tab, text="CONFIGURAÇÕES", hover_color=self.colors[4], fg_color=self.colors[5], command=lambda:self.changemainbuttons(self.button_config))
        self.button_config.place(relx=0.2, rely=0, relwidth=0.1, relheight=0.285)

    def mainwindow(self):
        
        self.deletewindow()
        self.currentwindow = "MAIN"
        self.str_searchcommands = tk.StringVar()
        self.str_searchcommands.set("")
        self.label_searchcommand = ctk.CTkLabel(self.root, fg_color=self.colors[1], textvariable=self.str_searchcommands, font=("Arial", 20))
        self.label_searchcommand.place(relx=0.01, rely=0.15, relwidth=0.88, relheight=0.05)

        self.button_addcommand = ctk.CTkButton(self.root, fg_color=self.colors[3], text="ADICIONAR COMANDA", hover_color=self.colors[2], command=self.newcommands)
        self.button_addcommand.place(relx=0.90, rely=0.15, relwidth=0.09, relheight=0.05)
        
        self.root.bind_all("<KeyPress>", self.presskey)

        self.frame_commands = ctk.CTkScrollableFrame(self.root, fg_color=self.colors[1])
        self.frame_commands.place(relx=0.01, rely=0.21, relwidth=0.98, relheight=0.71)

        

        self.frame_down = ctk.CTkFrame(self.root, fg_color=self.colors[3], border_color=self.colors[0])
        self.frame_down.place(relx=0, rely=0.93, relwidth=1, relheight=0.07)

        self.entry_namecommand = ctk.CTkEntry(self.frame_down, placeholder_text="PESQUISAR POR NOME", fg_color=self.colors[7], font=("Arial", 20))
        self.entry_namecommand.place(relx=0.3, rely=0.175 , relwidth=0.15, relheight=0.65)

        self.button_updatecommand = ctk.CTkButton(self.frame_down, fg_color=self.colors[7], text="ATUALIZAR", hover_color=self.colors[6])
        self.button_updatecommand.place(relx=0.02, rely=0.175, relwidth=0.1, relheight=0.65)

        self.button_mergecommands = ctk.CTkButton(self.frame_down, fg_color=self.colors[7], text="JUNTAR COMANDAS", hover_color=self.colors[6])
        self.button_mergecommands.place(relx=0.135, rely=0.175, relwidth=0.15, relheight=0.65)

        self.root.bind("<Button-1>", self.clickmain)
        threading.Thread(self.reloadcommands()).start()
    def productswindow(self):
        self.deletewindow()
        self.currentwindow = "PRODUCTS"

        self.frame_modproducts = ctk.CTkFrame(self.root, fg_color=self.colors[3])
        self.frame_modproducts.place(relx=0, rely=0.14, relwidth=1, relheight=0.05)
        
        self.frame_producttypes = ctk.CTkFrame(self.root, fg_color=self.colors[4])
        self.frame_producttypes.place(relx=0, rely=0.19, relwidth=1, relheight=0.05)

        self.entry_searchproducts = ctk.CTkEntry(self.frame_modproducts, fg_color=self.colors[5], placeholder_text="PESQUISAR PRODUTO")
        self.entry_searchproducts.place(relx=0.01, rely=0.1, relwidth=0.19, relheight=0.80)

        self.button_addproduct = ctk.CTkButton(self.frame_modproducts, fg_color=self.colors[5], hover_color=self.colors[4], text="ADICIONAR", command=self.addproductwindow)
        self.button_addproduct.place(relx=0.8, rely=0.1, relwidth=0.19, relheight=0.80)

        self.button_products = ctk.CTkButton(self.frame_producttypes, text="PRODUTOS", hover_color=self.colors[5], fg_color=self.colors[6], command=lambda:self.changeproductlistbuttons(self.button_products))
        self.button_products.place(relx=0, rely=0, relwidth=0.1, relheight=1)

        self.button_producttypes = ctk.CTkButton(self.frame_producttypes, text="PRODUTOS POR TAMANHO", hover_color=self.colors[5], fg_color=self.colors[6], command=lambda:self.changeproductlistbuttons(self.button_producttypes))
        self.button_producttypes.place(relx=0.1, rely=0, relwidth=0.15, relheight=1)

        self.button_productcombos = ctk.CTkButton(self.frame_producttypes, text="COMBOS", hover_color=self.colors[5], fg_color=self.colors[6], command=lambda:self.changeproductlistbuttons(self.button_productcombos))
        self.button_productcombos.place(relx=0.25, rely=0, relwidth=0.1, relheight=1)

        self.frame_productreeviews = ctk.CTkScrollableFrame(self.root, fg_color=self.colors[3])
        self.frame_productreeviews.place(relx=0, rely=0.24, relwidth=1, relheight=0.76)
        self.changeproductlistbuttons(self.button_products)
    def changeproductlistbuttons(self, button):
        self.button_products.configure(fg_color=self.colors[5], hover_color=self.colors[4], hover=True)
        self.button_producttypes.configure(fg_color=self.colors[5], hover_color=self.colors[4], hover=True)
        self.button_productcombos.configure(fg_color=self.colors[5], hover_color=self.colors[4], hover=True)
        button.configure(fg_color=self.colors[3], hover=False)
        temp = button.cget("text")
        try:
            if self.current_productlisttab == "PRODUTOS":
                self.productcategory_heading.destroy(); self.productname_heading.destroy(); self.productprice_heading.destroy(), self.productedit_heading.destroy(); self.productdel_heading.destroy()
                for i in self.current_productslist:
                    for n in i:
                        n.destroy()
            elif self.current_productlisttab == "PRODUTOS POR TAMANHO":
                self.productsizecategory_heading.destroy(); self.productsizename_heading.destroy(); self.productsizeprice_heading.destroy(); self.productsizeedit_heading.destroy(); self.productsizedel_heading.destroy()
                for i in self.current_productslist:
                    i[0].destroy()
                    i[1].destroy()
                    i[2].destroy()
                    i[3].destroy()
                    i[4].destroy()
            elif self.current_productlisttab == "COMBOS":
                pass
        
        except Exception as error:
            print(error)
        if temp == "PRODUTOS":
            self.current_productlisttab = "PRODUTOS"
            
            self.productcategory_heading = ctk.CTkLabel(self.frame_productreeviews, text="CATEGORIA", width=400, height=50, fg_color=self.colors[4])
            self.productcategory_heading.grid(row=1, column=1, padx=1, pady=1)

            self.productname_heading = ctk.CTkLabel(self.frame_productreeviews, text="PRODUTO", width=400, height=50, fg_color=self.colors[4])
            self.productname_heading.grid(row=1, column=2, padx=1, pady=1)

            self.productprice_heading = ctk.CTkLabel(self.frame_productreeviews, text="PREÇO", width=100, height=50, fg_color=self.colors[4])
            self.productprice_heading.grid(row=1, column=3, padx=1, pady=1)

            self.productedit_heading = ctk.CTkLabel(self.frame_productreeviews, text="EDITAR", width=100, height=50, fg_color=self.colors[4])
            self.productedit_heading.grid(row=1, column=4, padx=1, pady=1)

            self.productdel_heading = ctk.CTkLabel(self.frame_productreeviews, text="EXCLUIR", width=100, height=50, fg_color=self.colors[4])
            self.productdel_heading.grid(row=1, column=5, padx=1, pady=1)

            self.reloadproductsnormal()

        elif temp == "PRODUTOS POR TAMANHO":
            self.current_productlisttab = "PRODUTOS POR TAMANHO"

            self.productsizecategory_heading = ctk.CTkLabel(self.frame_productreeviews, text="CATEGORIA", width=400, height=50, fg_color=self.colors[4])
            self.productsizecategory_heading.grid(row=1, column=1, padx=1, pady=1)

            self.productsizename_heading = ctk.CTkLabel(self.frame_productreeviews, text="PRODUTO", width=400, height=50, fg_color=self.colors[4])
            self.productsizename_heading.grid(row=1, column=2, padx=1, pady=1)

            self.productsizeprice_heading = ctk.CTkLabel(self.frame_productreeviews, text="PREÇOS", width=200, height=50, fg_color=self.colors[4])
            self.productsizeprice_heading.grid(row=1, column=3, padx=1, pady=1)

            self.productsizeedit_heading = ctk.CTkLabel(self.frame_productreeviews, text="EDITAR", width=100, height=50, fg_color=self.colors[4])
            self.productsizeedit_heading.grid(row=1, column=4, padx=1, pady=1)

            self.productsizedel_heading = ctk.CTkLabel(self.frame_productreeviews, text="EXCLUIR", width=100, height=50, fg_color=self.colors[4])
            self.productsizedel_heading.grid(row=1, column=5, padx=1, pady=1)

            self.reloadproductssize()
        elif temp == "COMBOS":
            self.current_productlisttab = "COMBOS"
    def reloadproductssize(self):
        def deleteproductsize(product, category):
            self.connectproduct()
            self.productcursor.execute("DELETE FROM SizeofProducts WHERE product = ? AND category = ?", (product, category))
            self.productcursor.execute("DELETE FROM Products WHERE name = ? AND category = ? AND type = ?", (product, category, "SIZE"))
            self.desconnectproduct()
            self.reloadproductssize()
        listofproducts = []
        try:
            for i in self.current_productslist:
                i[0].destroy()
                i[1].destroy()
                i[2].destroy()
                i[3].destroy()
                i[4].destroy()
        except:
            pass
        self.connectproduct()
        self.current_productslist = []
        temp = self.productcursor.execute("SELECT name, category, printer FROM Products WHERE type = ?", ("SIZE", ))
        for i in temp:
            listofproducts.append(i)
        for k, i in enumerate(listofproducts):
            print(i)
            product, category, printer = i
            temp = self.productcursor.execute("SELECT price FROM SizeofProducts WHERE product = ? AND category = ?", (product, category))
            prices = [9999, -1]
            for n in temp:
                price = n[0]
                price.replace(",", ".")
                price = float(price)
                if prices[0] > price:
                    prices[0] = price
                if prices[1] < price:
                    prices[1] = price
            self.current_productslist.append([ctk.CTkLabel(self.frame_productreeviews, fg_color=self.colors[5], text=category, width=400, height=50), 
                                             ctk.CTkLabel(self.frame_productreeviews, fg_color=self.colors[5], text=product, width=400, height=50), 
                                             ctk.CTkLabel(self.frame_productreeviews, fg_color=self.colors[5], text=str(prices[0]) + " - " + str(prices[1]), width=200, height=50), 
                                             ctk.CTkButton(self.frame_productreeviews, fg_color=self.colors[5], text="", width=100, height=50, image=ctk.CTkImage(Image.open("./imgs/pencil.jpg"), size=(40,40)), hover=False, command=lambda x = product, y = category, z = printer:self.addproductwindow(x, y, z)), 
                                             ctk.CTkButton(self.frame_productreeviews, fg_color=self.colors[5], text="", width=100, height=50, image=ctk.CTkImage(Image.open("./imgs/lixeira.png"), size=(40,40)), hover=False, command=lambda x=product, y=category:deleteproductsize(x, y))])
            self.current_productslist[k][0].grid(row=k + 2, column=1, padx=1, pady=1)
            self.current_productslist[k][1].grid(row=k + 2, column=2, padx=1, pady=1)
            self.current_productslist[k][2].grid(row=k + 2, column=3, padx=1, pady=1)
            self.current_productslist[k][3].grid(row=k + 2, column=4, padx=1, pady=1)
            self.current_productslist[k][4].grid(row=k + 2, column=5, padx=1, pady=1)
        self.desconnectproduct()
    def notewindow(self):
        def click(event):
            if event.keysym == "Escape":
                close()
        def close():
            self.root.bind_all("<KeyPress>", self.presskeycommandwindow)
            self.editnote.destroy()
            self.root.grab_set()
        def edit(category):
            def remove(id):
                self.connectproduct()
                self.productcursor.execute("DELETE FROM Notes WHERE id = ?", (id, ))
                self.desconnectproduct()
                reload()
            def add():
                self.connectproduct()
                self.productcursor.execute("INSERT INTO Notes (text, category) VALUES (?, ?)", (self.entrynote.get(), category))
                self.desconnectproduct()
                reload()
                
            def reload():
                try:
                    for i in self.current_notes:
                        for j in i:
                            j.destroy()
                except:
                    pass
                self.connectproduct()
                self.current_notes = []
                temp = self.productcursor.execute("SELECT id, text FROM Notes WHERE category = ?", (category, ))
                for k, i in enumerate(temp):
                    self.current_notes.append([ctk.CTkLabel(self.framenotes, bg_color=self.colors[4], text=i[1], width=500, height=50), ctk.CTkButton(self.framenotes, fg_color=self.colors[4], hover=False, width=60, height=50, image=ctk.CTkImage(Image.open("./imgs/lixeira.png"), size=(45, 45)), text="", command=lambda x = i[0]:remove(x))])

                    n = k + 2
                    self.current_notes[k][0].grid(row=n, column=1, padx=1, pady=1)
                    self.current_notes[k][1].grid(row=n, column=2, padx=1, pady=1)
                self.desconnectproduct()
            self.editnote = ctk.CTkToplevel(self.root)
            self.editnote.geometry("600x500")
            self.editnote.transient(self.root)
            self.editnote.resizable(False, False)
            self.editnote.title("EDITAR ANOTAÇÕES DA CATEGORIA " + str(category))
            self.editnote.grab_set()

            self.framenotes = ctk.CTkScrollableFrame(self.editnote)
            self.framenotes.place(relx=0.01, rely=0.2, relwidth=0.98, relheight=0.79)

            self.entrynote = ctk.CTkEntry(self.editnote)
            self.entrynote.place(relx=0.01, rely=0.03, relwidth=0.75, relheight=0.15)

            self.addnote = ctk.CTkButton(self.editnote, text="Adicionar", fg_color=self.colors[4], hover_color=self.colors[3], command=add)
            self.addnote.place(relx=0.76, rely=0.03, relwidth=0.23, relheight=0.15)

            self.notes = ctk.CTkLabel(self.framenotes, bg_color=self.colors[4], text="ANOTAÇÕES", width=500, height=50)
            self.notes.grid(row=1, column=1, padx=1, pady=1)

            self.dellabel = ctk.CTkLabel(self.framenotes, bg_color=self.colors[4], text="DELETAR", width=60, height=50)
            self.dellabel.grid(row=1, column=2, padx=1, pady=1)

            self.root.bind_all("<KeyPress>", click)
            self.editnote.protocol("WM_DELETE_WINDOW", close)
            reload()

        self.deletewindow()
        self.currentwindow = "ANOTAÇÕES"
        
        self.frame_note = ctk.CTkScrollableFrame(self.root)
        self.frame_note.place(relx=0.01, rely=0.145, relwidth=0.98, relheight=0.85)

        self.categoryname = ctk.CTkLabel(self.frame_note, width=300, height=50, bg_color=self.colors[4], text="CATEGORIA")
        self.categoryname.grid(row=1, column=1, padx=1, pady=2)

        self.editnotes = ctk.CTkLabel(self.frame_note, width=50, height=50, bg_color=self.colors[4], text="EDITAR")
        self.editnotes.grid(row=1, column=2, padx=1, pady=2)

        self.tablecategory = []

        self.connectproduct()
        temp = self.productcursor.execute("SELECT cod, name From Category")

        for k, i in enumerate(temp):
            self.tablecategory.append([ctk.CTkLabel(self.frame_note, fg_color=self.colors[4], width=300, height=50, text=i[1]), ctk.CTkButton(self.frame_note, hover=False, fg_color=self.colors[4], width=50, height=50, text="", image=ctk.CTkImage(Image.open("./imgs/pencil.jpg"), size=(35, 35)), command=lambda x = i[1]:edit(x))])

            n = k + 2

            self.tablecategory[k][0].grid(row=n, column=1, padx=1, pady=1)
            self.tablecategory[k][1].grid(row=n, column=2, padx=1, pady=1)
            

        self.desconnectproduct()
    def configwindow(self):
        def save():
            self.connectconfig()
            self.configcursor.execute("""UPDATE Config SET stylemode = ?, maxcommands = ?, cnpj = ?, housename = ?, adress = ?, fone = ?, printer = ?, male = ?, female = ? WHERE cod = 1""", (self.stylevar.get(), self.limitcommands.get(), self.entry_cnpj.get(), self.entry_namehome.get(), self.entry_adress.get(), self.entry_fone.get(), self.printerclosedvar.get(), self.male.get(), self.female.get()))
            self.desconnectconfig()
        self.deletewindow()
        self.currentwindow = "CONFIG"

        self.connectconfig()
        temp = self.configcursor.execute("SELECT stylemode, maxcommands, cnpj, housename, adress, fone, printer, female, male FROM Config WHERE cod = '1'")

        for i in temp:
            style, maxcommands, cnpj, housename, adress, fone, prynter, male, female = i
        self.desconnectconfig()

        self.frame_config = ctk.CTkScrollableFrame(self.root)
        self.frame_config.place(relx=0.01, rely=0.2, relwidth=0.98, relheight=0.79)

        self.ipserver = ctk.CTkLabel(self.frame_config, width=200, height=50, text="IP DO SERVIDOR:", bg_color=self.colors[4])
        self.ipserver.grid(row=1, column=1, padx=1, pady=1)

        self.ipserverlb = ctk.CTkLabel(self.frame_config, width=200, height=50, bg_color=self.colors[4], text=socket.gethostbyname(socket.gethostname()))
        self.ipserverlb.grid(row=1, column=2, padx=1, pady=1)

        self.limitcommandslb = ctk.CTkLabel(self.frame_config, text="LIMITE DE COMANDAS:", bg_color=self.colors[4], width=200, height=40)
        self.limitcommandslb.grid(row=2, column=1, padx=1, pady=1)

        self.limitcommands = ctk.CTkEntry(self.frame_config, width=200, height=40)
        self.limitcommands.grid(row=2, column=2, padx=1, pady=1)
        self.limitcommands.insert(0, maxcommands)

        self.stylelb = ctk.CTkLabel(self.frame_config, text="MODO:", bg_color=self.colors[4], width=200, height=40)
        self.stylelb.grid(row=3, column=1, padx=1, pady=1)

        self.stylevar = ctk.StringVar(value=style)
        self.style = ctk.CTkComboBox(self.frame_config, values=("ESCURO", "CLARO"), variable=self.stylevar, width=200, height=40)
        self.style.grid(row=3, column=2, padx=1, pady=1)

        self.lb_namehome = ctk.CTkLabel(self.frame_config, text="Nome do estabelecimento", bg_color=self.colors[4], width=200, height=40)
        self.lb_namehome.grid(row=4, column=1, padx=1, pady=1)

        self.entry_namehome = ctk.CTkEntry(self.frame_config, width=200, height=40)
        self.entry_namehome.grid(row=4, column=2, padx=1, pady=1)
        self.entry_namehome.insert(0, housename)

        self.lb_cnpj = ctk.CTkLabel(self.frame_config, text="CNPJ:", bg_color=self.colors[4], width=200, height=40)
        self.lb_cnpj.grid(row=5, column=1, padx=1, pady=1)

        self.entry_cnpj = ctk.CTkEntry(self.frame_config, width=200, height=40)
        self.entry_cnpj.grid(row=5, column=2, padx=1, pady=1)
        self.entry_cnpj.insert(0, cnpj)

        self.lb_adress = ctk.CTkLabel(self.frame_config, text="Endereço:", bg_color=self.colors[4], width=200, height=40)
        self.lb_adress.grid(row=6, column=1, padx=1, pady=1)

        self.entry_adress = ctk.CTkEntry(self.frame_config, width=200, height=40)
        self.entry_adress.grid(row=6, column=2, padx=1, pady=1)
        self.entry_adress.insert(0, adress)

        self.lb_fone = ctk.CTkLabel(self.frame_config, text="Telefone:", bg_color=self.colors[4], width=200, height=40)
        self.lb_fone.grid(row=7, column=1, padx=1, pady=1)

        self.entry_fone = ctk.CTkEntry(self.frame_config, width=200, height=40)
        self.entry_fone.grid(row=7, column=2, padx=1, pady=1)

        self.entry_fone.insert(0, fone)

        self.lb_printerclosed = ctk.CTkLabel(self.frame_config, text="Impressão padrão:", bg_color=self.colors[4], width=200, height=40)
        self.lb_printerclosed.grid(row=8, column=1, padx=1, pady=1)

        printers = []
        self.connectprinter()
        temp = self.printercursor.execute("SELECT name FROM Printers")
        for i in temp:
            printers.append(i[0])
        self.desconnectprinter()

        self.printerclosedvar = ctk.StringVar(value=prynter)
        self.printerclosed = ctk.CTkComboBox(self.frame_config, width=200, height=40, values=printers, variable=self.printerclosedvar)
        self.printerclosed.grid(row=8, column=2, padx=1, pady=1)

        self.malelb = ctk.CTkLabel(self.frame_config, width=200, height=40, text="ENTRADA MASCULINO:", bg_color=self.colors[4])
        self.malelb.grid(row=9, column=1, padx=1, pady=1)

        self.male = ctk.CTkEntry(self.frame_config, width=200, height=40)
        self.male.grid(row=9, column=2, padx=1, pady=1)
        self.male.insert(0, male)

        self.femalelb = ctk.CTkLabel(self.frame_config, text="ENTRADA FEMININO:", width=200, height=40, bg_color=self.colors[4])
        self.femalelb.grid(row=10, column=1, padx=1, pady=1)

        self.female = ctk.CTkEntry(self.frame_config, width=200, height=40)
        self.female.grid(row=10, column=2, padx=1, pady=1)
        self.female.insert(0, female)

        self.button_saveconfig = ctk.CTkButton(self.root, fg_color=self.colors[4], hover_color=self.colors[3], text="SALVAR", command=save)
        self.button_saveconfig.place(relx=0.8, rely=0.145, relwidth=0.1, relheight=0.05)

    def reloadproductsnormal(self):
        self.connectproduct()
        try:
            for i in self.current_productslist:
                for n in i:
                    n.destroy()
        except:
            pass
        tmp = self.productcursor.execute("SELECT * FROM Products WHERE Type = ?", ("NORMAL", ))
        listen = []
        for i in tmp:
            listen.append(i)
        self.current_productslist = []
        for k, i in enumerate(listen):
            name, ttype, category, price, prynter = i
            self.current_productslist.append([ctk.CTkLabel(self.frame_productreeviews, text=category, fg_color=self.colors[5], width=400, height=40), 
                                              ctk.CTkLabel(self.frame_productreeviews, text=name, fg_color=self.colors[5], width=400, height=40), 
                                              ctk.CTkLabel(self.frame_productreeviews, text=price, fg_color=self.colors[5], width=100, height=40), 
                                              ctk.CTkLabel(image=ctk.CTkImage(Image.open("./imgs/pencil.jpg"), size=(30, 30)), master=self.frame_productreeviews, text="", fg_color=self.colors[5], width=100, height=40), 
                                              ctk.CTkButton(self.frame_productreeviews, command=lambda x=name, y=category, z=ttype:self.deleteproductnormal(x, y, z), image=ctk.CTkImage(Image.open("./imgs/lixeira.png"), size=(30,30)), text="", fg_color=self.colors[5], width=100, hover=False)])
            self.current_productslist[k][0].grid(row=k + 2, column=1, padx=1, pady=1)
            self.current_productslist[k][1].grid(row=k + 2, column=2, padx=1, pady=1)
            self.current_productslist[k][2].grid(row=k + 2, column=3, padx=1, pady=1)
            self.current_productslist[k][3].grid(row=k + 2, column=4, padx=1, pady=1)
            self.current_productslist[k][4].grid(row=k + 2, column=5, padx=1, pady=1)
        self.desconnectproduct()
    def deleteproductnormal(self, name, category, tipe):
        self.connectproduct()
        self.productcursor.execute("DELETE FROM Products WHERE name = ? AND category = ? AND type = ?", (name, category, tipe))
        self.desconnectproduct()
        self.reloadproductsnormal()
    def deletewindow(self):
        try:
            self.reloadthread.terminate()
        except:
            pass
        if self.currentwindow == "MAIN":
            self.frame_commands.destroy();self.frame_down.destroy();del self.str_searchcommands; self.label_searchcommand.destroy();self.button_addcommand.destroy(); self.frame_commands.place_forget()
            self.root.bind("<Button-1>", self.nonclick)
            self.root.bind_all("<KeyPress>", self.nonclick)
        elif self.currentwindow == "PRODUCTS":
            self.frame_producttypes.destroy(); self.frame_modproducts.destroy(); self.frame_productreeviews.destroy(); self.frame_productreeviews.place_forget()
        elif self.currentwindow == "CATEGORIES":
            self.treeview_categories.destroy(); self.treeview_categories.place_forget(); self.frame_categoriesmod.destroy()
        elif self.currentwindow == "CONFIG":
            self.button_saveconfig.destroy(); self.frame_config.destroy(); self.frame_config.place_forget()
        elif self.currentwindow == "FUNCIONÁRIOS":
            self.scroolframe_functionary.destroy; self.scroolframe_functionary.place_forget(); self.button_addfunctionary.destroy(); self.entry_name.destroy(); self.entry_passwordcont.destroy()
        elif self.currentwindow == "CLIENTES":
            self.frameclients.destroy(); self.frameclients.place_forget(); self.buttonaddclient.destroy(); self.searchclients.destroy()
        elif self.currentwindow == "CASH":
            self.scrollframehis.destroy(); self.scrollframehis.place_forget(); self.entrysearchhis.destroy(); 
            try:
                self.buttonopencash.destroy()
            except:
                pass
        elif self.currentwindow == "ANOTAÇÕES":
            self.frame_note.destroy(); self.frame_note.place_forget()
        elif self.currentwindow == "CASHDESKHISTORY":
            self.scrollframecashs.destroy(); self.scrollframecashs.place_forget(); self.initlb.destroy(); self.initentry.destroy(); self.finishlb.destroy(); self.finishentry.destroy(); self.confirmdate.destroy()
        elif self.currentwindow == "RANKINGPRODUCTS":
            self.initlb.destroy(); self.initentry.destroy(); self.finishlb.destroy(); self.finishentry.destroy(); self.confirmdate.destroy(); self.frameranking.destroy(); self.frameranking.place_forget(); self.frameinithour.destroy(); self.frameinitmin.destroy(); self.framefinishhour.destroy(); self.framefinishmin.destroy()
        elif self.currentwindow == "PRINTERS":
            self.nameprinter.destroy(); self.ipprinter.destroy(); self.addprinter.destroy(); self.frameprinters.destroy(); self.frameprinters.place_forget()
        elif self.currentwindow == "RANKINGSERVICE":
            self.initlb.destroy(); self.initentry.destroy(); self.finishlb.destroy(); self.finishentry.destroy(); self.confirmdate.destroy(); self.frame_ranking.destroy(); self.frame_ranking.place_forget(); self.frameinithour.destroy(); self.frameinitmin.destroy(); self.framefinishhour.destroy(); self.framefinishmin.destroy()
        elif self.currentwindow == "HISTORYPRODUCTS":
            self.frame_hisproducts.destroy(); self.frame_hisproducts.place_forget()
        self.root.bind_all("<KeyPress>", self.nonclick)
        self.root.bind("<Button-1>", self.nonclick)
    def clientswindow(self):
        def removeclient(id):
            self.connectclients()
            self.clientscursor.execute("DELETE FROM Clients WHERE id = ?", (id, ))
            self.desconnectclients()
            reloadclients()
        def reloadclients():
            try:
                for i in self.clientstable:
                    for j in i:
                        j.destroy()
            except:
                pass
            self.clientstable = []
            self.connectclients()
            temp = self.clientscursor.execute("SELECT * FROM Clients")
            listen = []
            for i in temp:
                listen.append(i)
            self.desconnectclients()
            for k, i in enumerate(listen):
                id, name, fone, email, idade, gender = i
                self.clientstable.append([ctk.CTkLabel(self.frameclients, text=id, bg_color=self.colors[4], width=50, height=40), 
                ctk.CTkLabel(self.frameclients, text=name, bg_color=self.colors[4], width=300, height=40), 
                ctk.CTkLabel(self.frameclients, text=fone, bg_color=self.colors[4], width=150, height=40), 
                ctk.CTkLabel(self.frameclients, text=email, bg_color=self.colors[4], width=200, height=40), 
                ctk.CTkLabel(self.frameclients, text=idade, bg_color=self.colors[4], width=70, height=40),
                ctk.CTkButton(self.frameclients, text="", fg_color=self.colors[4], hover=False, image=ctk.CTkImage(Image.open("./imgs/lixeira.png"), size=(30, 30)), command=lambda x = id:removeclient(x), width=50, height=40)])
                n = k + 2
                self.clientstable[k][0].grid(row=n, column=1, padx=1, pady=1)
                self.clientstable[k][1].grid(row=n, column=2, padx=1, pady=1)
                self.clientstable[k][2].grid(row=n, column=3, padx=1, pady=1)
                self.clientstable[k][3].grid(row=n, column=4, padx=1, pady=1)
                self.clientstable[k][4].grid(row=n, column=5, padx=1, pady=1)
                self.clientstable[k][5].grid(row=n, column=6, padx=1, pady=1)
        def addclientwindow():
            def close():
                self.root.bind_all("<KeyPress>", self.nonclick)
                self.rootaddclient.destroy()
                self.root.grab_set()
            def press(event):
                if event.keysym == "Escape":
                    close()
            def addclient(cod = 0):
                iid, name, fone, email, year, gender = self.entryid.get(), self.entryname.get(), self.entryfone.get(), self.entryemail.get(), self.entryidade.get(), self.entrygender.get()
                self.connectclients()
                tp = ""
                temp = []
                if iid == "":
                    self.clientscursor.execute("INSERT INTO Clients (name, fone, email, idade, genero) VALUES (?, ?, ?, ?, ?)", (name, fone, email, year, gender))
                else:
                    try:
                        temp = self.clientscursor.execute("SELECT name, fone, email, idade, genero FROM Clients WHERE id = ?", (iid, ))
                        for i in temp:
                            tp = i
                    except:
                        pass
                    if tp != "":
                        self.clientscursor.execute("INSERT INTO Clients (name, fone, email, idade, genero) VALUES (?, ?, ?, ?, ?)", (tp[0], tp[1], tp[2], tp[3], tp[4]))
                        self.clientscursor.execute("UPDATE Clients SET name = ?, fone = ?, email = ?, idade = ?, genero = ? WHERE id = ?", (name, fone, email, year, gender, iid))
                    else:
                        self.clientscursor.execute("INSERT INTO Clients (id, name, fone, email, idade, genero) VALUES (?, ?, ?, ?, ?, ?)", (iid, name, fone, email, year, gender))
                tp = ""
                temp = self.clientscursor.execute("select name, fone, email, idade FROM Clients Where id = ?", (iid, ))
                self.desconnectclients()
                close()
                reloadclients()
            self.rootaddclient = ctk.CTkToplevel(self.root)
            self.rootaddclient.geometry("500x150")
            self.rootaddclient.transient(self.root)
            self.rootaddclient.grab_set()
            self.rootaddclient.title("ADICIONAR CLIENTE")

            self.entryid = ctk.CTkEntry(self.rootaddclient, placeholder_text="ID")
            self.entryid.place(relx=0.01, rely=0.01, relwidth=0.1, relheight=0.3)

            self.entryname = ctk.CTkEntry(self.rootaddclient, placeholder_text="Nome")
            self.entryname.place(relx=0.12, rely=0.01, relwidth=0.87, relheight=0.3)

            self.entryfone = ctk.CTkEntry(self.rootaddclient, placeholder_text="Telefone")
            self.entryfone.place(relx=0.01, rely=0.31, relwidth=0.3, relheight=0.3)
            
            self.entryemail = ctk.CTkEntry(self.rootaddclient, placeholder_text="Email")
            self.entryemail.place(relx=0.32, rely=0.31, relwidth=0.67, relheight=0.3)

            self.entryidade = ctk.CTkEntry(self.rootaddclient, placeholder_text="Idade")
            self.entryidade.place(relx=0.01, rely=0.62, relwidth=0.2, relheight=0.3)

            self.entrygender = ctk.CTkComboBox(self.rootaddclient, values=["Masculino", "Feminino"], width=500*0.47, height=150*0.3)
            self.entrygender.place(relx=0.22, rely=0.62)

            self.buttonconclient = ctk.CTkButton(self.rootaddclient, text="CONFIRMAR", fg_color=self.colors[4], hover_color=self.colors[3], command=addclient)
            self.buttonconclient.place(relx=0.70, rely=0.62, relwidth=0.29, relheight=0.3)


            self.root.bind_all("<KeyPress>", press)
            self.rootaddclient.protocol("WM_DELETE_WINDOW", close)
        self.deletewindow()
        self.currentwindow = "CLIENTES"

        self.buttonaddclient = ctk.CTkButton(self.root, text="ADICIONAR CLIENTE", fg_color=self.colors[4], hover_color=self.colors[3], command=addclientwindow)
        self.buttonaddclient.place(relx=0.89, rely=0.15, relwidth=0.1 , relheight=0.05)
        
        self.frameclients = ctk.CTkScrollableFrame(self.root)
        self.frameclients.place(relx=0.01, rely=0.21, relwidth=0.98, relheight=0.79)
        
        self.searchclients = ctk.CTkEntry(self.root, placeholder_text="PESQUISAR CLIENTE")
        self.searchclients.place(relx=0.01, rely=0.15, relwidth=0.2 , relheight=0.05)

        self.headidclient = ctk.CTkLabel(self.frameclients, bg_color=self.colors[4], text="ID", width=50, height=40)
        self.headidclient.grid(row=1, column=1, padx=1, pady=1)

        self.headnameclient = ctk.CTkLabel(self.frameclients, bg_color=self.colors[4], text="NOME", width=300, height=40)
        self.headnameclient.grid(row=1, column=2, padx=1, pady=1)

        self.headfoneclient = ctk.CTkLabel(self.frameclients, bg_color=self.colors[4], text="TELEFONE", width=150, height=40)
        self.headfoneclient.grid(row=1, column=3, padx=1, pady=1)

        self.heademailclient = ctk.CTkLabel(self.frameclients, bg_color=self.colors[4], text="EMAIL", width=200, height=40)
        self.heademailclient.grid(row=1, column=4, padx=1, pady=1)

        self.headyearsclient = ctk.CTkLabel(self.frameclients, bg_color=self.colors[4], text="IDADE", width=70, height=40)
        self.headyearsclient.grid(row=1, column=5, padx=1, pady=1)

        self.deleteclient = ctk.CTkLabel(self.frameclients, bg_color=self.colors[4], text="DELETAR", width=50, height=40)
        self.deleteclient.grid(row=1, column=6, padx=1, pady=1)

        reloadclients()
    def addproductwindow(self, product = "", category = "", prynter = ""):
        self.connectprinter()
        tmp = self.printercursor.execute("SELECT name FROM Printers")
        printers = []
        for i in tmp:
            printers.append(i[0])
        self.desconnectprinter()
        if self.current_productlisttab == "PRODUTOS":
            self.rootnewproduct = ctk.CTkToplevel()
            self.rootnewproduct.title("ADICIONAR PRODUTO")
            self.rootnewproduct.geometry("500x300")
            self.rootnewproduct.transient(self.root)
            self.rootnewproduct.grab_set()

            self.frame_mainnewproduct = ctk.CTkFrame(self.rootnewproduct, fg_color=self.colors[2])
            self.frame_mainnewproduct.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.49)

            self.entry_price = ctk.CTkEntry(self.frame_mainnewproduct, placeholder_text="PREÇO", fg_color=self.colors[4])
            self.entry_price.place(relx=0.41, rely=0.11, relwidth=0.39, relheight=0.39)

            self.entry_namenewproduct = ctk.CTkEntry(self.frame_mainnewproduct, placeholder_text="NOME", fg_color=self.colors[4])
            self.entry_namenewproduct.place(relx=0.01, rely=0.11, relwidth=0.29, relheight=0.39)
            categories = []
            self.connectproduct()
            temp = self.productcursor.execute("SELECT name FROM Category")
            for i in temp:
                categories.append(i[0])
            self.desconnectproduct()

            self.combobox_categoryname = ctk.CTkComboBox(self.frame_mainnewproduct, fg_color=self.colors[4], values=categories, width=200,height=60)
            self.combobox_categoryname.place(relx=0.5, rely=0.6)

            self.combobox_printer = ctk.CTkComboBox(self.rootnewproduct, values=printers, width=150, height=55)
            self.combobox_printer.place(relx=0.4, rely=0.6)

            self.button_addproductconfirm = ctk.CTkButton(self.rootnewproduct, fg_color=self.colors[4], hover_color=self.colors[5], text="CONFIRMAR", command=self.addproductfunc)
            self.button_addproductconfirm.place(relx=0.7, rely=0.6, relwidth=0.29, relheight=0.2)
        elif self.current_productlisttab == "PRODUTOS POR TAMANHO":
            self.current_sizesfornewproduct = []
            self.rootaddproductsize = ctk.CTkToplevel(self.root)
            self.rootaddproductsize.geometry("800x500")
            self.rootaddproductsize.transient(self.root)
            self.rootaddproductsize.title("ADICIONAR PRODUTO POR TAMANHO")
            self.rootaddproductsize.grab_set()

            self.frame_mainnewproduct = ctk.CTkFrame(self.rootaddproductsize, fg_color=self.colors[2])
            self.frame_mainnewproduct.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.29)

            self.entry_price = ctk.CTkEntry(self.frame_mainnewproduct, placeholder_text="PREÇO", fg_color=self.colors[4])
            self.entry_price.place(relx=0.41, rely=0.60, relwidth=0.27, relheight=0.39)

            self.entry_namenewproduct = ctk.CTkEntry(self.frame_mainnewproduct, placeholder_text="NOME", fg_color=self.colors[4])
            self.entry_namenewproduct.place(relx=0.01, rely=0.11, relwidth=0.22, relheight=0.39)

            self.entry_namesize = ctk.CTkEntry(self.frame_mainnewproduct, placeholder_text="NOME DO TAMANHO", fg_color= self.colors[4])
            self.entry_namesize.place(relx=0.01, rely=0.60, relwidth=0.39, relheight=0.39)

            categories = []
            self.connectproduct()
            temp = self.productcursor.execute("SELECT name FROM Category")
            for i in temp:
                categories.append(i[0])
            self.desconnectproduct()

            self.combobox_categoryname = ctk.CTkComboBox(self.frame_mainnewproduct, fg_color=self.colors[4], values=categories, width=200,height=60)
            self.combobox_categoryname.place(relx=0.24, rely=0.10)

            self.combobox_printer = ctk.CTkComboBox(self.frame_mainnewproduct, values=printers, width=150, height=60)
            self.combobox_printer.place(relx=0.5, rely=0.10)

            self.button_addproductconfirm = ctk.CTkButton(self.frame_mainnewproduct, fg_color=self.colors[4], hover_color=self.colors[5], text="SALVAR", command=self.addproductsize)
            self.button_addproductconfirm.place(relx=0.70, rely=0.11, relwidth=0.29, relheight=0.39)

            self.scroolframe_sizeproductsseize = ctk.CTkScrollableFrame(self.rootaddproductsize, fg_color=self.colors[4])
            self.scroolframe_sizeproductsseize.place(relx=0.01, rely=0.31, relwidth=0.98, relheight=0.68)

            self.button_addsize = ctk.CTkButton(self.frame_mainnewproduct, fg_color=self.colors[4], hover_color=self.colors[5], text="ADICIONAR TAMANHO", command=self.addsizeforproduct)
            self.button_addsize.place(relx=0.69, rely=0.60, relwidth=0.30, relheight=0.39)

            self.name_heading = ctk.CTkLabel(self.scroolframe_sizeproductsseize, fg_color=self.colors[5], width=300, height=50, text="TAMANHO")
            self.name_heading.grid(row=1, column=1, padx=1, pady=1)

            self.price_heading = ctk.CTkLabel(self.scroolframe_sizeproductsseize, fg_color=self.colors[5], width=200, height=50, text="PREÇO")
            self.price_heading.grid(row=1, column=2, padx=1, pady=1)
            
            self.delete_heading = ctk.CTkLabel(self.scroolframe_sizeproductsseize, fg_color=self.colors[5], width=100, height=50, text="EXCLUIR")
            self.delete_heading.grid(row=1, column=3, padx=1, pady=1)

            if product != "" and category != "":
                self.connectproduct()
                self.rootaddproductsize.title("EDITAR PRODUTO POR TAMANHO")
                temp = self.productcursor.execute("SELECT name, price FROM SizeofProducts WHERE product = ? AND category = ?", (product, category))
                for i in temp:
                    self.current_sizesfornewproduct.append(i)
                self.desconnectproduct()
                self.entry_namenewproduct.insert(0, product)
                self.combobox_categoryname.set(category)
                self.button_addproductconfirm.configure(command=lambda x=product, y=category:self.addproductsize(x, y))
                self.combobox_printer.set(prynter)
                self.reloadsizesinwindow()
    def addsizeforproduct(self):
        name = self.entry_namesize.get()
        price = self.entry_price.get()
        temp = ""
        for i in self.current_sizesfornewproduct:
            if i[0] == name:
                temp = name
        if temp == "":
            self.current_sizesfornewproduct.append([name, price])
        self.reloadsizesinwindow()
    def reloadsizesinwindow(self):
        try:
            for i in self.current_tablesizes:
                for n in i:
                    n.destroy()
        except:
            pass
        self.current_tablesizes = []
        for i, temp in enumerate(self.current_sizesfornewproduct):
            self.current_tablesizes.append([ctk.CTkLabel(self.scroolframe_sizeproductsseize, text=temp[0], width=300, height=40, fg_color=self.colors[6]), 
                                               ctk.CTkLabel(self.scroolframe_sizeproductsseize, text=temp[1], width=200, height=40, fg_color=self.colors[6]),
                                               ctk.CTkButton(self.scroolframe_sizeproductsseize, text="", width=100, height=40, image=ctk.CTkImage(Image.open("./imgs/lixeira.png"), size=(30,30)), fg_color=self.colors[6], hover=False, command=lambda x=i:self.deletesizefromproduct(x))])
            self.current_tablesizes[i][0].grid(row=i + 2, column=1, padx=1, pady=1)
            self.current_tablesizes[i][1].grid(row=i + 2, column=2, padx=1, pady=1)
            self.current_tablesizes[i][2].grid(row=i + 2, column=3, padx=1, pady=1)
    def deletesizefromproduct(self, i):
        del(self.current_sizesfornewproduct[i])
        self.reloadsizesinwindow()
    def addproductsize(self, oldname = "", oldcategory = ""):
        name = self.entry_namenewproduct.get()
        category = self.combobox_categoryname.get()
        self.connectproduct()
        if oldname != "":
            self.productcursor.execute("DELETE FROM SizeofProducts WHERE product = ? AND category = ?", (oldname, oldcategory))
            self.productcursor.execute("DELETE FROM Products WHERE name = ? AND category = ? AND type = ?",(oldname, oldcategory, "SIZE"))
            temp = ""
        else:
            temp = ""
            tmp = self.productcursor.execute("SELECT name, category FROM Products WHERE name = ? AND category = ? AND type = ?", (name, category, "SIZE"))
            for i in tmp:
                if i[0] == name and i[1] == category:
                    temp = "a"
        if temp == "":
            for i in self.current_sizesfornewproduct:
                self.productcursor.execute("INSERT INTO SizeofProducts (product, price, name, category) VALUES (?, ?, ?, ?)", (name, i[1], i[0], category))
            self.product.execute("INSERT INTO Products (name, category, type, printer) VALUES (?, ?, ?, ?)", (name, category, "SIZE", self.combobox_printer.get()))
            self.rootaddproductsize.destroy()
        self.desconnectproduct()
        self.reloadproductssize()
    def addproductfunc(self):
        name = self.entry_namenewproduct.get()
        category = self.combobox_categoryname.get()
        price = self.entry_price.get()
        self.connectproduct()
        self.productcursor.execute("INSERT INTO Products (name, type, category, price, printer) VALUES (?, ?, ?, ?, ?)", (name, "NORMAL", category, price, self.combobox_printer.get()))
        self.desconnectproduct()
        self.rootnewproduct.destroy()
        self.reloadproductsnormal()
    def categorieswindow(self):
        self.deletewindow()
        self.currentwindow = "CATEGORIES"

        self.frame_categoriesmod = ctk.CTkFrame(self.root, fg_color=self.colors[2])
        self.frame_categoriesmod.place(relx=0, rely=0.14, relwidth=1, relheight=0.07)

        
        self.entry_addcategoryname = ctk.CTkEntry(self.frame_categoriesmod, fg_color=self.colors[3], placeholder_text="NOME DA CATEGORIA")
        self.entry_addcategoryname.place(relx=0.3, rely=0.1, relwidth=0.2, relheight=0.8)

        self.entry_positioncategory = ctk.CTkEntry(self.frame_categoriesmod, fg_color=self.colors[3], placeholder_text="POSIÇÃO")
        self.entry_positioncategory.place(relx=0.05, rely=0.1, relwidth=0.2, relheight=0.8)

        self.button_addcategorie = ctk.CTkButton(self.frame_categoriesmod, text="ADICIONAR", fg_color=self.colors[4], hover_color=self.colors[5], command=self.addcategoryfunc)
        self.button_addcategorie.place(relx=0.85, rely=0.1, relwidth=0.1, relheight=0.8)

        self.treeview_categories = ctk.CTkScrollableFrame(self.root, fg_color=self.colors[1])
        self.treeview_categories.place(relx=0, rely=0.21, relwidth=1, relheight=0.79)

        self.categoriesheadingid = ctk.CTkLabel(self.treeview_categories, fg_color=self.colors[3], width=100, height=50, text="POSIÇÃO")
        self.categoriesheadingid.grid(row=1, column=1, padx=0, pady=0)

        self.categoriesheadingname = ctk.CTkLabel(self.treeview_categories, fg_color=self.colors[3], width=400, height=50, text="NOME")
        self.categoriesheadingname.grid(row=1, column=2, padx=1, pady=1)

        self.categoriesheadingedit = ctk.CTkLabel(self.treeview_categories, fg_color=self.colors[3], width=100, height=50, text="EDITAR")
        self.categoriesheadingedit.grid(row=1, column=3, padx=1, pady=1)

        self.categoriesheadingdelete = ctk.CTkLabel(self.treeview_categories, fg_color=self.colors[3], width=100, height=50, text="DELETAR")
        self.categoriesheadingdelete.grid(row=1, column=4, padx=1,pady=1)

        self.reloadcategories()
    def addcategoryfunc(self):
        def insert(id, name):
            try:
                temp = self.productcursor.execute("SELECT * FROM Category WHERE cod = ?", (id, ))
                for i in temp:
                    cod, nm = i
                self.productcursor.execute("UPDATE Category SET name = ? WHERE cod = ?", (name, id))
                insert(int(cod) + 1, nm)
            except Exception as error:
                self.productcursor.execute("INSERT INTO Category (name) VALUES (?)", (name,) )
        name = self.entry_addcategoryname.get()
        id = self.entry_positioncategory.get()
        self.connectproduct()
        names = self.productcursor.execute("SELECT * FROM Category WHERE name = ?", (name, ))
        cd, nm = "", ""
        for i in names:
            cd, nm = i
        if nm == "" and name != "":
            if id != "":
                ids = self.productcursor.execute("SELECT * FROM Category WHERE cod = ?", (id, ))
                cod, nm = "", ""
                for i in ids:
                    cod, nm = i
                if cod == "":
                    self.productcursor.execute("INSERT INTO Category (name) VALUES (?)", (name,) )
                else:
                    insert(id, name)
                    
            else:
                self.productcursor.execute("INSERT INTO Category (name) VALUES (?)", (name,))
                        
        self.desconnectproduct()
        self.reloadcategories()
    def editcategorybutton(self, name, id):
        self.entry_positioncategory.delete(0, "end")
        self.entry_addcategoryname.delete(0, "end")
        try:
            self.button_editcategory.destroy()
        except:
            pass
        self.button_editcategory = ctk.CTkButton(self.frame_categoriesmod, hover_color=self.colors[5], fg_color=self.colors[4], text="EDITAR", command=lambda:self.editcategoryfunc(id))
        self.button_editcategory.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.8)
        self.entry_positioncategory.insert(0, id)
        self.entry_addcategoryname.insert(0, name)
    def editcategoryfunc(self, id):
        newname = self.entry_addcategoryname.get()
        newid = self.entry_positioncategory.get()
        self.connectproduct()
        print(id)
        print(newid)
        if int(newid) != int(id):
            temp = self.productcursor.execute("SELECT name FROM Category WHERE cod = ?", (newid))
            for i in temp:
                nm = i[0]
            print(nm)
            self.productcursor.execute("UPDATE Category SET name = ? WHERE COD = ?", (newname, newid))
            self.productcursor.execute("UPDATE Category SET name = ? WHERE COD = ?", (nm, id))
        else:
            self.productcursor.execute("UPDATE Category SET name = ? WHERE COD = ?", (newname, id))
        self.desconnectproduct()
        self.reloadcategories()
        self.editcategorybutton(newname, newid)
    def reloadcategories(self):
        try:
            for i in self.currentcategory:
                i[0].destroy()
                i[1].destroy()
                i[2].destroy()
                i[3].destroy()
        except:
            pass
        self.currentcategory = []
        self.connectproduct()
        temp = self.productcursor.execute("SELECT cod, name FROM Category")
        for i, date in enumerate(temp):
            id, name = date
            self.currentcategory.append([ctk.CTkLabel(self.treeview_categories, fg_color=self.colors[4], text=id, width=100, height=40), ctk.CTkLabel(self.treeview_categories,fg_color=self.colors[4], text=name, width=400, height=40), ctk.CTkButton(self.treeview_categories, image=ctk.CTkImage(Image.open("./imgs/pencil.jpg"), size=(30, 30)),command=lambda x=id, y=name:self.editcategorybutton(y, x), fg_color=self.colors[4], hover=False, text="", width=100, height=40), ctk.CTkButton(self.treeview_categories, image=ctk.CTkImage(Image.open("./imgs/lixeira.png"), size=(30, 30)), command=lambda x=id:self.deletecategory(x), fg_color=self.colors[4], hover=False, text="", width=100, height=40)])
            self.currentcategory[i][0].grid(row= i + 2, column= 1, padx= 1, pady=1)
            self.currentcategory[i][1].grid(row= i + 2, column= 2, padx= 1, pady=1)
            self.currentcategory[i][2].grid(row= i + 2, column= 3, padx= 1, pady=1)
            self.currentcategory[i][3].grid(row= i + 2, column= 4, padx= 1, pady=1)
        self.desconnectproduct()
    def deletecategory(self, id):
        def revert(id2):
            try:
                temp = self.productcursor.execute("SELECT * FROM Category WHERE cod = ?", (str(id2 + 1), ))
                for i in temp:
                    cod, name = i
                self.productcursor.execute("UPDATE Category SET name = ? WHERE cod = ?", (name, str(id2)))
                revert(cod)
            except:
                self.productcursor.execute("DELETE FROM Category WHERE cod = ?", (str(id2), ))
        self.connectproduct()
        revert(id)
        self.desconnectproduct()
        self.reloadcategories()
    def windowcommand(self, command = 0, closed = 0):
        def onpresskey(event):
            if event.keysym == "Escape":
                ondelete()
        def ondelete():
            self.root.bind_all("<KeyPress>", self.presskey)
            self.rootcommand.destroy()
        def close():
            self.root.bind_all("<KeyPress>", self.presskeycommandwindow)
            self.rootconfirmdelete.destroy()
            self.rootcommand.grab_set()
        def presskey(event):
            if event.keysym == "Escape":
                close()
        def delfunc():
            self.connectcommands()
            self.commandscursor.execute("DELETE FROM Consumption WHERE number = ?", (self.currentcommandwindow, ))
            self.commandscursor.execute("DELETE FROM CommandsActive WHERE number = ?", (self.currentcommandwindow, ))
            self.desconnectcommands()
            close()
            self.on_closingcommandwindow()
            self.reloadcommands()
        def deletecommand():
            self.rootconfirmdelete = ctk.CTkToplevel(self.rootcommand)
            self.rootconfirmdelete.geometry("300x200")
            self.rootconfirmdelete.transient(self.rootcommand)
            self.rootconfirmdelete.grab_set()
            self.rootconfirmdelete.title("DELETAR COMANDA")

            self.button_confirmdelete = ctk.CTkButton(self.rootconfirmdelete, fg_color=self.colors[4], hover_color=self.colors[5], text="CONFIRMAR", command= delfunc)
            self.button_confirmdelete.place(relx=0.01, rely=0.01, relwidth=1, relheight=0.48)

            self.button_canceldelete = ctk.CTkButton(self.rootconfirmdelete, fg_color=self.colors[4], hover_color=self.colors[5], text="CANCELAR", command= close,)
            self.button_canceldelete.place(relx=0.01, rely=0.51, relwidth=1, relheight=0.48)
            
            self.rootconfirmdelete.bind_all("<KeyPress>", presskey)
            self.rootconfirmdelete.protocol("WM_DELETE_WINDOW", close)
        def selectid(id):
            self.connectclients()
            temp = self.clientscursor.execute("SELECT name FROM Clients WHERE id = ?", (id, ))
            for i in temp:
                self.nameclient.set(i[0])
            self.desconnectclients()
        def selectname(name):
            self.nameclient.set(name.split("- ")[1])
            self.idclient.set(name.split(" -")[0])
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
            def confirmpay():
                if self.totalprice.cget("text") >= 0:
                    self.connectcommands()
                    self.connecthistory()

                    temp = self.commandscursor.execute("SELECT * FROM CommandsActive WHERE number = ?", (self.currentcommandwindow, ))
                    for i in temp:
                        commandactive = i
                    temp = self.commandscursor.execute("SELECT * FROM Consumption WHERE number = ?", (commandactive[0], ))
                    totalprice = 0
                    products = []
                    for i in temp:
                        products.append(i)
                        totalprice = totalprice + float(i[5])
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
                    pay -= float(i[0])
                if pay < 0:
                    self.totalprice.configure(text=pay, text_color="#D81315")
                else:
                    self.totalprice.configure(text=pay, text_color="#7CCD5C")
                self.desconnectcommands()
            def addpay():
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

                self.tipepayvar = ctk.StringVar(value="Dinheiro")

                self.confirmaddpay = ctk.CTkButton(self.rootaddpay, command=addpayment, text="CONFIRMAR", bg_color=self.colors[4], hover_color=self.colors[3])
                self.confirmaddpay.place(relx=0.01, rely=0.51, relwidth=0.98, relheight=0.48)

                self.tipepay = ctk.CTkComboBox(self.rootaddpay, width=196, height=73, variable=self.tipepayvar, values=["Dinheiro", "Débito", "Crédito"])
                self.tipepay.place(relx=0.01, rely=0.01, relwidth=0.49, relheight=0.49)

                self.qtdpay = ctk.CTkEntry(self.rootaddpay, placeholder_text="Quantidade")
                self.qtdpay.place(relx=0.51, rely=0.01, relwidth=0.48, relheight=0.49)

                self.root.bind_all("<KeyPress>", clickpay)
                self.rootaddpay.protocol("WM_DELETE_WINDOW", closeadd)
            self.rootpay = ctk.CTkToplevel(self.rootcommand)
            self.rootpay.geometry("500x500")
            self.rootpay.transient(self.rootcommand)
            self.rootpay.title("Pagamento")
            self.rootpay.grab_set()

            self.root.bind_all("<KeyPress>", click)
            self.rootpay.protocol("WM_DELETE_WINDOW", closepay)

            self.scrollframepay = ctk.CTkScrollableFrame(self.rootpay)
            self.scrollframepay.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.75)
            
            self.paytype = ctk.CTkLabel(self.scrollframepay, bg_color=self.colors[4], width=300, height=50, text="TIPO DE PAGAMENTO")
            self.paytype.grid(row=1, column=1, padx=1, pady=1)

            self.payment = ctk.CTkLabel(self.scrollframepay, bg_color=self.colors[4], width=100, height=50, text="QUANTIDADE")
            self.payment.grid(row=1, column=2, padx=1, pady=1)

            self.deletepay = ctk.CTkLabel(self.scrollframepay, bg_color=self.colors[4], width=50, height=50, text="Deletar")
            self.deletepay.grid(row=1, column=3, padx=1, pady=1)

            self.framepay = ctk.CTkFrame(self.rootpay)
            self.framepay.place(relx=0.01, rely=0.77, relwidth=0.98, relheight=0.22)

            self.confirmpay = ctk.CTkButton(self.framepay, text="CONFIRMAR", fg_color=self.colors[4], hover_color=self.colors[3], command=confirmpay)
            self.confirmpay.place(relx=0.61, rely=0.32, relwidth=0.38, relheight=0.67)

            self.addpay = ctk.CTkButton(self.framepay, text="ADICIONAR PAGAMENTO", fg_color=self.colors[4], hover_color=self.colors[3], command=addpay)
            self.addpay.place(relx=0.01, rely=0.32, relwidth=0.59, relheight=0.67)

            self.totalpricelbl = ctk.CTkLabel(self.framepay, text="TOTAL:", bg_color=self.colors[3])
            self.totalpricelbl.place(relx=0.01, rely=0.01, relwidth=0.2, relheight=0.3)

            self.totalprice = ctk.CTkLabel(self.framepay, text="", bg_color=self.colors[3])
            self.totalprice.place(relx=0.2, rely=0.01, relwidth=0.79, relheight=0.3)

            reloadpay()
        def reprint(cod):
            self.connecthistory()
            self.connectprinter()
            temp = self.historycursor.execute("SELECT number, date, hour, nameclient, datefinish FROM ClosedCommand WHERE cod = ?",(str(cod), ))
            products = []
            for i in temp:
                print(i)
                command = i
                self.printercursor.execute("INSERT INTO ClosedPrinter (command, date, permission, client) VALUES (?, ?, ?, ?)", (command[0], command[1] + " " + command[2], "False", command[3]))
                printertemp = self.printercursor.execute("SELECT id FROM ClosedPrinter WHERE command = ? AND date = ?", (command[0], command[1] + " " + command[2]))
            for i in printertemp:
                idcom = i[0]
            temp = self.historycursor.execute("SELECT name, type, quantity, unitprice FROM Products WHERE commandid = ?", (str(cod), ))
            for i in temp:
                products.append(i)
                self.printercursor.execute("INSERT INTO ProductsClosed (id, product, type, qtd, unitprice) VALUES (?, ?, ?, ?, ?)", (idcom, i[0], i[1], i[2], i[3]))
            self.desconnecthistory()
            self.printercursor.execute("UPDATE ClosedPrinter SET permission = ? WHERE command = ? AND date = ?", ("True", command[0], command[1] + " " + command[2]))
            self.desconnectprinter()
        try:
            if int(command) > 0:
                num = command
        except:
            num = ""
            text = command.cget("text")
            for i in text:
                if i == " ":
                    break
                num = num + i

        self.rootcommand = ctk.CTkToplevel()

        
        self.frame_infocommand = ctk.CTkFrame(self.rootcommand, fg_color=self.colors[2])
        self.frame_infocommand.place(relx=0,rely=0.8,relwidth=1,relheight=0.2)
    
        if closed == 0:
            self.rootcommand.geometry("900x800")
            
            self.button_addproductoncommand = ctk.CTkButton(self.rootcommand, text="ADICIONAR PRODUTO", command=self.addpdctcommandwindow, fg_color=self.colors[4], hover_color=self.colors[5])
            self.button_addproductoncommand.place(relx=0.7, rely=0.002, relwidth=0.29, relheight=0.057)
            
            self.edit_heading = ctk.CTkLabel(self.rootcommand, text="EDITAR", fg_color=self.colors[4], width=50, height=30)
            self.edit_heading.grid(row=1, column=7, padx=1, pady=50)

            self.del_heading = ctk.CTkLabel(self.rootcommand, text="EXCLUIR", fg_color=self.colors[4], width=50, height=30)
            self.del_heading.grid(row=1, column=8, padx=1, pady=50)
            
            self.button_delcommand = ctk.CTkButton(self.frame_infocommand, fg_color=self.colors[4], text="EXCLUIR COMANDA", hover_color=self.colors[5], command=deletecommand)
            self.button_delcommand.place(relx=0.01, rely=0.15, relwidth=0.29, relheight=0.7)

            self.button_finishcommand = ctk.CTkButton(self.frame_infocommand, fg_color=self.colors[4], text="PAGAMENTO", hover_color=self.colors[5], command=windowpay)
            self.button_finishcommand.place(relx=0.7, rely=0.15, relwidth=0.29, relheight=0.7)
            
            self.connectcommands()
            tmp = self.commandscursor.execute("SELECT idclient, nameclient FROM CommandsActive WHERE number = ?", (num, ))
            idclient, self.actuallyname = "", ""
            for i in tmp:
                idclient, self.actuallyname = i
            self.desconnectcommands()
            self.connectclients()
            temp = self.clientscursor.execute("SELECT * FROM Clients")
            ids = []
            names = []
            for i in temp:
                ids.append(str(i[0]))
                names.append(f"{str(i[0])} - {i[1]}")
            self.desconnectclients()

            self.idclient = ctk.StringVar(value=idclient)
            self.nameclient = ctk.StringVar(value=self.actuallyname)

            self.clientid = ctk.CTkComboBox(self.frame_infocommand, width=100, height=50, values=ids, command=selectid, font=("Arial", 15), variable=self.idclient)
            self.clientid.place(relx=0.31, rely=0.51)

            self.clientname = ctk.CTkComboBox(self.frame_infocommand, width=235, height=50, values=names, command=selectname, font=("Arial", 15), variable=self.nameclient)
            self.clientname.place(relx=0.43, rely=0.51)

            self.time_heading = ctk.CTkLabel(self.rootcommand, text="TEMPO", fg_color=self.colors[4], width=100, height=30)
            self.time_heading.grid(row=1, column=6, padx=1, pady=50)
            self.root.bind_all("<KeyPress>", self.presskeycommandwindow)
            self.rootcommand.protocol("WM_DELETE_WINDOW", self.on_closingcommandwindow)
        else:
            self.rootcommand.geometry("900x800")
            self.connecthistory()
            temp = self.historycursor.execute("SELECT * FROM ClosedCommand WHERE cod = ?", (str(closed), ))
            for i in temp:
                temp = i
                num = i[1]
            self.desconnecthistory()
            self.time_heading = ctk.CTkLabel(self.rootcommand, text="TEMPO", fg_color=self.colors[4], width=150, height=30)
            self.time_heading.grid(row=1, column=6, padx=1, pady=50)
            self.button_finishcommand = ctk.CTkButton(self.frame_infocommand, fg_color=self.colors[4], text="Reimprimir", hover_color=self.colors[5], command=lambda x = closed:reprint(x))
            self.button_finishcommand.place(relx=0.7, rely=0.15, relwidth=0.29, relheight=0.7)
            self.root.bind_all("<KeyPress>", onpresskey)
            self.rootcommand.protocol("WM_DELETE_WINDOW", ondelete)
        self.rootcommand.title("COMANDA " + num)
        self.rootcommand.resizable(False, False)
        self.rootcommand.transient(self.root)
        self.rootcommand.grab_set()

        self.frame_consume = ctk.CTkScrollableFrame(self.rootcommand, fg_color=self.colors[3])
        self.frame_consume.place(relx=0, rely=0.1, relwidth=1, relheight=0.7)


        

        self.placeholder_heading = ctk.CTkLabel(self.rootcommand, text="", fg_color=self.colors[0], width=5, height=30)
        self.placeholder_heading.grid(row=1, column=0, padx=0, pady=50)

        self.productname_heading = ctk.CTkLabel(self.rootcommand, text="PRODUTO", fg_color=self.colors[4], width=200, height=30)
        self.productname_heading.grid(row=1, column=1, padx=1, pady=50)

        self.waiter_heading = ctk.CTkLabel(self.rootcommand, text="GARÇOM", fg_color=self.colors[4], width=200, height=30)
        self.waiter_heading.grid(row=1, column=2, padx=0, pady=50)

        self.productpriceunit_heading = ctk.CTkLabel(self.rootcommand, text="PREÇO UNIDADE", fg_color=self.colors[4], width=100, height=30)
        self.productpriceunit_heading.grid(row=1, column=3, padx=1, pady=50)

        self.quantity_heading = ctk.CTkLabel(self.rootcommand, text="QTD.", fg_color=self.colors[4], width=50, height=30)
        self.quantity_heading.grid(row=1, column=4, padx=1, pady=50)

        self.productprice_heading = ctk.CTkLabel(self.rootcommand, text="PREÇO TOTAL", fg_color=self.colors[4], width=100, height=30)
        self.productprice_heading.grid(row=1, column=5, padx=1, pady=50)

        


        self.totalpricelabel = ctk.CTkLabel(self.frame_infocommand, text="TOTAL:", fg_color=self.colors[4])
        self.totalpricelabel.place(relx=0.31, rely=0.15, relwidth=0.06, relheight=0.3)
        
        self.currentcommandwindow = num
        self.reloadproductforcommands(num, closed)
    def reloadproductforcommands(self, number, closed = 0):
        def delete(cod):
            self.connectcommands()
            self.commandscursor.execute("DELETE FROM Consumption WHERE cod = ?", (cod,))
            self.desconnectcommands()
            self.reloadproductforcommands(self.currentcommandwindow)
        
        self.connectcommands()
        self.connecthistory()
        if closed == 0:
            temp = self.commandscursor.execute("SELECT cod, number, date, hour, waiter, price, unitprice, quantity, product, type, size FROM Consumption WHERE number = ?",
            (number, ))
        else:
            temp = self.historycursor.execute("SELECT releasedate, releasehour, waiter, price, quantity, name, unitprice FROM Products WHERE commandid = ?",
            (closed, ))
        try:
            self.label_totalprice.destroy()
            for i in self.current_productsincommands:
                for n in i:
                    n.destroy()
        except:
            pass
        listen = []
        for i in temp:
            listen.append(i)
        self.current_productsincommands = []
        totalprice = 0
        for k, i in enumerate(listen):
            if closed == 0:
                cod, number, date, hour, waiter, price, unitprice, quantity, product, tipe, size = i
                tyme =  datetime.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]), int(hour[0:2]), int(hour[3:5]), int(hour[6:8]))
                now = datetime.datetime.now()
                delta = now - tyme
                total_sec = delta.total_seconds()
                total_min, sec = divmod(int(total_sec), 60)
                total_hour, minute = divmod(total_min, 60)
                total_days, hour = divmod(total_hour, 24)
                text = ""
                if total_days != 0:
                    text = text + str(total_days) + "D " + str(hour) + "H "
                elif total_hour != 0:
                    text = text + str(hour) + "H "
            
                text = text + str(minute) + "M " + str(sec) + "S"
            
                self.current_productsincommands.append([ctk.CTkLabel(self.frame_consume, text=product, fg_color=self.colors[4], width=200, height=40),
                                                   ctk.CTkLabel(self.frame_consume, text=waiter, fg_color=self.colors[4], width=200, height=40),
                                                   ctk.CTkLabel(self.frame_consume, text=unitprice, fg_color=self.colors[4], width=100, height=40),
                                                   ctk.CTkLabel(self.frame_consume, text=quantity, fg_color=self.colors[4], width=50, height=40),
                                                   ctk.CTkLabel(self.frame_consume, text=price, fg_color=self.colors[4], width=100, height=40),
                                                   ctk.CTkLabel(self.frame_consume, text=text, fg_color=self.colors[4], width=100, height=40),
                                                   ctk.CTkButton(self.frame_consume, text="", fg_color=self.colors[4], width=50, height=40, image=ctk.CTkImage(Image.open("./imgs/pencil.jpg"), size=(30, 30)),hover=False, command=lambda x= cod:self.addproductincommandwindow(cod=x)),
                                                   ctk.CTkButton(self.frame_consume, text="", fg_color=self.colors[4], width=50, height=40, image=ctk.CTkImage(Image.open("./imgs/lixeira.png"), size=(30, 30)),hover=False, command=lambda x = cod: delete(x))
                                                   ])
                self.current_productsincommands[k][0].grid(row= k + 1, column=1, padx=0, pady=1)
                self.current_productsincommands[k][1].grid(row= k + 1, column=2, padx=1, pady=1)
                self.current_productsincommands[k][2].grid(row= k + 1, column=3, padx=1, pady=1)
                self.current_productsincommands[k][3].grid(row= k + 1, column=4, padx=1, pady=1)
                self.current_productsincommands[k][4].grid(row= k + 1, column=5, padx=1, pady=1)
                self.current_productsincommands[k][5].grid(row= k + 1, column=6, padx=1, pady=1)
                self.current_productsincommands[k][6].grid(row= k + 1, column=7, padx=1, pady=1)
                self.current_productsincommands[k][7].grid(row= k + 1, column=8, padx=1, pady=1) 
            else:
                date, hour, waiter, price, quantity, product, unitprice = i
            
                self.current_productsincommands.append([ctk.CTkLabel(self.frame_consume, text=product, fg_color=self.colors[4], width=200, height=40),
                                                   ctk.CTkLabel(self.frame_consume, text=waiter, fg_color=self.colors[4], width=200, height=40),
                                                   ctk.CTkLabel(self.frame_consume, text=unitprice, fg_color=self.colors[4], width=100, height=40),
                                                   ctk.CTkLabel(self.frame_consume, text=quantity, fg_color=self.colors[4], width=50, height=40),
                                                   ctk.CTkLabel(self.frame_consume, text=price, fg_color=self.colors[4], width=100, height=40),
                                                   ctk.CTkLabel(self.frame_consume, text=date + " ÀS " + hour, fg_color=self.colors[4], width=150, height=40)
                                                   ])
                self.current_productsincommands[k][0].grid(row= k + 1, column=1, padx=0, pady=1)
                self.current_productsincommands[k][1].grid(row= k + 1, column=2, padx=1, pady=1)
                self.current_productsincommands[k][2].grid(row= k + 1, column=3, padx=1, pady=1)
                self.current_productsincommands[k][3].grid(row= k + 1, column=4, padx=1, pady=1)
                self.current_productsincommands[k][4].grid(row= k + 1, column=5, padx=1, pady=1)
                self.current_productsincommands[k][5].grid(row= k + 1, column=6, padx=1, pady=1)
            totalprice = totalprice + float(price)
        self.label_totalprice = ctk.CTkLabel(self.frame_infocommand, text=totalprice, fg_color=self.colors[4])
        self.label_totalprice.place(relx=0.37, rely=0.15, relwidth=0.32, relheight=0.3)
        self.desconnecthistory()
        self.desconnectcommands()
    def closewindowaddproduct(self):
        self.rootcommand.grab_set()
        self.root.bind_all("<KeyPress>",self.presskeycommandwindow)
        self.rootcommand.protocol("WM_DELETE_WINDOW", self.on_closingcommandwindow)
        self.rootaddpdctcommand.destroy()
    def addpdctcommandwindow(self):
        self.rootaddpdctcommand = ctk.CTkToplevel(self.rootcommand)
        self.rootaddpdctcommand.title("ADICIONAR CONSUMO")
        self.rootaddpdctcommand.transient(self.rootcommand)
        self.rootaddpdctcommand.resizable(False, False)
        self.rootaddpdctcommand.geometry("700x600")
        self.rootaddpdctcommand.grab_set()

        self.scroolframe_addproduct = ctk.CTkScrollableFrame(self.rootaddpdctcommand, fg_color=self.colors[3])
        self.scroolframe_addproduct.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

        self.categoryadd_heading = ctk.CTkLabel(self.scroolframe_addproduct, fg_color=self.colors[4], text="CATEGORIA", width=200, height=50)
        self.categoryadd_heading.grid(row=1, column=1, padx=1, pady=1)

        self.productadd_heading = ctk.CTkLabel(self.scroolframe_addproduct, fg_color=self.colors[4], text="PRODUTO", width=200, height=50)
        self.productadd_heading.grid(row=1, column=2, padx=1, pady=1)

        self.priceadd_heading = ctk.CTkLabel(self.scroolframe_addproduct, fg_color=self.colors[4], text="PREÇO", width=90, height=50)
        self.priceadd_heading.grid(row=1, column=3, padx=1, pady=1)

        self.addproduct_heading = ctk.CTkLabel(self.scroolframe_addproduct, fg_color=self.colors[4], text="ADICIONAR 1", width=70, height=50)
        self.addproduct_heading.grid(row=1, column=4, padx=1, pady=1)

        self.peraddproduct_heading = ctk.CTkLabel(self.scroolframe_addproduct, fg_color=self.colors[4], text="ADICIONAR" , width=70, height=50)
        self.peraddproduct_heading.grid(row=1, column=5, padx=1, pady=1)

        self.rootaddpdctcommand.protocol("WM_DELETE_WINDOW", self.closewindowaddproduct)
        self.root.bind_all("<KeyPress>",self.pressesccommand)
        self.reloadproductstable()
    def insertproductlisten(self, i):
        self.insertproductlist.append(i)
    def pressesccommand(self, event):
        if event.keysym == "Escape":
            self.closewindowaddproduct()
    def insertcurrentproduct(self):
        self.connecttemp()
        TEMp = self.tempdbcursor.execute("SELECT * FROM TempProducts")
        temp = []
        for i in TEMp:
            temp.append(i)
        self.desconnecttemp()
        while temp != []:
            listen = [temp[0]]
            self.connectcommands()
            cod, command, product, category, unitprice, qtd, text, waiter, tipe, prynter = temp[0]
            date = str(datetime.datetime.now())[0:19]
            date, hour = date[0:10], date[11:20]
            self.commandscursor.execute("INSERT INTO Consumption (number, date, hour, waiter, price, unitprice, quantity, product, type, size, text, category) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (command, date, hour, waiter, float(unitprice)*qtd, unitprice, qtd, product, tipe, "", text, category))
            del temp[0]
            self.connecttemp()
            self.tempdbcursor.execute("DELETE FROM TempProducts Where cod = ?", (cod, ))
            self.desconnecttemp()
            oi = ""
            tmp = self.commandscursor.execute("SELECT * FROM CommandsActive WHERE number = ?", (command, ))
            for i in tmp:
                oi = i
            if oi == "":
                date = str(datetime.datetime.now())[0:19]
                date, hour = date[0:10], date[11:20]
                self.commandscursor.execute("INSERT INTO CommandsActive (number, initdate, hour, nameclient, idclient) VALUES (?, ?, ?, ?, ?)", (command, date, hour, "", ""))           
            self.desconnectcommands()        
            if prynter != "":
                self.connectprinter()
                self.printercursor.execute("INSERT INTO ProductPrint (product, printer, type, command, waiter, date, qtd, text) VALUES (?, ?, 'product', ?, ?, ?, ?, ?)", (product, prynter, command, waiter, str(datetime.datetime.now())[0:19], qtd, text))
                self.desconnectprinter()
            
        self.root.after(3000, self.insertcurrentproduct)
    def addproductincommandwindow(self, product = "", category = "", tipe = "", price = "", cod = ""):
        def close():
            self.rootaddpdctcommand.grab_set()
            self.root.bind_all("<KeyPress>",self.pressesccommand)
            self.rooteditaddproduct.destroy()
        def pressesc(event):
            if event.keysym == "Escape":
                close()
        def select(product):
            self.entry_unitprice.delete(0, "end")
            self.entry_unitprice.insert(0, self.dicproduct[product])
        def close2():
            self.root.bind_all("<KeyPress>",self.presskeycommandwindow)
            self.rooteditaddproduct.destroy()
        def confirm():
            self.connectcommands()
            date = str(datetime.datetime.now())[0:19]
            date, hour = date[0:10], date[11:20]
            quantity = self.entry_quantity.get()
            unitprice = self.entry_unitprice.get()
            if tipe == "SIZE":
                name = product + " (" + self.combobox_products.get() + ")"
            elif tipe == "NORMAL":
                name = product
            self.commandscursor.execute("INSERT INTO Consumption (number, date, hour, waiter, price, unitprice, quantity, product, type, size, category) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (self.currentcommandwindow, date, hour, self.namelogin, str(float(unitprice)*int(quantity)), unitprice, quantity, name, tipe, "", category))
            self.desconnectcommands()
            close()
            self.reloadproductforcommands(self.currentcommandwindow)
            self.insertcommandactive(self.currentcommandwindow)
        def confirm2(cod):
            self.connectcommands()
            unitprice = self.entry_unitprice.get()
            quantity = self.entry_quantity.get()
            self.commandscursor.execute("UPDATE Consumption SET unitprice = ?, quantity = ?, price = ? WHERE cod = ?", (unitprice, quantity, str(float(unitprice)*int(quantity)), cod))
            self.desconnectcommands()
            self.reloadproductforcommands(self.currentcommandwindow)
            close2()
        def select(id, par):
            self.connectcommands()
            if self.currentpredefnotesvar[id].get() == "":
                temp = self.commandscursor.execute("SELECT text FROM Consumption WHERE cod = ?", (cod, ))
                for i in temp:
                    temp = i[0].split(".=")
                text = ""
                num = 1
                for i in temp:
                    if par != i:
                        if num != 1:
                            text = text + ".=" + i
                        else:
                            text = i
                            num = 2
            else:
                temp = self.commandscursor.execute("SELECT text FROM Consumption WHERE cod = ?", (cod, ))
                for i in temp:
                    if i[0] != "":
                        text = i[0] + ".=" + self.currentpredefnotesvar[id].get()
                    else:
                        text = self.currentpredefnotesvar[id].get()
            self.commandscursor.execute("UPDATE Consumption SET text = ? WHERE cod = ?", (text, cod))
            self.desconnectcommands()
        def delete(x):
            self.connectcommands()
            temp = self.commandscursor.execute("SELECT text FROM Consumption WHERE cod = ?", (cod, ))
            text = ""
            for i in temp:
                temp = i[0].split(".=")
            num = 1
            for i in temp:
                if x != i:
                    if num != 1:
                        text = text + ".=" + i
                    else:
                        text = i
                        num = 2
            self.commandscursor.execute("UPDATE Consumption SET text = ? WHERE cod = ?", (text, cod))
            self.desconnectcommands()
            reloadnotes()
        def add():
            self.connectcommands()
            temp = self.commandscursor.execute("SELECT text FROM Consumption WHERE cod = ?", (cod, ))
            text = ""
            for i in temp:
                temp = i[0]
            if self.entryaddnote.get() != "":
                if temp != "":
                    text = temp + ".=" + self.entryaddnote.get()
                else:
                    text = self.entryaddnote.get()
            print(text)
            self.commandscursor.execute("UPDATE Consumption SET text = ? WHERE cod = ?", (text, cod))
            self.desconnectcommands()
            reloadnotes()
        def reloadnotes():
            try:
                for i in self.currentnotes:
                    for j in i:
                        j.destroy()
            except:
                pass
            self.connectproduct()
            self.connectcommands()
            temp = self.commandscursor.execute("SELECT text, category FROM Consumption WHERE cod = ?",(cod, ))
            for i in temp:
                temp = i[0].split(".=")
                category = i[1]
            tmp = self.productcursor.execute("SELECT text FROM Notes WHERE category = ?", (category, ))
            predeftexts = []
            for i in tmp:
                predeftexts.append(i[0])
            self.currentnotes = []
            self.currentpredefnotesvar = []
            for k, i in enumerate(predeftexts): 
                self.currentpredefnotesvar.append(ctk.StringVar(value=""))
                for n, l in enumerate(temp):
                    if i[0] == l:
                        self.currentpredefnotesvar[k].set(i[0])
                        del temp[n]
                        break
                n = k + 2
                self.currentnotes.append([ctk.CTkLabel(self.scrollframenote, text=i[0], width=300, height=50, bg_color=self.colors[4]), ctk.CTkCheckBox(self.scrollframenote, text="", variable=self.currentpredefnotesvar[k], onvalue=i[0], offvalue="", command=lambda x = k - 1, y = i[0]:select(x, y), width=130, height=50, bg_color=self.colors[4])])
            if temp != [""] and temp != "":
                for i in temp:
                    self.currentnotes.append([ctk.CTkLabel(self.scrollframenote, text=i, width=300, height=50, bg_color=self.colors[4]), ctk.CTkButton(self.scrollframenote, text="", command=lambda x = i:delete(x), width=130, height=50, fg_color=self.colors[4], hover=False, image=ctk.CTkImage(Image.open("./imgs/lixeira.png"), size=(45, 45)))])
            for k, i in enumerate(self.currentnotes):
                n = k + 2
                self.currentnotes[k][0].grid(row=n, column=1, padx=1, pady=1)
                self.currentnotes[k][1].grid(row=n, column=2, padx=1, pady=1)
            self.desconnectcommands()
            self.desconnectproduct()
                
        if cod != "":
            self.rooteditaddproduct = ctk.CTkToplevel(self.rootcommand)
            self.rooteditaddproduct.transient(self.rootcommand)
        else:
            self.rooteditaddproduct = ctk.CTkToplevel(self.rootaddpdctcommand)
            self.rooteditaddproduct.transient(self.rootaddpdctcommand)
        self.rooteditaddproduct.geometry("750x750")
        self.rooteditaddproduct.resizable(False, False)
        self.rooteditaddproduct.title("CONFIGURAÇÕES DO PRODUTO")
        self.rooteditaddproduct.grab_set()

        self.label_product = ctk.CTkLabel(self.rooteditaddproduct, text= product + " (" + category + ")", fg_color=self.colors[4], font=("Arial", 25))
        self.label_product.place(relx=0.01, rely=0.01, relwidth=0.59, relheight=0.1)

        self.entry_quantity = ctk.CTkEntry(self.rooteditaddproduct, fg_color=self.colors[4], font=("Arial", 25))
        self.entry_quantity.place(relx=0.61, rely=0.01, relwidth=0.14, relheight=0.1)
        self.entry_quantity.insert(0, "1")

        self.entry_unitprice = ctk.CTkEntry(self.rooteditaddproduct, fg_color=self.colors[4], font=("Arial", 25), placeholder_text="PREÇO")
        self.entry_unitprice.place(relx=0.76, rely=0.01, relwidth=0.23, relheight=0.1)
        
        self.button_confirm = ctk.CTkButton(self.rooteditaddproduct, fg_color=self.colors[4], hover_color=self.colors[5], command=confirm, text="CONFIRMAR", font=("Arial", 25))
        self.button_confirm.place(relx=0.51, rely=0.12, relwidth=0.48, relheight=0.1)
        
        self.scrollframenote = ctk.CTkScrollableFrame(self.rooteditaddproduct, )
        self.scrollframenote.place(relx=0.01, rely=0.34, relwidth=0.98, relheight=0.65)

        self.buttonaddnote = ctk.CTkButton(self.rooteditaddproduct, fg_color=self.colors[4], hover_color=self.colors[3], text="ADICIONAR ANOTAÇÃO", command=add)
        self.buttonaddnote.place(relx=0.71, rely=0.23, relwidth=0.28, relheight=0.1)

        self.entryaddnote = ctk.CTkEntry(self.rooteditaddproduct, bg_color=self.colors[4])
        self.entryaddnote.place(relx=0.01, rely=0.23, relwidth=0.69, relheight=0.1)

        self.titletext = ctk.CTkLabel(self.scrollframenote, width=300, height=50, text="Anotação", bg_color=self.colors[3])
        self.titletext.grid(row=1, column=1, padx=1, pady=1)

        self.titleremove = ctk.CTkLabel(self.scrollframenote, width=130, height=50, text="SELECIONAR/EXLUIR", bg_color=self.colors[3])
        self.titleremove.grid(row=1, column=2, padx=1, pady=1)

        currentnotes = []

        self.root.bind_all("<KeyPress>", pressesc)
        self.rooteditaddproduct.protocol("WM_DELETE_WINDOW", close)
        if tipe == "NORMAL":
            self.entry_unitprice.insert(0, price)
        elif tipe == "SIZE":
            self.dicproduct = {}
            self.connectproduct()
            temp = self.productcursor.execute("SELECT price, name FROM SizeofProducts WHERE product = ? AND category = ?", (product, category))
            listencb = []
            listencb.append("")
            for i in temp:
                self.dicproduct[i[1]] = i[0]
                listencb.append(i[1])
            self.combobox_products = ctk.CTkComboBox(self.rooteditaddproduct, width=240, height=95, values=listencb, command=select, font=("Arial", 25))
            self.combobox_products.place(relx=0.01, rely=0.50)
            self.desconnectproduct()
        elif cod != "":
            self.rooteditaddproduct.protocol("WM_DELETE_WINDOW", close2)
            self.connectcommands()
            temp = self.commandscursor.execute("SELECT unitprice, quantity, product FROM Consumption WHERE cod = ?",(cod, ))
            for i in temp:
                unitprice, quantity, product = i
            self.entry_quantity.delete(0, "end")
            self.entry_quantity.insert(0, quantity)

            self.label_product.configure(text=product)

            self.entry_unitprice.insert(0, unitprice)

            self.button_confirm.configure(command=lambda x=cod:confirm2(x))
            self.desconnectcommands()
        reloadnotes()
    def reloadproductstable(self, search = ""):
        def addproductincommand(product, category, tipe, price):
            if tipe == "SIZE":
                self.addproductincommandwindow(product, category, tipe)
            else:
                self.connectcommands()
                date = str(datetime.datetime.now())[0:19]
                date, hour = date[0:10], date[11:20]
                self.commandscursor.execute("INSERT INTO Consumption (number, date, hour, waiter, price, unitprice, quantity, product, type, size, category) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (self.currentcommandwindow, date, hour, self.namelogin, price, price, "1", product, tipe, "", category))
                self.desconnectcommands()
                self.insertcommandactive(self.currentcommandwindow)
                self.reloadcommands()
            self.reloadproductforcommands(self.currentcommandwindow)
        try:
            for i in self.currentproductsaddlist:
                for n in i:
                    n.destroy()
        except:
            pass
        self.connectproduct()
        temp = self.productcursor.execute("SELECT * FROM Products")
        listentemp = []
        listen = []
        for i in temp:
            listentemp.append(i)
        if search == "":
            listen = listentemp   
        else:
            for i in listentemp :
                if unidecode(search.upper()) in unidecode(i[0].upper()):
                    listen = i
        self.currentproductsaddlist = []
        for k, i in enumerate(listen):
            print(i)
            name, tipe, category, price, printer = i
            self.currentproductsaddlist.append([ctk.CTkLabel(self.scroolframe_addproduct, text=category, width=200, height=40, fg_color=self.colors[5]),
                                                ctk.CTkLabel(self.scroolframe_addproduct, text=name, width=200, height=40, fg_color=self.colors[5]),
                                                ctk.CTkLabel(self.scroolframe_addproduct, text=price, width=90, height=40, fg_color=self.colors[5]),
                                                ctk.CTkButton(self.scroolframe_addproduct, text="", width=70, height=40, image=ctk.CTkImage(Image.open("./imgs/add1.png"), size=(30, 30)), fg_color=self.colors[5], hover=False, command=lambda x= name, y = category, z = tipe, a= price:addproductincommand(x, y, z, a)),
                                                ctk.CTkButton(self.scroolframe_addproduct, text="", width=70, height=40, image=ctk.CTkImage(Image.open("./imgs/add.png"), size=(30, 30)), fg_color=self.colors[5], hover=False, command=lambda x= name, y= category, z= tipe, a= price:self.addproductincommandwindow(x, y, z, a))])
            self.currentproductsaddlist[k][0].grid(row=k + 2, column=1, padx=1, pady=1)
            self.currentproductsaddlist[k][1].grid(row=k + 2, column=2, padx=1, pady=1)
            self.currentproductsaddlist[k][2].grid(row=k + 2, column=3, padx=1, pady=1)
            self.currentproductsaddlist[k][3].grid(row=k + 2, column=4, padx=1, pady=1)
            self.currentproductsaddlist[k][4].grid(row=k + 2, column=5, padx=1, pady=1)
        self.desconnectproduct()
    def insertcommandactive(self, number):
        self.connectcommands()
        temp = self.commandscursor.execute("SELECT number FROM CommandsActive WHERE number = ?", (number, ))
        tmp = ""
        for i in temp:
            tmp = i[0]
        if tmp == "":
            date = str(datetime.datetime.now())[0:19]
            date, hour = date[0:10], date[11:20]
            self.commandscursor.execute("INSERT INTO CommandsActive (number, initdate, hour, nameclient, idclient) VALUES (?, ?, ?, ?, ?)", (number, date, hour, "", ""))
        self.desconnectcommands()
        self.reloadcommands()
    def presskeycommandwindow(self, event):
        if event.keysym == "Escape":
            self.on_closingcommandwindow()
    def presskeyaddproductoncommand(self, event):
        if event.keysym == "Escape":
            self.closewindowaddproduct()
    def nonclick(self, event):
        pass
    def reloadcommands(self):
        self.number =[]
        try:
            for i in self.currentcommands:
                i.destroy()
        except:
            pass
        self.connectcommands()
        currentcommands = self.commandscursor.execute("""SELECT number, initdate, hour, nameclient FROM CommandsActive""")
        self.currentcommands = []
        framewidth = self.width - self.width * 0.02
        qtdrow = int(framewidth//280)
        for i, command in enumerate(currentcommands):
            number, initdate, inithour, nameclient  = command
            now = datetime.datetime.now()
            date = datetime.datetime(int(initdate[0:4]), int(initdate[5:7]), int(initdate[8:10]), int(inithour[0:2]), int(inithour[3:5]), int(inithour[6:8]))
            delta = now - date
            total_sec = delta.total_seconds()
            total_min, sec = divmod(int(total_sec), 60)
            total_hour, minute = divmod(total_min, 60)
            total_days, hour = divmod(total_hour, 24)
            text = ""
            if total_days != 0:
                text = text + str(total_days) + "D " + str(hour) + "H "
            elif total_hour != 0:
                text = text + str(hour) + "H "
            
            text = text + str(minute) + "M " + str(sec) + "S"
            if len(nameclient) >= 16:
                nameclient = nameclient[0:15]
            self.currentcommands.append(ctk.CTkButton(self.frame_commands,fg_color=self.colors[3], command=lambda m = i:self.windowcommand(self.currentcommands[m]), hover=False, width=260, height= 150, text= str(number) + " "+ nameclient +"\n" + "TEMPO: " + text, font=("Arial", 20)))
            
            self.currentcommands[i].grid(row=i//qtdrow, column=i%qtdrow, padx=5, pady=5)
            self.number.append(number)
        
        self.desconnectcommands()
    def newcommands (self):
        def close():
            self.root.bind_all("<KeyPress>", self.presskey)
            self.rootnewcom.destroy()
        def presskey(event):
            if event.keysym == "Escape":
                close()
        self.rootnewcom = ctk.CTkToplevel()
        self.rootnewcom.title("ADICIONAR COMANDA")
        #self.rootnewcom.iconbitmap('imagens\Icon.ico')
        self.rootnewcom.geometry("800x600")
        self.rootnewcom.resizable(False, False)
        self.rootnewcom.transient(self.root)
        self.rootnewcom.grab_set()
        self.frame_newcommands = ctk.CTkScrollableFrame(master=self.rootnewcom, fg_color=self.colors[1])
        self.frame_newcommands.place(relx=0.01, rely=0.01, relwidth= 0.98, relheight= 0.98)
        commandsactives = []
        try:
            for i in self.button_newcommand:
                i.destroy()
        except:
            pass
        self.button_newcommand = []
        threading.Thread(self.addnewcommandwindow()).start()
        self.rootnewcom.protocol("WM_DELETE_WINDOW", close)
        self.root.bind_all("<KeyPress>", presskey)
    def addnewcommandwindow(self):
        def addnewcommandactive(command):
            num = command.cget("text")
            self.connectcommands()
            self.root.bind_all("<KeyPress>", self.presskey)
            self.rootnewcom.destroy()
            self.desconnectcommands()
            self.insertcommandactive(num)
            threading.Thread(self.reloadcommands()).start()
        for i in range(int(self.maxcommands)):
            k = False
            for m in self.number:
                if m == i + 1:
                    k = True
            self.button_newcommand.append(ctk.CTkButton(self.frame_newcommands, command=lambda m=i:addnewcommandactive(self.button_newcommand[m]), fg_color="#006f00", text=str(i+ 1), font=("Arial", 15), width=150, height=75, hover_color="#004f00"))
            if k:
                self.button_newcommand[i].configure(fg_color="#6f0000", hover_color="#4f0000")
            self.button_newcommand[i].grid(row=int(i/4), column=i%4, padx=10 ,pady=10)
    def clickmain(self, event):
        """
            position = pa.position()
            if position.x >  and position.x < self.position_namecommand[0] + self.position_namecommand[3]:
                if position.y > self.position_namecommand[1] and position.y < self.position_namecommand[1] + position.y[3]:
                    pass
                else:
                    self.entry_namecommand.delete(0, "end")
                    event.widget.focus_set()
            else:
                self.entry_namecommand.delete(0, "end")
                event.widget.focus_set()
    """
    def presskey(self, event):
        key = event.keysym
        n = self.entry_namecommand.get()
        i = self.str_searchcommands.get()
        if n == "":
            if key == "0" or key == "1" or key == "2" or key == "3" or key == "4" or key == "5" or key == "6" or key == "7" or key == "8" or key == "9":
                self.str_searchcommands.set(i + key)
            elif key == "Return":
                if int(i) <= self.maxcommands and int(i) >=0:
                    self.str_searchcommands.set("")
                    self.windowcommand(i)
            elif key == "BackSpace":
                self.str_searchcommands.set(i[0:-1])
            else:
                self.str_searchcommands.set("")
        elif key == "Delete":
            self.entry_namecommand.delete(0, "end")
        elif key == "Return":
            pass
    def functionarywindow(self):
        def update(up, new, name):
            self.connectconts()
            if up == "permissionmaster":
                self.contscursor.execute("UPDATE Conts SET permissionmaster = ? WHERE name = ?", (self.currentfunctionaryvar[new][0].get(), name))
            elif up == "permissionrelease":
                self.contscursor.execute("UPDATE Conts SET permissionrelease = ? WHERE name = ?", (self.currentfunctionaryvar[new][1].get(), name))
            elif up == "permissionentry":
                self.contscursor.execute("UPDATE Conts SET permissionentry = ? WHERE name = ?", (self.currentfunctionaryvar[new][2].get(), name))
            self.desconnectconts()
        def reload():
            try:
                for i in self.currentfunctionarylabel:
                    for n in i:
                        n.destroy()
                del self.currentfunctionaryvar
            except:
                pass
            self.connectconts()
            temp = self.contscursor.execute("SELECT * FROM Conts")
            tempm = []
            for i in temp:
                tempm.append(i)
            self.desconnectconts()
            self.currentfunctionarylabel = []
            self.currentfunctionaryvar = []
            for k, i in enumerate(tempm):
                username, name, password, permissionmaster, permissionrelease, permissionentry = i
                self.currentfunctionaryvar.append([ctk.StringVar(), ctk.StringVar(), ctk.StringVar()])
                if permissionmaster == "Y":
                    self.currentfunctionaryvar[k][0].set("Y")
                if permissionrelease == "Y":
                    self.currentfunctionaryvar[k][1].set("Y")
                if permissionentry == "Y":
                    self.currentfunctionaryvar[k][2].set("Y")
                self.currentfunctionarylabel.append([ctk.CTkLabel(self.scroolframe_functionary, fg_color=self.colors[4], width=200, height=40, text=username),
                                                     ctk.CTkLabel(self.scroolframe_functionary, fg_color=self.colors[4], width=50, height=40, text=name), 
                                                    ctk.CTkCheckBox(self.scroolframe_functionary, fg_color=self.colors[4], variable=self.currentfunctionaryvar[k][0], onvalue="Y", offvalue="F", width=70, height=40, text="", command=lambda x = "permissionmaster", y = k,z = name:update(x, y, z)),
                                                    ctk.CTkCheckBox(self.scroolframe_functionary, fg_color=self.colors[4], variable=self.currentfunctionaryvar[k][1], onvalue="Y", offvalue="F", width=70, height=40, text="", command=lambda x = "permissionrelease", y = k,z = name:update(x, y, z)),
                                                    ctk.CTkCheckBox(self.scroolframe_functionary, fg_color=self.colors[4], variable=self.currentfunctionaryvar[k][2], onvalue="Y", offvalue="F", width=70, height=40, text="", command=lambda x = "permissionentry", y = k,z = name:update(x, y, z)),
                                                    ctk.CTkButton(self.scroolframe_functionary, fg_color=self.colors[4], width=60, height=40, text="", hover=False, image=ctk.CTkImage(Image.open("./imgs/pencil.jpg"), size=(30,30)), command=lambda x=name: edit(x)),
                                                    ctk.CTkButton(self.scroolframe_functionary, fg_color=self.colors[4], width=60, height=40, text="", hover=False, image=ctk.CTkImage(Image.open("./imgs/lixeira.png"), size=(30,30)), command=lambda x=name: delete(x))])
                self.currentfunctionarylabel[k][0].grid(row=k + 2, column=1, padx=1, pady=1)
                self.currentfunctionarylabel[k][1].grid(row=k + 2, column=2, padx=1, pady=1)
                self.currentfunctionarylabel[k][2].grid(row=k + 2, column=3, padx=1, pady=1)
                self.currentfunctionarylabel[k][3].grid(row=k + 2, column=4, padx=1, pady=1)
                self.currentfunctionarylabel[k][4].grid(row=k + 2, column=5, padx=1, pady=1)
                self.currentfunctionarylabel[k][5].grid(row=k + 2, column=6, padx=1, pady=1)
                self.currentfunctionarylabel[k][6].grid(row=k + 2, column=7, padx=1, pady=1)
        def edit(name):
            try:
                self.button_editfunctionary.destroy()
            except:
                pass
            self.button_editfunctionary = ctk.CTkButton(self.root, fg_color=self.colors[4], hover_color=self.colors[5],command=lambda x= name:insert(x), text="CONFIRMAR EDIÇÃO")
            self.button_editfunctionary.place(relx=0.6, rely=0.145, relwidth=0.19, relheight=0.05)
            self.connectconts()
            temp = self.contscursor.execute("SELECT username, name, password FROM Conts WHERE name = ?", (name, ))
            for i in temp:
                username, name, password = i
            self.desconnectconts()
            self.entry_name.delete(0, "end")
            self.entry_name.insert(0, name)

            self.entry_username.delete(0, "end")
            self.entry_username.insert(0, username)

            self.entry_passwordcont.delete(0, "end")
            self.entry_passwordcont.insert(0, password)
        def insert(oldname = ""):
            try:
                self.button_editfunctionary.destroy()
            except:
                pass
            self.connectconts()            
            tmp = self.contscursor.execute("SELECT username, name FROM Conts WHERE username = ?",(self.entry_username.get(), ))
            temp = ""
            for i in tmp:
                if self.entry_username.get() != i[0]:
                    temp = "A"
            tmp = self.contscursor.execute("SELECT username, name FROM Conts WHERE name = ?",(self.entry_name.get(), ))
            for i in tmp:
                if i[1] != self.entry_name.get():
                    temp = "A"
            if temp == "" and oldname == "" and self.entry_username.get() != "" and self.entry_name.get() != "":
                username, name, password, permissionmaster, permissionrelease, permissionentry = self.entry_username.get(), self.entry_name.get(), self.entry_passwordcont.get(), "F", "F", "F"
                self.contscursor.execute("INSERT INTO Conts (username, name, password, permissionmaster, permissionrelease, permissionentry) VALUES (?, ?, ?, ?, ?, ?)",(username, name, password, permissionmaster, permissionrelease, permissionentry))
            elif temp == "" and self.entry_username.get() != "" and self.entry_name.get() != "":
                username, name, password = self.entry_username.get(), self.entry_name.get(), self.entry_passwordcont.get()
                self.contscursor.execute("UPDATE Conts SET username = ?, name = ?, password = ? WHERE name = ?", (username, name, password, oldname))
                self.entry_username.delete(0, "end")
                self.entry_passwordcont.delete(0, "end")
                self.entry_name.delete(0, "end")
            self.desconnectconts()
            reload()
        def delete(name):
            self.connectconts()
            self.contscursor.execute("DELETE FROM Conts WHERE name = ?", (name, ))
            self.desconnectconts()
            reload()
        self.deletewindow()
        self.currentwindow = "FUNCIONÁRIOS"

        self.scroolframe_functionary = ctk.CTkScrollableFrame(self.root, fg_color=self.colors[3])
        self.scroolframe_functionary.place(relx=0.01, rely=0.20, relwidth=0.98, relheight=0.79)

        self.button_addfunctionary = ctk.CTkButton(self.root, fg_color=self.colors[4], hover_color=self.colors[5], text="ADICIONAR", command=insert)
        self.button_addfunctionary.place(relx=0.85, rely=0.145, relwidth=0.14, relheight=0.05)

        self.entry_username = ctk.CTkEntry(self.root, fg_color=self.colors[4], placeholder_text="FUNCIONÁRIO")
        self.entry_username.place(relx=0.01, rely=0.145, relwidth=0.14, relheight=0.05)
        
        self.entry_passwordcont = ctk.CTkEntry(self.root, fg_color=self.colors[4], placeholder_text="SENHA", show="*")
        self.entry_passwordcont.place(relx=0.31, rely=0.145, relwidth=0.14, relheight=0.05)

        self.entry_name = ctk.CTkEntry(self.root, fg_color=self.colors[4], placeholder_text="LOGIN")
        self.entry_name.place(relx=0.16, rely=0.145, relwidth=0.14, relheight=0.05)

        self.username_headingfunctionary = ctk.CTkLabel(self.scroolframe_functionary, fg_color=self.colors[4], width=200, height=50, text="FUNCIONÁRIO")
        self.username_headingfunctionary.grid(row=1, column=1, padx=1, pady=1)

        self.name_headingfunctionery = ctk.CTkLabel(self.scroolframe_functionary, fg_color=self.colors[4], width=50, height=50, text="LOGIN")
        self.name_headingfunctionery.grid(row=1, column=2, padx=1, pady=1)

        self.permissionmaster_heading = ctk.CTkLabel(self.scroolframe_functionary, fg_color=self.colors[4], width=70, height=50, text="ADMIN")
        self.permissionmaster_heading.grid(row=1, column=3, padx=1, pady=1)

        self.permissionrelease_heading = ctk.CTkLabel(self.scroolframe_functionary, fg_color=self.colors[4], width=70, height=50, text="GARÇOM")
        self.permissionrelease_heading.grid(row=1, column=4, padx=1, pady=1)

        self.permissionentry_heading = ctk.CTkLabel(self.scroolframe_functionary, fg_color=self.colors[4], width=70, height=50, text="PORTEIRO")
        self.permissionentry_heading.grid(row=1, column=5, padx=1, pady=1)

        self.editfunctionary_heading = ctk.CTkLabel(self.scroolframe_functionary, fg_color=self.colors[4], width=60, height=50, text="EDITAR")
        self.editfunctionary_heading.grid(row=1, column=6, padx=1, pady=1)

        self.deletefunctionary_heading = ctk.CTkLabel(self.scroolframe_functionary, fg_color=self.colors[4], width=60, height=50, text="DELETAR")
        self.deletefunctionary_heading.grid(row=1, column=7, padx=1, pady=1)

        reload()
    def cash(self, idcash = "open"):
        def open():
            self.connecthistory()
            date = str(datetime.datetime.now())[0:19]
            self.historycursor.execute("INSERT INTO Cashdesk (initdate, status) VALUES (?, ?)", (date, "open"))
            self.desconnecthistory()
            self.cash()
        def close():
            self.connecthistory()
            date = str(datetime.datetime.now())[0:19]
            temp = self.historycursor.execute("SELECT id FROM Cashdesk WHERE status = ?", ("open", ))
            for i in temp:
                temp = i[0]
            temp = self.historycursor.execute("SELECT totalprice FROM Closedcommand WHERE cashdesk = ?", (temp, ))
            totalprice = 0
            for i in temp:
                totalprice = totalprice + float(i[0])
            self.historycursor.execute("UPDATE Cashdesk set finishdate = ?, status = ?, totalcash = ? WHERE status = ?", (date, "closed", totalprice, "open"))
            self.desconnecthistory()
            self.cash()
        def reload():
            try:
                for i in self.currenthistory:
                    for j in i:
                        j.destroy()
            except:
                pass
            self.connecthistory()
            if idcash == "open":
                temp = self.historycursor.execute("SELECT id FROM Cashdesk WHERE status = ?", (idcash, ))
                for i in temp:
                    temp = i[0]
            else:
                temp = idcash
            try:
                temp = self.historycursor.execute("SELECT * FROM ClosedCommand WHERE cashdesk = ?", (temp, ))
            except:
                pass
            self.currenthistory = []
            for k, i in enumerate(temp):
                self.currenthistory.append([ctk.CTkLabel(self.scrollframehis, bg_color=self.colors[4], width=100, height=50, text=i[1]), ctk.CTkLabel(self.scrollframehis, bg_color=self.colors[4], width=200, height=50, text=f"{i[2]} às {i[3]}"), ctk.CTkLabel(self.scrollframehis, bg_color=self.colors[4], width=200, height=50, text=f"{i[7][0:10]} às {i[7][11:20]}"), ctk.CTkLabel(self.scrollframehis, bg_color=self.colors[4], width=100, height=50, text=i[6]), ctk.CTkLabel(self.scrollframehis, bg_color=self.colors[4], width=100, height=50, text=i[9]), ctk.CTkLabel(self.scrollframehis, bg_color=self.colors[4], width=200, height=50, text=i[4]), ctk.CTkButton(self.scrollframehis, command=lambda x = i[0]: self.windowcommand(closed=x), width=150, height=50, fg_color=self.colors[4], hover=False, text="", image=ctk.CTkImage(Image.open("./imgs/info.png"), size=(43, 43)))])
                n = k + 2
                
                self.currenthistory[k][0].grid(row=n, column=1, padx=1, pady=1)
                self.currenthistory[k][1].grid(row=n, column=2, padx=1, pady=1)
                self.currenthistory[k][2].grid(row=n, column=3, padx=1, pady=1)
                self.currenthistory[k][3].grid(row=n, column=4, padx=1, pady=1)
                self.currenthistory[k][4].grid(row=n, column=5, padx=1, pady=1)
                self.currenthistory[k][5].grid(row=n, column=6, padx=1, pady=1)
                self.currenthistory[k][6].grid(row=n, column=7, padx=1, pady=1)
            self.desconnecthistory()
        self.deletewindow()
        self.currentwindow = "CASH"

        self.scrollframehis = ctk.CTkScrollableFrame(self.root)
        self.scrollframehis.place(relx=0.01, rely=0.20, relwidth=0.98, relheight=0.78)

        self.entrysearchhis = ctk.CTkEntry(self.root, placeholder_text="Cliente ou comanda")
        self.entrysearchhis.place(relx=0.01, rely=0.145, relwidth=0.2, relheight=0.05)


        self.numberhis = ctk.CTkLabel(self.scrollframehis, bg_color=self.colors[4], text="COMANDA", width=100, height=50)
        self.numberhis.grid(row=1, column=1, padx=1, pady=1)

        self.oppened = ctk.CTkLabel(self.scrollframehis, bg_color=self.colors[4], text="ABERTA ÀS", width=200, height=50)
        self.oppened.grid(row=1, column=2, padx=1, pady=1)

        self.closed = ctk.CTkLabel(self.scrollframehis, bg_color=self.colors[4], text="FECHADA ÀS", width=200, height=50)
        self.closed.grid(row=1, column=3, padx=1, pady=1)

        self.totalhis = ctk.CTkLabel(self.scrollframehis, bg_color=self.colors[4], text="TOTAL", width=100, height=50)
        self.totalhis.grid(row=1, column=4, padx=1, pady=1)

        self.payhis = ctk.CTkLabel(self.scrollframehis, bg_color=self.colors[4], text="PAGO", width=100, height=50)
        self.payhis.grid(row=1, column=5, padx=1, pady=1)

        self.clienthis = ctk.CTkLabel(self.scrollframehis, bg_color=self.colors[4], text="CLIENTE", width=200, height=50)
        self.clienthis.grid(row=1, column=6, padx=1, pady=1)

        self.infohis = ctk.CTkLabel(self.scrollframehis, bg_color=self.colors[4], text="INFO", width=150, height=50) 
        self.infohis.grid(row=1, column=7, padx=1, pady=1)

        self.connecthistory()
        if idcash == "open":
            tmp = self.historycursor.execute("SELECT status FROM Cashdesk WHERE status = ?", (idcash, ))
            for i in tmp:
                print(i[0])
                tmp = i[0]
            if tmp == "open":
                self.buttonopencash = ctk.CTkButton(self.root, fg_color=self.colors[4], hover_color=self.colors[3], text="FECHAR CAIXA", command=close)
            else:
                self.buttonopencash = ctk.CTkButton(self.root, fg_color=self.colors[4], hover_color=self.colors[3], text="ABRIR CAIXA", command=open)
        else:
            self.buttonopencash = ctk.CTkButton(self.root, fg_color=self.colors[4], hover_color=self.colors[3], text="VOLTAR", command=self.cashdeskwindow)
        
        self.buttonopencash.place(relx=0.75, rely=0.145, relwidth=0.2, relheight=0.05)
        self.desconnecthistory()

        
        reload()
    def rankingproducts(self):
        def reload(date = False):
            try:
                for i in self.currentranking:
                    for j in i:
                        j.destroy()
            except:
                pass
            self.connecthistory()
            temp = self.historycursor.execute("SELECT name, quantity, unitprice, releasedate, releasehour, price FROM Products")
            products = {}
            self.currentranking = []
            initdate = datetime.datetime(int(str(self.initentry.get_date())[0:4]), int(str(self.initentry.get_date())[5:7]), int(str(self.initentry.get_date())[8:10]), self.inithourvar.get(), self.initminvar.get(), 0)
            finishdate = datetime.datetime(int(str(self.finishentry.get_date())[0:4]), int(str(self.finishentry.get_date())[5:7]), int(str(self.finishentry.get_date())[8:10]), self.finishhourvar.get(), self.finishminvar.get(), 59)
            for i in temp:
                name, quantity, unitprice, releasedate, releasehour, price = i
                                    
                productdate = datetime.datetime(int(releasedate[0:4]), int(releasedate[5:7]), int(releasedate[8:10]), int(releasehour[0:2]), int(releasehour[3:5]), int(releasehour[6:8]))

                if productdate >= initdate and productdate <= finishdate:
                    try:
                        products[name] = [name, products[name][1] + int(quantity), unitprice, products[name][3] + float(price)]
                    except:
                        products[name] = [name, int(quantity), unitprice, float(price)]
            for k, i in enumerate(products):
                self.currentranking.append([ctk.CTkLabel(self.frameranking, bg_color=self.colors[4], width=300, height=50, text=products[i][0]), ctk.CTkLabel(self.frameranking, bg_color=self.colors[4], width=100, height=50, text=products[i][1]), ctk.CTkLabel(self.frameranking, bg_color=self.colors[4], width=100, height=50, text=products[i][2]), ctk.CTkLabel(self.frameranking, bg_color=self.colors[4], width=100, height=50, text=products[i][3])])

                n = k + 1
                self.currentranking[k][0].grid(row=n, column=1, padx=1, pady=1)
                self.currentranking[k][1].grid(row=n, column=2, padx=1, pady=1)
                self.currentranking[k][2].grid(row=n, column=3, padx=1, pady=1)
                self.currentranking[k][3].grid(row=n, column=4, padx=1, pady=1)
            self.desconnecthistory()
        self.deletewindow()
        self.currentwindow = "RANKINGPRODUCTS"

        self.frameranking = ctk.CTkScrollableFrame(self.root)
        self.frameranking.place(relx=0.17, rely=0.145, relwidth=0.82, relheight=0.98)

        self.initlb = ctk.CTkLabel(self.root, text="Lançado dia")
        self.initlb.place(relx=0.01, rely=0.19, relwidth=0.15, relheight=0.05)

        self.initentry = DateEntry(self.root)
        self.initentry.place(relx=0.01, rely=0.25, relwidth=0.15, relheight=0.05)
        
        self.frameinithour = ctk.CTkFrame(self.root)
        self.frameinithour.place(relx=0.01, rely=0.31, relwidth=0.15, relheight=0.05)

        self.inithourlb = ctk.CTkLabel(self.frameinithour, text="Hora:", width=70)
        self.inithourlb.pack(side= ctk.LEFT)

        self.inithourvar = ctk.IntVar()
        self.inithour = CTkSpinbox(self.frameinithour, start_value=0, min_value=0, max_value=23, variable=self.inithourvar)
        self.inithour.pack(side= ctk.RIGHT)

        self.frameinitmin = ctk.CTkFrame(self.root)
        self.frameinitmin.place(relx=0.01, rely=0.37, relwidth=0.15, relheight=0.05)

        self.initminlb = ctk.CTkLabel(self.frameinitmin, text="Min:", width=70)
        self.initminlb.pack(side= ctk.LEFT)

        self.initminvar = ctk.IntVar()
        self.initmin = CTkSpinbox(self.frameinitmin, start_value=0, min_value=0, max_value=59, variable=self.initminvar)
        self.initmin.pack(side= ctk.RIGHT)

        self.finishlb = ctk.CTkLabel(self.root, text="ATÉ")
        self.finishlb.place(relx=0.01, rely=0.43, relwidth=0.15, relheight=0.05)

        self.finishentry = DateEntry(self.root)
        self.finishentry.place(relx=0.01, rely=0.49, relwidth=0.15, relheight=0.05)

        self.framefinishhour = ctk.CTkFrame(self.root)
        self.framefinishhour.place(relx=0.01, rely=0.55, relwidth=0.15, relheight=0.05)

        self.finishhourlb = ctk.CTkLabel(self.framefinishhour, text="Hora:", width=70)
        self.finishhourlb.pack(side= ctk.LEFT)

        self.finishhourvar = ctk.IntVar()
        self.finishhour = CTkSpinbox(self.framefinishhour, start_value=23, min_value=0, max_value=23, variable=self.finishhourvar)
        self.finishhour.pack(side= ctk.RIGHT)

        self.framefinishmin = ctk.CTkFrame(self.root)
        self.framefinishmin.place(relx=0.01, rely=0.61, relwidth=0.15, relheight=0.05)

        self.finishminlb = ctk.CTkLabel(self.framefinishmin, text="Min:", width=70)
        self.finishminlb.pack(side= ctk.LEFT)
        print(self.initentry.get_date())
        self.finishminvar = ctk.IntVar()
        self.finishmin = CTkSpinbox(self.framefinishmin, start_value=59, min_value=0, max_value=59, variable=self.finishminvar)
        self.finishmin.pack(side= ctk.RIGHT)

        self.confirmdate = ctk.CTkButton(self.root, fg_color=self.colors[4], hover_color=self.colors[3], text="Procurar", command=lambda:reload(True))
        self.confirmdate.place(relx=0.01, rely=0.67, relwidth=0.15, relheight=0.05)

        self.nameproduct = ctk.CTkLabel(self.frameranking, bg_color=self.colors[4], width=300, height=50, text="PRODUTO")
        self.nameproduct.grid(row=0, column=1, padx=1, pady=1)

        self.qtdproduct = ctk.CTkLabel(self.frameranking, bg_color=self.colors[4], width=100, height=50, text="QTD.")
        self.qtdproduct.grid(row=0, column=2, padx=1, pady=1)

        self.unitpriceproduct = ctk.CTkLabel(self.frameranking, bg_color=self.colors[4], width=100, height=50, text="PREÇO UNIT")
        self.unitpriceproduct.grid(row=0, column=3, padx=1, pady=1)

        self.totalpriceproduct = ctk.CTkLabel(self.frameranking, bg_color=self.colors[4], width=100, height=50, text="TOTAL")
        self.totalpriceproduct.grid(row=0, column=4, padx=1, pady=1)

        reload()
    def cashdeskwindow(self):
        def reload(date = False):
            try:
                for i in self.currentcashs:
                    for j in i:
                        j.destroy()
            except:
                pass
            self.currentcashs = []

            self.connecthistory()
            temp = self.historycursor.execute("SELECT * FROM Cashdesk")

            if date:
                dateinit = str(self.initentry.get_date())
                datefinish = str(self.finishentry.get_date())
                dateinit = datetime.date(int(dateinit[0:4]), int(dateinit[5:7]), int(dateinit[8:]))
                datefinish = datetime.date(int(datefinish[0:4]), int(datefinish[5:7]), int(datefinish[8:]))
                listen = []
                for i in temp:
                    listen.append(i)
                temp = []
                for i in listen:
                    if i[2]:
                        datefinishcash = datetime.date(int(i[2][0:4]), int(i[2][5:7]), int(i[2][8:10]))
                    else:
                        datefinishcash = datetime.date.today() 
                    num = 0
                    if (datefinishcash >= dateinit) and (datefinishcash <= datefinish):
                        temp.append(i)
            for k, i in enumerate(temp):
                self.currentcashs.append([ctk.CTkLabel(self.scrollframecashs, bg_color=self.colors[4], width=75, height=50, text=i[0]), ctk.CTkLabel(self.scrollframecashs, bg_color=self.colors[4], width=200, height=50, text=i[1]), ctk.CTkLabel(self.scrollframecashs, bg_color=self.colors[4], width=200, height=50, text=i[2]), ctk.CTkLabel(self.scrollframecashs, bg_color=self.colors[4], width=100, height=50, text=i[4]), ctk.CTkButton(self.scrollframecashs, fg_color=self.colors[4], width=75, height=50, hover=False, text="", command=lambda x = i[0]:self.cash(x), image=ctk.CTkImage(Image.open("./imgs/info.png"), size=(43, 43)))])
                n = k + 2
                self.currentcashs[k][0].grid(row=n, column=1, padx=1, pady=1)
                self.currentcashs[k][1].grid(row=n, column=2, padx=1, pady=1)
                self.currentcashs[k][2].grid(row=n, column=3, padx=1, pady=1)
                self.currentcashs[k][3].grid(row=n, column=4, padx=1, pady=1)
                self.currentcashs[k][4].grid(row=n, column=5, padx=1, pady=1)
            self.desconnecthistory()
        self.deletewindow()
        self.currentwindow = "CASHDESKHISTORY"

        self.connecthistory()
        temp = self.historycursor.execute("SELECT id, initdate, finishdate, totalcash FROM Cashdesk WHERE status = ?", ("closed", ))
        self.desconnecthistory()

        self.scrollframecashs = ctk.CTkScrollableFrame(self.root)
        self.scrollframecashs.place(relx=0.17, rely=0.145, relwidth=0.82, relheight=0.85)

        self.idcash = ctk.CTkLabel(self.scrollframecashs, text="Numero", bg_color=self.colors[4], width=75, height=50)
        self.idcash.grid(row=1, column=1, padx=1, pady=1)

        self.initdate = ctk.CTkLabel(self.scrollframecashs, text="Aberto em", bg_color=self.colors[4], width=200, height=50)
        self.initdate.grid(row=1, column=2, padx=1, pady=1)

        self.finishdate = ctk.CTkLabel(self.scrollframecashs, text="Fechado em", bg_color=self.colors[4], width=200, height=50)
        self.finishdate.grid(row=1, column=3, padx=1, pady=1)

        self.totalcash = ctk.CTkLabel(self.scrollframecashs, text="Total", bg_color=self.colors[4], width=100, height=50)
        self.totalcash.grid(row=1, column=4, padx=1, pady=1)

        self.infocash = ctk.CTkLabel(self.scrollframecashs, text="Visualizar", bg_color=self.colors[4], width=75, height=50)
        self.infocash.grid(row=1, column=5, padx=1, pady=1)

        self.initlb = ctk.CTkLabel(self.root, text="FECHADO EM")
        self.initlb.place(relx=0.01, rely=0.19, relwidth=0.15, relheight=0.05)

        self.initentry = DateEntry(self.root)
        self.initentry.place(relx=0.01, rely=0.25, relwidth=0.15, relheight=0.05)

        self.finishlb = ctk.CTkLabel(self.root, text="ATÉ")
        self.finishlb.place(relx=0.01, rely=0.31, relwidth=0.15, relheight=0.05)

        self.finishentry = DateEntry(self.root)
        self.finishentry.place(relx=0.01, rely=0.37, relwidth=0.15, relheight=0.05)

        self.confirmdate = ctk.CTkButton(self.root, fg_color=self.colors[4], hover_color=self.colors[3], text="Procurar", command=lambda:reload(True))
        self.confirmdate.place(relx=0.01, rely=0.43, relwidth=0.15, relheight=0.05)

        reload()
    def windowprinters(self):
        def reload():
            try:
                for i in self.printers:
                    for j in i:
                        j.destroy()
            except:
                pass
            
            self.printers = []

            self.connectprinter()
            temp = self.printercursor.execute("SELECT * FROM Printers")
            for k, i in enumerate(temp):
                self.printers.append([ctk.CTkLabel(self.frameprinters, bg_color=self.colors[4], width=300, height=50, text=i[0], ), ctk.CTkLabel(self.frameprinters, bg_color=self.colors[4], width=200, height=50, text=i[1], ), ctk.CTkButton(self.frameprinters, fg_color=self.colors[4], hover=False, image=ctk.CTkImage(Image.open("./imgs/lixeira.png"), size=(45, 45)), command=lambda x=i[0], y=i[1]: delete(x,y), text="", width=100, height=50)])

                n = k+2
                self.printers[k][0].grid(row=n, column=1, padx=1, pady=1)
                self.printers[k][1].grid(row=n, column=2, padx=1, pady=1)
                self.printers[k][2].grid(row=n, column=3, padx=1, pady=1)

            self.desconnectprinter()
        def delete(name, ip):
            self.connectprinter()
            self.printercursor.execute("DELETE FROM Printers WHERE name = ? AND ip = ?",(name, ip))
            self.desconnectprinter()
            reload()
            aprinter.reloadprinters()
        def add():
            if self.nameprinter.get() != "" and self.ipprinter.get() != "":
                self.connectprinter()
                temp = self.printercursor.execute("SELECT * FROM Printers WHERE name = ?", (self.nameprinter.get(), ))
                tmp = ""
                for i in temp:
                    tmp = "a"
                if tmp == "":
                    self.printercursor.execute("INSERT INTO Printers (name, ip) VALUES (?, ?)", (self.nameprinter.get(), self.ipprinter.get()))
                self.desconnectprinter()
                
                self.nameprinter.delete(0, ctk.END)
                self.ipprinter.delete(0, ctk.END)
                reload()
            aprinter.reloadprinters()
        self.deletewindow()

        self.currentwindow = "PRINTERS"

        self.nameprinter = ctk.CTkEntry(self.root, placeholder_text="Nome da impressora")
        self.nameprinter.place(relx=0.01, rely=0.145, relwidth=0.2, relheight=0.05)

        self.ipprinter = ctk.CTkEntry(self.root, placeholder_text="IP da impressora")
        self.ipprinter.place(relx=0.22, rely=0.145, relwidth=0.2, relheight=0.05)

        self.addprinter = ctk.CTkButton(self.root, fg_color=self.colors[4], hover_color=self.colors[3], text="ADICIONAR", command=add)
        self.addprinter.place(relx=0.8, rely=0.145, relwidth=0.19, relheight=0.05)

        self.frameprinters = ctk.CTkScrollableFrame(self.root)
        self.frameprinters.place(relx=0.01, rely=0.2, relwidth=0.98, relheight=0.79)

        self.printername = ctk.CTkLabel(self.frameprinters, text="NOME", width=300, height=50, bg_color=self.colors[4])
        self.printername.grid(row=1, column=1, padx=1, pady=1)

        self.printerip = ctk.CTkLabel(self.frameprinters, text="IP", width=200, height=50, bg_color=self.colors[4])
        self.printerip.grid(row=1, column=2, padx=1, pady=1)

        self.delprinter = ctk.CTkLabel(self.frameprinters, text="DELETAR", width=100, height=50, bg_color=self.colors[4])
        self.delprinter.grid(row=1, column=3, padx=1, pady=1)

        reload()
    def rankingservice(self):
        def reload(table = 1):
            try:
                for i in self.currenttable:
                    for j in i:
                        j.destroy()
            except:
                pass

            self.connecthistory()
            temp = self.historycursor.execute("SELECT quantity, releasedate, releasehour, waiter, price FROM Products")
            listen = {}
            initdate = datetime.datetime(int(str(self.initentry.get_date())[0:4]), int(str(self.initentry.get_date())[5:7]), int(str(self.initentry.get_date())[8:10]), self.inithourvar.get(), self.initminvar.get(), 0)
            finishdate = datetime.datetime(int(str(self.finishentry.get_date())[0:4]), int(str(self.finishentry.get_date())[5:7]), int(str(self.finishentry.get_date())[8:10]), self.finishhourvar.get(), self.finishminvar.get(), 59)
            for i in temp:
                date = datetime.datetime(int(i[1][0:4]), int(i[1][5:7]), int(i[1][8:10]), int(i[2][0:2]), int(i[2][3:5]), int(i[2][6:8]))
                if date >= initdate and date <= finishdate:
                    try:
                        listen[i[3]] = [listen[i[3]][0] + int(i[0]), listen[i[3]][1] + float(i[4])]
                    except:
                        listen[i[3]] = [int(i[0]), float(i[4])]
            self.desconnecthistory()
            tablelist = []
            if table == 1:
                for i in listen:
                    if tablelist == []:
                        tablelist.append([i, listen[i][0], listen[i][1]])
                    else:
                        for k, j in enumerate(tablelist):
                            if listen[i][1] > j[2]:
                                tablelist.insert(k, [i, listen[i][0], listen[i][1]])
                                break
                            if len(tablelist) - 1 == k:
                                tablelist.append([i, listen[i][0], listen[i][1]])
                                break
            elif table == 2:
                for i in listen:
                    if tablelist == []:
                        tablelist.append([i, listen[i][0], listen[i][1]])
                    else:
                        for k, j in enumerate(tablelist):
                            if listen[i][0] > j[1]:
                                tablelist.insert(k, [i, listen[i][0], listen[i][1]])
                                break
                            if len(tablelist) - 1 == k:
                                tablelist.append([i, listen[i][0], listen[i][1]])
                                break
            print(listen)
            print(tablelist)
            self.currenttable = []
            for k, i in enumerate(tablelist):
                self.currenttable.append([
                    ctk.CTkLabel(self.frame_ranking, width=300, height=50, bg_color=self.colors[4], text=i[0]), 
                    ctk.CTkLabel(self.frame_ranking, width=150, height=50, bg_color=self.colors[4], text=i[2]), 
                    ctk.CTkLabel(self.frame_ranking, width=150, height=50, bg_color=self.colors[4], text=i[1])])
                n = k + 1

                self.currenttable[k][0].grid(row=n, column=0, padx=1, pady=1)
                self.currenttable[k][1].grid(row=n, column=1, padx=1, pady=1)
                self.currenttable[k][2].grid(row=n, column=2, padx=1, pady=1)
        self.deletewindow()
        self.currentwindow = "RANKINGSERVICE"

        self.frame_ranking = ctk.CTkScrollableFrame(self.root)
        self.frame_ranking.place(relx=0.17, rely=0.145, relwidth=0.82, relheight=0.845)

        self.namewaiter = ctk.CTkLabel(self.frame_ranking, bg_color=self.colors[4], text="Colaborador", width=300, height=50)
        self.namewaiter.grid(row=0, column=0, padx=1, pady=1)

        self.buttoninvoicing = ctk.CTkButton(self.frame_ranking, fg_color=self.colors[4], hover_color=self.colors[3], text="Faturamento", width=150, height=50, command=lambda x = 1:reload(x))
        self.buttoninvoicing.grid(row=0, column=1, padx=1, pady=1)

        self.buttonqtdsell = ctk.CTkButton(self.frame_ranking, fg_color=self.colors[4], hover_color=self.colors[3], text="QTD de vendas", width=150, height=50, command=lambda x = 2:reload(x))
        self.buttonqtdsell.grid(row=0, column=2, padx=1, pady=1)

        self.initlb = ctk.CTkLabel(self.root, text="Lançado dia")
        self.initlb.place(relx=0.01, rely=0.19, relwidth=0.15, relheight=0.05)

        self.initentry = DateEntry(self.root)
        self.initentry.place(relx=0.01, rely=0.25, relwidth=0.15, relheight=0.05)
        
        self.frameinithour = ctk.CTkFrame(self.root)
        self.frameinithour.place(relx=0.01, rely=0.31, relwidth=0.15, relheight=0.05)

        self.inithourlb = ctk.CTkLabel(self.frameinithour, text="Hora:", width=70)
        self.inithourlb.pack(side= ctk.LEFT)

        self.inithourvar = ctk.IntVar()
        self.inithour = CTkSpinbox(self.frameinithour, start_value=0, min_value=0, max_value=23, variable=self.inithourvar)
        self.inithour.pack(side= ctk.RIGHT)

        self.frameinitmin = ctk.CTkFrame(self.root)
        self.frameinitmin.place(relx=0.01, rely=0.37, relwidth=0.15, relheight=0.05)

        self.initminlb = ctk.CTkLabel(self.frameinitmin, text="Min:", width=70)
        self.initminlb.pack(side= ctk.LEFT)

        self.initminvar = ctk.IntVar()
        self.initmin = CTkSpinbox(self.frameinitmin, start_value=0, min_value=0, max_value=59, variable=self.initminvar)
        self.initmin.pack(side= ctk.RIGHT)

        self.finishlb = ctk.CTkLabel(self.root, text="ATÉ")
        self.finishlb.place(relx=0.01, rely=0.43, relwidth=0.15, relheight=0.05)

        self.finishentry = DateEntry(self.root)
        self.finishentry.place(relx=0.01, rely=0.49, relwidth=0.15, relheight=0.05)

        self.framefinishhour = ctk.CTkFrame(self.root)
        self.framefinishhour.place(relx=0.01, rely=0.55, relwidth=0.15, relheight=0.05)

        self.finishhourlb = ctk.CTkLabel(self.framefinishhour, text="Hora:", width=70)
        self.finishhourlb.pack(side= ctk.LEFT)

        self.finishhourvar = ctk.IntVar()
        self.finishhour = CTkSpinbox(self.framefinishhour, start_value=23, min_value=0, max_value=23, variable=self.finishhourvar)
        self.finishhour.pack(side= ctk.RIGHT)

        self.framefinishmin = ctk.CTkFrame(self.root)
        self.framefinishmin.place(relx=0.01, rely=0.61, relwidth=0.15, relheight=0.05)

        self.finishminlb = ctk.CTkLabel(self.framefinishmin, text="Min:", width=70)
        self.finishminlb.pack(side= ctk.LEFT)
        print(self.initentry.get_date())
        self.finishminvar = ctk.IntVar()
        self.finishmin = CTkSpinbox(self.framefinishmin, start_value=59, min_value=0, max_value=59, variable=self.finishminvar)
        self.finishmin.pack(side= ctk.RIGHT)

        self.confirmdate = ctk.CTkButton(self.root, fg_color=self.colors[4], hover_color=self.colors[3], text="Procurar", command=lambda x = 1:reload(x))
        self.confirmdate.place(relx=0.01, rely=0.67, relwidth=0.15, relheight=0.05)
        reload(1)
    def historyproducts(self):
        def reload():
            try:
                for i in self.currenthisproducts:
                    for j in i:
                        j.destroy()
            except:
                pass
            self.connectcommands()
            temp = self.commandscursor.execute("SELECT number, date, hour, waiter, price, unitprice, quantity, product FROM Consumption")
            self.currenthisproducts = []
            products = []
            for i in temp:
                products.append(i)
            products.reverse()
            for k, i in enumerate(products):
                self.currenthisproducts.append([
                    ctk.CTkLabel(self.frame_hisproducts, bg_color=self.colors[4], width=80, height=50, text=i[0]), 
                    ctk.CTkLabel(self.frame_hisproducts, bg_color=self.colors[4], width=200, height=50, text=i[7]), 
                    ctk.CTkLabel(self.frame_hisproducts, bg_color=self.colors[4], width=60, height=50, text=i[6]), 
                    ctk.CTkLabel(self.frame_hisproducts, bg_color=self.colors[4], width=100, height=50, text=i[5]), 
                    ctk.CTkLabel(self.frame_hisproducts, bg_color=self.colors[4], width=100, height=50, text=i[4]), 
                    ctk.CTkLabel(self.frame_hisproducts, bg_color=self.colors[4], width=150, height=50, text=f"{i[1]} {i[2]}".replace("-", "/")), 
                    ctk.CTkLabel(self.frame_hisproducts, bg_color=self.colors[4], width=200, height=50, text=i[3])])
                n = k + 1

                self.currenthisproducts[k][0].grid(row=n, column=0, padx=1, pady=1)
                self.currenthisproducts[k][1].grid(row=n, column=1, padx=1, pady=1)
                self.currenthisproducts[k][2].grid(row=n, column=2, padx=1, pady=1)
                self.currenthisproducts[k][3].grid(row=n, column=3, padx=1, pady=1)
                self.currenthisproducts[k][4].grid(row=n, column=4, padx=1, pady=1)
                self.currenthisproducts[k][5].grid(row=n, column=5, padx=1, pady=1)
                self.currenthisproducts[k][6].grid(row=n, column=6, padx=1, pady=1)
            
            
            self.desconnectcommands()
        self.deletewindow()
        self.currentwindow = "HISTORYPRODUCTS"

        self.frame_hisproducts = ctk.CTkScrollableFrame(self.root)
        self.frame_hisproducts.place(relx=0.01, rely=0.145, relwidth=0.98, relheight=0.845)

        self.productcomhis = ctk.CTkLabel(self.frame_hisproducts, bg_color=self.colors[4], width=80, height=50, text="COMANDA")
        self.productcomhis.grid(row=0, column=0, padx=1, pady=1)

        self.producthis = ctk.CTkLabel(self.frame_hisproducts, bg_color=self.colors[4], width=200, height=50, text="PRODUTO")
        self.producthis.grid(row=0, column=1, padx=1, pady=1)

        self.productqtdhis = ctk.CTkLabel(self.frame_hisproducts, bg_color=self.colors[4], width=60, height=50, text="QTD")
        self.productqtdhis.grid(row=0, column=2, padx=1, pady=1)

        self.productunitpricehis = ctk.CTkLabel(self.frame_hisproducts, bg_color=self.colors[4], width=100, height=50, text="PREÇO UNIT.")
        self.productunitpricehis.grid(row=0, column=3, padx=1, pady=1)

        self.productpricehis = ctk.CTkLabel(self.frame_hisproducts, bg_color=self.colors[4], width=100, height=50, text="TOTAL")
        self.productpricehis.grid(row=0, column=4, padx=1, pady=1)

        self.productdatehis = ctk.CTkLabel(self.frame_hisproducts, bg_color=self.colors[4], width=150, height=50, text="LANÇADO EM")
        self.productdatehis.grid(row=0, column=5, padx=1, pady=1)

        self.productwaiterhis = ctk.CTkLabel(self.frame_hisproducts, bg_color=self.colors[4], width=200, height=50, text="LANÇADO POR")
        self.productwaiterhis.grid(row=0, column=6, padx=1, pady=1)

        reload()
    def changemainbuttons(self, button):
        
        self.button_main.configure(fg_color=self.colors[7], hover_color=self.colors[5], hover=True)
        self.button_product.configure(fg_color=self.colors[7], hover_color=self.colors[5], hover=True)
        self.button_config.configure(fg_color=self.colors[7], hover_color=self.colors[5], hover=True)
        button.configure(fg_color=self.colors[4], hover=False)
        text = button.cget("text")
        
        try:
            for i in self.currentmain:
                buttontemp, texttemp = i
                buttontemp.destroy()
        except:
            pass
        if text == "PRINCIPAL":

            mainimgs = [ctk.CTkImage(Image.open("./imgs/caixa.png"), size=(60,60)), ctk.CTkImage(Image.open("./imgs/relogio.png"), size=(60,60)), ctk.CTkImage(Image.open("./imgs/tables.png"), size=(60,60)), ctk.CTkImage(Image.open("./imgs/clientes.png"), size=(60,60)), ctk.CTkImage(Image.open("./imgs/trofeu.png"), size=(60,60)), ctk.CTkImage(Image.open("./imgs/relogio.png"), size=(60,60)), ctk.CTkImage(Image.open("./imgs/garçom.png"), size=(60,60))]
            
            mainbuttons = [[ctk.CTkButton(master= self.frame_tab, command=self.cash), "ABRIR CAIXA"], [ctk.CTkButton(master= self.frame_tab, command=self.cashdeskwindow), "HISTÓRICO DO CAIXA"], [ctk.CTkButton(master= self.frame_tab, command=self.mainwindow), "MESAS / COMANDAS"], [ctk.CTkButton(master= self.frame_tab, command=self.clientswindow), "CLIENTES"], [ctk.CTkButton(master= self.frame_tab, command=self.rankingproducts), "MAIS VENDIDOS"], [ctk.CTkButton(master= self.frame_tab, command=self.historyproducts), "HISTÓRICO DE PEDIDOS"], [ctk.CTkButton(master= self.frame_tab, command=self.rankingservice), "RANKING DE ATENDIMENTOS"]]
            
            self.currentmain = mainbuttons
            self.currentimgs = mainimgs
        elif text == "PRODUTO":
            productimgs = [ctk.CTkImage(Image.open("./imgs/produtos.png"), size=(60,60)), ctk.CTkImage(Image.open("./imgs/complementos.png"), size=(60,60)), ctk.CTkImage(Image.open("./imgs/anotacoes.jpg"), size=(60,60)), ctk.CTkImage(Image.open("./imgs/tiposetamanhos.png"), size=(60,60)), ctk.CTkImage(Image.open("./imgs/categorias.jpg"), size=(60,60)), ctk.CTkImage(Image.open("./imgs/promocoes.png"), size=(60,60))]
            
            productbuttons = [[ctk.CTkButton(master= self.frame_tab, command=self.productswindow), "PRODUTOS"], [ctk.CTkButton(master= self.frame_tab), "COMPLEMENTOS"], [ctk.CTkButton(master= self.frame_tab, command=self.notewindow), "ANOTAÇÕES"], [ctk.CTkButton(master= self.frame_tab), "TIPOS E TAMANHOS"], [ctk.CTkButton(master= self.frame_tab, command=self.categorieswindow), "CATEGORIAS"], [ctk.CTkButton(master= self.frame_tab), "PROMOÇÕES"], ]
            
            self.currentmain = productbuttons
            self.currentimgs = productimgs
        elif text == "CONFIGURAÇÕES":  
            configimgs = [ctk.CTkImage(Image.open("./imgs/config.png"), size=(60,60)), ctk.CTkImage(Image.open("./imgs/garçom.png"), size=(60,60)), ctk.CTkImage(Image.open("./imgs/caixa.png"), size=(60, 60))]
            configbuttons = [[ctk.CTkButton(master=self.frame_tab, command=self.configwindow), "CONFIGURAÇÕES"], [ctk.CTkButton(master=self.frame_tab, command=self.functionarywindow), "FUNCIONÁRIOS"], [ctk.CTkButton(self.frame_tab, command=self.windowprinters), "IMPRESSORAS"]]

            self.currentmain = configbuttons
            self.currentimgs = configimgs
        for i, m in enumerate(self.currentmain):
            buttontemp, texttemp = m
            buttontemp.configure(text=texttemp, fg_color=self.colors[4], hover_color=self.colors[2], image=self.currentimgs[i], compound="top", anchor="bottom")
            buttontemp.place(relx=0.1*i, rely=0.285, relwidth=0.1, relheight=0.715)
    def login(self):
        name = self.entry_name.get()
        password = self.entry_password.get()
        self.connectconts()
        try:
            data = self.contscursor.execute("""SELECT name, password, permissionmaster FROM Conts WHERE name = ?""", (name, ))
            namedata = ""
            passworddata = ""
            permissionmasterdata = ""
            for i in data:
                namedata, passworddata, permissionmasterdata = i
            
            
            if password != passworddata or name != namedata or name == "" or password == "":
                raise Exception("NOME OU SENHA INCORRETOS")
            elif permissionmasterdata != "Y" and passworddata == password:
                raise Exception("ESSE USUÁRIO NÃO TEM PERMISSÃO")
                
        except Exception as error:
            try:
                self.label_failedlogin.destroy()
            except:
                pass
            self.label_failedlogin = ctk.CTkLabel(self.root, text=error, font=("Arial", 18))
            self.label_failedlogin.place(relx=0.4, rely=0.70, relwidth=0.2, relheight=0.05)
        if passworddata == password and permissionmasterdata == "Y" and name == namedata:
            print("login efetuado")
            self.namelogin = namedata
            self.passwordlogin = passworddata
            self.permissionmaster = permissionmasterdata
            self.window()
            self.mainwindow()
            self.changemainbuttons(self.button_main)
        self.desconnectconts()
    def connectconts(self):
        self.conts = sql.connect("sql.db")
        self.contscursor = self.conts.cursor()
    def desconnectconts(self):
        self.conts.commit()
        self.conts.close()
    def connectcommands(self):
        self.commands = sql.connect("commands.db")
        self.commandscursor = self.commands.cursor()
    def desconnectcommands(self):
        self.commands.commit()
        self.commands.close()
    def connectproduct(self):
        self.product = sql.connect("products.db")
        self.productcursor = self.product.cursor()
    def desconnectproduct(self):
        self.product.commit()
        self.product.close()
    def connecthistory(self):
        self.history = sql.connect("his.db")
        self.historycursor = self.history.cursor()
    def desconnecthistory(self):
        self.history.commit()
        self.historycursor.close()
    def connectclients(self):
        self.clients = sql.connect("clients.db")
        self.clientscursor = self.clients.cursor()
    def desconnectclients(self):
        self.clients.commit()
        self.clients.close()
    def connectconfig(self):
        self.config = sql.connect("config.db")
        self.configcursor = self.config.cursor()
    def desconnectconfig(self):
        self.config.commit()
        self.config.close()
    def connecttemp(self):
        self.tempdb = sql.connect("temp.db")
        self.tempdbcursor = self.tempdb.cursor()
    def desconnecttemp(self):
        self.tempdb.commit()
        self.tempdb.close()
    def connectprinter(self):
        self.database = sql.connect("printer.db")
        self.printercursor = self.database.cursor()
    def desconnectprinter(self):
        self.database.commit()
        self.database.close()
    def createtables(self):
        self.connectconfig()
        self.configcursor.execute("""CREATE TABLE IF NOT EXISTS Config(
                                  cod INTEGER PRIMARY KEY,
                                  stylemode VARCHAR,
                                  maxcommands INTEGER(4), 
                                  cnpj VARCHAR(20),
                                  housename VARCHAR(30),
                                  adress VARCHAR(30),
                                  fone VARCHAR(10),
                                  printer VARCHAR(30),
                                  male VARCHAR(30),
                                  female VARCHAR(30)
                                  )""")
        self.desconnectconfig()
        self.connectconts()
        self.contscursor.execute("""CREATE TABLE IF NOT EXISTS Conts(
                                 username VARCHAR(30) NOT NULL,
                                 name VARCHAR(30) NOT NULL,
                                 password VARCHAR(30) NOT NULL,
                                 permissionmaster CHAR(1) NOT NULL, 
                                 permissionrelease CHAR(1),
                                 permissionentry CHAR(1)
                                 )""")
        self.desconnectconts()
        self.connectcommands()
        self.commandscursor.execute("""CREATE TABLE IF NOT EXISTS CommandsActive(
                                    number INTEGER PRIMARY KEY,
                                    initdate CHAR(10),
                                    hour CHAR(5),
                                    nameclient VARCHAR(30),
                                    idclient INTEGER(5)
                                    )""")
        self.commandscursor.execute("""CREATE TABLE IF NOT EXISTS Consumption(
                                    cod INTEGER PRIMARY KEY,
                                    number VARCHAR(4),
                                    date CHAR(10),
                                    hour CHAR(5),
                                    waiter VARCHAR(30),
                                    price VARCHAR(8),
                                    unitprice VARCHAR(8),
                                    quantity INTERGER(3),
                                    product VARCHAR(30),
                                    type VARCHAR(30),
                                    size VARCHAR(30),
                                    text VARCHAR(100),
                                    category VARCHAR(30),
                                    printer VARCHAR(30)
                                    )""")
        self.commandscursor.execute("""CREATE TABLE IF NOT EXISTS Payments(
                                    cod INTEGER PRIMARY KEY,
                                    number INTEGER(4),
                                    type VARCHAR(10),
                                    quantity VARCHAR(8)
                                    )""")
        self.desconnectcommands()
        self.connectproduct()
        self.productcursor.execute("""CREATE TABLE IF NOT EXISTS Products(
                                   name VARCHAR(30),
                                   type VARCHAR(10),
                                   category VARCHAR(10),
                                   price VARCHAR(8),
                                   printer VARCHAR(30)
                                   )""")
        self.productcursor.execute("""CREATE TABLE IF NOT EXISTS Notes(
                                    id INTEGER PRIMARY KEY,
                                    text VARCHAR(30),
                                    category VARCHAR(30)
                                    )""")
        self.productcursor.execute("""CREATE TABLE IF NOT EXISTS Combo(
                                   name VARCHAR(30),
                                   price VARCHAR(8),
                                   products VARCHAR(50)
                                   )""")
        self.productcursor.execute("""CREATE TABLE IF NOT EXISTS CurrentProducts(
                                   name VARCHAR(30),
                                   type VARCHAR(10),
                                   command VARCHAR(10),
                                   releasedate CHAR(10),
                                   releasehour CHAR(5),
                                   releasefunctionary VARCHAR(30),
                                   currentprice VARCHAR(8)
                                   )""")
        self.productcursor.execute("""CREATE TABLE IF NOT EXISTS Category(
                                   cod INTEGER PRIMARY KEY,
                                   name VARCHAR(30)
                                   
                                   )""")
        self.productcursor.execute("""CREATE TABLE IF NOT EXISTS SizeofProducts(
                                   product VARCHAR(30),
                                   price VARCHAR(8),
                                   name VARCHAR(30),
                                   category VARCHAR(30)
                                   )""")
        self.desconnectproduct() 
        self.connecthistory()
        self.historycursor.execute("""CREATE TABLE IF NOT EXISTS ClosedCommand(
                                    cod INTEGER PRIMARY KEY,
                                    number VARCHAR(4),
                                    date CHAR(10),
                                    hour CHAR(5),
                                    nameclient VARCHAR(30),
                                    idclient INTEGER(5),
                                    totalprice VARCHAR(8),
                                    datefinish VARCHAR(19),
                                    cashier VARCHAR(30),
                                    pay VARCHAR(8),
                                    cashdesk INTEGER(6)
                                    )""")
        self.historycursor.execute("""CREATE TABLE IF NOT EXISTS Cashdesk(
                                    id INTEGER PRIMARY KEY,
                                    initdate VARCHAR(20),
                                    finishdate VARCHAR(20),
                                    status VARCHAR(5),
                                    totalcash VARCHAR(10)
                                    )""")
        self.historycursor.execute("""CREATE TABLE IF NOT EXISTS Payments(
                                    commandid INTEGER(4),
                                    type VARCHAR(10),
                                    quantity VARCHAR(8)
                                    )""")
        self.historycursor.execute("""CREATE TABLE IF NOT EXISTS Products(
                                    commandid INTEGER(6),
                                    name VARCHAR(30),
                                    type VARCHAR(10),
                                    quantity VARCHAR(4),
                                    unitprice VARCHAR(8),
                                    releasedate CHAR(10),
                                    releasehour CHAR(5),
                                    waiter VARCHAR(30),
                                    price VARCHAR(8)
                                    )""")
        self.desconnecthistory()
        self.connecttemp()
        self.tempdbcursor.execute("""CREATE TABLE IF NOT EXISTS TempProducts(
                                cod INTEGER PRIMARY KEY,
                                number INTEGER(4),
                                product VARCHAR(30),
                                category VARCHAR(30),
                                unitprice VARCHAR(8),
                                quatity INTEGER(3),
                                text VARCHAR(100),
                                waiter VARCHAR(30),
                                type VARCHAR(10),
                                printer VARCHAR(30)
                                    )""")
        self.desconnecttemp()
        self.connectclients()
        self.clientscursor.execute("""CREATE TABLE IF NOT EXISTS Clients(
                                id INTEGER PRIMARY KEY,
                                name VARCHAR(30),
                                fone INTEGER(13),
                                email VARCHAR(30),
                                idade INTEGER(3),
                                genero VARCHAR(10)
        )""")
        self.desconnectclients()
        self.connectprinter()
        self.printercursor.execute("""CREATE TABLE IF NOT EXISTS ProductPrint(
                                   product VARCHAR(500),
                                   printer VARCHAR(30),
                                   type VARCHAR(10),
                                   command INTEGER(4),
                                   waiter VARCHAR(30),
                                   date VARCHAR(20),
                                   qtd INTEGER(3), 
                                   text VARCHAR(100)
                                   )""")
        self.printercursor.execute("""CREATE TABLE IF NOT EXISTS ClosedPrinter(
                                    id INTEGER PRIMARY KEY,
                                    command INTEGER(4),
                                    date VARCHAR(20),
                                    permission VARCHAR(5),
                                    client VARCHAR(30)
        )""")
        self.printercursor.execute("""CREATE TABLE IF NOT EXISTS ProductsClosed(
                                    id INTEGER(10),
                                    product VARCHAR(500),
                                    type VARCHAR(10),
                                    qtd INTEGER(3), 
                                    unitprice VARCHAR(8)
                                    )""")
        self.printercursor.execute("""CREATE TABLE IF NOT EXISTS Printers(
                                   name VARCHAR(30),
                                   ip VARCHAR(19)
                                   )""")
        self.desconnectprinter()
class server():
    def connectproduct(self):
        self.product = sql.connect("products.db")
        self.productcursor = self.product.cursor()
    def desconnectproduct(self):
        self.product.commit()
        self.product.close()
    def connectconts(self):
        self.conts = sql.connect("sql.db")
        self.contscursor = self.conts.cursor()
    def desconnectconts(self):
        self.conts.commit()
        self.conts.close()
    def connectconfig(self):
        self.config = sql.connect("config.db")
        self.configcursor = self.config.cursor()
    def desconnectconfig(self):
        self.config.commit()
        self.config.close()
    def connectcommands(self):
        self.commands = sql.connect("commands.db")
        self.commandscursor = self.commands.cursor()
    def desconnectcommands(self):
        self.commands.commit()
        self.commands.close()
    def connecttemp(self):
        self.tempdb = sql.connect("temp.db")
        self.tempdbcursor = self.tempdb.cursor()
    def desconnecttemp(self):
        self.tempdb.commit()
        self.tempdb.close()
    def close(self):
        self.servervar.terminate()
    def connectclients(self):
        self.clients = sql.connect("clients.db")
        self.clientscursor = self.clients.cursor()
    def desconnectclients(self):
        self.clients.commit()
        self.clients.close()
    def __init__(self):
        self.servervar =  Process(target=self.server)
        self.permission = True
        self.servervar.start()
    def server(self):
        if self.permission:
            self.HOST = socket.gethostbyname(socket.gethostname())
            self.PORT = 55261
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind((self.HOST, self.PORT))
            name = socket.gethostname()
            print(socket.gethostbyname(name))
            self.s.listen()
            while self.permission:
                conn, ender = self.s.accept()
                data = None
                while not data:
                    data = conn.recv(1024)
                text = data.decode()
                listen = text.split(",=")
                if listen[0] == "LOGIN":
                    self.connectconts()
                    temp = ""
                    TEMp = self.contscursor.execute("SELECT * FROM Conts WHERE name = ? AND password = ?", (listen[1], listen[2]))
                    for i in TEMp:
                        temp = i
                    if temp == "":
                        conn.sendall(str.encode("NOT"))
                    else:
                        conn.sendall(str.encode("YES"))
                    self.desconnectconts()
                elif listen[0] == "LIMITCOMMANDS":
                    self.connectconfig()
                    TEMp = self.configcursor.execute("SELECT maxcommands FROM Config")
                    temp = ""
                    for i in TEMp:
                        temp = i[0]
                    conn.sendall(str.encode(str(temp)))
                    self.desconnectconfig()
                elif listen[0] == "OPENCOMMANDS":
                    self.connectcommands()
                    TEMp = self.commandscursor.execute("SELECT number FROM CommandsActive")
                    temp = ""
                    commands = ""
                    for i in TEMp:
                        if temp == "":
                            temp = "a"
                            commands = str(i[0])
                        else:
                            commands = commands + ",=" + str(i[0]) 
                    self.desconnectcommands()
                    conn.sendall(str.encode(commands))
                elif listen[0] == "PRODUCTSON":
                    self.connectcommands()
                    TEMp = self.commandscursor.execute("SELECT product, quantity, price, type, size FROM Consumption WHERE number = ?", (listen[1], ))
                    temp = ""
                    for i in TEMp:
                        product, quantity, price, tipe, size = i
                        if temp == "":
                            temp = f"{product}|{quantity}|{price}"
                        else:
                            temp = temp + f",={product}|{quantity}|{price}"
                    self.desconnectcommands()
                    conn.sendall(str.encode(temp))
                elif listen[0] == "CATEGORIES":
                    self.connectproduct()
                    TEMp = self.productcursor.execute("SELECT name FROM Category")
                    temp = ""

                    for i in TEMp:
                        if temp != "":
                            temp = temp + f",={i[0]}"
                        else:
                            temp = temp + f"{i[0]}"
                    self.desconnectproduct()
                    conn.sendall(str.encode(temp))
                elif listen[0] == "PRODUCTSCATEGORY":
                    self.connectproduct()
                    TEMp = self.productcursor.execute("SELECT name, type, price, printer FROM Products WHERE category = ?", (listen[1], ))
                    temp = ""
                    for i in TEMp:
                        if temp != "":
                            temp = temp + f",={i[0]}|{i[1]}|{i[2]}|{i[3]}"
                        else:
                            temp = f"{i[0]}|{i[1]}|{i[2]}|{i[3]}"                    
                    self.desconnectproduct()
                    conn.sendall(str.encode(temp))
                elif listen[0] == "SIZESCATEGORY":
                    self.connectproduct()
                    TEMp = self.productcursor.execute("SELECT name, price FROM SizeofProducts WHERE product = ? and category = ?", ( listen[1], listen[2]))
                    temp = ""
                    for i in TEMp:
                        if temp != "":
                            temp = temp + f",={i[0]}|{i[1]}"
                        else:
                            temp = f"{i[0]}|{i[1]}"
                    self.desconnectproduct()
                    conn.sendall(str.encode(temp))
                elif listen[0] == "INSERT":
                    number, username, password = listen[1], listen[2], listen[3]
                    del listen[0]; del listen[0]; del listen[0]; del listen[0]
                    listen = listen[0].split(".-")
                    self.connectconts()
                    TEMp = self.contscursor.execute("SELECT name FROM Conts WHERE name = ? AND password = ?", (username, password))
                    temp = ""
                    for i in TEMp:
                        temp = i
                    self.desconnectconts()
                    if temp != "":
                        self.connecttemp()
                        if len(listen) == 6:
                            product, category, unitprice, qtd, tipe, prynter = listen
                            description = ""
                        else:
                            product, category, unitprice, qtd, description, tipe, prynter = listen
                        self.tempdbcursor.execute("INSERT INTO TempProducts (number, product, category, unitprice, quatity, text, waiter, type, printer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (number, product, category, unitprice, qtd, description, username, tipe, prynter))
                        self.desconnecttemp()
                        conn.sendall(str.encode("Y"))
                    else:
                        conn.sendall(str.encode("N"))
                elif listen[0] == "GETNOTES":
                    self.connectproduct()
                    temp = self.productcursor.execute("SELECT text FROM Notes WHERE category = ?", (listen[1],  ))
                    text = ""
                    num = 1
                    for i in temp:
                        if num == 1:
                            text = i[0]
                            num = 2
                        else:
                            text = text + ".=" + i[0]
                    self.desconnectproduct()
                    conn.sendall(str.encode(text))
                elif listen[0] == "INSERTCLIENT":
                    self.connectcommands()
                    del listen[0]
                    waiter, passw, command, idclient, client, male, female = listen
                    
                    date = str(datetime.datetime.now())[0:19]
                    date, hour = date[0:10], date[11:20]
                    try:
                        idclient = int(idclient)
                    except:
                        idclient = ""
                    if idclient != "":
                        self.connectclients()
                        tempclient = self.clientscursor.execute("SELECT name FROM Clients WHERE id = ?", (idclient, ))
                        for i in tempclient:
                            client = i[0]
                        self.desconnectclients()
                    
                    self.connecttemp()
                    self.connectconfig()
                    self.connectproduct()
                    self.connectconts()
                    temp = self.contscursor.execute("SELECT name, password, permissionmaster, permissionentry FROM Conts WHERE name = ?", (waiter, ))
                    name, password, permissionmaster, permissionentry = "", "", "", ""
                    for i in temp:
                        name, password, permissionmaster, permissionentry = i
                    if name == waiter and passw == password:
                        if permissionmaster == "Y" or permissionentry == "Y":
                            temp = self.commandscursor.execute("SELECT number FROM CommandsActive WHERE number = ?", (command, ))
                            tmp = ""
                            for i in temp:
                                tmp = i[0]
                            if tmp == "":
                                self.commandscursor.execute("INSERT INTO CommandsActive (number, initdate, hour, nameclient, idclient) VALUES (?, ?, ?, ?, ?)", (command, date, hour, client, idclient))
                            else:
                                self.commandscursor.execute("UPDATE CommandsActive SET nameclient = ?, idclient = ? WHERE number = ?", (client, idclient, command))
                            if int(male) > 0:
                                temp = self.configcursor.execute("SELECT male FROM Config WHERE cod = '1'")
                                for i in temp:
                                    temp = i[0]
                                temp = self.productcursor.execute("SELECT name, type, category, price, printer FROM Products WHERE name = ?", (temp, ))
                                for i in temp:
                                    product, tipe, category, price, prynter = i
                                self.tempdbcursor.execute("INSERT INTO TempProducts (number, product, category, unitprice, quatity, text, waiter, type, printer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (command, product, category, price, male, "", waiter, tipe, prynter))
                            if int(female) > 0:
                                temp = self.configcursor.execute("SELECT female FROM Config WHERE cod = '1'")
                                for i in temp:
                                    temp = i[0]
                                temp = self.productcursor.execute("SELECT name, type, category, price, printer FROM Products WHERE name = ?", (temp, ))
                                for i in temp:
                                    product, tipe, category, price, prynter = i
                                self.tempdbcursor.execute("INSERT INTO TempProducts (number, product, category, unitprice, quatity, text, waiter, type, printer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (command, product, category, price, female, "", waiter, tipe, prynter))
                            conn.sendall(str.encode("OK"))
                    self.desconnectconts()
                    self.desconnectproduct()
                    self.desconnecttemp()
                    self.desconnectconfig()
                    self.desconnectcommands()
                else:
                    conn.sendall(data)
                conn.close()
def closeprinter():
    aprinter.active = False
class printer():
    active = False
    paused = False
    printers = {}
    def connectconfig(self):
        self.config = sql.connect("config.db")
        self.configcursor = self.config.cursor()
    def desconnectconfig(self):
        self.config.commit()
        self.config.close()
    def connect(self):
        self.database = sql.connect("printer.db")
        self.cursor = self.database.cursor()
    def desconnect(self):
        self.database.commit()
        self.database.close()
    def init(self):
        self.printervar = Process(target=self.processprinter)  
        self.printervar.start()  
    def pause(self):
        self.paused = True
    def retome(self):
        self.paused = False
    def connectcommands(self):
        self.commands = sql.connect("commands.db")
        self.commandscursor = self.commands.cursor()
    def desconnectcommands(self):
        self.commands.commit()
        self.commands.close()
    def processprinter(self):
        while True:
            self.connect()
            temp = self.cursor.execute('SELECT * FROM ProductPrint')
            listen = []
            for i in temp:
                #product, prynter, tipe, command, waiter, date, qtd, text = i
                if listen == []:
                    listen.append(i)
                else:
                    if listen[0][4] == i[4] and listen[0][1] == i[1] and listen[0][3] == i[3]:
                        listen.append(i)
            if listen != []:
                temp = self.cursor.execute("SELECT ip FROM Printers WHERE name = ?", (listen[0][1], ))
                for i in temp:
                    prynter = i[0]
                prynter = Network(prynter)
                prynter.set(bold=True, align='center', width=2, height=2, custom_size=True)
                prynter.textln(listen[0][1].replace("ã", "a").replace("Ã", "A"))
                prynter.ln()
                prynter.set(bold=False, align='left', width=2, height=2, custom_size=True)
                prynter.textln(listen[0][5].replace("-", "/"))
                prynter.ln()
                prynter.set(bold=True, align='center', width=2, height=2, custom_size=True)
                prynter.textln(f"COMANDA: {listen[0][3]}")
                prynter.ln()
                prynter.set(bold=False, align='left', width=2, height=2, custom_size=True)
                self.connectcommands()
                temp = self.commandscursor.execute("SELECT nameclient FROM CommandsActive WHERE number = ?", (listen[0][3], ))
                for i in temp:
                    if i[0] != "":
                        print(i[0])
                        prynter.textln(i[0].replace("ã", "a").replace("Ã", "A"))
                self.desconnectcommands()
                prynter.textln(f"Atendente: {listen[0][4]}")
                prynter.set(bold=True)
                for i in listen:
                    prynter.set(smooth=False, bold=False, align='left', width=2, height=2, custom_size=True)
                    prynter.textln(f"{i[6]} {i[0]}".replace("ã", "a").replace("Ã", "A"))
                    if i[7] != "":
                        prynter.set(smooth=True, align='left', width=2, height=2, custom_size=True, font='b')
                        prynter.textln(f"*{i[7]}")
                prynter.cut()
                for i in listen:
                    self.cursor.execute("DELETE FROM ProductPrint WHERE product = ? AND printer = ? AND type = ? AND command = ? AND waiter = ? AND date = ? AND qtd = ?", (i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
                prynter.close()
            
            tmp = []
            temp = self.cursor.execute("SELECT * FROM ClosedPrinter")
            for i in temp:
                tmp.append(i)
            if tmp != [] and tmp[0][3] == "True": 
                id, command, date, permission, client = tmp[0]
                print(date)
                self.connectconfig()
                config = self.configcursor.execute("SELECT cnpj, housename, adress, fone, printer FROM Config WHERE cod = 1")
            
                for i in config:
                    cnpj, housename, adress, fone, prynter = i
                prynter = self.cursor.execute("SELECT ip FROM Printers WHERE name = ?", (prynter, ))
                for i in prynter:
                    ip = i[0]
                listen = []
                for i in temp:
                    listen.append(i)
                prynter = Network(ip)
                    
                self.desconnectconfig()
                productstemp = []
                temp = self.cursor.execute("SELECT * FROM ProductsClosed WHERE id = ?", (tmp[0][0], ))
                for i in temp:
                    productstemp.append(i)
                prynter.set(bold=True, align='center', width=2, height=2, custom_size=True)
                prynter.textln(housename.replace("ã", "a").replace("Ã", "A"))
                prynter.set(font="b", custom_size=True, width=1, height=1)
                prynter.ln()
                if adress != "":
                    prynter.set(bold=True, font='b', align='center', width=2, height=2, custom_size=True)
                    prynter.textln(adress.replace("ã", "a").replace("Ã", "A"))
                    prynter.set(font="b", custom_size=True, width=1, height=1)
                    prynter.ln()
                prynter.set(font="b", custom_size=True, width=2, height=2, align="left")
                prynter.textln("CNPJ: " + str(cnpj))
                prynter.set(font="b", custom_size=True, width=1, height=1)
                prynter.ln()
                prynter.set(font="b", custom_size=True, width=2, height=2)
                prynter.textln("IMPRESSO EM: " + str(datetime.datetime.now())[0:19].replace("-", "/"))
                
                prynter.set(font="b", custom_size=True, width=1, height=1)
                prynter.ln()
                prynter.set(font="b", align="center", custom_size=True, width=2, height=2)
                prynter.text('"NAO É DOCUMENTO FISCAL"')
                prynter.set(font="b", align="left", custom_size=True, width=1, height=1)
                prynter.ln()
                if client != "":
                    prynter.set(font="b", custom_size=True, width=2, height=2)
                    prynter.ln()
                    prynter.textln("Cliente: " + client.replace("ã", "a").replace("Ã", "A"))
                prynter.set(font="b", custom_size=True, width=1, height=1)
                prynter.ln()
                prynter.set(bold=False, align='center', width=2, height=2, custom_size=True)
                prynter.textln("COMANDA: " + str(command))
                prynter.set(font="b", custom_size=True, width=1, height=1)
                prynter.ln()
                prynter.set(bold=False, align='center', width=2, height=2, custom_size=True)
                prynter.textln("PRODUTOS (V.Unit): TOTAL")
                products = {}
                prynter.set(font="b", custom_size=True, width=1, height=1)
                prynter.ln()
                for i in productstemp:
                    try:
                        product = products[i[1]]
                        product[3] = product[3] + i[3]
                        products[i[1]] = product
                    except:
                        products[i[1]] = [i[0], i[1], i[2], i[3], i[4]]
                totalpay = 0.0
                for i in products:
                    text = f"{products[i][3]} {products[i][1].replace('ã', 'a').replace('Ã', 'A')} ({products[i][4]})"
                    num = len(text)
                    times = num//24
                    if num%24 != 0:
                        times += 1
                    a = 0
                    totalprice = str(float(products[i][3]) * float(products[i][4])).replace(".", ",")
                    if not "," in totalprice:
                        totalprice = totalprice + ",00"
                    elif ",00" in totalprice:
                        pass
                    elif ",0" in totalprice:
                        totalprice = totalprice + "0"
                    while len(totalprice) < 7:
                        totalprice = " " + totalprice
                    totalpay = totalpay + float(totalprice.replace(",", "."))
                    while a < times:
                        prynter.set(font="b", custom_size=True, width=2, height=2)
                        if a == 0:
                            print(times)
                            if times == 1:
                                qtdword = len(text + " " + str(totalprice))
                                textprice = text + " " * (32 - qtdword) + totalprice
                                prynter.textln(f"{textprice}")
                            else:    
                                prynter.textln(f"{text[0:24]} {totalprice}")
                        else:
                            prynter.textln(f"{text[a*24:(a+1)*24]}")
                        a = a + 1
                prynter.textln("-" * 32)
                totalpay = str(totalpay).replace(".", ",")
                if not "," in totalpay:
                    totalpay = totalpay + ",00"
                elif ",00" in totalpay:
                    pass
                elif ",0" in totalpay:
                    totalpay = totalpay + "0"
                qtdword = len("Total:" + totalpay)
                prynter.textln("Total:" + " " * (31 - qtdword) + totalpay)
                prynter.set(font="b", custom_size=True, width=2, height=2)
                prynter.ln()
                now = datetime.datetime.now()
                date = datetime.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]), int(date[11:13]), int(date[14:16]), int(date[17:19]))
                delta = now - date
                total_sec = delta.total_seconds()
                total_min, sec = divmod(int(total_sec), 60)
                total_hour, minute = divmod(total_min, 60)
                total_days, hour = divmod(total_hour, 24)
                text = ""
                if total_days != 0:
                    text = text + str(total_days) + "D " + str(hour) + "H "
                elif total_hour != 0:
                    text = text + str(hour) + "H "
            
                text = text + str(minute) + "M " + str(sec) + "S"
                prynter.textln("TEMPO: " + text)
                if fone != "":
                    prynter.ln()
                    prynter.textln(f"TELEFONE: {fone}")
                prynter.cut()
                
                prynter.close()
                self.cursor.execute("DELETE FROM ClosedPrinter WHERE id = ?", (tmp[0][0], ))
                self.cursor.execute("DELETE FROM ProductsClosed WHERE id = ?", (tmp[0][0], ))

            self.desconnect()
            sleep(3)
if __name__ ==  "__main__":
    aserver = server()
    aprinter = printer()
    application() 