import flet as ft

def main(page: ft.Page):
    page.title = "Routes Example"

    def route_change():
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                    ft.ElevatedButton("Visit Store", on_click=lambda _: page.go("/store")),
                ],
            )
        )
        page.views.append(
            ft.View(
                "/store",
                [
                    ft.AppBar(title=ft.Text("Store"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                    ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                ],
            )
        )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    route_change()
    page.go(page.route)


ft.app(main, view=ft.AppView.WEB_BROWSER)