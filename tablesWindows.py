from table import table as tableClass
from customtkinter import CTkButton, CTkLabel, CTkImage
from PIL import Image

class tablesWindows():
    def __init__(self, master, db:str, table:str, columnsname = ("*", ), where:tuple = (), values:tuple = (), bgcolor:str="", placeholder_color:str=""):
        self.master = master
        self.where = where
        self.columnsname = columnsname
        self.values = values
        self.table = tableClass(db, table)
        self.bgcolor = bgcolor
        self.placeholder_color = placeholder_color
    def create(self, columns:tuple= (), widthColumns:tuple = (), heightColumns:tuple= (), editdata= (), deldata=()):
        self.content = []
        self.columns = columns
        self.widthColumns = widthColumns
        self.heightColumns = heightColumns
        self.editdata = editdata
        self.deldata = deldata
        listen = self.table.getData(self.columnsname, self.where, self.values)
        listen.insert(0, columns)
        self.listenValues = list(listen)
        print(listen)
        for contentid in range(len(listen)):
            self.addRow(listen[contentid], contentid)
                
    def addRow(self, content, cod):
        images = {"edit":CTkImage(Image.open("./imgs/pencil.jpg"), size=(40,40)), "del": CTkImage(Image.open("./imgs/lixeira.png"), size=(40,40))}
        self.content.append([])
        for i in range(len(content)):
            self.content[cod].append(CTkLabel(self.master, width=self.widthColumns[i], height=self.heightColumns[i], bg_color=self.bgcolor, text=content[i]))
            print(cod)
            print(i)
            self.content[cod][i].grid(row=cod, column=i, padx=1, pady=1)
        num = len(self.content[cod])
        if self.editdata != ():
            self.content[cod].append(CTkButton(self.master, width=50, height=self.heightColumns[i], fg_color=self.bgcolor, text="", image=images["edit"], command=lambda cod=cod:self.editCommand(cod), hover=False))
            self.content[cod][num].grid(row=cod, column=num, padx=1, pady=1)
            num += 1
        if self.deldata != ():
            self.content[cod].append(CTkButton(self.master, width=50, height=self.heightColumns[i], fg_color=self.bgcolor, text="", image=images["del"], command=lambda cod=cod:self.delCommand(cod), hover=False))
            self.content[cod][num].grid(row=cod, column=num, padx=1, pady=1)
    def editCommand(self, cod):
        print()
        if self.editdata[1] == "TABLE":
            if self.editdata[2] != "":
                self.editdata[0](self.listenValues[cod][self.editdata[2]])
                return
            self.editdata[0](self.listenValues[cod])
    def delCommand(self, cod):
        if self.deldata[1] == "TABLE":
            if self.deldata[2] != "":
                self.deldata[0](self.listenValues[cod][self.deldata[2]])
                return
            self.deldata[0](self.listenValues[cod])
    def getTable(self, ):
        return self.listenValues
    def reload(self, where:tuple = (), values:tuple = ()):
        newcontent = self.table.getData(self.columnsname, where, values)
        print(newcontent)
        num = len(self.content) - 1
        maxx = max(num, len(newcontent))
        newcontent.insert(0, self.columns)
        self.listenValues = list(newcontent)
        for contentid in range(maxx):
            print(contentid)
            print(num)
            if contentid <= num:
                try:
                    for columnid in range(len(self.columns)):
                        self.content[contentid][columnid].configure(text = newcontent[contentid][columnid])

                except:
                    self.deleteRow(contentid)
                    break
            else:
                print('oiii')
                self.addRow(newcontent[contentid], contentid)
        
    def deleteRow(self, rowid):
        for i in range(len(self.content)):
            if i >= rowid:
                for j in self.content[i]:
                    j.destroy()

    def delete(self, ):
        for i in self.content:
            for j in i:
                j.destroy()
        self.currentTable.place_forget()