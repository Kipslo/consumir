import tkinter as tk
import socket
import customtkinter as ctk
import sqlite3 as sql
from PIL import Image
import threading

#class funcs():



class application():
    def __init__(self):
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.loginwindow()
        self.createtables()

        self.root.mainloop()
    def loginwindow(self):

        self.root.attributes("-fullscreen", True)
        self.entry_name = ctk.CTkEntry(self.root, bg_color="#7f7f7f", placeholder_text="NOME")
        self.entry_name.place(relx=0.4, rely=0.45, relwidth=0.2, relheight=0.05)

        self.entry_password = ctk.CTkEntry(self.root, bg_color="#7f7f7f", placeholder_text="SENHA", show="*")
        self.entry_password.place(relx=0.4, rely=0.55, relwidth=0.2, relheight=0.05)
        
        self.button_login = ctk.CTkButton(self.root, fg_color="#7f7f7f", text="LOGIN", hover_color="#6f6f6f", command=self.login)
        self.button_login.place(relx=0.4, rely=0.65, relwidth=0.2, relheight=0.05)
        

        self.personimg = ctk.CTkImage(Image.open("imgs/person.png"), size=(300,300))
        self.label_person = ctk.CTkLabel(self.root, image = self.personimg, bg_color="#242424", text="")
        self.label_person.place(relx=0.423, rely=0.15)

        self.button_temp = ctk.CTkButton(self.root, fg_color="#7f7f7f", text="add cont", hover_color="#6f6f6f", command=self.addcont)
        self.button_temp.place(relx=0.8, rely=0.95, relwidth=0.2, relheight=0.05)
    def mainwindow(self):
        self.entry_name.destroy(); self.entry_password.destroy(); self.button_login.destroy(); self.button_temp.destroy(); self.label_person.destroy()
        del self.personimg
        try:
            self.label_failedlogin.destroy()
        except:
            pass
        self.frame_tab = ctk.CTkFrame(self.root, fg_color="#383838", border_color="#1f1f1f")
        self.frame_tab.place(relx=0, rely=0, relwidth=1, relheight=0.14)

        self.label_none = ctk.CTkLabel(self.frame_tab, fg_color="#585858", text="")
        self.label_none.place(relx=0.2, rely=0, relwidth=0.8, relheight=0.285)

        self.button_main = ctk.CTkButton(self.frame_tab, text="PRINCIPAL", hover_color="#484848", fg_color="#4f4f4f", command=lambda:self.changemainbutton(self.button_main))
        self.button_main.place(relx=0, rely=0, relwidth=0.1, relheight=0.285)
        self.button_product = ctk.CTkButton(self.frame_tab, text="PRODUTO", hover_color="#484848", fg_color="#4f4f4f", command=lambda:self.changemainbutton(self.button_product))
        self.button_product.place(relx=0.1, rely=0, relwidth=0.1, relheight=0.285)

        print("alternando tela")
    def changemainbutton(self, button):
        mainimgs = [tk.PhotoImage("imgs/caixa.png"), tk.PhotoImage("imgs/relógio.png"), tk.PhotoImage("imgs/tables.png"),tk.PhotoImage("img/garçom.png"), tk.PhotoImage("imgs/troféu.png"), tk.PhotoImage("imgs/relógio.png"), tk.PhotoImage("imgs/garçom.png")]
        #productimgs = [tk.PhotoImage(""), tk.PhotoImage("")]
        mainbuttons = [[ctk.CTkButton(master= self.frame_tab, image= mainimgs[0]), "ABRIR OU FECHAR CAIXA"], []]
        #productbuttons = [ctk.CTkButton(master= self.frame_tab, image= productimgs[0]), ]
        self.button_main.configure(fg_color="#4f4f4f", hover_color="#3f3f3f")
        self.button_product.configure(fg_color="#4f4f4f", hover_color="#3f3f3f")
        button.configure(fg_color="#383838", hover_color="#383838")
        text = button.text()
        print(text)
    def login(self):
        name = self.entry_name.get()
        password = self.entry_password.get()
        self.connectconts()
        try:
            data = self.contscursor.execute("""SELECT * FROM Conts WHERE name = ?""", (name, ))
            namedata = ""
            passworddata = ""
            permissionmasterdata = ""
            for i in data:
                namedata, passworddata, permissionmasterdata = i
            
            
            if password != passworddata or name != namedata or name == "" or password == "":
                raise Exception("NOME OU SENHA INCORRETOS")
            elif permissionmasterdata == "N" and passworddata == password:
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
            self.mainwindow()
        self.desconnectconts()
    def connectconts(self):
        self.conts = sql.connect("sql.db")
        self.contscursor = self.conts.cursor()
    def desconnectconts(self):
        self.conts.commit()
        self.conts.close()
    def addcont(self):
        self.connectconts()
        name = "Gabriel"
        password = "sim123"
        permissionmaster = "Y"
        self.contscursor.execute("""INSERT INTO Conts (name, password, permissionmaster) VALUES (?, ?, ?)""", (name, password, permissionmaster))
        self.desconnectconts()
    def createtables(self):
        self.connectconts()
        self.contscursor.execute("""CREATE TABLE IF NOT EXISTS Conts(
                                 name VARCHAR(30) NOT NULL,
                                 password VARCHAR(30) NOT NULL,
                                 permissionmaster CHAR(1) NOT NULL)""")
        self.desconnectconts()
        
application()
