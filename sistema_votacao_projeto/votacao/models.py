from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator



from django.core.exceptions import ValidationError

def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] retorna path+filename
    valid_extensions = ['.png', '.jpg', '.jpeg', '.svg']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')


    
class MesaDiretora(models.Model):
    nome_mesa = models.CharField(max_length=255, null=True)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    

    def __str__(self):
        return self.nome_mesa
    
class PartidoPolitico(models.Model):
    sigla = models.CharField(max_length=20, null=True)  # Definindo um tamanho máximo de 10 caracteres para a sigla.
    nome_partido = models.CharField(max_length=255, null=True)
    logo = models.FileField(upload_to='logo_partido/', null=True, validators=[validate_file_extension])


    def __str__(self):
        return f"{self.sigla} - {self.nome_partido}"

class Vereador(models.Model):
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nome_vereador = models.CharField(max_length=80)
    nome_completo = models.CharField(max_length=255, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=True, blank=True)
    partido = models.ForeignKey(PartidoPolitico, on_delete=models.SET_NULL, null=True)   # Chave estrangeira vinculando a um partido político
    foto = models.ImageField(upload_to='vereadores_fotos/', null=True)
    funcao_mesa_diretora = models.CharField(max_length=255, null=True, blank=True)
    mesa = models.ForeignKey(MesaDiretora, on_delete=models.SET_NULL, null=True, blank=True)   # Chave estrangeira vinculando a uma mesa diretora

    def __str__(self):
        return self.nome_vereador
    
    
from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models.signals import post_save

class GroupConfig(models.Model):
    grupo = models.OneToOneField(Group, on_delete=models.CASCADE)
    atual = models.BooleanField(default=False)
    
@receiver(pre_save, sender=GroupConfig)
def ensure_single_current_group(sender, instance, **kwargs):
    if instance.atual:
        GroupConfig.objects.exclude(id=instance.id).update(atual=False)
        
@receiver(post_save, sender=Group)
def create_group_config(sender, instance, created, **kwargs):
    if created:  # Apenas se o objeto Group for criado, não atualizado
        GroupConfig.objects.create(grupo=instance)



class Reuniao(models.Model):
    
    TIPO_REUNIAO_ORDINARIA = 'Ordinária'
    TIPO_REUNIAO_EXTREORDINARIA = 'Extraordinária'
    TIPO_REUNIAO_ESPECIAL = 'Especial'
    TIPO_REUNIAO_ELEICAO = 'Eleição'
    TIPO_REUNIAO_SOLENE = 'Solene'
    TIPO_REUNIAO_DEBATE = 'Debate'
    TIPO_REUNIAO_PREPARATORIA = 'Preparatoria'
    TIPO_REUNIAO_CONJUNTA = 'Conjunta'
    TIPO_REUNIAO_REGIONAL = 'Regional'
    TIPO_REUNIAO_PLENARIO = 'Plénario'
    TIPO_REUNIAO_OUTRO = 'Outro'

                
    
    TIPO_REUNIAO_CHOICES = (
        (TIPO_REUNIAO_ORDINARIA, 'Ordinária'),
        (TIPO_REUNIAO_EXTREORDINARIA, 'Extraordinária'),
        (TIPO_REUNIAO_ESPECIAL, 'Especial'),
        (TIPO_REUNIAO_ELEICAO, 'Eleição'),
        (TIPO_REUNIAO_SOLENE, 'Solene'),
        # Novos tipos de reunião
        (TIPO_REUNIAO_DEBATE, 'Debate'),
        (TIPO_REUNIAO_PREPARATORIA, 'Preparatoria'),
        (TIPO_REUNIAO_CONJUNTA, 'Conjunta'),
        (TIPO_REUNIAO_REGIONAL, 'Regional'),
        (TIPO_REUNIAO_PLENARIO, 'Plénario'),
        (TIPO_REUNIAO_OUTRO, 'Outro'),
    )
    
    # Status
    STATUS_PREVISTA = 'Prevista'
    STATUS_ABERTA = 'Aberta'
    STATUS_REALIZADA = 'Realizada'

    STATUS_CHOICES = (
        (STATUS_PREVISTA, 'Prevista'),
        (STATUS_ABERTA, 'Aberta'),
        (STATUS_REALIZADA, 'Realizada'),
    )
    
    titulo = models.CharField(max_length=255)
    data_prevista = models.DateTimeField()
    numero_reuniao = models.IntegerField(null=True)
    tipo_reuniao = models.CharField(max_length=20, choices=TIPO_REUNIAO_CHOICES,null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PREVISTA)

    def __str__(self):
        return self.titulo


class ParametrosVotacao(models.Model):
    nome_parametro = models.CharField(max_length=255)
    quorun_aprovacao = models.IntegerField()  # Quantidade mínima de votos "SIM" para aprovação.
    quorun_validacao = models.IntegerField()  # Quantidade mínima de vereadores presentes para pauta ser considerada aprovada.

    def __str__(self):
        return self.nome_parametro
    
class TipoAcao(models.Model):
    CATEGORIA_PREJUDICADA = 'Prejudicada'
    CATEGORIA_APROVADA = 'Aprovada'
    CATEGORIA_REPROVADA = 'Reprovada'
    CATEGORIA_EMPATADA = 'Empatada'
    CATEGORIA_NAO_REALIZADA = 'Não Realizada'
    CATEGORIA_EM_ANDAMENTO = 'Em Andamento'
    
    CATEGORIA_CHOICES = (
        (CATEGORIA_PREJUDICADA, 'Prejudicada'),
        (CATEGORIA_APROVADA, 'Aprovada'),
        (CATEGORIA_REPROVADA, 'Reprovada'),
        (CATEGORIA_EMPATADA, 'Empatada'),
        (CATEGORIA_NAO_REALIZADA, 'Não Realizada'),
        (CATEGORIA_EM_ANDAMENTO, 'Em Andamento'),
    )

    nome_acao = models.CharField(max_length=255)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)

    def __str__(self):
        return f'{self.nome_acao} - {self.categoria}'


class Pauta(models.Model):
    
    # Status
    STATUS_PREVISTA = 'Prevista'
    STATUS_ABERTA = 'Aberta'
    STATUS_REALIZADA = 'Realizada'

    STATUS_VOTACAO_CHOICES = (
        (STATUS_PREVISTA, 'Prevista'),
        (STATUS_ABERTA, 'Aberta'),
        (STATUS_REALIZADA, 'Realizada'),
    )
    
    titulo = models.CharField(max_length=1000)
    reuniao = models.ForeignKey(Reuniao, on_delete=models.CASCADE, related_name='pautas')
    parametros_votacao = models.ForeignKey(ParametrosVotacao, on_delete=models.SET_NULL,null=True, blank=True, related_name='pautas')
    resultado = models.ForeignKey(TipoAcao, on_delete=models.SET_NULL, null=True, blank=True, related_name='pautas')
    status_votacao = models.CharField(max_length=10, choices=STATUS_VOTACAO_CHOICES, default=STATUS_PREVISTA)
    data_realizacao = models.DateTimeField(null=True, blank=True)
    ementa = models.CharField(max_length=2000, null=True, blank=True)
    # Adicionando a coluna 'autor' que é uma chave estrangeira para a coluna 'vereador'
    autor = models.ForeignKey(Vereador, on_delete=models.SET_NULL, null=True, blank=True, related_name='pautas_autoradas')
    # Adicionando a coluna 'documento' para armazenar links de documentos (PDF)
    documento = models.URLField(validators=[URLValidator()], blank=True, null=True)
    resultado_categoria = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        if self.status_votacao == Pauta.STATUS_ABERTA:
            pauta_aberta_existente = Pauta.objects.filter(status_votacao=Pauta.STATUS_ABERTA).exclude(pk=self.pk).exists()
            if pauta_aberta_existente:
                raise ValidationError('Já existe uma pauta com o status "Aberta". Não é possível abrir outra.')
        
        if self.resultado_categoria:
            # Encontre o TipoAcao com base na categoria fornecida
            try:
                tipo_acao = TipoAcao.objects.get(categoria=self.resultado_categoria)
                self.resultado = tipo_acao
            except TipoAcao.DoesNotExist:
                # Lidar com o caso de não encontrar o TipoAcao correspondente
                pass


        # Se o status da votação é "Prevista" e o resultado não está definido, definimos como "Não Realizada"
        if self.status_votacao == Pauta.STATUS_PREVISTA and not self.resultado:
            nao_realizada = TipoAcao.objects.get(categoria=TipoAcao.CATEGORIA_NAO_REALIZADA)
            self.resultado = nao_realizada

        # Se o status da votação é "Aberta" e o resultado não está definido, definimos como "Em Andamento"
        elif self.status_votacao == Pauta.STATUS_ABERTA and not self.resultado:
            em_andamento = TipoAcao.objects.get(categoria=TipoAcao.CATEGORIA_EM_ANDAMENTO)
            self.resultado = em_andamento

        # Se o status da votação é "Realizada", verificamos se cumpre os parâmetros para ser "Aprovada" ou "Reprovada"
        elif self.status_votacao == Pauta.STATUS_REALIZADA and self.parametros_votacao:
            total_presentes = Presenca.objects.filter(reuniao=self.reuniao, presenca=True).count()

            # Se o quórum de validação não for atendido, definimos o resultado como "Prejudicada"
            if total_presentes < self.parametros_votacao.quorun_validacao:
                self.resultado = TipoAcao.objects.get(categoria=TipoAcao.CATEGORIA_PREJUDICADA)
            else:
                total_votos_sim = Voto.objects.filter(pauta=self, voto=Voto.VOTO_SIM).count()

                if total_votos_sim >= self.parametros_votacao.quorun_aprovacao:
                    self.resultado = TipoAcao.objects.get(categoria=TipoAcao.CATEGORIA_APROVADA)
                else:
                    self.resultado = TipoAcao.objects.get(categoria=TipoAcao.CATEGORIA_REPROVADA)

        super(Pauta, self).save(*args, **kwargs)


    
class Presenca(models.Model):
    vereador = models.ForeignKey(Vereador, on_delete=models.CASCADE)
    reuniao = models.ForeignKey(Reuniao, on_delete=models.CASCADE)
    presenca = models.BooleanField(default=False)
    data_presenca = models.DateTimeField( null=True, blank=True)
    

    def __str__(self):
        return f'{self.vereador} - {self.reuniao}'

class Voto(models.Model):
    VOTO_INEXISTENTE = 'Inexistente'
    VOTO_SIM = 'Sim'
    VOTO_NAO = 'Nao'
    VOTO_ABSTER = 'Abster'

    VOTO_CHOICES = (
        (VOTO_INEXISTENTE, 'Inexistente'),
        (VOTO_SIM, 'Sim'),
        (VOTO_NAO, 'Nao'),
        (VOTO_ABSTER, 'Abster'),
    )

    vereador = models.ForeignKey(Vereador, on_delete=models.CASCADE)
    pauta = models.ForeignKey(Pauta, on_delete=models.CASCADE)
    reuniao = models.ForeignKey(Reuniao, on_delete=models.CASCADE, null=True, blank=True)
    voto = models.CharField(max_length=15, choices=VOTO_CHOICES, default=VOTO_INEXISTENTE)
    
    class Meta:

        constraints = [
            models.UniqueConstraint(fields=['vereador', 'pauta'], name='unique_vereador_pauta')
        ]

    def __str__(self):
        return f'{self.vereador} - {self.pauta} - {self.voto}'

