import tkinter as tk

from tkinter import ttk, messagebox
from ConexaoBanco import ConexaoBanco

# from GUIMenu import MenuGUI


class LoginGui:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Tela de login")

        # Frame para organizar os elementos

        self.frame = tk.Frame(janela, padx=40, pady=40)
        self.frame.pack()

        # Label e Entry para login
        self.label_login = tk.Label(self.frame, text="Login: ")
        self.label_login.grid(row=0, column=0, sticky=tk.W)
        self.entry_login = tk.Entry(self.frame)
        self.entry_login.grid(row=0, column=1)

if __name__ == "__main__":
    janela = tk.Tk()
    app = LoginGui(janela)

    janela.mainloop()
