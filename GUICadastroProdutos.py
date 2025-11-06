import tkinter as tk
from tkinter import messagebox
from decimal import Decimal
from ProdutoVO import ProdutoVO


class CadastroProdutos:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Produtos")
        self.root.geometry("270x150")

        # Labels e entradas para os dados dos produtos

        tk.Label(self.root, text="Nome: ").grid(row=0, column=0)
        self.entry_nome = tk.Entry(self.root)
        self.entry_nome.grid(row=0, column=1)

        tk.Label(self.root, text="Valor: ").grid(row=1, column=0)
        self.entry_valor = tk.Entry(self.root)
        self.entry_valor.grid(row=1, column=1)

        tk.Label(self.root, text="Quantidade: ").grid(row=2, column=0)
        self.entry_quantidade = tk.Entry(self.root)
        self.entry_quantidade.grid(row=2, column=1)

        # Botão para salvar

        btn_salvar = tk.Button(self.root, text="Salvar",
                               command=self.salvar_produto)
        btn_salvar.grid(row=3, column=1, pady=10)

        # Botão para limpar
        btn_limpar = tk.Button(self.root, text="Limpar",
                               command=self.limpar_produtos)
        btn_limpar.grid(row=3, column=2, padx=5)

    def salvar_produto(self):
        pass

    def limpar_produtos(self):
        pass
