from table import table as tableClass
from customtkinter import CTkButton, CTkLabel, CTkImage, CTkScrollableFrame
from PIL import Image

class tablesWindows():
    def __init__(self, master, tableLocal:tuple, db:str, table:str, columnsname = ("*", ), where:tuple = (), values:tuple = (), bgcolor:str="", placeholder_color:str=""):
        self.where = where
        self.tableLocal = tableLocal
        self.columnsname = columnsname
        self.values = values
        self.table = tableClass(db, table)
        self.bgcolor = bgcolor
        self.placeholder_color = placeholder_color
        self.frame = CTkScrollableFrame(master)
    def create(self, columns:tuple= ((), ()), widthColumns:tuple = (), heightColumns:tuple= (), editdata= (None, None, ""), deldata=(None, None, "")):
        self.content = []
        self.columns = columns
        self.frame.place(relx=self.tableLocal[0], rely=self.tableLocal[1], relwidth=self.tableLocal[2], relheight=self.tableLocal[3])
        self.widthColumns = widthColumns
        self.heightColumns = heightColumns
        self.editdata = editdata
        self.deldata = deldata
        listen = self.table.getData(self.columnsname, self.where, self.values)
        if len(columns[0]) < len(self.columnsname):
            firstRow = []
            for i in range(len(self.columnsname) - len(columns[0])):
                firstRow.append("")
            firstRow = 
        else:  
            firstRow = columns[0]
        listen.insert(0, firstRow)
        self.listenValues = list(listen)
        print(listen)
        for contentid in range(len(listen)):
            contentRow = []
            for id in range(len(self.columns[0])):
                print(self.columns[1][id])
                print(listen[contentid])
                print(listen[contentid][self.columns[1][id]])
                contentRow.append(listen[contentid][self.columns[1][id]])
            self.addRow(contentRow, contentid)
                
    def addRow(self, content, cod, editPermission = True, delPermission = True):
        images = {"edit":CTkImage(Image.open("./imgs/pencil.jpg"), size=(40,40)), "del": CTkImage(Image.open("./imgs/lixeira.png"), size=(40,40))}
        self.content.append([])
        for i in range(len(content)):
            self.content[cod].append(CTkLabel(self.frame, width=self.widthColumns[i], height=self.heightColumns[i], bg_color=self.bgcolor, text=content[i]))
            print(cod)
            print(i)
            self.content[cod][i].grid(row=cod, column=i, padx=1, pady=1)
        num = len(self.content[cod])
        if self.editdata != () and editPermission:
            self.content[cod].append(CTkButton(self.frame, width=50, height=self.heightColumns[i], fg_color=self.bgcolor, text="", image=images["edit"], command=lambda cod=cod:self.editCommand(cod), hover=False))
            self.content[cod][num].grid(row=cod, column=num, padx=1, pady=1)
            num += 1
        if self.deldata != () and delPermission:
            self.content[cod].append(CTkButton(self.frame, width=50, height=self.heightColumns[i], fg_color=self.bgcolor, text="", image=images["del"], command=lambda cod=cod:self.delCommand(cod), hover=False))
            self.content[cod][num].grid(row=cod, column=num, padx=1, pady=1)
    def editCommand(self, cod):
        if self.editdata[1] == "TABLE":
            if self.editdata[2] != None:
                self.editdata[0](self.listenValues[cod][self.editdata[2]])
                return
            self.editdata[0](self.listenValues[cod])
    def delCommand(self, cod):
        if self.deldata[1] == "TABLE":
            if self.deldata[2] != None:
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
                self.addRow(newcontent[contentid], contentid)
        
    def deleteRow(self, rowid):
        for i in self.content[rowid:]:
            for j in i:
                j.destroy()