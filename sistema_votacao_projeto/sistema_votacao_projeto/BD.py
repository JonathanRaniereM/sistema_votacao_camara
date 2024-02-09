from django.db import models
from django.contrib.auth.models import User

class Reuniao(models.Model):
    titulo = models.CharField(max_length=255)
    data_hora = models.DateTimeField()

    def __str__(self):
        return self.titulo

class Pauta(models.Model):
    titulo = models.CharField(max_length=1000)
    reuniao = models.ForeignKey(Reuniao, on_delete=models.CASCADE, related_name='pautas')

    def __str__(self):
        return self.titulo

class Vereador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_vereador = models.CharField(max_length=80)

    def __str__(self):
        return self.nome_vereador

class Presenca(models.Model):
    vereador = models.ForeignKey(Vereador, on_delete=models.CASCADE)
    reuniao = models.ForeignKey(Reuniao, on_delete=models.CASCADE)
    presenca = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.vereador} - {self.reuniao}'

class Voto(models.Model):
    VOTO_INEXISTENTE = 0
    VOTO_SIM = 1
    VOTO_NAO = 2
    VOTO_ABSTER = 3

    VOTO_CHOICES = (
        (VOTO_INEXISTENTE, 'Inexistente'),
        (VOTO_SIM, 'Sim'),
        (VOTO_NAO, 'Não'),
        (VOTO_ABSTER, 'Abster'),
    )

    vereador = models.ForeignKey(Vereador, on_delete=models.CASCADE)
    pauta = models.ForeignKey(Pauta, on_delete=models.CASCADE)
    voto = models.IntegerField(choices=VOTO_CHOICES, default=VOTO_INEXISTENTE)

    def __str__(self):
        return f'{self.vereador} - {self.pauta} - {self.get_voto_display()}'
    def __str__(self):
        return f'{self.vereador} - {self.pauta} - {self.voto}'