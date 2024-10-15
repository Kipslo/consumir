import flet as ft
import socket

def main(page: ft.Page):
    def sendstr(datas):
    def connectserver():
        HOST = "127.0.0.1"
        PORT = 85250
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
    def login(event): 
        pass
    connectserver()
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    page.title = "APP"

    loginarea = ft.Column([ft.Container(
                            width=300,
                            height=300,
                            bgcolor=ft.colors.BLACK12
                                      )
                          
                        ])

    page.add(loginarea)
ft.app(target=main)