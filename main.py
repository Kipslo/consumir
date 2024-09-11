import tkinter as tk
import socket
import customtkinter as ctk
import sqlite3 as sql

#class funcs():



class application():
    def __init__(self):
        self.root = tk.Tk()
        self.initwindow()


        self.root.mainloop()
    def initwindow(self):
        self.root.attributes("-fullscreen", True)
        self.root.configure(background="#1f1f1f")

    def connectconts(self):
        self.conts = sql.connect("sql.db")
        self.contscursor = self.conts.cursor()

    def desconnectconts(self):
        self.conts.close()

    def createtables(self):
        self.contscursor.execute("""CREATE TABLE IF NOT EXISTS Conts(
                                 name VARCHAR(30) NOT NULL,
                                 password VARCHAR(30) NOT NULL,
                                 
                                 
                                 
                                 
                                 )""")
        
application()
