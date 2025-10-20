from faker import Faker
from banco_receitas import MiniBancoCSV
from entidade_receita import Receita
import random

fake = Faker("pt_BR")

banco = MiniBancoCSV(
    "receitas.csv",
    "receitas.seq",
    ["nome", "ingredientes", "modo_preparo", "tempo_preparo", "dificuldade", "categoria"]
)

dificuldades = ["Fácil", "Média", "Difícil"]
categorias = ["Sobremesa", "Prato Principal", "Entrada", "Lanche"]

# --- DADOS EM PORTUGUÊS CRIADOS MANUALMENTE ---
nomes_base = ["Bolo", "Torta", "Mousse", "Salada", "Escondidinho", "Frango", "Peixe", "Sopa", "Pudim", "Feijoada"]
complementos = ["de Chocolate", "Cremoso", "na Manteiga", "com Cobertura", "Especial", "da Vovó", "Simples", "Rápida"]

ingredientes_base = [
    "farinha de trigo", "açúcar", "ovos", "leite", "manteiga", 
    "fermento em pó", "sal", "cebola", "alho", "tomate", 
    "azeite", "queijo muçarela", "carne moída", "frango desfiado", 
    "chocolate em pó", "creme de leite", "leite condensado", 
    "pimenta do reino", "manjericão", "arroz", "feijão", "batata"
]

passos_preparo = [
    "Misture todos os ingredientes secos em uma tigela grande.",
    "Bata os ovos com o açúcar até formar um creme claro.",
    "Adicione o leite e a manteiga derretida à mistura.",
    "Incorpore a farinha aos poucos e misture bem.",
    "Despeje a massa em uma forma untada e enfarinhada.",
    "Leve ao forno pré-aquecido a 180°C por 30 minutos.",
    "Refogue o alho e a cebola no azeite até dourarem.",
    "Adicione o ingrediente principal e deixe cozinhar por 10 minutos.",
    "Sirva quente com acompanhamento de sua preferência.",
    "Deixe esfriar antes de desenformar e finalizar com o recheio."
]
# ----------------------------------------------


for _ in range(1000):
    # Geração de Nome mais realista
    nome_receita_realista = f"{random.choice(nomes_base)} {random.choice(complementos)}"
    
    # Ingredientes: 5 a 10 itens aleatórios
    num_ingredientes = random.randint(5, 10)
    ingredientes_selecionados = random.sample(ingredientes_base, k=min(num_ingredientes, len(ingredientes_base)))
    
    # Modo de Preparo: 3 a 5 passos combinados
    num_passos = random.randint(3, 5)
    modo_preparo_selecionado = " ".join(random.sample(passos_preparo, k=num_passos))

    r = Receita(
        nome=nome_receita_realista,
        ingredientes=", ".join(ingredientes_selecionados),
        modo_preparo=modo_preparo_selecionado,
        tempo_preparo=random.randint(10, 120),
        dificuldade=random.choice(dificuldades),
        categoria=random.choice(categorias)
    )
    banco.insert(r.to_dict())

print("Banco populado com 1.000 receitas em português!")