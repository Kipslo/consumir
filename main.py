import tkinter as tk
import socket
import customtkinter as ctk
import sqlite3 as sql
from PIL import Image
#class funcs():



class application():
    def __init__(self):
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.initwindow()


        self.root.mainloop()
    def initwindow(self):

        self.root.attributes("-fullscreen", True)
        self.entry_name = ctk.CTkEntry(self.root, bg_color="#5f5f5f", placeholder_text="NOME")
        self.entry_name.place(relx=0.4, rely=0.45, relwidth=0.2, relheight=0.05)

        self.entry_password = ctk.CTkEntry(self.root, bg_color="#5f5f5f", placeholder_text="SENHA", show="*")
        self.entry_password.place(relx=0.4, rely=0.55, relwidth=0.2, relheight=0.05)
        
        self.button_login = ctk.CTkButton(self.root, fg_color="#5f5f5f", text="LOGIN", hover_color="#4f4f4f")
        self.button_login.place(relx=0.4, rely=0.65, relwidth=0.2, relheight=0.05)
        

        self.personimg = ctk.CTkImage(Image.open("imgs/person.png"), size=(300,300))
        self.label_person = ctk.CTkLabel(self.root, image = self.personimg, bg_color="#242424", text="")
        self.label_person.place(relx=0.423, rely=0.15)


    def connectconts(self):
        self.conts = sql.connect("sql.db")
        self.contscursor = self.conts.cursor()

    def desconnectconts(self):
        self.conts.commit()
        self.conts.close()

    def addcont(self):
        self.connectconts()
        self.contscursor.execute("""INSERT INTO Conts (name, password, permissionmaster) VALUES (Gabriel, 12345678910, Y)""")
        self.desconnectconts()
    def createtables(self):
        self.contscursor.execute("""CREATE TABLE IF NOT EXISTS Conts(
                                 name VARCHAR(30) NOT NULL,
                                 password VARCHAR(30) NOT NULL,
                                 permissionmaster CHAR(1) NOT NULL,
                                 
                                 
                                 
                                 )""")
        
application()
