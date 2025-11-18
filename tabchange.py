from customtkinter import CTkImage, CTkButton, CTkFrame
from PIL import Image
from tabFunctions import controlTabs
class changeTabsButtons():
    def __init__(self, root):
        self.listenFunctions = controlTabs(root)
        self.frame_tab = CTkFrame(self.root, fg_color=self.colors[7], border_color=self.colors[0])
        self.frame_tab.place(relx=0, rely=0, relwidth=1, relheight=0.14)
        self.listImageButton = {"caixa": CTkImage(Image.open("./imgs/caixa.png"), size=(60,60)), 
                                "relogio": CTkImage(Image.open("./imgs/relogio.png"), size=(60,60)), 
                                "tabelas": CTkImage(Image.open("./imgs/tables.png"), size=(60,60)), 
                                "clientes": CTkImage(Image.open("./imgs/clientes.png"), size=(60,60)), 
                                "trofeu": CTkImage(Image.open("./imgs/trofeu.png"), size=(60,60)), 
                                "garçom": CTkImage(Image.open("./imgs/garçom.png"), size=(60,60)), 
                                "produto": CTkImage(Image.open("./imgs/produtos.png"), size=(60,60)),
                                "complemento": CTkImage(Image.open("./imgs/complementos.png"), size=(60,60)),
                                "anotacoes": CTkImage(Image.open("./imgs/anotacoes.jpg"), size=(60,60)),
                                "tiposetamanhos": CTkImage(Image.open("./imgs/tiposetamanhos.png"), size=(60,60)),
                                "categorias": CTkImage(Image.open("./imgs/categorias.jpg"), size=(60,60)),
                                "promocoes": CTkImage(Image.open("./imgs/promocoes.png"), size=(60,60)),
                                "config": CTkImage(Image.open("./imgs/config.png"), size=(60,60)),
                                "info": CTkImage(Image.open("./imgs/info.png"), size=(60, 60)),

                                }
        self.mainButtonsList = {"PRINCIPAL": CTkButton(self.frame_tab, text="PRINCIPAL", hover_color=self.colors[4], fg_color=self.colors[5], command=lambda:self.changeTabButton("PRINCIPAL")),
                                "PRODUTO": CTkButton(self.frame_tab, text="PRODUTO", hover_color=self.colors[4], fg_color=self.colors[5], command=lambda:self.changeTabButton("PRODUTO")),
                                "CONFIGURACOES": CTkButton(self.frame_tab, text="CONFIGURACOES", hover_color=self.colors[4], fg_color=self.colors[5], command=lambda:self.changeTabButton("CONFIGURACOES"))
                                }
        
        self.mainButtonsList["PRINCIPAL"].place(relx=0, rely=0, relwidth=0.1, relheight=0.285)
        self.mainButtonsList["PRODUTO"].place(relx=0.1, rely=0, relwidth=0.1, relheight=0.285)
        self.mainButtonsList["CONFIGURACOES"].place(relx=0.2, rely=0, relwidth=0.1, relheight=0.285)
        self.listenFunctions.changeTab("listacomandas")
    def createTabButtons(self, tab):
        if tab == "PRINCIPAL":
            self.currentTabButtons = [CTkButton(master= self.frame_tab, command=self.cash, image=self.listImageButton["caixa"], text="ABRIR CAIXA", fg_color=self.colors[4], hover_color=self.colors[2], compound="top", anchor="bottom"), 
                                             CTkButton(master= self.frame_tab, command=lambda tab = "historicocaixa":self.listenFunctions.changeTab(tab), image=self.listImageButton["relogio"], text="HISTÓRICO DO CAIXA", fg_color=self.colors[4], hover_color=self.colors[2], compound="top", anchor="bottom"), 
                                             CTkButton(master= self.frame_tab, command=lambda tab = "listacomandas":self.listenFunctions.changeTab(tab), image=self.listImageButton["tabelas"], text="MESAS / COMANDAS", fg_color=self.colors[4], hover_color=self.colors[2], compound="top", anchor="bottom"), 
                                             CTkButton(master= self.frame_tab, command=self.clientswindow, image=self.listImageButton["clientes"], text="CLIENTES", fg_color=self.colors[4], hover_color=self.colors[2], compound="top", anchor="bottom"), 
                                             CTkButton(master= self.frame_tab, command=self.rankingproducts, image=self.listImageButton["trofeu"], text="MAIS VENDIDOS", fg_color=self.colors[4], hover_color=self.colors[2], compound="top", anchor="bottom"), 
                                             CTkButton(master= self.frame_tab, command=self.historyproducts, image=self.listImageButton["relogio"], text="HISTÓRICO DE PEDIDOS", fg_color=self.colors[4], hover_color=self.colors[2], compound="top", anchor="bottom"), 
                                             CTkButton(master= self.frame_tab, command=self.rankingservice, image=self.listImageButton["garçom"], text="RANKING DE ATENDIMENTOS", fg_color=self.colors[4], hover_color=self.colors[2], compound="top", anchor="bottom")]
        elif tab == "PRODUTO":
            self.currentTabButtons = [CTkButton(master= self.frame_tab, command=self.productswindow, image=self.listImageButton["produto"], text="PRODUTOS", fg_color=self.colors[4], hover_color=self.colors[2], compound="top", anchor="bottom"), 
                                            CTkButton(master= self.frame_tab, image=self.listImageButton["complemento"], text="COMPLEMENTOS", fg_color=self.colors[4], hover_color=self.colors[2], compound="top", anchor="bottom"), 
                                            CTkButton(master= self.frame_tab, command=self.notewindow, image=self.listImageButton["anotacoes"], text="ANOTAÇÕES", fg_color=self.colors[4], hover_color=self.colors[2], compound="top", anchor="bottom"), 
                                            CTkButton(master= self.frame_tab, command=self.stockwindow, image=self.listImageButton["anotacoes"], text="ESTOQUE", fg_color=self.colors[4], hover_color=self.colors[2], compound="top", anchor="bottom"), 
                                            CTkButton(master= self.frame_tab, image=self.listImageButton["tiposetamanhos"], text="TIPOS E TAMANHOS", fg_color=self.colors[4], hover_color=self.colors[2], compound="top", anchor="bottom"), 
                                            CTkButton(master= self.frame_tab, command=self.categorieswindow, image=self.listImageButton["categorias"], text="CATEGORIAS", fg_color=self.colors[4], hover_color=self.colors[2], compound="top", anchor="bottom"), 
                                            CTkButton(master= self.frame_tab, image=self.listImageButton["promocoes"], text="PROMOÇÕES", fg_color=self.colors[4], hover_color=self.colors[2], compound="top", anchor="bottom"), ]
        elif tab == "CONFIGURACOES":
            self.currentTabButtons = [CTkButton(master=self.frame_tab, command=self.configwindow, image=self.listImageButton["config"], text="CONFIGURAÇÕES", fg_color=self.colors[4], hover_color=self.colors[2], compound="top", anchor="bottom"), 
                                                  CTkButton(master=self.frame_tab, command=self.functionarywindow, image=self.listImageButton["garçom"], text="FUNCIONÁRIOS", fg_color=self.colors[4], hover_color=self.colors[2], compound="top", anchor="bottom"), 
                                                  CTkButton(self.frame_tab, command=self.windowprinters, image=self.listImageButton["caixa"], text="IMPRESSORAS", fg_color=self.colors[4], hover_color=self.colors[2], compound="top", anchor="bottom"), 
                                                  CTkButton(self.frame_tab, command=self.reloadserverandprinter, image=self.listImageButton["garçom"], text="RELOAD", fg_color=self.colors[4], hover_color=self.colors[2], compound="top", anchor="bottom"), 
                                                  CTkButton(self.frame_tab, command=self.standartentries, image=self.listImageButton["info"], text="ENTRADAS", fg_color=self.colors[4], hover_color=self.colors[2], compound="top", anchor="bottom")]
                                            
    def changeTabButton(self, tab:str = "PRINCIPAL"):
        self.mainButtonsList["PRINCIPAL"].configure(fg_color=self.colors[7], hover_color=self.colors[5], hover=True)
        self.mainButtonsList["PRODUTO"].configure(fg_color=self.colors[7], hover_color=self.colors[5], hover=True)
        self.mainButtonsList["CONFIGURACOES"].configure(fg_color=self.colors[7], hover_color=self.colors[5], hover=True)
        self.mainButtonsList[tab].configure(fg_color=self.colors[4], hover=False)
        try:
            for i in self.currentTabButtons:
                i.destroy()
        except:
            pass
        self.createTabButtons(tab)
        num = 0
        for tabButton in self.currentTabButtons:
            tabButton.place(relx=0.1*num, rely=0.285, relwidth=0.1, relheight=0.715)
            num += 1
