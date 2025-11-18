from customtkinter import CTkEntry, CTkButton, CTkImage, CTkLabel
from tabchange import changeTabsButtons
from table import table
from PIL import Image
from colorsList import getColors
class loginTab():
    def login(self):
        name = self.entry_name.get()
        password = self.entry_password.get()
        contsTable = table("contas", "Conts")
        try:
            data = contsTable.getData(("name", "password", "permissionmaster"), ("name", ), (name, ))
            namedata, passworddata, permissionmasterdata = data[0]
            if password != passworddata or name != namedata or name == "" or password == "":
                raise Exception("NOME OU SENHA INCORRETOS")
            elif permissionmasterdata != "Y" and passworddata == password:
                raise Exception("ESSE USUÁRIO NÃO TEM PERMISSÃO")
                
        except Exception as error:
            try:
                self.label_failedlogin.destroy()
            except:
                pass
            self.label_failedlogin = CTkLabel(self.root, text=error, font=("Arial", 18))
            self.label_failedlogin.place(relx=0.4, rely=0.70, relwidth=0.2, relheight=0.05)
        if passworddata == password and permissionmasterdata == "Y" and name == namedata:
            print("login efetuado")
            self.entry_name.destroy(); self.entry_password.destroy(); self.button_login.destroy(); self.label_person.destroy()
            self.namelogin = namedata
            self.passwordlogin = passworddata
            self.permissionmaster = permissionmasterdata
            changeTabsButtons(self.root)
    def keypresslogin(self, event):
        n = event.keysym
        if n == "Return":
            self.login()
    def __init__(self, root):
        self.currentwindow = "LOGIN"
        self.colors = getColors()
        self.root = root
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()
        print(self.height)

        self.entry_name = CTkEntry(self.root, bg_color=self.colors[9], placeholder_text="NOME", font=("Arial", 20))
        self.entry_name.place(relx=0.4, rely=0.45, relwidth=0.2, relheight=0.05)

        self.entry_password = CTkEntry(self.root, bg_color=self.colors[9], placeholder_text="SENHA", show="*", font=("Arial", 20))
        self.entry_password.place(relx=0.4, rely=0.55, relwidth=0.2, relheight=0.05)
        
        self.button_login = CTkButton(self.root, fg_color=self.colors[9], text="LOGIN", hover_color=self.colors[8], command=self.login, font=("Arial", 20))
        self.button_login.place(relx=0.4, rely=0.65, relwidth=0.2, relheight=0.05)
        
        print(self.height//3.6)
        self.personimg = CTkImage(Image.open("./imgs/person.png"), size=(self.height//3.6,self.height//3.6))
        self.label_person = CTkLabel(self.root, image = self.personimg, bg_color="#242424", text="")
        self.label_person.place(relx=0.423, rely=0.15)
        temp = ""
        conts_table = table("contas", "Conts")
        if conts_table.getData() == "NULL":
            conts_table.insertData(("username", "name", "password", "permissionmaster", "permissionrelease", "permissionentry", "permissionclose"), ("ADMIN", "Admin", "ADMIN", "Y", "Y", "Y", "Y"))
        self.root.bind("<KeyPress>", self.keypresslogin)