import customtkinter
from tablesWindows import tablesWindows
def printar(oi):
    print(oi)
def reload():
    table.reload(("name", ), ("Biel", ))
root = customtkinter.CTk()
root.title("oii")
root.geometry("800x800")
table = tablesWindows(root, (0.01, 0.01, 0.49, 0.49), "contas", "Conts", ("username", "name", "password"), bgcolor="#999999", )
table.create((("Nome", "Nome de usuário"), (0, 2)), (150, 75, 150), (50, 50, 50), editdata=(printar, "TABLE", ""), deldata=(printar, "TABLE", 0))

button = customtkinter.CTkButton(root, command=reload)
button.place(relx=0.7, rely=0.1, relwidth=0.2, relheight=0.1)

root.mainloop()