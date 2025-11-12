class ProdutoVO:
# Pode ou não ter id_produtos no init
    # def __init__(self, nome, valor, quantidade, id_produtos=None):
    #     self.id_produtos = id_produtos
    #     self.nome = nome
    #     self.valor = valor 
    #     self.quantidade = quantidade 

    def __init__(self, nome, valor, quantidade):
        self.nome = nome
        self.valor = valor 
        self.quantidade = quantidade 

    def to_dict(self):
        return {"nome": self.nome,
                "valor": self.valor,
                "quantidade": self.quantidade
            }
    