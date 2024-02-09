from datetime import datetime
from votacao.models import Vereador



def update_vereador_data():
    # Crie uma lista com as informações fornecidas
    data = [
        {'nome_completo': 'Aldair Fagundes Brito', 'data_nascimento': '14/09/1970', 'sexo': 'Masculino'},
        {'nome_completo': 'Cecília Meireles Ferreira', 'data_nascimento': '17/08/1985', 'sexo': 'Feminino'},
        {'nome_completo': 'Cláudio Rodrigues de Jesus', 'data_nascimento': '12/12/1974', 'sexo': 'Masculino'},
        {'nome_completo': 'Daniel Dias Da Silva', 'data_nascimento': '29/04/1982', 'sexo': 'Masculino'},
        {'nome_completo': 'Edmílson Bispo dos Santos', 'data_nascimento': '12/02/1970', 'sexo': 'Masculino'},    
        {'nome_completo': 'Edson Pereira Dos Santos', 'data_nascimento': '12/02/1982', 'sexo': 'Masculino'},
        {'nome_completo': 'Elair Augusto Pimentel Gomes', 'data_nascimento': '17/04/1967', 'sexo': 'Masculino'},
        {'nome_completo': 'Eldair Gonçalves Dos Santos', 'data_nascimento': '01/11/1970', 'sexo': 'Masculino'},
        {'nome_completo': 'Igor Gustavo Dias', 'data_nascimento': '02/09/1981', 'sexo': 'Masculino'},
        {'nome_completo': 'Manoel Stálin Costa Cordeiro', 'data_nascimento': '30/12/1985', 'sexo': 'Masculino'},
        {'nome_completo': 'Heudes da Silva Siqueira', 'data_nascimento': '12/04/1992', 'sexo': 'Masculino'},
        {'nome_completo': 'José Marcos Martins Freitas', 'data_nascimento': '24/02/1968', 'sexo': 'Masculino'},
        {'nome_completo': 'Maria Helena De Quadros Lopes', 'data_nascimento': '14/02/1972', 'sexo': 'Feminino'},
        {'nome_completo': 'Maria das Graças Gonçalves Dias', 'data_nascimento': '21/11/1968', 'sexo': 'Feminino'},
        {'nome_completo': 'Marlus Mendes Soares', 'data_nascimento': '30/07/1976', 'sexo': 'Masculino'},
        {'nome_completo': 'Martins Lima Filho', 'data_nascimento': '20/10/1978', 'sexo': 'Masculino'},
        {'nome_completo': 'Odair Ferreira Oliveira', 'data_nascimento': '10/09/1971', 'sexo': 'Masculino'},
        {'nome_completo': 'Iara de Fatima Pimentel Veloso', 'data_nascimento': '16/09/1969', 'sexo': 'Feminino'},
        {'nome_completo': 'Raimundo Pereira da Silva', 'data_nascimento': '03/10/1947', 'sexo': 'Masculino'},
        {'nome_completo': 'Reinaldo Barbosa Da Silva', 'data_nascimento': '08/11/1966', 'sexo': 'Masculino'},
        {'nome_completo': 'Rodrigo Maia de Oliveira', 'data_nascimento': '19/05/1980', 'sexo': 'Masculino'},
        {'nome_completo': 'Valdecy Fagundes De Oliveira', 'data_nascimento': '14/07/1965', 'sexo': 'Masculino'},
        {'nome_completo': 'Wilton Afonso Dias Soares', 'data_nascimento': '01/04/1973', 'sexo': 'Masculino'},
    ]

    # Comece com o id=2
    current_id = 2

    # Convertendo os valores completos para as abreviações correspondentes
    def convert_sex_to_abbr(sexo):
        if sexo == "Masculino":
            return 'M'
        elif sexo == "Feminino":
            return 'F'
        else:
            # Caso algum outro valor seja fornecido, retorne None ou levante um erro
            return None

    # Atualize cada parlamentar
    for item in data:
        vereador = Vereador.objects.get(id=current_id)
        vereador.nome_completo = item['nome_completo']
        vereador.data_nascimento = datetime.strptime(item['data_nascimento'], '%d/%m/%Y').date()
        vereador.sexo = convert_sex_to_abbr(item['sexo'])
        vereador.save()
        current_id += 1



