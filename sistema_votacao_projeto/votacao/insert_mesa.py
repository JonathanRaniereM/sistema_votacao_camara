
from votacao.models import MesaDiretora

def handle():
    data = [
        ("MESA BIENIO 23/24"),

    ]
    
    for nome_mesa in data:
        print(f"Inserindo {nome_mesa}...")
        create_mesa(nome_mesa)

    print('Dados inseridos com sucesso!')

def create_mesa(nome_mesa):
    mesa = MesaDiretora(nome_mesa=nome_mesa)
    mesa.save()