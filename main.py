import tkinter as tk
import socket
import customtkinter as ctk
import sqlite3 as sql
from PIL import Image
import threading
import pyautogui as pa
import datetime

#class funcs():



class application():
    def __init__(self):
        self.positionp = True
        self.cod, self.stylemode, self.maxcommands = "", "", ""
        mod, up = False, False
        self.createtables()
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
        self.desconnectconfig()
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.loginwindow()

        self.root.mainloop()
    def loginwindow(self):

        self.root.attributes("-fullscreen", True)
        self.entry_name = ctk.CTkEntry(self.root, bg_color="#7f7f7f", placeholder_text="NOME", font=("Arial", 20))
        self.entry_name.place(relx=0.4, rely=0.45, relwidth=0.2, relheight=0.05)

        self.entry_password = ctk.CTkEntry(self.root, bg_color="#7f7f7f", placeholder_text="SENHA", show="*", font=("Arial", 20))
        self.entry_password.place(relx=0.4, rely=0.55, relwidth=0.2, relheight=0.05)
        
        self.button_login = ctk.CTkButton(self.root, fg_color="#7f7f7f", text="LOGIN", hover_color="#6f6f6f", command=self.login, font=("Arial", 20))
        self.button_login.place(relx=0.4, rely=0.65, relwidth=0.2, relheight=0.05)
        

        self.personimg = ctk.CTkImage(Image.open("imgs/person.png"), size=(300,300))
        self.label_person = ctk.CTkLabel(self.root, image = self.personimg, bg_color="#242424", text="")
        self.label_person.place(relx=0.423, rely=0.15)

        self.button_temp = ctk.CTkButton(self.root, fg_color="#7f7f7f", text="add cont", hover_color="#6f6f6f", command=self.addcont)
        self.button_temp.place(relx=0.8, rely=0.95, relwidth=0.2, relheight=0.05)
        self.root.bind("<KeyPress>", self.keypresslogin)
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
    def mainwindow(self):
        self.entry_name.destroy(); self.entry_password.destroy(); self.button_login.destroy(); self.button_temp.destroy(); self.label_person.destroy()
        del self.personimg
        try:
            self.label_failedlogin.destroy()
        except:
            pass
        self.frame_tab = ctk.CTkFrame(self.root, fg_color="#5f5f5f", border_color="#1f1f1f")
        self.frame_tab.place(relx=0, rely=0, relwidth=1, relheight=0.14)


        self.label_none = ctk.CTkLabel(self.frame_tab, fg_color="#585858", text="")
        self.label_none.place(relx=0.2, rely=0, relwidth=0.8, relheight=0.285)

        self.button_main = ctk.CTkButton(self.frame_tab, text="PRINCIPAL", hover_color="#484848", fg_color="#4f4f4f", command=lambda:self.changemainbuttons(self.button_main))
        self.button_main.place(relx=0, rely=0, relwidth=0.1, relheight=0.285)

        self.button_product = ctk.CTkButton(self.frame_tab, text="PRODUTO", hover_color="#484848", fg_color="#4f4f4f", command=lambda:self.changemainbuttons(self.button_product))
        self.button_product.place(relx=0.1, rely=0, relwidth=0.1, relheight=0.285)

        self.button_config = ctk.CTkButton(self.frame_tab, text="CONFIGURAÇÕES", hover_color="#484848", fg_color="#4f4f4f", command=lambda:self.changemainbuttons(self.button_config))
        self.button_config.place(relx=0.2, rely=0, relwidth=0.1, relheight=0.285)


        self.str_searchcommands = tk.StringVar()
        self.str_searchcommands.set("")
        self.label_searchcommand = ctk.CTkLabel(self.root, fg_color="#2f2f2f", textvariable=self.str_searchcommands, font=("Arial", 20))
        self.label_searchcommand.place(relx=0.01, rely=0.15, relwidth=0.88, relheight=0.05)

        self.button_addcommand = ctk.CTkButton(self.root, fg_color="#3f3f3f", text="ADICIONAR COMANDA", hover_color="#383838", command=self.newcommands)
        self.button_addcommand.place(relx=0.90, rely=0.15, relwidth=0.09, relheight=0.05)
        
        self.root.bind("<KeyPress>", self.presskey)

        self.frame_commands = ctk.CTkScrollableFrame(self.root, fg_color="#2f2f2f")
        self.frame_commands.place(relx=0.01, rely=0.21, relwidth=0.98, relheight=0.71)

        

        self.frame_down = ctk.CTkFrame(self.root, fg_color="#3f3f3f", border_color="#1f1f1f")
        self.frame_down.place(relx=0, rely=0.93, relwidth=1, relheight=0.07)

        self.entry_namecommand = ctk.CTkEntry(self.frame_down, placeholder_text="PESQUISAR POR NOME", fg_color="#5f5f5f", font=("Arial", 20))
        self.entry_namecommand.place(relx=0.3, rely=0.175 , relwidth=0.15, relheight=0.65)

        self.button_updatecommand = ctk.CTkButton(self.frame_down, fg_color="#5f5f5f", text="ATUALIZAR", hover_color="#585858")
        self.button_updatecommand.place(relx=0.02, rely=0.175, relwidth=0.1, relheight=0.65)

        self.button_mergecommands = ctk.CTkButton(self.frame_down, fg_color="#5f5f5f", text="JUNTAR COMANDAS", hover_color="#585858")
        self.button_mergecommands.place(relx=0.135, rely=0.175, relwidth=0.15, relheight=0.65)

        self.root.after(500, self.searchnameentry)

        self.root.bind_all("<Button-1>", self.click)
        threading.Thread(self.reloadcommands()).start()
        print("começou")
    def windowcommand(self, command):
        self.rootcommand = ctk.CTkToplevel()
        text = command.cget("text")
        num = ""
        for i in text:
            if i == " ":
                break
            num = num + i
        self.rootcommand.title("COMANDA " + num)
        self.rootcommand.geometry("500x700")
        self.rootcommand.resizable(True, True)
        self.rootcommand.transient(self.root)
        self.rootcommand.grab_set()
        



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
            datenow = str(datetime.datetime.now())[0:19]
            secondnow, minnow, hournow, daynow, mounthnow, yearnow = int(datenow[17:19]), int(datenow[14:16]), int(datenow[11:13]), int(datenow[8:10]), int(datenow[5:7]), int(datenow
            [0:4])

            second, min, hour, day, mounth, year = int(inithour[6:8]), int(inithour[3:5]), int(inithour[0:2]), int(initdate[8:10]), int(initdate[5:7]), int(initdate[0:4]) 
            time = str(hournow - hour) +"h" + str(minnow - min) + "m"
            self.currentcommands.append(ctk.CTkButton(self.frame_commands,fg_color="#3f3f3f", command=lambda m = number:self.windowcommand(self.currentcommands[m]), hover=False, width=250, height= 150, text= str(number) + " "+ nameclient +"\n" + "TEMPO: " + time, font=("Arial", 15)))
            self.currentcommands[i].grid(row=int(i/6), column=i%6, padx=10, pady=5)
            self.number.append(number)
        print("terminou")
        
        self.desconnectcommands()
    def newcommands (self):
        self.rootnewcom = ctk.CTkToplevel()
        self.rootnewcom.title("ADICIONAR COMANDA")
        #self.rootnewcom.iconbitmap('imagens\Icon.ico')
        self.rootnewcom.geometry("800x600")
        self.rootnewcom.resizable(True, True)
        self.rootnewcom.transient(self.root)
        self.rootnewcom.grab_set()
        self.frame_newcommands = ctk.CTkScrollableFrame(master=self.rootnewcom, fg_color="#2f2f2f")
        self.frame_newcommands.place(relx=0.01, rely=0.01, relwidth= 0.98, relheight= 0.98)
        commandsactives = []
        try:
            for i in self.button_newcommand:
                i.destroy()
        except:
            pass
        self.button_newcommand = []
        threading.Thread(self.addnewcommandwindow()).start()
    def addnewcommandactive(self, command):
        num = command.cget("text")
        self.connectcommands()
        number = ""
        com = self.commandscursor.execute("""SELECT number FROM CommandsActive WHERE number = ?""", (num, ))
        for i in com:
            number = i
        if number == "":
            date = datetime.datetime.now()
            date = str(date)[0:19]
            date, hour = date[0:10], date[11:20]
            nameclient = ""
            idclient = ""
            self.commandscursor.execute("""INSERT INTO CommandsActive (number, initdate, hour, nameclient, idclient) VALUES (?, ?, ?, ?, ?)""", (num, date, hour, nameclient, idclient))
            self.rootnewcom.destroy()
        self.desconnectcommands()
        threading.Thread(self.reloadcommands()).start()
    def addnewcommandwindow(self):
        for i in range(int(self.maxcommands)):
            k = False
            for m in self.number:
                if m == i + 1:
                    print(m)
                    k = True
            self.button_newcommand.append(ctk.CTkButton(self.frame_newcommands, command=lambda m=i:self.addnewcommandactive(self.button_newcommand[m]), fg_color="#006f00", text=str(i+ 1), font=("Arial", 15), width=150, height=75))
            if k == True:
                self.button_newcommand[i].configure(fg_color="#6f0000", hover_color="#4f0000")
            self.button_newcommand[i].grid(row=int(i/4), column=i%4, padx=10 ,pady=10)
        
    def click(self, event):
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
    def presskey(self, event):
        key = event.keysym
        n = self.entry_namecommand.get()
        if n == "":
            if key == "0" or key == "1" or key == "2" or key == "3" or key == "4" or key == "5" or key == "6" or key == "7" or key == "8" or key == "9":
                self.changesearchcommandlabel(key)
            elif key == "Return":
                self.changesearchcommandlabel()
            elif key == "BackSpace":
                self.changesearchcommandlabel("o")
            else:
                self.changesearchcommandlabel()
        elif key == "Delete":
            self.entry_namecommand.delete(0, "end")
    def changesearchcommandlabel(self, a = ""):
        i = self.str_searchcommands.get()
        if a != "" and a != "o":
            self.str_searchcommands.set(i + a)
        elif a == "o":
            self.str_searchcommands.set(i[0:-1])
        else:
            self.str_searchcommands.set("")
    def changemainbuttons(self, button):
        
        
        
        self.button_main.configure(fg_color="#5f5f5f", hover_color="#4f4f4f")
        self.button_product.configure(fg_color="#5f5f5f", hover_color="#4f4f4f")
        self.button_config.configure(fg_color="#5f5f5f", hover_color="#4f4f4f")
        button.configure(fg_color="#484848", hover_color="#484848")
        text = button.cget("text")
        
        try:
            for i in self.currentmain:
                buttontemp, texttemp = i
                buttontemp.destroy()
        except:
            pass
        if text == "PRINCIPAL":

            mainimgs = [ctk.CTkImage(Image.open("imgs/caixa.png"), size=(60,60)), ctk.CTkImage(Image.open("imgs/relogio.png"), size=(60,60)), ctk.CTkImage(Image.open("imgs/tables.png"), size=(60,60)), ctk.CTkImage(Image.open("imgs/clientes.png"), size=(60,60)), ctk.CTkImage(Image.open("imgs/trofeu.png"), size=(60,60)), ctk.CTkImage(Image.open("imgs/relogio.png"), size=(60,60)), ctk.CTkImage(Image.open("imgs/garçom.png"), size=(60,60))]
            
            mainbuttons = [[ctk.CTkButton(master= self.frame_tab), "ABRIR OU FECHAR CAIXA"], [ctk.CTkButton(master= self.frame_tab), "HISTÓRICO DO CAIXA"], [ctk.CTkButton(master= self.frame_tab), "MESAS / COMANDAS"], [ctk.CTkButton(master= self.frame_tab), "CLIENTES"], [ctk.CTkButton(master= self.frame_tab), "MAIS VENDIDOS"], [ctk.CTkButton(master= self.frame_tab), "HISTÓRICO DE PEDIDOS"], [ctk.CTkButton(master= self.frame_tab), "RANKING DE ATENDIMENTOS"]]
            
            self.currentmain = mainbuttons
            self.currentimgs = mainimgs
        elif text == "PRODUTO":
            productimgs = [ctk.CTkImage(Image.open("imgs/produtos.png"), size=(60,60)), ctk.CTkImage(Image.open("imgs/complementos.png"), size=(60,60)), ctk.CTkImage(Image.open("imgs/anotacoes.jpg"), size=(60,60)), ctk.CTkImage(Image.open("imgs/tiposetamanhos.png"), size=(60,60)), ctk.CTkImage(Image.open("imgs/categorias.jpg"), size=(60,60)), ctk.CTkImage(Image.open("imgs/promocoes.png"), size=(60,60))]
            
            productbuttons = [[ctk.CTkButton(master= self.frame_tab), "PRODUTOS"], [ctk.CTkButton(master= self.frame_tab), "COMPLEMENTOS"], [ctk.CTkButton(master= self.frame_tab), "ANOTAÇÕES"], [ctk.CTkButton(master= self.frame_tab), "TIPOS E TAMANHOS"], [ctk.CTkButton(master= self.frame_tab), "CATEGORIAS"], [ctk.CTkButton(master= self.frame_tab), "PROMOÇÕES"], ]
            
            self.currentmain = productbuttons
            self.currentimgs = productimgs
        elif text == "CONFIGURAÇÕES":
            pass
        for i, m in enumerate(self.currentmain):
            buttontemp, texttemp = m
            buttontemp.configure(text=texttemp, fg_color="#484848", hover_color="#383838", image=self.currentimgs[i], compound="top", anchor="bottom")
            buttontemp.place(relx=0.1*i, rely=0.285, relwidth=0.1, relheight=0.715)
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
    def addcont(self):
        self.connectconts()
        name = "Gabriel"
        password = "sim123"
        permissionmaster = "Y"
        self.contscursor.execute("""INSERT INTO Conts (name, password, permissionmaster) VALUES (?, ?, ?)""", (name, password, permissionmaster))
        self.desconnectconts()
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
                                 name VARCHAR(30) NOT NULL,
                                 password VARCHAR(30) NOT NULL,
                                 permissionmaster CHAR(1) NOT NULL)""")
        self.desconnectconts()
        self.connectcommands()
        self.commandscursor.execute("""CREATE TABLE IF NOT EXISTS CommandsActive(
                                    number INTEGER PRIMARY KEY,
                                    initdate CHAR(10),
                                    hour CHAR(5),
                                    nameclient VARCHAR(30),
                                    idclient INTEGER(5)
                                    )""")
        self.desconnectcommands()
application()
