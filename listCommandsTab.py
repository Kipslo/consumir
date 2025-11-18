from customtkinter import StringVar, CTkLabel, CTkButton, CTkScrollableFrame, CTkFrame, CTkEntry
from colorsList import getColors
from table import table
import datetime
class listCommandsTab():
    def __init__(self, root, frameMain, data):
        self.colors = getColors()
        self.width = frameMain.master.winfo_width()
        self.frameMain = frameMain
        self.currentwindow = "MAIN"
        self.str_searchcommands = StringVar()
        self.str_searchcommands.set("")
        self.listfordelete = []
        self.label_searchcommand = CTkLabel(self.frameMain, fg_color=self.colors[1], textvariable=self.str_searchcommands, font=("Arial", 20))
        self.label_searchcommand.place(relx=0.01, rely=0.02, relwidth=0.88, relheight=0.05)
        
        #add command
        self.button_addcommand = CTkButton(self.frameMain, fg_color=self.colors[3], text="ADICIONAR COMANDA", hover_color=self.colors[2])
        self.button_addcommand.place(relx=0.90, rely=0.02, relwidth=0.09, relheight=0.05)
        
        root.bind("<KeyPress>", self.presskey)

        self.scroolFrame = CTkScrollableFrame(self.frameMain, fg_color=self.colors[1])
        self.scroolFrame.place(relx=0.01, rely=0.09, relwidth=0.98, relheight=0.84)

        self.frame_down = CTkFrame(self.frameMain, fg_color=self.colors[3], border_color=self.colors[0])
        self.frame_down.place(relx=0, rely=0.93, relwidth=1, relheight=0.07)
        
        self.entry_namecommand = CTkEntry(self.frame_down, placeholder_text="PESQUISAR POR NOME", fg_color=self.colors[7], font=("Arial", 20))
        self.entry_namecommand.place(relx=0.3, rely=0.175 , relwidth=0.15, relheight=0.65)
        
        self.button_updatecommand = CTkButton(self.frame_down, fg_color=self.colors[7], text="ATUALIZAR", hover_color=self.colors[6], command=lambda: self.reloadcommands().start())
        self.button_updatecommand.place(relx=0.02, rely=0.175, relwidth=0.1, relheight=0.65)

        self.button_mergecommands = CTkButton(self.frame_down, fg_color=self.colors[7], text="JUNTAR COMANDAS", hover_color=self.colors[6])
        self.button_mergecommands.place(relx=0.135, rely=0.175, relwidth=0.15, relheight=0.65)
        
        self.aplyname = CTkButton(self.frame_down, fg_color=self.colors[7], text="PROCURAR", hover_color=self.colors[6], command=lambda x = True:self.reloadcommands(x))
        self.aplyname.place(relx=0.89, rely=0.175, relwidth=0.1, relheight=0.65)
        self.frameMain.bind("<Button-1>", self.clickmain)
        self.reloadcommands()
        self.maxcommands = int(table("configuracoes", "Config").getData(("maxcommands", ), ("cod", ), ("1", ))[0][0])
    def reloadcommands(self, x = False ):
        self.number = []
        try:
            for i in self.currentcommands:
                i.destroy()
        except:
            pass
        commands = table("comandas", "CommandsActive").getData(("number", "initdate", "hour", "nameclient"), )
        self.currentcommands = []
        framewidth = self.width - (self.width * 0.02)
        print(framewidth)
        qtdrow = int(framewidth//280)
        currentcommands = []
        if x:
            x = self.entry_namecommand.get()
            for i in commands:
                if x.upper() in i[3].upper():
                    currentcommands.append(i)
        else:
            currentcommands = commands
        for i, command in enumerate(currentcommands):
            number, initdate, inithour, nameclient  = command
            now = datetime.datetime.now()
            date = datetime.datetime(int(initdate[0:4]), int(initdate[5:7]), int(initdate[8:10]), int(inithour[0:2]), int(inithour[3:5]), int(inithour[6:8]))
            delta = now - date
            total_sec = delta.total_seconds()
            total_min, sec = divmod(int(total_sec), 60)
            total_hour, minute = divmod(total_min, 60)
            total_days, hour = divmod(total_hour, 24)
            text = ""
            if total_days != 0:
                text = text + str(total_days) + "D " + str(hour) + "H "
            elif total_hour != 0:
                text = text + str(hour) + "H "
            
            text = text + str(minute) + "M " + str(sec) + "S"
            if len(nameclient) >= 16:
                nameclient = nameclient[0:15]
            self.currentcommands.append(CTkButton(self.scroolFrame,fg_color=self.colors[3], command="lambda m = i:self.windowcommand(self.currentcommands[m])", hover=False, width=260, height= 150, text= str(number) + " "+ nameclient +"\n" + "TEMPO: " + text, font=("Arial", 20)))
            
            self.currentcommands[i].grid(row=i//qtdrow, column=i%qtdrow, padx=5, pady=5)
            self.number.append(number)
        
    def clickmain(self, event):
        event.widget.focus_set()
    def presskey(self, event):
        key = event.keysym
        n = self.entry_namecommand.get()
        i = self.str_searchcommands.get()
        if n == "":
            if key == "0" or key == "1" or key == "2" or key == "3" or key == "4" or key == "5" or key == "6" or key == "7" or key == "8" or key == "9":
                self.str_searchcommands.set(i + key)
            elif key == "Return":
                if int(i) <= self.maxcommands and int(i) >= 1:
                    self.str_searchcommands.set("")
                    "self.windowcommand(str(int(i)))"
            elif key == "BackSpace": 
                self.str_searchcommands.set(i[0:-1])
            else:
                self.str_searchcommands.set("")
        elif key == "Delete":
            self.entry_namecommand.delete(0, "end")
        elif key == "Return":
            pass