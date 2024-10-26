import flet as ft
import socket

def main(page: ft.Page):
    def sendstr(datas):
        pass
    def connectserver():
        HOST = "127.0.0.1"
        PORT = 55262
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.sendall(str.encode("oioidata"))
        data = s.recv(1024)
        print(data.decode())
    def login(event):
        
        page.clean()
        
    connectserver()
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    page.title = "APP"

    entry_name = ft.TextField(label="NOME", width=350)

    entry_password = ft.TextField(label="SENHA", width=350)

    conteiner = ft.Container(content=ft.Column([ft.Container(width=500, height=100), entry_name, entry_password, ft.ElevatedButton("LOGIN", width=350, height=50, on_click=login)], horizontal_alignment= "center"), width=500, height=500, bgcolor=ft.colors.CYAN_500)
    


    loginarea = ft.Column([conteiner], horizontal_alignment="center")

    page.add(loginarea)
ft.app(target=main)