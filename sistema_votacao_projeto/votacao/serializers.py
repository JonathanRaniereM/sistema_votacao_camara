from rest_framework import serializers
from .models import Reuniao, Pauta, Vereador, Presenca, Voto,PartidoPolitico,MesaDiretora, ParametrosVotacao, TipoAcao,GroupConfig

class ReuniaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reuniao
        fields = '__all__'

class ParametrosVotacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametrosVotacao
        fields = '__all__'
        
        
class MesaDiretoraSerializer(serializers.ModelSerializer):  # Serializer para a nova tabela
    class Meta:
        model = MesaDiretora
        fields = '__all__'
        
from django.contrib.auth.models import Group
from rest_framework import serializers

class GroupConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupConfig
        fields = ['group', 'atual']

class GroupSerializer(serializers.ModelSerializer):
    atual = serializers.BooleanField(source='groupconfig.atual', read_only=True)
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'atual']

        
class VereadorSerializer(serializers.ModelSerializer):
    partido = serializers.PrimaryKeyRelatedField(queryset=PartidoPolitico.objects.all())
    mesa = serializers.PrimaryKeyRelatedField(queryset=MesaDiretora.objects.all(), required=False, allow_null=True)
    grupo = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=False, allow_null=True)
    
    partido_nome = serializers.StringRelatedField(source='partido.nome_partido')  # Nome do partido
    sigla_partido = serializers.StringRelatedField(source='partido.sigla')  # Sigla do partido
    logo_partido = serializers.ImageField(source='partido.logo', read_only=True)

        # Adicionar campo de username relacionado ao usuário
    username = serializers.CharField(source='user.username', read_only=True)
    


    class Meta:
        model = Vereador
        fields = [
            'id', 'nome_vereador', 'nome_completo', 'data_nascimento', 
            'sexo', 'foto', 'funcao_mesa_diretora', 'mesa', 'grupo', 'partido', 
            'partido_nome', 'sigla_partido', 'logo_partido','username'  
        ]


class PresencaSerializer(serializers.ModelSerializer):
    vereador = serializers.PrimaryKeyRelatedField(queryset=Vereador.objects.all(), required=False, allow_null=True)
    reuniao = serializers.PrimaryKeyRelatedField(queryset=Reuniao.objects.all(), required=False, allow_null=True)
    nome_vereador = serializers.SerializerMethodField()  # Campo extra para o nome do vereador

    def get_nome_vereador(self, obj):
        return obj.vereador.nome_vereador if obj.vereador else None
    

    class Meta:
        model = Presenca
        fields = '__all__'


class TipoAcaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAcao
        fields = '__all__'

class PautaSerializer(serializers.ModelSerializer):
    parametros_votacao = serializers.PrimaryKeyRelatedField(queryset=ParametrosVotacao.objects.all(), allow_null=True, required=False)
    resultado = serializers.PrimaryKeyRelatedField(queryset=TipoAcao.objects.all(), allow_null=True, required=False)
    reuniao = serializers.PrimaryKeyRelatedField(queryset=Reuniao.objects.all())
    parametros_votacao_nome = serializers.SerializerMethodField()
    resultado_descricao = serializers.SerializerMethodField()
    autor_nome = serializers.SerializerMethodField()  # Novo campo para o nome do autor

    def get_parametros_votacao_nome(self, obj):
        return obj.parametros_votacao.nome_parametro if obj.parametros_votacao else None

    def get_resultado_descricao(self, obj):
        return obj.resultado.nome_acao if obj.resultado else None

    def get_autor_nome(self, obj):
        return obj.autor.nome_vereador if obj.autor else None

    class Meta:
        model = Pauta
        fields = '__all__'
  

    


class PartidoPoliticoSerializer(serializers.ModelSerializer):  # Serializer para a nova tabela
    class Meta:
        model = PartidoPolitico
        fields = '__all__'
        


class VotoSerializer(serializers.ModelSerializer):
    vereador = serializers.PrimaryKeyRelatedField(queryset=Vereador.objects.all(), allow_null=True, required=False)
    pauta = serializers.PrimaryKeyRelatedField(queryset=Pauta.objects.all(), allow_null=True, required=False)
    reuniao = serializers.PrimaryKeyRelatedField(queryset=Reuniao.objects.all(), allow_null=True, required=False)
    vereador_nome = serializers.StringRelatedField(source='vereador.nome_vereador')
    sigla_partido = serializers.StringRelatedField(source='vereador.partido.sigla')
    
    class Meta:
        model = Voto
        fields = '__all__'
