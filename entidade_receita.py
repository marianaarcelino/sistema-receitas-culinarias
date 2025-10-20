from pydantic import BaseModel

class Receita(BaseModel):

    id: int | None = None
    nome: str
    ingredientes: str
    modo_preparo: str
    tempo_preparo: int
    dificuldade: str
    categoria: str
    deleted: str = "False"

    def to_dict(self):
        # Converte o objeto Receita em dicionário (para salvar no CSV).
        return self.dict()

    @staticmethod
    def from_dict(dados: dict):
        # Cria uma instância de Receita a partir de um dicionário.
        return Receita(**dados)