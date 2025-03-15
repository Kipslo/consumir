import flet

def app(page: flet.Page):
    def reload(a = 0):
        page.clean()
        #page.appbar = flet.AppBar(title=flet.Text("oi"), bgcolor="#efefef", actions=[flet.ElevatedButton(on_click=reload)])
        row = flet.Row(wrap=True)
        page.scroll = "always"
        page.appbar = flet.AppBar(bgcolor="#efefef", title=flet.Text("oi") ,actions=[flet.ElevatedButton(text="Voltar", on_click=reload)])
        commandsactive = [100, 123, 145, 125, 363]
        for i in range(400):
            n = int(i) + 1
            if n in commandsactive:
                row.controls.append(flet.Container(content=flet.Text(n), width=100, height=50, bgcolor="#ff0000", on_click=lambda x, y = n:nada(y), margin=0, padding=10))
            else:
                row.controls.append(flet.Container(content=flet.Text(n), width=100, height=50, bgcolor="#00ff00", on_click=lambda x, y=n:nada(y), margin=0, padding=10))
        
        page.add(row)
    def nada(oi):
        print(oi)   
    reload()
flet.app(app)