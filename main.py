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
from escpos.printer import network
class application():
    def __init__(self):
        self.createtables()
        self.positionp = True
        self.cod, self.stylemode, self.maxcommands = "", "", ""
        mod, up = False, False
        self.connectconfig()
        self.currentconfig = self.configcursor.execute("""SELECT * FROM Config WHERE cod = 1""") 
        for i in self.currentconfig:
            self.cod, self.stylemode, self.maxcommands = i
        if self.cod == "":
            self.cod = 1
            mod = True
        if self.stylemode == "":
            self.stylemode = "DARK"
            up = True
        if self.maxcommands == "":
            self.maxcommands = 400
            up = True
        if mod:
            self.configcursor.execute("""INSERT INTO Config (stylemode, maxcommands) VALUES (?, ?)""", (self.stylemode, self.maxcommands))
        elif mod == False and up == True:
            self.configcursor.execute("""UPDATE Config SET stylemode = ?, maxcommands = ? WHERE cod = 1""", (self.stylemode, self.maxcommands))
        if self.stylemode == "DARK":
            ctk.set_appearance_mode("dark")
            self.colors = ["#1f1f1f", "#2f2f2f", "#383838", "#3f3f3f", "#484848", "#4f4f4f", "#585858", "#5f5f5f", "#6f6f6f", "#7f7f7f"]
        elif self.stylemode == "LIGHT":
            ctk.set_appearance_mode("light")
            self.colors = ["#8f8f8f", "#8f8f8f", "#787878", "#7f7f7f", "#686868", "#6f6f6f", "#585858", "#5f5f5f", "#5f5f5f", "#4f4f4f"]
        self.desconnectconfig()
        
        self.root = ctk.CTk()
        self.loginwindow()

        self.root.mainloop()
    def loginwindow(self):
        self.currentwindow = "LOGIN"
        self.root.attributes("-fullscreen", True)
        self.entry_name = ctk.CTkEntry(self.root, bg_color=self.colors[9], placeholder_text="NOME", font=("Arial", 20))
        self.entry_name.place(relx=0.4, rely=0.45, relwidth=0.2, relheight=0.05)

        self.entry_password = ctk.CTkEntry(self.root, bg_color=self.colors[9], placeholder_text="SENHA", show="*", font=("Arial", 20))
        self.entry_password.place(relx=0.4, rely=0.55, relwidth=0.2, relheight=0.05)
        
        self.button_login = ctk.CTkButton(self.root, fg_color=self.colors[9], text="LOGIN", hover_color=self.colors[8], command=self.login, font=("Arial", 20))
        self.button_login.place(relx=0.4, rely=0.65, relwidth=0.2, relheight=0.05)
        

        self.personimg = ctk.CTkImage(Image.open("imgs/person.png"), size=(300,300))
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
    def searchnameentry(self, n = True):
        if self.positionp == True:
            try:
                pa.moveTo(0,0)
                self.position_namecommand = pa.locateOnScreen("imgs/buttonname.PNG", confidence=0.7)
                self.positionp = False
            except:
                self.root.after(500, self.searchnameentry)
    def keypresslogin(self, event):
        n = event.keysym
        if n == "Return":
            self.login()
    def on_closingcommandwindow(self):
        self.root.bind_all("<KeyPress>", self.presskey)
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

        self.root.after(500, self.searchnameentry)

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
        temp = self.productcursor.execute("SELECT name, category FROM Products WHERE type = ?", ("SIZE", ))
        for i in temp:
            listofproducts.append(i)
        for k, i in enumerate(listofproducts):
            print(i)
            product, category = i
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
                                             ctk.CTkButton(self.frame_productreeviews, fg_color=self.colors[5], text="", width=100, height=50, image=ctk.CTkImage(Image.open("imgs/pencil.jpg"), size=(40,40)), hover=False, command=lambda x = product, y = category:self.addproductwindow(x, y)), 
                                             ctk.CTkButton(self.frame_productreeviews, fg_color=self.colors[5], text="", width=100, height=50, image=ctk.CTkImage(Image.open("imgs/lixeira.png"), size=(40,40)), hover=False, command=lambda x=product, y=category:deleteproductsize(x, y))])
            self.current_productslist[k][0].grid(row=k + 2, column=1, padx=1, pady=1)
            self.current_productslist[k][1].grid(row=k + 2, column=2, padx=1, pady=1)
            self.current_productslist[k][2].grid(row=k + 2, column=3, padx=1, pady=1)
            self.current_productslist[k][3].grid(row=k + 2, column=4, padx=1, pady=1)
            self.current_productslist[k][4].grid(row=k + 2, column=5, padx=1, pady=1)
        self.desconnectproduct()
 
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
            name, ttype, category, price = i
            self.current_productslist.append([ctk.CTkLabel(self.frame_productreeviews, text=category, fg_color=self.colors[5], width=400, height=40), 
                                              ctk.CTkLabel(self.frame_productreeviews, text=name, fg_color=self.colors[5], width=400, height=40), 
                                              ctk.CTkLabel(self.frame_productreeviews, text=price, fg_color=self.colors[5], width=100, height=40), 
                                              ctk.CTkLabel(image=ctk.CTkImage(Image.open("imgs/pencil.jpg"), size=(30, 30)), master=self.frame_productreeviews, text="", fg_color=self.colors[5], width=100, height=40), 
                                              ctk.CTkButton(self.frame_productreeviews, command=lambda x=name, y=category, z=ttype:self.deleteproductnormal(x, y, z), image=ctk.CTkImage(Image.open("imgs/lixeira.png"), size=(30,30)), text="", fg_color=self.colors[5], width=100, hover=False)])
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
        if self.currentwindow == "MAIN":
            self.frame_commands.destroy();self.frame_down.destroy();del self.str_searchcommands; self.label_searchcommand.destroy();self.button_addcommand.destroy(); self.frame_commands.place_forget()
            self.root.bind("<Button-1>", self.nonclick)
            self.root.bind_all("<KeyPress>", self.nonclick)
        elif self.currentwindow == "PRODUCTS":
            self.frame_producttypes.destroy(); self.frame_modproducts.destroy(); self.frame_productreeviews.destroy(); self.frame_productreeviews.place_forget()
        elif self.currentwindow == "CATEGORIES":
            self.treeview_categories.destroy(); self.treeview_categories.place_forget(); self.frame_categoriesmod.destroy()
        elif self.currentwindow == "CONFIGURAÇÕES":
            pass
        elif self.currentwindow == "FUNCIONÁRIOS":
            self.scroolframe_functionary.destroy; self.scroolframe_functionary.place_forget(); self.button_addfunctionary.destroy(); self.entry_name.destroy(); self.entry_passwordcont.destroy()
        self.root.bind_all("<KeyPress>", self.nonclick)
        self.root.bind("<Button-1>", self.nonclick)
    
    def addproductwindow(self, product = "", category = ""):
        
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
            self.entry_namenewproduct.place(relx=0.01, rely=0.11, relwidth=0.42, relheight=0.39)

            self.entry_namesize = ctk.CTkEntry(self.frame_mainnewproduct, placeholder_text="NOME DO TAMANHO", fg_color= self.colors[4])
            self.entry_namesize.place(relx=0.01, rely=0.60, relwidth=0.39, relheight=0.39)

            categories = []
            self.connectproduct()
            temp = self.productcursor.execute("SELECT name FROM Category")
            for i in temp:
                categories.append(i[0])
            self.desconnectproduct()

            self.combobox_categoryname = ctk.CTkComboBox(self.frame_mainnewproduct, fg_color=self.colors[4], values=categories, width=200,height=60)
            self.combobox_categoryname.place(relx=0.44, rely=0.10)

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
                                               ctk.CTkButton(self.scroolframe_sizeproductsseize, text="", width=100, height=40, image=ctk.CTkImage(Image.open("imgs/lixeira.png"), size=(30,30)), fg_color=self.colors[6], hover=False, command=lambda x=i:self.deletesizefromproduct(x))])
            self.current_tablesizes[i][0].grid(row=i + 2, column=1, padx=1, pady=1)
            self.current_tablesizes[i][1].grid(row=i + 2, column=2, padx=1, pady=1)
            self.current_tablesizes[i][2].grid(row=i + 2, column=3, padx=1, pady=1)
    def deletesizefromproduct(self, i):
        del(self.current_sizesfornewproduct[i])
        self.reloadsizesinwindow()
    def addproductsize(self, oldname = "", oldcategory = ""):
        name = self.entry_namenewproduct.get()
        category = self.combobox_categoryname.get()
        print(category)
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
            self.product.execute("INSERT INTO Products (name, category, type) VALUES (?, ?, ?)", (name, category, "SIZE"))
            self.rootaddproductsize.destroy()
        self.desconnectproduct()
        self.reloadproductssize()
    def addproductfunc(self):
        name = self.entry_namenewproduct.get()
        category = self.combobox_categoryname.get()
        price = self.entry_price.get()
        self.connectproduct()
        self.productcursor.execute("INSERT INTO Products (name, type, category, price) VALUES (?,?,?,?)", (name, "NORMAL", category, price))
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
            self.currentcategory.append([ctk.CTkLabel(self.treeview_categories, fg_color=self.colors[4], text=id, width=100, height=40), ctk.CTkLabel(self.treeview_categories,fg_color=self.colors[4], text=name, width=400, height=40), ctk.CTkButton(self.treeview_categories, image=ctk.CTkImage(Image.open("imgs/pencil.jpg"), size=(30, 30)),command=lambda x=id, y=name:self.editcategorybutton(y, x), fg_color=self.colors[4], hover=False, text="", width=100, height=40), ctk.CTkButton(self.treeview_categories, image=ctk.CTkImage(Image.open("imgs/lixeira.png"), size=(30, 30)), command=lambda x=id:self.deletecategory(x), fg_color=self.colors[4], hover=False, text="", width=100, height=40)])
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
    def windowcommand(self, command = 0):
        def close():
            self.root.bind_all("<KeyPress>",self.presskeycommandwindow)
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
        
        self.rootcommand.title("COMANDA " + num)
        self.rootcommand.geometry("900x800")
        self.rootcommand.resizable(False, False)
        self.rootcommand.transient(self.root)
        self.rootcommand.grab_set()

        self.frame_consume = ctk.CTkScrollableFrame(self.rootcommand, fg_color=self.colors[3])
        self.frame_consume.place(relx=0, rely=0.1, relwidth=1, relheight=0.7)

        self.frame_infocommand = ctk.CTkFrame(self.rootcommand, fg_color=self.colors[2])
        self.frame_infocommand.place(relx=0,rely=0.8,relwidth=1,relheight=0.2)

        self.button_delcommand = ctk.CTkButton(self.frame_infocommand, fg_color=self.colors[4], text="EXCLUIR COMANDA", hover_color=self.colors[5], command=deletecommand)
        self.button_delcommand.place(relx=0.01, rely=0.15, relwidth=0.29, relheight=0.7)

        self.button_finishcommand = ctk.CTkButton(self.frame_infocommand, fg_color=self.colors[4], text="PAGAMENTO", hover_color=self.colors[5])
        self.button_finishcommand.place(relx=0.7, rely=0.15, relwidth=0.29, relheight=0.7)

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

        self.time_heading = ctk.CTkLabel(self.rootcommand, text="TEMPO", fg_color=self.colors[4], width=100, height=30)
        self.time_heading.grid(row=1, column=6, padx=1, pady=50)

        self.edit_heading = ctk.CTkLabel(self.rootcommand, text="EDITAR", fg_color=self.colors[4], width=50, height=30)
        self.edit_heading.grid(row=1, column=7, padx=1, pady=50)

        self.del_heading = ctk.CTkLabel(self.rootcommand, text="EXCLUIR", fg_color=self.colors[4], width=50, height=30)
        self.del_heading.grid(row=1, column=8, padx=1, pady=50)

        self.totalpricelabel = ctk.CTkLabel(self.frame_infocommand, text="TOTAL:", fg_color=self.colors[4])
        self.totalpricelabel.place(relx=0.31, rely=0.15, relwidth=0.06, relheight=0.3)

        self.button_addproductoncommand = ctk.CTkButton(self.rootcommand, text="ADICIONAR PRODUTO", command=self.addpdctcommandwindow, fg_color=self.colors[4], hover_color=self.colors[5])
        self.button_addproductoncommand.place(relx=0.7, rely=0.002, relwidth=0.29, relheight=0.057)
        self.currentcommandwindow = num
        self.root.bind_all("<KeyPress>",self.presskeycommandwindow)
        self.rootcommand.protocol("WM_DELETE_WINDOW", self.on_closingcommandwindow)
        self.reloadproductforcommands(num)
    def reloadproductforcommands(self, number):
        def delete(cod):
            self.connectcommands()
            self.commandscursor.execute("DELETE FROM Consumption WHERE cod = ?", (cod,))
            self.desconnectcommands()
            self.reloadproductforcommands(self.currentcommandwindow)
        self.connectcommands()
        temp = self.commandscursor.execute("SELECT cod, number, date, hour, waiter, price, unitprice, quantity, product, type, size FROM Consumption WHERE number = ?", (number, ))
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
                                                   ctk.CTkButton(self.frame_consume, text="", fg_color=self.colors[4], width=50, height=40, image=ctk.CTkImage(Image.open("imgs/pencil.jpg"), size=(30, 30)),hover=False, command=lambda x= cod:self.addproductincommandwindow(cod=x)),
                                                   ctk.CTkButton(self.frame_consume, text="", fg_color=self.colors[4], width=50, height=40, image=ctk.CTkImage(Image.open("imgs/lixeira.png"), size=(30, 30)),hover=False, command=lambda x = cod: delete(x))
                                                   ])
            self.current_productsincommands[k][0].grid(row= k + 1, column=1, padx=0, pady=1)
            self.current_productsincommands[k][1].grid(row= k + 1, column=2, padx=1, pady=1)
            self.current_productsincommands[k][2].grid(row= k + 1, column=3, padx=1, pady=1)
            self.current_productsincommands[k][3].grid(row= k + 1, column=4, padx=1, pady=1)
            self.current_productsincommands[k][4].grid(row= k + 1, column=5, padx=1, pady=1)
            self.current_productsincommands[k][5].grid(row= k + 1, column=6, padx=1, pady=1)
            self.current_productsincommands[k][6].grid(row= k + 1, column=7, padx=1, pady=1)
            self.current_productsincommands[k][7].grid(row= k + 1, column=8, padx=1, pady=1)  
            totalprice = totalprice + float(price)
        self.label_totalprice = ctk.CTkLabel(self.frame_infocommand, text=totalprice, fg_color=self.colors[4])
        self.label_totalprice.place(relx=0.37, rely=0.15, relwidth=0.32, relheight=0.3)
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
    def pressesccommand(self, event):
        if event.keysym == "Escape":
            self.closewindowaddproduct()
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
            self.commandscursor.execute("INSERT INTO Consumption (number, date, hour, waiter, price, unitprice, quantity, product, type, size) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (self.currentcommandwindow, date, hour, self.namelogin, str(float(unitprice)*int(quantity)), unitprice, quantity, name, tipe, ""))
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
        if cod != "":
            self.rooteditaddproduct = ctk.CTkToplevel(self.rootcommand)
            self.rooteditaddproduct.transient(self.rootcommand)
        else:
            self.rooteditaddproduct = ctk.CTkToplevel(self.rootaddpdctcommand)
            self.rooteditaddproduct.transient(self.rootaddpdctcommand)
        self.rooteditaddproduct.geometry("500x200")
        self.rooteditaddproduct.resizable(False, False)
        self.rooteditaddproduct.title("CONFIGURAÇÕES DO PRODUTO")
        self.rooteditaddproduct.grab_set()

        self.label_product = ctk.CTkLabel(self.rooteditaddproduct, text= product + " (" + category + ")", fg_color=self.colors[4], font=("Arial", 25))
        self.label_product.place(relx=0.01, rely=0.01, relwidth=0.59, relheight=0.48)

        self.entry_quantity = ctk.CTkEntry(self.rooteditaddproduct, fg_color=self.colors[4], font=("Arial", 25))
        self.entry_quantity.place(relx=0.61, rely=0.01, relwidth=0.14, relheight=0.48)
        self.entry_quantity.insert(0, "1")

        self.entry_unitprice = ctk.CTkEntry(self.rooteditaddproduct, fg_color=self.colors[4], font=("Arial", 25), placeholder_text="PREÇO")
        self.entry_unitprice.place(relx=0.76, rely=0.01, relwidth=0.23, relheight=0.48)
        
        self.button_confirm = ctk.CTkButton(self.rooteditaddproduct, fg_color=self.colors[4], hover_color=self.colors[5], command=confirm, text="CONFIRMAR", font=("Arial", 25))
        self.button_confirm.place(relx=0.51, rely=0.50, relwidth=0.48, relheight=0.49)
        
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
    def reloadproductstable(self, search = ""):
        def addproductincommand(product, category, tipe, price):
            if tipe == "SIZE":
                self.addproductincommandwindow(product, category, tipe)
            else:
                self.connectcommands()
                date = str(datetime.datetime.now())[0:19]
                date, hour = date[0:10], date[11:20]
                self.commandscursor.execute("INSERT INTO Consumption (number, date, hour, waiter, price, unitprice, quantity, product, type, size) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (self.currentcommandwindow, date, hour, self.namelogin, price, price, "1", product, tipe, ""))
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
            name, tipe, category, price = i
            self.currentproductsaddlist.append([ctk.CTkLabel(self.scroolframe_addproduct, text=category, width=200, height=40, fg_color=self.colors[5]),
                                                ctk.CTkLabel(self.scroolframe_addproduct, text=name, width=200, height=40, fg_color=self.colors[5]),
                                                ctk.CTkLabel(self.scroolframe_addproduct, text=price, width=90, height=40, fg_color=self.colors[5]),
                                                ctk.CTkButton(self.scroolframe_addproduct, text="", width=70, height=40, image=ctk.CTkImage(Image.open("imgs/add1.png"), size=(30, 30)), fg_color=self.colors[5], hover=False, command=lambda x= name, y = category, z = tipe, a= price:addproductincommand(x, y, z, a)),
                                                ctk.CTkButton(self.scroolframe_addproduct, text="", width=70, height=40, image=ctk.CTkImage(Image.open("imgs/add.png"), size=(30, 30)), fg_color=self.colors[5], hover=False, command=lambda x= name, y= category, z= tipe, a= price:self.addproductincommandwindow(x, y, z, a))])
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

            self.currentcommands.append(ctk.CTkButton(self.frame_commands,fg_color=self.colors[3], command=lambda m = i:self.windowcommand(self.currentcommands[m]), hover=False, width=250, height= 150, text= str(number) + " "+ nameclient +"\n" + "TEMPO: " + text, font=("Arial", 20)))
            
            self.currentcommands[i].grid(row=int(i/6), column=i%6, padx=10, pady=5)
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
        try:
            if not "self.rootnewcom" in globals():
                if "self.rootnewcom" in globals() or "self.rootnewcom" in locals():
                    pass
                else:
                    position = pa.position()
                    if position.x > self.position_namecommand[0] and position.x < self.position_namecommand[0] + self.position_namecommand[3]:
                        if position.y > self.position_namecommand[1] and position.y < self.position_namecommand[1] + position.y[3]:
                            pass
                        else:
                            self.entry_namecommand.delete(0, "end")
                            event.widget.focus_set()
                    else:
                        self.entry_namecommand.delete(0, "end")
                        event.widget.focus_set()
        except:
            pass
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
                                                    ctk.CTkButton(self.scroolframe_functionary, fg_color=self.colors[4], width=60, height=40, text="", hover=False, image=ctk.CTkImage(Image.open("imgs/pencil.jpg"), size=(30,30)), command=lambda x=name: edit(x)),
                                                    ctk.CTkButton(self.scroolframe_functionary, fg_color=self.colors[4], width=60, height=40, text="", hover=False, image=ctk.CTkImage(Image.open("imgs/lixeira.png"), size=(30,30)), command=lambda x=name: delete(x))])
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
                temp = "A"
            tmp = self.contscursor.execute("SELECT username, name FROM Conts WHERE name = ?",(self.entry_name.get(), ))
            for i in tmp:
                temp = "A"
            if temp == "" and oldname == "":
                username, name, password, permissionmaster, permissionrelease, permissionentry = self.entry_username.get(), self.entry_name.get(), self.entry_passwordcont.get(), "F", "F", "F"
                self.contscursor.execute("INSERT INTO Conts (username, name, password, permissionmaster, permissionrelease, permissionentry) VALUES (?, ?, ?, ?, ?, ?)",(username, name, password, permissionmaster, permissionrelease, permissionentry))
            elif temp == "":
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

            mainimgs = [ctk.CTkImage(Image.open("imgs/caixa.png"), size=(60,60)), ctk.CTkImage(Image.open("imgs/relogio.png"), size=(60,60)), ctk.CTkImage(Image.open("imgs/tables.png"), size=(60,60)), ctk.CTkImage(Image.open("imgs/clientes.png"), size=(60,60)), ctk.CTkImage(Image.open("imgs/trofeu.png"), size=(60,60)), ctk.CTkImage(Image.open("imgs/relogio.png"), size=(60,60)), ctk.CTkImage(Image.open("imgs/garçom.png"), size=(60,60))]
            
            mainbuttons = [[ctk.CTkButton(master= self.frame_tab), "ABRIR OU FECHAR CAIXA"], [ctk.CTkButton(master= self.frame_tab), "HISTÓRICO DO CAIXA"], [ctk.CTkButton(master= self.frame_tab, command=self.mainwindow), "MESAS / COMANDAS"], [ctk.CTkButton(master= self.frame_tab), "CLIENTES"], [ctk.CTkButton(master= self.frame_tab), "MAIS VENDIDOS"], [ctk.CTkButton(master= self.frame_tab), "HISTÓRICO DE PEDIDOS"], [ctk.CTkButton(master= self.frame_tab), "RANKING DE ATENDIMENTOS"]]
            
            self.currentmain = mainbuttons
            self.currentimgs = mainimgs
        elif text == "PRODUTO":
            productimgs = [ctk.CTkImage(Image.open("imgs/produtos.png"), size=(60,60)), ctk.CTkImage(Image.open("imgs/complementos.png"), size=(60,60)), ctk.CTkImage(Image.open("imgs/anotacoes.jpg"), size=(60,60)), ctk.CTkImage(Image.open("imgs/tiposetamanhos.png"), size=(60,60)), ctk.CTkImage(Image.open("imgs/categorias.jpg"), size=(60,60)), ctk.CTkImage(Image.open("imgs/promocoes.png"), size=(60,60))]
            
            productbuttons = [[ctk.CTkButton(master= self.frame_tab, command=self.productswindow), "PRODUTOS"], [ctk.CTkButton(master= self.frame_tab), "COMPLEMENTOS"], [ctk.CTkButton(master= self.frame_tab), "ANOTAÇÕES"], [ctk.CTkButton(master= self.frame_tab), "TIPOS E TAMANHOS"], [ctk.CTkButton(master= self.frame_tab, command=self.categorieswindow), "CATEGORIAS"], [ctk.CTkButton(master= self.frame_tab), "PROMOÇÕES"], ]
            
            self.currentmain = productbuttons
            self.currentimgs = productimgs
        elif text == "CONFIGURAÇÕES":  
            configimgs = [ctk.CTkImage(Image.open("imgs/config.png"), size=(60,60)), ctk.CTkImage(Image.open("imgs/garçom.png"), size=(60,60))]
            configbuttons = [[ctk.CTkButton(master=self.frame_tab), "CONFIGURAÇÕES"], [ctk.CTkButton(master=self.frame_tab, command=self.functionarywindow), "FUNCIONÁRIOS"]]

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
    def connectconfig(self):
        self.config = sql.connect("config.db")
        self.configcursor = self.config.cursor()
    def desconnectconfig(self):
        self.config.commit()
        self.config.close()
    def createtables(self):
        self.connectconfig()
        self.configcursor.execute("""CREATE TABLE IF NOT EXISTS Config(
                                  cod INTEGER PRIMARY KEY,
                                  stylemode VARCHAR,
                                  maxcommands INTEGER(4)
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
                                    size VARCHAR(30)
                                    )""")
        self.desconnectcommands()
        self.connectproduct()
        self.productcursor.execute("""CREATE TABLE IF NOT EXISTS Products(
                                   name VARCHAR(30),
                                   type VARCHAR(10),
                                   category VARCHAR(10),
                                   price VARCHAR(8)
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
                                    waiter VARCHAR(30),
                                    price VARCHAR(8),
                                    unitprice VARCHAR(8),
                                    quantity INTERGER(3),
                                    product VARCHAR(30),
                                    type VARCHAR(30),
                                    size VARCHAR(30),
                                    datefinish VARCHAR(16)

                                    )""")
        self.desconnecthistory()

application() 