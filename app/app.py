import flet as ft
import socket
import threading
class app():
    def __init__(self):
        ft.app(target=self.main)
    def sendstr(self, data):
        self.PORT = 55261
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))
        self.s.sendall(str.encode(data))
        data = self.s.recv(2024)
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()
        return data.decode()
    
    def main(self, page: ft.Page):
        def initpage(event = 0):
            def commandpage(number):
                del self.commands
                self.command = number
                def reviewpage(event = 0):
                    def send():
                        tem = ""
                        for i in self.products:
                            name, category, unitprice, qtd, texts, tipe, prynter = i
                            data = f"INSERT,={self.command}"
                            if self.divisioncommands != "":
                                for i in self.divisioncommands.split(","):    
                                    data = data + f".={i}"
                            
                            data = data + f",={self.name},={self.password},="
                            if texts == "":
                                data = data + f"{name}.-{category}.-{unitprice}.-{qtd}.-{tipe}.-{prynter}"
                            else:
                                data = data + f"{name}.-{category}.-{unitprice}.-{qtd}"
                                n = 0
                                for j in texts:
                                    if n == 0:
                                        data = data + f".-{j}"
                                        n = 1
                                    else:
                                        data = data + f".={j}"
                                data = data + f".-{tipe}.-{prynter}"
                                
                            print(data)
                            t = self.sendstr(data)
                            if t != "Y":
                                tem = t
                        del t
                        if tem == "":
                            alert = ft.Banner(bgcolor="#ff0000", content=ft.Text("PEDIDO ENVIADO COM SUCESSO", color="#000000"), actions=[ft.TextButton("OK", on_click=lambda x:page.close(alert))])
                        else:
                            alert = ft.Banner(bgcolor="#ff0000", content=ft.Text(tem, color="#000000"), actions=[ft.TextButton("OK", on_click=lambda x:page.close(alert))])
                        page.open(alert)
                        initpage()
                    def editt(i):
                        self.text = self.products[i][4]
                        edit(i)
                    def edit(i):
                        def addtext(event):
                            temp = entry.value
                            self.text.append(temp)
                            edit(i)
                        def confirm(event):
                            self.products[i][4] = self.text
                            reviewpage()
                        def edittext(event, x):
                            if event.data == "true":
                                self.text.append(x)
                            else:
                                for k, i in enumerate(self.text):
                                    if i == x:
                                        del self.text[k]
                        def delete(x):
                            del self.text[x]
                            edit(i)
                        page.clean()
                        page.bottom_appbar = ft.BottomAppBar(content=ft.Row(controls=[ft.ElevatedButton("CANCELAR", on_click=reviewpage), ft.Container(expand=True), ft.ElevatedButton("CONFIRMAR", on_click=confirm)]))
                        page.appbar = ft.AppBar()
                        
                        page.add(ft.Row(controls=[ft.Container(ft.Row(controls=[ft.Container(width=10), ft.Container(content=ft.Text(self.products[i][0]), expand=True), ft.Container(content=ft.Text(self.products[i][1]), width=100), ft.Container(ft.Text(self.products[i][2]), width=50)]), expand=True, bgcolor="#c4c4c3", height=50)]))

                        entry = ft.TextField(expand=True, height=50)
                        buttonadd = ft.CupertinoFilledButton(on_click=addtext, width=75, height=50, text="add")

                        predefnotes = self.sendstr(f"GETNOTES,={self.products[i][1]}")
                        predefnotes = predefnotes.split(".=")
                        if predefnotes[0] != '':
                            for j in predefnotes:
                                page.add(ft.Row(height=5))
                                num = 0
                                for p in self.text:
                                    if p == j:
                                        page.add(ft.Row(controls=[ft.Container(content=ft.Row([ft.Container(width=10), ft.Checkbox(label=j, value="true", on_change=lambda n, x = j:edittext(n, x))], height=50))]))
                                        num = 1
                                        break
                                for p in self.products[i][4]:
                                    if p == j and num == 0:
                                        page.add(ft.Row(controls=[ft.Container(content=ft.Row([ft.Container(width=10), ft.Checkbox(label=j, value="true", on_change=lambda n, x = j:edittext(n, x))], height=50))]))
                                        num = 1
                                        break
                                if num == 0:
                                    page.add(ft.Row(controls=[ft.Container(content=ft.Row([ft.Container(width=10), ft.Checkbox(label=j, on_change=lambda n, x = j:edittext(n, x))], height=50))]))

                        for k, j in enumerate(self.text):
                            t = True
                            for p in predefnotes:
                                if p == j:
                                    t = False
                            if t:
                                page.add(ft.Row(height=5))
                                page.add(ft.Row(controls=[ft.Container(content=ft.Row([ft.Container(width=10), ft.Container(ft.Text(j), expand=True), ft.CupertinoButton(text="DELETAR", on_click=lambda x, y = k:delete(y), width=100)]), expand=True, bgcolor="#c4c4c3")], height=50))

                        page.add(ft.Row(height=10))
                        page.add(ft.Row(controls=[entry, buttonadd]))

                    def add1(i):
                        self.products[i][3] = self.products[i][3] + 1
                        reviewpage()
                    def remove1(i):
                        if self.products[i][3] > 1:
                            self.products[i][3] = self.products[i][3] - 1
                        reviewpage()
                    def delete(i):
                        del self.products[i]
                        reviewpage()
                    def divisionpage(event):
                        def confirm(event):
                            

                            self.divisioncommands = str(divisionentry.value)
                            reviewpage()
                        page.clean()

                        page.appbar = ft.AppBar(bgcolor="#efefef", title=ft.Text("Dividir produtos da comanda " + str(self.command)))
                        page.bottom_appbar = ft.BottomAppBar(content=ft.Row(controls=[ft.ElevatedButton("VOLTAR", on_click=reviewpage), ft.Container(expand=True), ft.ElevatedButton("CONFIRMAR", on_click=confirm)]))

                        divisionentry = ft.TextField(value=self.divisioncommands)

                        divisionrow = ft.Row([divisionentry, ft.TextButton()])

                        page.add(divisionrow)
                    page.clean()
                    rows = []
                    page.spacing = 0
                    page.appbar = ft.AppBar(bgcolor="#efefef", title=ft.Text("Comanda " + str(self.command)), actions=[ft.ElevatedButton("Dividir", on_click=divisionpage)])
                    page.bottom_appbar = ft.BottomAppBar(content=ft.Row(controls=[ft.ElevatedButton("VOLTAR", on_click=addpage), ft.Container(expand=True), ft.ElevatedButton("ENVIAR", on_click=lambda x:send())]))


                    rows.append(ft.Row(controls=[ft.Container(content=ft.Row([ft.Container(expand=True, width=100, height=49, content=ft.Text("PRODUTO", text_align="center")), ft.Container(expand=True, width=100, height=49, content=ft.Text("CATEGORIA", text_align="center")), ft.Container(expand=True, width=30, height=49, content=ft.Text("QTD.", text_align="center"))]), bgcolor="#c4c4c3", height=50, expand=True)]))
                    
                    rows.append(ft.Row(height=8))


                    for k, i in enumerate(self.products):
                        rows.append(ft.Row(height=50, controls=[ft.Container(content=ft.Row([ft.Container(width=100, height=50, content=ft.Text(i[0], text_align="center")), ft.Container(expand=True, width=100, height=49, content=ft.Text(i[1], text_align="center")), ft.Container(expand=True, width=30, height=49, content=ft.Text(i[3], text_align="center"))]), bgcolor="#c4c4c3", height=50, expand=True)]))

                        rows.append(ft.Row(height=50, controls=[ft.Container(content=ft.Row(controls=[ft.Container(content=ft.CupertinoButton(text="-1", on_click=lambda x, y = k:remove1(y)), expand=True), ft.Container(content=ft.CupertinoButton("+1", on_click=lambda x, y = k:add1(y)), expand=True), ft.Container(content=ft.CupertinoButton("EDITAR", on_click=lambda x, y = k:editt(y)), expand=True), ft.Container(content=ft.CupertinoButton("EXCLUIR", on_click=lambda x, y = k:delete(y)), expand=True)], height=50), height=50, bgcolor="#c4c4c3", expand=True)]))

                        rows.append(ft.Row(height=5))

                    for i in rows:
                        page.add(i)
                def categorypage(category):
                    self.category = category
                    productscategory = self.sendstr(f"PRODUCTSCATEGORY,={category}")
                    page.clean()
                    productscategory = productscategory.split(",=")
                    vcategorypage = ft.Row(wrap=True, spacing=10)
                    for k, i in enumerate(productscategory):
                        productscategory[k] = i.split("|")
                    if productscategory[0][0] != '':
                        for i in productscategory:
                            if i[1] != "SIZE":
                                vcategorypage.controls.append(ft.Container(content=ft.CupertinoButton(content=ft.Column([ft.Text(i[0], text_align=ft.alignment.top_left, ), ft.Text(i[2], text_align=ft.alignment.bottom_right)], width=150, height=100), width=150, height=100, on_click=lambda x, y = i[0], z = i[2], a = i[1], b = i[3]:addproductlist(y, z, a, b)), bgcolor="#c4c4c3", width=150, height=100, margin=0, padding=0))
                            else: 
                                vcategorypage.controls.append(ft.Container(content=ft.CupertinoButton(content=ft.Column([ft.Text(i[0], text_align=ft.alignment.top_left)], width=150, height=100), width=150, height=100, on_click=lambda x, y = i[0], z = i[3]: sizepage(y, z)), bgcolor="#c4c4c3", width=150, height=100), margin=10, padding=10)
                    page.bottom_appbar = ft.BottomAppBar(content=ft.Row(controls=[ft.ElevatedButton("VOLTAR", on_click=addpage), ft.Container(expand=True), ft.ElevatedButton("REVISAR", on_click=reviewpage)]))                        
                    page.add(vcategorypage)    
                def addproductlist(product, unitprice, tipe, prynter):
                    self.products.append([product, self.category, unitprice, 1, [], tipe, prynter])
                def addpage(event):
                    pdt = self.sendstr("CATEGORIES")
                    page.clean()
                    pdt = pdt.split(",=")
                    vaddpage = ft.Row(wrap=True, spacing=10)
                    page.appbar = ft.AppBar(bgcolor="#efefef", title=ft.Text("COMANDA " + str(self.command)))
                    page.bottom_appbar = ft.BottomAppBar(content=ft.Row(controls=[ft.ElevatedButton("VOLTAR", on_click=lambda x, y = self.command:(commandpage(y))), ft.Container(expand=True), ft.ElevatedButton("REVISAR", on_click=reviewpage)]))
                    for i in pdt:
                        vaddpage.controls.append(ft.Container(content=ft.CupertinoButton(i, width=150, height=75, on_click=lambda x, y = i:categorypage(y)), width=150, height=75, bgcolor="#c4c4c3"))
                    page.add(vaddpage)
                def sizepage(product, prynter):
                    sizes = self.sendstr(f"SIZESCATEGORY,={product},={self.category}")
                    page.clean()
                    sizes = sizes.split(",=")
                    for k, i in enumerate(sizes):
                        sizes[k] = i.split("|")
                    page.bottom_appbar = ft.BottomAppBar(content=ft.Row(controls=[ft.ElevatedButton("VOLTAR", on_click=lambda x, y = self.category:categorypage(y)), ft.Container(expand=True), ft.ElevatedButton("REVISAR", on_click=reviewpage)]))
                    sizesbutton = ft.Row(wrap=True, spacing=10)
                    for i in sizes:
                        sizesbutton.controls.append(ft.Container(content=ft.TextButton(text=f"""{i[0]}
                        
                        {i[1]}""", width=150, height=75, on_click=lambda x, y = product + f" ({i[0]})", z = i[1], a = "SIZE", b = prynter:addproductlist(y, z, a, b)), bgcolor="#c4c4c3", width=150, height=75))

                    page.add(sizesbutton)
                def addclientpage(event):
                    def addmale(x):
                        maleqtd.value = str(int(maleqtd.value) + 1)
                        maleqtd.update()
                    def removemale(x):
                        if int(maleqtd.value) > 0: 
                            maleqtd.value = str(int(maleqtd.value) - 1)
                            maleqtd.update()
                    def addfemale(x):
                        femaleqtd.value = str(int(femaleqtd.value) + 1)
                        femaleqtd.update()
                    def removefemale(x):
                        if int(femaleqtd.value) > 0:
                            femaleqtd.value = str(int(femaleqtd.value) - 1)
                            femaleqtd.update()
                    def sendclient(x):
                        result = self.sendstr(f"INSERTCLIENT,={self.name},={self.password},={self.command},={idclient.value},={nameclient.value},={maleqtd.value},={femaleqtd.value}")

                        commandpage(number)
                    page.clean()
                    page.bottom_appbar = []
                    page.appbar = ft.AppBar(bgcolor="#efefef", title=ft.Text("COMANDA " + str(self.command)) ,actions=[ft.ElevatedButton(text="Voltar", on_click=lambda x, y = number:commandpage(y))])

                    idclient = ft.TextField(expand=True, value=self.idclient)
                    nameclient = ft.TextField(expand=True, value=self.clientname)
                    maleqtd = ft.TextField(width=50, value="0")
                    femaleqtd = ft.TextField(width=50, value="0")

                    widgets = ft.Column([ft.Row([ft.Text("ID do cliente:"), idclient], expand=True), ft.Row([ft.Text("Nome do cliente:"), nameclient]), ft.Row([ft.Text("QTD. Masculino:", expand=True), ft.IconButton(ft.icons.REMOVE_CIRCLE, on_click=removemale), maleqtd, ft.IconButton(ft.icons.ADD_CIRCLE, on_click=addmale)], expand=True), ft.Row([ft.Text("QTD. Feminino:", expand=True, text_align='left'), ft.IconButton(ft.icons.REMOVE_CIRCLE, on_click=removefemale), femaleqtd, ft.IconButton(ft.icons.ADD_CIRCLE, on_click=addfemale)]), ft.Row([ft.Container(expand=True), ft.ElevatedButton(text="Enviar", expand=True, on_click=sendclient), ft.Container(expand=True)])])
                    page.add(widgets)
                page.scroll = "always"
                self.products = []
                try:
                    self.clientname, self.idclient = self.sendstr("CLIENTNAME,=" + str(self.command)).split(",=")
                except:
                    self.clientname, self.idclient = "", ""
                if self.clientname == "":
                    page.appbar = ft.AppBar(bgcolor="#efefef", title=ft.Text("COMANDA " + str(self.command)) ,actions=[ft.ElevatedButton(text="Voltar", on_click=initpage)])
                else:
                    page.appbar = ft.AppBar(bgcolor="#efefef", title=ft.Text(f"{self.clientname} ({str(self.command)})") ,actions=[ft.ElevatedButton(text="Voltar", on_click=initpage)])
                products = self.sendstr("PRODUCTSON,=" + str(self.command))
                page.clean()
                products = products.split(",=")
                for k, i in enumerate(products):
                    products[k] = i.split("|")
                column = ft.Column(spacing=2)
                self.divisioncommands = ""
                column.controls.append(ft.Row(controls=[ft.Container(content=ft.Row(controls=[ft.Container(width=10, height=49), ft.Container(ft.Text("PRODUTO"), expand=True), ft.Container(ft.Text("QUANTIDADE", text_align="center"), width=100), ft.Container(ft.Text("PREÇO", text_align="center"), width=50), ft.Container(width=5, height=49)]), bgcolor="c4c4c3", height=60, expand=True)]))
                if products != [[""]]:
                    total = 0.0
                    for i in products:
                        column.controls.append(ft.Row(controls=[ft.Container(content=ft.Row(controls=[ft.Container(width=10, height=49), ft.Container(ft.Text(i[0]), expand=True), ft.Container(ft.Text(i[1], text_align="center"), width=100), ft.Container(ft.Text(i[2], text_align="center"), width=50), ft.Container(width=5, height=49)]), bgcolor="#c4c4c3", height=60, expand=True)]))
                        total = total + float(i[2])
                    column.controls.append(ft.Row(controls=[ft.Container(content=ft.Row(controls=[ft.Container(width=10, height=49), ft.Container(ft.Text("TOTAL:"), expand=True), ft.Container(width=100), ft.Container(ft.Text(total, text_align="center"), width=50), ft.Container(width=5, height=49)]), bgcolor="#c4c4c3", height=60, expand=True)]))
                page.bottom_appbar = ft.BottomAppBar(bgcolor="#c4c4c3", content=ft.Row(controls=[ft.ElevatedButton("ADD produto", on_click=addpage), ft.Container(expand=True), ft.ElevatedButton("ADD cliente", on_click=addclientpage)]))
                page.add(column)
            try:
                self.commands.controls[0]
            
                opencommands = self.sendstr("OPENCOMMANDS")

                
                opencommands = opencommands.split(",=")
                for i in self.tempcommandred:
                    self.commands.controls[i].bgcolor = "#00a000"
                self.tempcommandred = []
                
                for i in opencommands:
                    number = int(i)
                    self.commands.controls[number].bgcolor = "#dd0000"
                    self.tempcommandred.append(number)
                
                page.update()
            except:
                page.appbar = ft.AppBar(bgcolor="#efefef", actions=[ft.ElevatedButton(text="Recarregar", on_click=initpage)])
                page.clean()
                self.commands = ft.Row(wrap=True)
                limitcommands = self.sendstr("LIMITCOMMANDS")
                page.scroll = "always"
                for i in range(int(limitcommands)):
                    n = i + 1
                    self.commands.controls.append(ft.ElevatedButton(content=ft.Text(str(n), color="#ffffff", size=25), on_click=lambda y, x = n: commandpage(x), width=100,height=50, bgcolor="#00a000"))
                self.tempcommandred = []
                opencommands = self.sendstr("OPENCOMMANDS").split(",=")
                page.bottom_appbar = None
                for i in opencommands:
                    number = int(i)
                    self.commands.controls[number].bgcolor = "#dd0000"
                    self.tempcommandred.append(number)
                page.add(self.commands)
            
        
        def login(event):
            data = ""
            try:
                self.HOST = self.entry_ip.value
                data = self.sendstr("LOGIN,=" + self.entry_name.value + ",=" + self.entry_password.value)
                data = data
                if data == "YES":
                    page.client_storage.set("NAMECONSUMER", self.entry_name.value)
                    page.client_storage.set("IPCONSUMER", self.HOST)
                    self.name, self.password = self.entry_name.value, self.entry_password.value
                    initpage()
                elif data == "NOT":
                    self.errorlogintext.value = "NOME E/OU SENHA INCORRETOS"
                    self.errorlogintext.update()
            except Exception as error:
                    print(error)
                    self.errorlogintext.value = "FALHA NA CONEXÃO"
                    self.errorlogintext.update()
        page.horizontal_alignment = "center"
        page.vertical_alignment = "center"

        page.title = "APP"

        self.entry_name = ft.TextField(label="NOME", width=350, value=page.client_storage.get("NAMECONSUMER"))

        self.entry_password = ft.TextField(label="SENHA", width=350)

        self.entry_ip = ft.TextField(label="IP", width=350)

        self.errorlogintext = ft.Text(value="", width=350, height=100, size=18, text_align="center")

        self.entry_ip.value = page.client_storage.get("IPCONSUMER")

        container = ft.Container(content=ft.Column([ft.Container(width=500, height=100), self.entry_name, self.entry_password, self.entry_ip, ft.ElevatedButton("LOGIN", width=350, height=50, on_click=login), self.errorlogintext], horizontal_alignment= "center"), width=500, height=500, bgcolor="#ffffff")
        


        loginarea = ft.Column([container], horizontal_alignment="center")

        page.add(loginarea)
app()