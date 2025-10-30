import tkinter as tk


class MenuGUI(tk.Tk):
    def __init__(self):
        super().__init__()  # Inicializa a classe base tk.Tk

        self.title("Sistema de Gerenciamento de Cadastro")
        self.geometry("450x400")

        menu_principal = tk.Menu(self)
        self.config(menu=menu_principal)



if __name__ == "__main__":
    app = MenuGUI()
    app.mainloop()