import customtkinter
from tablesWindows import tablesWindows
root = customtkinter.CTk()
root.title("oii")
root.geometry("800x800")
table = tablesWindows(root, "contas", "Conts", ("username", "name", "password"), bgcolor="#999999")
table.create(("Nome", "Nome de usuário", "Senha"), (150, 75, 150), (40, 40, 40))

root.mainloop()