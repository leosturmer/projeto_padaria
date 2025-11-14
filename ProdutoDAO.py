from ConexaoBanco import ConexaoBanco
from tkinter import messagebox
from mysql.connector import Error
from ProdutoVO import ProdutoVO

class ProdutoDAO:
    # def __init__(self): # Método construtor
    #     self.conexao = ConexaoBanco().get_conexao() # Obtendo a conexão no construtor

    #     # Verificando se a conexão é válida antes de tentar criar o cursor

    #     if self.conexao and self.conexao.is_connected():
    #         self.cursor = self.conexao.cursor()
    #     else:
    #         self.cursor = None


    def cadastrar_produtos(self, produto_dict):
        conexao = ConexaoBanco().get_conexao()
       
        if conexao is None or not conexao.is_connected():
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return

        cursor = conexao.cursor()
     
        try:
            sql = """INSERT INTO produtos (nome, valor, quantidade)
                VALUES (%s, %s, %s) 
                """
            valores = (produto_dict["nome"], produto_dict["valor"], produto_dict["quantidade"])

            cursor.execute(sql, valores)
            conexao.commit()
            # Depurando 
            print(f"Produto {produto_dict["nome"]} salvo com sucesso no banco de dados")
        except Error as e:
            messagebox.showerror("Erro de cadastro", f"Erro ao cadastrar produto: {e}")

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
            sql = """UPDATE produtos 
            SET nome = %s, valor = %s, quantidade = %s
            WHERE id_produtos = %s;"""

            valores = (produto_dict['nome'], produto_dict['valor'], produto_dict['quantidade'], produto_dict['id_produtos'])
        
            cursor.execute(sql, valores)
            conexao.commit()
            return cursor.rowcount > 0 # Retorna True se alguma linha for alterada
            
        except Error as e:
            messagebox.showerror("Erro de alteração", f"Erro ao alterar produto: {e}")
            return False
        
        finally:
            cursor.close()
            conexao.close()        

    def excluir_produto(self, id_produtos):
        conexao = ConexaoBanco().get_conexao()
        if conexao is None or not conexao.is_connected():
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
            return False

        cursor = conexao.cursor()
        try:
            sql = "DELETE FROM produtos WHERE id_produtos = %s"
            cursor.execute(sql, (id_produtos,))
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
            sql = "SELECT id_produtos, nome, valor, quantidade FROM produtos"
            cursor.execute(sql)
            rows = cursor.fetchall()

            produtos = []
            for row in rows:
                pVO = ProdutoVO(
                    id_produtos=row[0],
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
       


class ProdutoVO:
    def __init__(self, id_produtos, nome, valor, quantidade):
        self.id_produtos = id_produtos
        self.nome = nome
        self.valor = valor
        self.quantidade = quantidade




