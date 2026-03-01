from table import table as tableClass
from customtkinter import CTkButton, CTkLabel, CTkImage, CTkScrollableFrame
from PIL import Image
from colorsList import getColors

class tablesWindows():
    def __init__(self, master, tableLocal:tuple, db:str, table:str, columnsname = ("*", ), where:tuple = (), values:tuple = (), bgcolor:str="", placeholder_color:str=""):
        self.where = where
        self.tableLocal = tableLocal
        self.columnsname = columnsname
        self.values = values
        self.table = tableClass(db, table)
        self.bgcolor = bgcolor
        if bgcolor == "":
            self.bgcolor = getColors()
        self.placeholder_color = placeholder_color
        self.frame = CTkScrollableFrame(master)
    def create(self, columns:tuple= ((), ()), widthColumns:tuple = (), heightColumns:tuple= (), editdata= (None, None, ""), deldata=(None, None, ""), reloadfunc=(None, None)):
        self.content = []
        self.columns = columns
        self.reloadFunc = reloadfunc
        self.frame.place(relx=self.tableLocal[0], rely=self.tableLocal[1], relwidth=self.tableLocal[2], relheight=self.tableLocal[3])
        self.widthColumns = widthColumns
        self.heightColumns = heightColumns
        self.editdata = editdata
        self.deldata = deldata
        self.addRow(columns[0], 0, True, True)
        
        self.reload()
    def addRow(self, content, cod, editHead = False, delHead = False):
        images = {"edit":CTkImage(Image.open("./imgs/pencil.jpg"), size=(40,40)), "del": CTkImage(Image.open("./imgs/lixeira.png"), size=(40,40))}
        self.content.append([])
        for i in range(len(content)):
            self.content[cod].append(CTkLabel(self.frame, width=self.widthColumns[i], height=self.heightColumns[i], bg_color=self.bgcolor[4], text=content[i]))
            self.content[cod][i].grid(row=cod, column=i, padx=1, pady=1)
        num = len(self.content[cod])
        if self.editdata != (None, None, ""):
            if editHead:
                self.content[cod].append(CTkLabel(self.frame, width=60, height=self.heightColumns[i], fg_color=self.bgcolor[4], text="Editar"))
                self.content[cod][num].grid(row=cod, column=num, padx=1, pady=1)
            else:
                self.content[cod].append(CTkButton(self.frame, width=60, height=self.heightColumns[i], fg_color=self.bgcolor[4], text="", image=images["edit"], command=lambda cod=cod:self.editCommand(cod), hover=False))
                self.content[cod][num].grid(row=cod, column=num, padx=1, pady=1)
            num += 1
        if self.deldata != (None, None, ""):
            if delHead:
                self.content[cod].append(CTkLabel(self.frame, width=60, height=self.heightColumns[i], fg_color=self.bgcolor[4], text="Excluir"))
                self.content[cod][num].grid(row=cod, column=num, padx=1, pady=1)
            else:
                self.content[cod].append(CTkButton(self.frame, width=60, height=self.heightColumns[i], fg_color=self.bgcolor[4], text="", image=images["del"], command=lambda cod=cod:self.delCommand(cod), hover=False))
                self.content[cod][num].grid(row=cod, column=num, padx=1, pady=1)
    def editCommand(self, cod):
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
        if where == ():
            where, values = self.where, self.values
        newcontent = self.table.getData(self.columnsname, where, values)
        if newcontent == "NULL":
            newcontent = ()
        num = len(self.content) - 1
        maxx = max(num, len(newcontent))
        self.listenValues = list(newcontent)
        for contentid in range(1, maxx):
            if contentid < num:
                for i in self.content[contentid]:
                    print(i.cget("text"))
                    print(newcontent[contentid])
                try:
                    for columnid in range(len(self.columns[0])):
                        print(contentid)
                        print(columnid)
                        print(newcontent[contentid][self.columns[1][columnid]])
                        self.content[contentid][columnid].configure(text = newcontent[contentid][self.columns[1][columnid]])

                except:
                    self.deleteRow(contentid)
                    break
            else:
                new = []
                for i in range(len(self.columns[1])):
                    new.append(newcontent[contentid][self.columns[1][i]])
                print("oii")
                self.addRow(new, contentid)
        print("aqui")
        if self.reloadFunc[0]:
            print(self.listenValues)
            print(self.reloadFunc[1])
            self.reloadFunc[0](self.listenValues, self.reloadFunc[1])
    def deleteRow(self, rowid):
        for i in self.content[rowid:]:
            for j in i:
                j.destroy()