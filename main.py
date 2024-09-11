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
        self.initwindow()
        self.createtables()

        self.root.mainloop()
    def initwindow(self):

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

    def login(self):
        name = self.entry_name.get()
        password = self.entry_password.get()
        self.connectconts()
        try:
            data = self.contscursor.execute("""SELECT * FROM Conts WHERE name = ?""", (name, ))
            passworddata = ""
            permissionmasterdata = ""
            for i in data:
                namedata, passworddata, permissionmasterdata = i
                print(namedata)
                print(passworddata)
                print(permissionmasterdata)
            if passworddata == password and permissionmasterdata == "Y":
                print("login efetuado")
            else:
                raise Exception("nome ou senha incorretos")
        except Exception as error:
            print(error)
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
        password = 12345678910
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
