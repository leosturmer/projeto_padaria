from ConexaoBanco import ConexaoBanco
from tkinter import messagebox
from mysql.connector import Error
from ProdutoVO import ProdutoVO

class ProdutoDAO:
    def __init__(self): # Método construtor
        self.conexao = ConexaoBanco().get_conexao()
        self.cursor = self.conexao.cursor()


    def cadastrar_produtos(self, produto_dict):
        sql = """INSERT INTO produtos (nome, valor, quantidade)
                VALUES (%s, %s, %s) 
                """
        valores = (produto_dict["nome"], produto_dict["valor"], produto_dict["quantidade"])

        
        self.cursor.execute(sql, valores)
        self.conexao.commit()

        # Depurando 
        print(f"Produto {produto_dict["nome"]} salvo com sucesso no banco de dados")


    def __del__(self): # Método destrutor
        self.cursor.close()
        self.conexao.close()

    # Função buscar_produtos

    def buscar_produtos(self):
        try:
            if self.conexao.is_connected():
                sql = "SELECT * FROM produtos;"
                self.cursor.execute(sql)
                rows = self.cursor.fetchall()

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
            messagebox.showerror("Erro!", f"Erro ao buscar produto: {e}")
        
        finally:
            if self.conexao.is_connected():
                self.conexao.close() 
            



class ProdutoVO:
    def __init__(self, id_produtos, nome, valor, quantidade):
        self.id_produtos = id_produtos
        self.nome = nome
        self.valor = valor
        self.quantidade = quantidade




