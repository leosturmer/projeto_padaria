import tkinter as tk
from tkinter import messagebox
from decimal import Decimal
from ProdutoVO import ProdutoVO

class CadastroProdutos:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Produtos")
        self.root.geometry("270x150")



