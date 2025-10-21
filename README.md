# API de Receitas Culinárias 🍰🍲

Projeto de uma API REST para gerenciar receitas culinárias, usando FastAPI, com um mini banco de dados em CSV e script para povoamento automático de 1.000 receitas fictícias.

## Estrutura do projeto
api_receitas.py         # API FastAPI com endpoints
banco_receitas.py       # Mini banco de dados CSV
entidade_receita.py     # Modelo da entidade Receita (Pydantic)
povoamento_receitas.py  # Script para gerar 1.000 receitas fictícias
receitas.csv            # Banco de dados inicial
receitas.seq            # Contador de IDs do banco
requirements.txt        # Bibliotecas necessárias

## Instalação

Clonar o repositório:

git clone <link-do-seu-repo>
cd <nome-da-pasta>


Criar e ativar ambiente virtual:

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate


Instalar dependências:

pip install -r requirements.txt

## Executando a API
uvicorn api_receitas:app --reload


- API rodando em: http://127.0.0.1:8000
- Documentação automática: http://127.0.0.1:8000/docs

## Funcionalidades

- Inserir, listar, obter, atualizar e deletar receitas
- Exportar banco em ZIP
- Gerar hashes (MD5, SHA1, SHA256)
- Vacuum: remover receitas deletadas permanentemente

## Povoamento do banco

Gerar 1.000 receitas fictícias:
python povoamento_receitas.py

## Dependências

- fastapi
- uvicorn
- pydantic
- faker
