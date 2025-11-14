-- Criação do banco de dados
CREATE DATABASE padaria;

USE padaria;

CREATE TABLE produtos(
   idprodutos INT AUTO_INCREMENT PRIMARY KEY,
   nome VARCHAR(50) NOT NULL,
   valor DECIMAL,
   quantidade INT
);

CREATE TABLE login(
   idlogin INT PRIMARY KEY AUTO_INCREMENT,
   login VARCHAR(50) NOT NULL,
   senha VARCHAR(255) NOT NULL
);

INSERT INTO login (idlogin, login, senha)
VALUES (null, 'admin', SHA2('123', 256) );


CREATE TABLE perfil(
   idperfil INT AUTO_INCREMENT PRIMARY KEY,
   nomeperfil VARCHAR(15) NOT NULL
);


INSERT INTO perfil VALUES
   (null, 'admin'),
   (null, 'usuario');


-- Adicionando a coluna 'perfil' na tabela 'login'
ALTER TABLE login ADD COLUMN perfil INT;


-- Adicionando a chave estrangeira (FOREIGN KEY) e incluir a cláusula ON DELETE CASCADE.
-- Isso significa que se um registro em 'perfil' for deletado, todos os registros em 'login que fazem referencia a ele também serão automaticamente deletados.

ALTER TABLE login
ADD FOREIGN KEY(perfil)
REFERENCES perfil(idperfil)
ON DELETE CASCADE;
 
--Atualiza o registro de login para ter o perfil 'admin' (idperfil = 1)
UPDATE login SET perfil = 1;

#############################################

# ConexaoBanco.py

#  pip install mysql-connector-python

# python.exe -m pip install --upgrade pip

import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

class ConexaoBanco:
    def get_conexao(self):
        conexao = None
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                database='padaria',
                user='root',
                password=''
            )
            if conexao.is_connected():
                print("Conectado ao MySQL")
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao conectar! {e}")
        return conexao


################################################

import tkinter as tk
from tkinter import ttk, messagebox
from ConexaoBanco import ConexaoBanco
from GUIMenu import MenuGUI

import hashlib 

class LoginGUI:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Tela de Login")

        # Frame para organizar os elementos
        self.frame = tk.Frame(janela, padx= 40, pady=40)
        self.frame.pack()

        # Label e Entry para Login
        self.label_login = tk.Label(self.frame, text="Login: ")
        self.label_login.grid(row=0, column=0, sticky=tk.W)
        self.entry_login = tk.Entry(self.frame)
        self.entry_login.grid(row=0, column=1)

        # Label e Entry para senha
        self.label_senha = tk.Label(self.frame, text="senha: ")
        self.label_senha.grid(row=1, column=0, sticky=tk.W)
        self.entry_senha = tk.Entry(self.frame, show="*")
        self.entry_senha.grid(row=1, column=1)

        # Label e ComboBox para perfil
        self.label_perfil = tk.Label(self.frame, text="Perfil: ")
        self.label_perfil.grid(row=2, column=0, sticky=tk.W)
        self.combobox_perfil = ttk.Combobox(self.frame, state="readonly")
        self.combobox_perfil.grid(row=2, column=1)

        # Botão de login
        self.button_login = tk.Button(self.frame, text="Login", command=self.verificar_login)
        self.button_login.grid(row=3, columnspan=2, pady=10)

        # Conectar com o Banco de Dados para preencher o ComboBox com os perfis
        self.carregar_perfis()


    # Populando o ComboBox
    def carregar_perfis(self):
        try:
            conexao = ConexaoBanco().get_conexao()
            # print("Conectado ao MySQL")
            cursor = conexao.cursor()

            # Consulta para obter os perfis em ordem alfabética
            query = "SELECT idperfil, nomeperfil FROM perfil ORDER BY nomeperfil"
            cursor.execute(query)
            resultados = cursor.fetchall()

            # Preencher o ComboBox com os perfis e garantindo que idperfil seja int
            self.perfis = {row[1]: int(row[0]) for row in resultados}
            self.combobox_perfil['values'] = list(self.perfis.keys() )

            # Fechar o cursor e a conexão
            cursor.close()
            conexao.close()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar perfis: {e}")


    # Verificando a Autenticação
    def verificar_login(self):
        login = self.entry_login.get().strip() # .strip() é usado para remover os espaços no inicio ou final da string
        senha = self.entry_senha.get().strip()
        nomeperfil = self.combobox_perfil.get().strip()

        # Verificando se as variáveis Login, senha e perfil estão vazias
        if not login or not senha or not nomeperfil:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return


        idperfil = self.perfis.get(nomeperfil)
        if idperfil is None:
            messagebox.showerror("Erro", "Perfil inválido!")
            return
        
        # Gerar hash SHA-256 da senha digitada
        senha_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()


        # Verificação dos valores antes da consulta
        # print(f"Login: {login}, Senha: {senha}, Perfil: {nomeperfil} (ID: {idperfil}) " )


   
        try:
            # Conexão com Banco de Dados
            conexao = ConexaoBanco().get_conexao()
            cursor = conexao.cursor()

            # Consulta para verificar o login, senha e perfil
            query = "SELECT * FROM login WHERE login = %s AND senha = %s AND perfil = %s "
            cursor.execute(query, (login, senha_hash, idperfil) )
            resultado = cursor.fetchone()

            # print(f"Resultado da consulta: {resultado}") # Adicionando depuração

            if resultado:
                messagebox.showinfo(f"Login bem-sucedido", f"Bem vindo, {login}!")
                self.janela.withdraw() # Fecha a janela de login
                self.abrir_menu_principal()
            else:
                messagebox.showerror("Erro de login", "Login, senha ou perfil incorretos!")

            cursor.close()
            conexao.close()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar login: {e}")


    def abrir_menu_principal(self):
        MenuGUI()





if __name__ == "__main__":
    janela = tk.Tk()
    app = LoginGUI(janela)
    janela.mainloop()    


#############################################


import tkinter as tk
from GUICadastroProdutos import CadastroProdutos
from GUIManutencaoProduto import ManutencaoProdutos


class MenuGUI(tk.Tk):
    def __init__(self):
        super().__init__() # Inicializa a classe base tk.Tk
        self.title("Sistema de Gerenciamento de cadastro")
        self.geometry("450x400")


        menu_principal = tk.Menu(self)
        self.config(menu=menu_principal)

        # Adicionando os itens de menu
        menu_arq = tk.Menu(menu_principal)
        menu_principal.add_cascade(label='Cadastro', menu=menu_arq)

        # Adicionando submenus ao Menu
        menu_arq.add_command(label='Clientes')
        menu_arq.add_command(label='Colaboradores')
        menu_arq.add_command(label='Fornecedores')
        menu_arq.add_separator()
        menu_arq.add_command(label='Produtos', command=self.abrir_CadProdutos)


        # Adicionando outro Menu e submenus
        menu_Manutencao = tk.Menu(menu_principal)
        menu_principal.add_cascade(label='Manutenção', menu= menu_Manutencao)
        menu_Manutencao.add_command(label='Clientes')
        menu_Manutencao.add_command(label='Colaboradores')
        menu_Manutencao.add_command(label='Fornecedores')
        menu_Manutencao.add_separator()
        menu_Manutencao.add_cascade(label='Produtos', command=self.abrir_ManuProdutos)

        menu_sair = tk.Menu(menu_principal)
        menu_principal.add_cascade(label='Sair', command=self.sair)


    # Criando o Menu
    def abrir_CadProdutos(self):
        menu_window = tk.Toplevel(self)
        CadastroProdutos(menu_window)

    def abrir_ManuProdutos(self):
        menu_window = tk.Toplevel(self)
        ManutencaoProdutos(menu_window)

    def sair(self):
        self.destroy()







if __name__ == "__main__":
    app = MenuGUI()
    app.mainloop()


######################################


# ProdutoVO.py

class ProdutoVO:
    def __init__(self, nome, valor, quantidade, idprodutos=None):
        self.idprodutos = idprodutos
        self.nome = nome
        self.valor = valor
        self.quantidade = quantidade

    def to_dict(self):
        return {
            "idprodutos": self.idprodutos,
            "nome": self.nome,
            "valor": self.valor,
            "quantidade": self.quantidade
        }


################################


# ProdutoDAO.py

from ConexaoBanco import ConexaoBanco
from tkinter import messagebox
from mysql.connector import Error
from ProdutoVO import ProdutoVO


class ProdutoDAO:

    def cadastrar_produtos(self, produto_dict):
        conexao = ConexaoBanco().get_conexao()
        if conexao is None or not conexao.is_connected():
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return

        cursor = conexao.cursor()
        try:
            sql = "INSERT INTO produtos(nome, valor, quantidade) VALUES(%s, %s, %s)"
            valores = (produto_dict['nome'], produto_dict['valor'], produto_dict['quantidade'])
            cursor.execute(sql, valores)
            conexao.commit()
            print(f"Produto {produto_dict['nome']} salvo com sucesso no banco de dados")
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar produto: {e}")
        finally:
            cursor.close()
            conexao.close()

    def alterar_produto(self, produto_dict):
        conexao = ConexaoBanco().get_conexao()
        if conexao is None or not conexao.is_connected():
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return False

        cursor = conexao.cursor()
        try:
            sql = "UPDATE produtos SET nome=%s, valor=%s, quantidade=%s WHERE idprodutos=%s"
            valores = (produto_dict['nome'], produto_dict['valor'], produto_dict['quantidade'], produto_dict['idprodutos'])
            cursor.execute(sql, valores)
            conexao.commit()
            # Retorna True se pelo menos uma linha foi afetada
            return cursor.rowcount > 0
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao alterar produto: {e}")
            return False
        finally:
            cursor.close()
            conexao.close()

    def excluir_produto(self, idprodutos):
        conexao = ConexaoBanco().get_conexao()
        if conexao is None or not conexao.is_connected():
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return False

        cursor = conexao.cursor()
        try:
            sql = "DELETE FROM produtos WHERE idprodutos = %s"
            cursor.execute(sql, (idprodutos,))
            conexao.commit()
            # Retorna True se pelo menos uma linha foi afetada
            return cursor.rowcount > 0
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao excluir produto: {e}")
            return False
        finally:
            cursor.close()
            conexao.close()

    # Função BuscarProduto
    def buscar_produtos(self):
        conexao = ConexaoBanco().get_conexao()
        if conexao is None or not conexao.is_connected():
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return []

        cursor = conexao.cursor()
        try:
            sql = "SELECT idprodutos, nome, valor, quantidade FROM produtos"
            cursor.execute(sql)
            rows = cursor.fetchall()

            produtos = []
            for row in rows:
                pVO = ProdutoVO(
                    idprodutos=row[0],
                    nome=row[1],
                    valor=row[2],
                    quantidade=row[3]
                )
                produtos.append(pVO)
            return produtos
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao buscar produtos: {e}")
            return []
        finally:
            cursor.close()
            conexao.close()

#########################################

import tkinter as tk
from tkinter import messagebox
from decimal import Decimal
from ProdutoVO import ProdutoVO

class CadastroProdutos:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Produtos")
        self.root.geometry('300x150')

        #Labels e Enradas para os dados dos produtos
        tk.Label(self.root, text="Nome: ").grid(row=0, column=0)
        self.entry_nome = tk.Entry(self.root)
        self.entry_nome.grid(row=0, column=1)

        tk.Label(self.root, text="Valor: ").grid(row=1, column=0)
        self.entry_valor = tk.Entry(self.root)
        self.entry_valor.grid(row=1, column=1)

        tk.Label(self.root, text="Quantidade: ").grid(row=2, column=0)
        self.entry_quantidade = tk.Entry(self.root)
        self.entry_quantidade.grid(row=2, column=1)

        # Botão para Salvar
        btn_salvar = tk.Button(self.root, text="Salvar", command=self.salvar_produtos)
        btn_salvar.grid(row=3, column=1, pady=10)

        # Botão para limpar
        btn_limpar = tk.Button(self.root, text="Limpar", command=self.limpar_produtos)
        btn_limpar.grid(row=3, column=2, padx=10)


    def salvar_produtos(self):
        # Importação movida para dentro da função para evitar circularidade
        from ProdutoDAO import ProdutoDAO


        try:
            nome = self.entry_nome.get().strip()
            valor = Decimal(self.entry_valor.get().strip() )
            quantidade = int(self.entry_quantidade.get().strip() )
        except Exception:
            messagebox.showerror("Erro de Entrada", "Verifique se o valor e a Quantidade estão preenchido corretamente.")
            return

        # Criando uma instância do ProdutoVO (Note que não passamos idprodutos)
        pVO = ProdutoVO(nome, valor, quantidade)

        # Salvando os produtos no Banco de Dados ou eibindo os dados
        pDAO = ProdutoDAO()
        pDAO.cadastrar_produtos(pVO.to_dict() )
        messagebox.showinfo("Produto Salvo",f"Produto {nome} salvo com sucesso!" )
        self.limpar_produtos() 


    def limpar_produtos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)

########################################

# GUIManutencaoProduto.py

import tkinter as tk
from tkinter import ttk, messagebox
from ProdutoDAO import ProdutoDAO
from ProdutoVO import ProdutoVO
from decimal import Decimal

class ManutencaoProdutos:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Manutenção de Produtos")
        self.janela.geometry("700x400")

        # Dicionário para mapear itens do Treeview ao ID do produto
        self.item_to_id = {}

        # Frame para a janela
        frame_tabela = tk.Frame(janela)
        frame_tabela.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Criando os Widgets
        # Apenas as colunas visíveis: nome, valor, quantidade
        self.tree = ttk.Treeview(janela, columns=("nome", "valor", "quantidade"), show='headings')
        self.tree.heading("nome", text="Nome")
        self.tree.column("nome", width=250)
        self.tree.heading("valor", text="Valor")
        self.tree.column("valor", width=100, anchor=tk.E)
        self.tree.heading("quantidade", text="Quantidade")
        self.tree.column("quantidade", width=100, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_produto)

        # Frame para os campos de alteração
        frame_campos = tk.LabelFrame(janela, text="Dados do Produto Selecionado", padx=10, pady=10)
        frame_campos.pack(pady=10, padx=10, fill=tk.X)

        # Campo de entrada de Alteração
        tk.Label(frame_campos, text="Nome: ").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_nome = tk.Entry(frame_campos, width=30)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_campos, text="Valor: ").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.entry_valor = tk.Entry(frame_campos, width=15)
        self.entry_valor.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_campos, text="Quantidade: ").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.entry_quantidade = tk.Entry(frame_campos, width=15)
        self.entry_quantidade.grid(row=0, column=5, padx=5, pady=5)

        # Variável para armazenar o ID do produto selecionado
        self.produto_selecionado_id = None

        # Frame para os botões de ação
        frame_botoes = tk.Frame(janela)
        frame_botoes.pack(pady=10)

        # Botões
        btn_alterar = tk.Button(frame_botoes, text="Alterar Produto", command=self.alterar_produto)
        btn_alterar.pack(side=tk.LEFT, padx=10)

        btn_excluir = tk.Button(frame_botoes, text="Excluir Produto", command=self.excluir_produto)
        btn_excluir.pack(side=tk.LEFT, padx=10)

        self.pDAO = ProdutoDAO()
        self.preecher_tabela()

    # Função para limpar os campos
    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.produto_selecionado_id = None

    # Função que preenche os campos com o item selecionado
    def selecionar_produto(self, event):
        self.limpar_campos()
        item_selecionado = self.tree.focus()
        if item_selecionado:
            # Recupera o ID do produto a partir do item do Treeview
            self.produto_selecionado_id = self.item_to_id.get(item_selecionado)
            if self.produto_selecionado_id:
                valores = self.tree.item(item_selecionado, 'values')
                if valores:
                    self.entry_nome.insert(0, valores[0])
                    self.entry_valor.insert(0, valores[1])
                    self.entry_quantidade.insert(0, valores[2])

    def preecher_tabela(self):
        # Limpa a tabela e o mapeamento antes de preencher novamente
        self.tree.delete(*self.tree.get_children())
        self.item_to_id.clear()

        try:
            produtos = self.pDAO.buscar_produtos()
            for produto in produtos:
                # Insere apenas os dados visíveis na tabela
                item_id = self.tree.insert("", "end", values=(produto.nome, produto.valor, produto.quantidade))
                # Mapeia o item do Treeview ao ID real do produto
                self.item_to_id[item_id] = produto.idprodutos
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao preencher a tabela: {e}")

    def alterar_produto(self):
        if not self.produto_selecionado_id:
            messagebox.showwarning("Aviso", "Selecione um produto na tabela para alterar.")
            return

        try:
            nome = self.entry_nome.get().strip()
            valor = Decimal(self.entry_valor.get().strip())
            quantidade = int(self.entry_quantidade.get().strip())
        except:
            messagebox.showerror("Erro", "Verifique se Valor e Quantidade são números válidos.")
            return

        if not nome or not valor or not quantidade:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        # Cria um ProdutoVO com o ID selecionado
        pVO = ProdutoVO(nome, valor, quantidade, idprodutos=self.produto_selecionado_id)

        if self.pDAO.alterar_produto(pVO.to_dict()):
            messagebox.showinfo("Sucesso", f"Produto ID {self.produto_selecionado_id} alterado com sucesso!")
            self.preecher_tabela()
            self.limpar_campos()
        else:
            messagebox.showerror("Erro", "Falha ao alterar o produto ou nenhum dado foi modificado.")

    def excluir_produto(self):
        if not self.produto_selecionado_id:
            messagebox.showwarning("Aviso", "Selecione um produto na tabela para excluir.")
            return

        # Confirmação de exclusão
        resposta = messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o produto ID {self.produto_selecionado_id}?")
        if resposta:
            if self.pDAO.excluir_produto(self.produto_selecionado_id):
                messagebox.showinfo("Sucesso", f"Produto ID {self.produto_selecionado_id} excluído com sucesso!")
                self.preecher_tabela()
                self.limpar_campos()
            else:
                messagebox.showerror("Erro", "Falha ao excluir o produto.")

###################################################



















