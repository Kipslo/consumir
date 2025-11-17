from listCommandsTab import listCommandsTab
class controlTabs():
    def __init__(self, frameMain):
        self.frameMain = frameMain
        self.listenFunctions = {"listacomandas": listCommandsTab,
                                
                                
                                
                                }
    def deleteTab(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
            
    def changeTab(self, tab, data = ()):
        self.deleteTab(self.frameMain)
        self.currentTab = self.listenFunctions[tab](self.frameMain, data, )