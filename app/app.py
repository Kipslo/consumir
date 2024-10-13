import flet as ft

def main(page: ft.Page):
    def login(event):
        pass
    page.title = "APP"

    entry_name = ft.TextField(label="DIGITE O NOME", width=200, text_align=ft.TextAlign.CENTER)
    entry_password = ft.TextField(label="DIGITE A SENHA")
    button_login = ft.ElevatedButton("LOGIN", on_click=login)
    page.add( ft.Column() )


ft.app(target=main)