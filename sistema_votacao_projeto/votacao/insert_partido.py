
from votacao.models import PartidoPolitico

def handle():
    data = [
        ("CIDADAN", "CIDADANIA"),
        ("PCdoB", "PARTIDO COMUNISTA DO BRASIL"),
        ("MDB", "PARTIDO DEMOCRATA BRASILEIRO"),
        ("PDT", "PARTIDO DEMOCRÁTICO TRABALHISTA"),
        ("PT", "PARTIDO DOS TRABALHADORES"),
        ("PP", "PARTIDO PROGRESSISTA"),
        ("PSC", "PARTIDO SOCIAL CRISTÃO"),
        ("PSD", "PARTIDO SOCIAL DEMOCRÁTICO"),
        ("PTB", "PARTIDO TRABALHISTA BRASILEIRO"),
        ("PV", "PARTIDO VERDE"),
        ("PATRIOTA", "PATRIOTA"),
        ("PODE", "PODEMOS"),
        ("REDE", "REDE"),
        ("PRB", "REPUBLICANOS"),
        ("SD", "SOLIDARIEDADE"),
        ("UNIAO BR", "UNIAO BRASIL"),
    ]
    
    for sigla, nome_partido in data:
        print(f"Inserindo {sigla}...")
        create_partido(sigla, nome_partido)

    print('Dados inseridos com sucesso!')

def create_partido(sigla, nome_partido):
    partido = PartidoPolitico(sigla=sigla, nome_partido=nome_partido)
    partido.save()