from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from votacao.models import Vereador

class Command(BaseCommand):
    help = 'Insert vereadores into the database'

    def handle(self, *args, **kwargs):
        data = [
            ("Aldair Fagundes", "aldair", "123456", "CIDADAN"),
            ("Cecília Meireles", "cecilia", "123456", "PP"),
            ("Cláudio Rodrigues", "claudio", "123456", "Rede"),
            ("Daniel Dias", "daniel", "123456", "PCdoB"),
            ("Edmílson Bispo", "edmilson", "123456", "PSD"),
            ("Edson Cabeleireiro", "edson", "123456", "PV"),
            ("Elair Gomes", "elair", "123456", "MDB"),
            ("Eldair Samambaia", "eldair", "123456", "PSD"),
            ("Igor Dias", "igor", "123456", "UNIÃO BRASIL"),
            ("Julinha da Pastoral", "julia", "123456", "PODE"),#LEMBRAR DE ALTERAR ESSE USER PARA "STALIN"
            ("Leãozinho", "leaozinho", "123456", "PATRIOTA"),
            ("Marcos Nem", "marcos", "123456", "PSC"),
            ("Maria Helena", "maria", "123456", "MDB"),
            ("Maria das Graças", "graca", "123456", "UNIÃO BRASIL"),
            ("Marlus do Independência","marlus","123456","PT"),
            ("Martins Lima", "junior", "123456", "CIDADANIA"),
            ("Odair Ferreira", "odair", "123456", "SOLIDARIEDADE"),
            ("Iara Pimentel", "iara", "123456", "PT"),
            ("Raimundo Pereira", "raimundo", "123456", "PDT"),
            ("Reinaldo Barbosa", "reinaldo", "123456", "PRB"),
            ("Rodrigo Cadeirante", "rodrigo", "123456", "REDE"),
            ("Valdecy Contador", "valdecy", "123456", "CIDADANIA"),
            ("Wilton Dias", "wilton", "123456", "PTB")
        ]
        for nome, username, password, partido in data:
            self.stdout.write(f"Inserindo {nome}...")  # Use self.stdout.write em vez de print
            self.create_vereador(nome, username, password, partido)

        self.stdout.write(self.style.SUCCESS('Dados inseridos com sucesso!'))

    @staticmethod
    def create_vereador(nome, username, password, partido):
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()

        vereador = Vereador(user=user, nome_vereador=nome, partido_politico=partido)
        vereador.save()
