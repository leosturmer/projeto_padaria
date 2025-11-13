class ProdutoVO:
    def __init__(self, nome, valor, quantidade, id_produtos=None):
        self.id_produtos = id_produtos
        self.nome = nome
        self.valor = valor 
        self.quantidade = quantidade 


    def to_dict(self):
        return {
                "id_produtos": self.id_produtos,
                "nome": self.nome,
                "valor": self.valor,
                "quantidade": self.quantidade
            }
    