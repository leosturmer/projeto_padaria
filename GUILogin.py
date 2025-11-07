import tkinter as tk
from tkinter import ttk, messagebox

from ConexaoBanco import ConexaoBanco

from GUIMenu import MenuGUI

import hashlib


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

        # Label e Entry para senha

        self.label_senha = tk.Label(self.frame, text="Senha: ")
        self.label_senha.grid(row=1, column=0, sticky=tk.W)
        self.entry_senha = tk.Entry(self.frame, show="*")
        self.entry_senha.grid(row=1, column=1)

        # Label e ComboBox para o perfil

        self.label_perfil = tk.Label(self.frame, text="Perfil: ")
        self.label_perfil.grid(row=2, column=0, sticky=tk.W)
        self.combobox_perfil = ttk.Combobox(self.frame, state="readonly")
        self.combobox_perfil.grid(row=2, column=1)

        # Botão de login

        self.button_login = tk.Button(
            self.frame, text="Login", command=self.verificar_login)
        self.button_login.grid(row=3, columnspan=2, pady=10)

        # Conectar com o banco de dados para prencher o ComboBox com os perfis

        self.carregar_perfis()

    # Populando o ComboBox

    def carregar_perfis(self):
        try:
            conexao = ConexaoBanco().get_conexao()
            cursor = conexao.cursor()

            # Consulta para obter os perfis em ordem alfabética

            query = "SELECT id_perfil, nome_perfil FROM perfil ORDER BY nome_perfil;"
            cursor.execute(query)

            resultados = cursor.fetchall()

            # Preencher ComboBox com os perfis e garantindo que id_perfil seja INT

            self.perfis = {row[1]: int(row[0]) for row in resultados}
            self.combobox_perfil['values'] = list(self.perfis.keys())

            # Fechar o cursor e a conexão
            cursor.close()
            conexao.close()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar perfis: {e}")

    # Verificando a autenticação
    def verificar_login(self):
        login = self.entry_login.get().strip() # .strip() é usado para remover os espaços em branco
        senha = self.entry_senha.get()
        nome_perfil = self.combobox_perfil.get().strip()

        # Verificando se as variáveis login, senha e nome_perfil estão vazias
        if not login or not senha or not nome_perfil:
            messagebox.showerror("Erro!", "Preencha todos os campos!")
            return 

        id_perfil = self.perfis.get(nome_perfil)

        if id_perfil is None:
            messagebox.showerror("Erro!", "Perfil inválido!")
            return 

        # Gerar hash SHA-256 da senha digitada

        senha_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()

        # Verificação dos valores antes da consulta
        # print(f"Login: {login}, Senha: {senha}, Perfil: {nome_perfil} (ID: {id_perfil}) ")
        
        try:
            # Conexão com Banco de Dados
            conexao = ConexaoBanco().get_conexao()
            cursor = conexao.cursor()

            # Consulta para verificar o login, senha e perfil
            query = "SELECT * FROM login WHERE login = %s AND senha = %s AND perfil = %s "
            cursor.execute(query, (login, senha_hash, id_perfil))
            resultado = cursor.fetchone()

            # Adicionando depuração
            # print(f"Resultado da consulta: {resultado}")

            if resultado:
                messagebox.showinfo(f"Login bem-sucedido",
                                    f"Bem vindo, {login}!")
                self.janela.withdraw()  # Fecha a janela de login
                self.abrir_menu_principal()
            else:
                messagebox.showerror(
                    "Erro de login", "Login, senha ou perfil incorretos!")

            cursor.close()
            conexao.close()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar login: {e}")

    def abrir_menu_principal(self):
        MenuGUI()


if __name__ == "__main__":
    janela = tk.Tk()
    app = LoginGui(janela)
    janela.mainloop()
