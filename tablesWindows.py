from table import table as tableClass
from customtkinter import CTkButton, CTkLabel


class tablesWindows():
    def __init__(self, master, db:str, table:str, columnsname = ("*", ), where:tuple = (), values:tuple = (), bgcolor:str="", placeholder_color:str=""):
        self.master = master
        self.where = where
        self.columnsname = columnsname
        self.values = values
        self.table = tableClass(db, table)
        self.bgcolor = bgcolor
        self.placeholder_color = placeholder_color
    def create(self, columns:tuple= (), widthColumns:tuple = (), heightColumns:tuple= (), editButton:bool= False, delButton:bool= False, funcEdit="", funcDel=""):
        self.content = []
        self.columns = columns
        self.widthColumns = widthColumns
        self.heightColumns = heightColumns
        listen = self.table.getData(self.columnsname, self.where, self.values)
        listen.insert(0, columns)
        print(listen)
        for contentid in range(len(listen)):
            self.addRow(listen[contentid], contentid)
                
    def addRow(self, content, cod):
        self.content.append([])
        for i in range(len(content)):
            self.content[cod].append(CTkLabel(self.master, width=self.widthColumns[i], height=self.heightColumns[i], bg_color=self.bgcolor, text=content[i]))
            print(cod)
            print(i)
            self.content[cod][i].grid(row=cod, column=i, padx=1, pady=1)
    def reload(self, where:tuple = (), values:tuple = ()):
        newcontent = self.table.getData(self.columnsname, where, values)
        num = len(self.content)
        maxx = max(num, len(newcontent))
        for contentid in range(maxx):
            if contentid <= num:
                try:
                    for columnid in range(len(elf.columns)):
                        self.content[contentid][columnid].configure(text = newcontent[contentid][columnid])
                except:
                    self.deleteRow(contentid)
            else:
                self.addRow(newcontent[contentid], contentid)
    def deleteRow(self, rowid):
        for i in range(len(self.content)):
            if i >= rowid:
                for j in rowid:
                    j.destroy()

    def delete(self, ):
        for i in self.content:
            for j in i:
                j.destroy()
        self.currentTable.place_forget()