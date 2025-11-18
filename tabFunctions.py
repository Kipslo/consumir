from listCommandsTab import listCommandsTab
from customtkinter import CTkFrame
class controlTabs():
    def printar(self):
        print("chegou")
    def __init__(self, root):
        self.root = root
        self.listenFunctions = {"listacomandas": listCommandsTab,
                                "historicocaixa": self.printar,
                                
                                
                                }
    
    def changeTab(self, tab, data = ()):
        try:
            self.mainFrame.destroy()
        except Exception as error:
            print(error)
        self.mainFrame = CTkFrame(self.root, )
        self.mainFrame.place(relx=0, rely=0.14, relwidth=1, relheight=0.86)
        self.currentTab = self.listenFunctions[tab](self.mainFrame, data, )
