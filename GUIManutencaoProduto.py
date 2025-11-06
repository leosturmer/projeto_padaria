import tkinter as tk
from tkinter import ttk, messagebox

# from ProdutoDAO import ProdutoDAO

class ManutencaoProduto:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Manutenção de Produtos")
        self.janela.geometry("600x200")

        self.tree = ttk.Treeview(janela, columns=("nome", "valor", "quantidade"), show="headings")

        self.tree.heading(column="nome", text="Nome")
        self.tree.heading(column="valor", text="Valor")
        self.tree.heading(column="quantidade", text="Quantidade")


        self.tree.pack(fill=tk.BOTH, expand=True)



        # self.dao = ProdutoDAO()
        # self.preencher_tabela(self)

    def excluir_produto_selecionado(self):
        item_selecionado = self.tree.selection()

        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto para excluir.")
            return
        
        # A TreeView só tem nome, valor e quantidade.
        # Para excluir, você precisa do ID
        # Você teria que armazenar o ID do produto junto com os dados ou buscar o ID.

        # Assumindo que você armazenou o ID como um valor oculto no 'item_selecionado'

        id_produto = self.tree.item(item_selecionado, "tags")[0]
        nome_produto = self.tree.item(item_selecionado, "values")[0]

        if messagebox.askyesno("Confirmação", f"Deseja realmente excluir o produto '{nome_produto}?"):
            if self.dao.excluir_produto(id_produto):
                messagebox.showinfo("Sucesso", "Produto excluído com sucesso.")
                self.limpar_tabela()
                self.preencher_tabela()

            # Se self.dao.excluir_produto falhar, uma mensagem de erro já será mostrada pelo DAO.

    def limpar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
    