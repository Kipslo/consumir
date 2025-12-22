from customtkinter import CTkToplevel
class newWindow():
    def __init__(self, master, title:str= "", size:tuple= (500, 500), data = (), onDelete = None):
        self.window = CTkToplevel(master)
        self.window.resizable(False, False)
        self.window.geometry(f"{size[0]}x{size[1]}")
        self.window.transient(master)
        self.window.title(title)
        self.window.grab_set()
        self.onDelete = onDelete
        self.master = master
        self.data = data
        self.window.protocol("WM_DELETE_WINDOW", self.deleteWindow)
        self.window.bind("<KeyPress>", self.click)
    def click(self, event):
        if event.keysym == "Escape":
            self.deleteWindow()
    def deleteWindow(self, ):
        if self.onDelete:
            self.onDelete(self.data)
        self.window.destroy()
        self.master.grab_set()