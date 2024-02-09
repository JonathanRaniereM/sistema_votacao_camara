from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest


# forms.py
from django import forms
from .models import Vereador

class VereadorForm(forms.ModelForm):
    class Meta:
        model = Vereador
        fields = '__all__'




from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)

            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Login bem-sucedido!', 'token': token, 'username': user.username})
        else:
            return JsonResponse({'status': 'error', 'message': 'Erro: Usuário ou senha incorretos!'}, status=401)
        
        
from rest_framework.response import Response
from rest_framework import status

class LogoutAPI(APIView):
    
    def post(self, request, *args, **kwargs):
        # Aqui, podemos invalidar o token de alguma forma ou apenas 
        # retornar uma resposta de sucesso. Porque, na prática, a 
        # invalidação do token será feita no lado do cliente removendo 
        # o token do armazenamento.

        # Por simplicidade, apenas retornaremos uma resposta de sucesso
        return Response({'status': 'success', 'message': 'Logout bem-sucedido!'}, status=status.HTTP_200_OK)
        

from django.shortcuts import render

from django.shortcuts import render
from votacao.models import Vereador

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

class HomeAPI(APIView):
    permission_classes = [IsAuthenticated]  # Permite apenas usuários autenticados

    def get(self, request, *args, **kwargs):
        try:
            vereador = request.user.vereador
            print("Vereador:", vereador)  # Debug
            mensagem_boas_vindas = f"{vereador.nome_vereador}"
            print("Mensagem:", mensagem_boas_vindas)  # Debug
            return JsonResponse({'mensagem_boas_vindas': mensagem_boas_vindas})
        except AttributeError:
            # Retorna uma resposta de erro se o usuário não tiver um vereador associado
            return JsonResponse({'error': 'Usuário não tem um vereador associado.'}, status=400)

from PIL import Image
from io import BytesIO
from django.http import HttpResponse

class VereadorPhotoAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            vereador = request.user.vereador
            foto = vereador.foto  # Substitua 'foto' pelo nome do campo de imagem no seu modelo Vereador

            # Abra a imagem usando Pillow
            image = Image.open(foto)

            # Converta a imagem para bytes
            image_bytes = BytesIO()
            image.save(image_bytes, format='JPEG')  # Altere o formato conforme necessário

            # Retorne a resposta com os bytes da imagem
            response = HttpResponse(image_bytes.getvalue(), content_type='image/jpeg')  # Altere o tipo de conteúdo conforme necessário
            return response

        except AttributeError:
            return Response({'error': 'Usuário não tem um vereador associado.'}, status=400)
        
        
class ReuniaoPlenarioAPI(APIView):
    permission_classes = [AllowAny]  # Permite apenas usuários autenticados

    def get(self, request, *args, **kwargs):
        try:
            vereador = request.user.vereador
            print("Vereador:", vereador)  # Debug
            mensagem_boas_vindas = f"Reuniões de Plenário | {vereador.nome_vereador}"
            print("Mensagem:", mensagem_boas_vindas)  # Debug
            return JsonResponse({'mensagem_boas_vindas': mensagem_boas_vindas})
        except AttributeError:
            # Retorna uma resposta de erro se o usuário não tiver um vereador associado
            return JsonResponse({'error': 'Usuário não tem um vereador associado.'}, status=400)
        
        
class TelaVotacaoAPI(APIView):
    permission_classes = [IsAuthenticated]  # Permite apenas usuários autenticados

    def get(self, request, *args, **kwargs):
        try:
            vereador = request.user.vereador
            print("Vereador:", vereador)  # Debug
            mensagem_boas_vindas = f"Votações | {vereador.nome_vereador}"
            print("Mensagem:", mensagem_boas_vindas)  # Debug
            return JsonResponse({'mensagem_boas_vindas': mensagem_boas_vindas})
        except AttributeError:
            # Retorna uma resposta de erro se o usuário não tiver um vereador associado
            return JsonResponse({'error': 'Usuário não tem um vereador associado.'}, status=400)






from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

class ConfiguracaoAPI(APIView):
    permission_classes = [IsAuthenticated]  # Permite apenas usuários autenticados

    def get(self, request, *args, **kwargs):
        # Por exemplo, suponha que você queira enviar algumas configurações padrão:
        data = {
            "theme": "light",
            "language": "pt-BR",
            # ... outras configurações que você possa ter
        }
        return JsonResponse(data)


class LegislaçaoAPI(APIView):
    permission_classes = [IsAuthenticated]  # Permite apenas usuários autenticados

    def get(self, request, *args, **kwargs):
        # Por exemplo, suponha que você queira enviar algumas configurações padrão:
        data = {
            "theme": "light",
            "language": "pt-BR",
            # ... outras configurações que você possa ter
        }
        return JsonResponse(data)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vereador,GroupConfig
from .serializers import VereadorSerializer,GroupSerializer
from django.shortcuts import get_object_or_404

from rest_framework import status
import logging


import logging
logger = logging.getLogger('django')
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group

from rest_framework import viewsets









class GroupConfigViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['PUT'])
    def set_group_as_current(self, request, grupo_id):
        try:
            # Encontrar o objeto GroupConfig correspondente ao Group
            group_config = GroupConfig.objects.get(grupo__id=grupo_id)


            # Garantir que apenas um GroupConfig seja marcado como atual
            GroupConfig.objects.update(atual=False)
            group_config.atual = True
            group_config.save()

            return Response({"status": "Grupo setado como atual"}, status=status.HTTP_200_OK)
        except GroupConfig.DoesNotExist:
            return Response({"error": "Grupo não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PaineisGroupViewSet(viewsets.ModelViewSet):
    
    queryset = Vereador.objects.all()
    serializer_class = VereadorSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['GET'], url_path='TvUm')
    def composicao_painelTvUm(self, request):
        return self._get_painel_composicao('TV 1')
    
    @action(detail=False, methods=['GET'], url_path='TvDois')
    def composicao_painelTvDois(self, request):
        return self._get_painel_composicao('TV 2')

    @action(detail=False, methods=['GET'], url_path='TvTres')
    def composicao_painelTvTres(self, request):
        return self._get_painel_composicao('TV 3')

    def _get_painel_composicao(self, nome_grupo):
        grupo = Group.objects.get(name=nome_grupo)
        vereadores = Vereador.objects.filter(user__in=grupo.user_set.all()).order_by('nome_vereador')
        serializer = self.get_serializer(vereadores, many=True)
        return Response(serializer.data)


class SpecificGroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.filter(name__in=["TV 1", "TV 2", "TV 3", "PAINEL"])
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    
    def list_not_in_group_and_group_atual(self, request, grupo_id=None):
        # Pega o config do grupo marcado como "atual"
        group_config = GroupConfig.objects.get(atual=True)
        grupo_atual = group_config.grupo

        # Filtra os vereadores cujos usuários fazem parte do grupo "atual"
        vereadores_no_grupo_atual = Vereador.objects.filter(user__in=grupo_atual.user_set.all())

        # Exclui os vereadores que fazem parte do grupo que está sendo editado
        vereadores = vereadores_no_grupo_atual.exclude(user__groups__id=grupo_id)

        serializer = VereadorSerializer(vereadores, many=True)
        return Response(serializer.data)

    # ... (restante do código, se necessário)

class GroupPainelViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.filter(name__in=["TV 1", "TV 2", "TV 3", "PAINEL"])
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    
     # Listar todos os grupos
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # Recuperar um grupo específico
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # Criar um novo grupo
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # Atualizar um grupo específico
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # Excluir um grupo específico
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class GroupViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.exclude(name__in=["TV 1", "TV 2", "TV 3", "PAINEL"])
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    
     # Listar todos os grupos
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # Recuperar um grupo específico
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # Criar um novo grupo
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # Atualizar um grupo específico
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # Excluir um grupo específico
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class VereadoresGroupViewSet(viewsets.ViewSet):  # Note que aqui mudamos para ViewSet simples

    permission_classes = [IsAuthenticated]

    def list_not_in_group(self, request, grupo_id=None):
        vereadores = Vereador.objects.exclude(user__groups__id=grupo_id)
        serializer = VereadorSerializer(vereadores, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def list_in_group(self, request, grupo_id=None):
        vereadores = Vereador.objects.filter(user__groups__id=grupo_id)
        serializer = VereadorSerializer(vereadores, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def add_to_group(self, request, grupo_id=None):
        try:
            group = Group.objects.get(pk=grupo_id)
            vereadores_ids = request.data.get('vereadores_ids', [])

            if not vereadores_ids:
                raise ValidationError("Os IDs dos vereadores são necessários.")

            for vereador_id in vereadores_ids:
                vereador = Vereador.objects.get(pk=vereador_id)
                vereador.user.groups.add(group)

            return Response({'status': f'Vereadores adicionados ao grupo {group.name}'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f"Erro ao adicionar vereadores ao grupo: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def remove_from_group(self, request, grupo_id=None):
        group = Group.objects.get(pk=grupo_id)
        vereador_id = request.data.get('vereador_id')
        vereador = Vereador.objects.get(pk=vereador_id)
        vereador.user.groups.remove(group)
        return Response({'status': f'Vereador removido do grupo {group.name}'}, status=status.HTTP_200_OK)

    



class VereadorViewSet(viewsets.ModelViewSet):

    serializer_class = VereadorSerializer
    permission_classes = [AllowAny]
    queryset = Vereador.objects.exclude(id=1)
    
    @action(detail=False, methods=['GET'], url_path='create_parlamentar')
    def composicao_parlamentarAtual(self, request):
        # Pega o config do grupo marcado como "atual"
        group_config = GroupConfig.objects.get(atual=True)
        grupo = group_config.grupo
        
        # Consulte os vereadores cujos usuários fazem parte do grupo "atual"
        vereadores = Vereador.objects.filter(user__in=grupo.user_set.all())
        serializer = self.get_serializer(vereadores, many=True)
        return Response(serializer.data)

    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Cria o usuário
            username = request.data.get('username')
            password = request.data.get('password')
            user = User(username=username)
            user.set_password(password)
            user.save()

            # Salva o vereador com o usuário associado
            vereador = serializer.save(user=user)
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        vereador = self.get_object()

        serializer = self.get_serializer(vereador, data=request.data)
        if serializer.is_valid():
            # Atualiza o usuário se necessário
            user = vereador.user
            username = request.data.get('username')
            password = request.data.get('password')

            if username:
                user.username = username
            if password:
                user.set_password(password)
            user.save()

            # Salva o vereador com o usuário atualizado
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
            vereador = self.get_object()
            
            # Verificar se o vereador tem um usuário associado e excluí-lo
            if vereador.user:
                user = vereador.user
                vereador.delete()  # Exclui o vereador
                user.delete()  # Exclui o usuário associado
                return Response({"status": "success", "message": "Vereador e usuário associado excluídos com sucesso"})
            
            vereador.delete()  # Exclui o vereador se não houver usuário associado
            return Response({"status": "success", "message": "Vereador excluído com sucesso"})
    
    def partial_update(self, request, *args, **kwargs):
        vereador = self.get_object()
        serializer = self.get_serializer(vereador, data=request.data, partial=True)
        if serializer.is_valid():
            # Atualiza o usuário se necessário
            user = vereador.user
            username = request.data.get('username')
            password = request.data.get('password')

            if username:
                user.username = username
            if password:
                user.set_password(password)
            user.save()

            # Salva o vereador com o usuário atualizado
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from rest_framework import viewsets, status
from rest_framework.response import Response

    
    
from .models import PartidoPolitico
from .serializers import PartidoPoliticoSerializer
from rest_framework import status
from rest_framework.response import Response

class PartidoPoliticoViewSet(viewsets.ModelViewSet):

    queryset = PartidoPolitico.objects.all()
    serializer_class = PartidoPoliticoSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partido = self.get_object()
        serializer = self.get_serializer(partido, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        partido = self.get_object()
        partido.delete()
        return Response({"status": "success"})

    def partial_update(self, request, *args, **kwargs):
        partido = self.get_object()
        serializer = self.get_serializer(partido, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class VereadoresByPartidoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vereador.objects.all()
    serializer_class = VereadorSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, partido_id=None):
        vereadores = Vereador.objects.filter(partido_id=partido_id)
        serializer = VereadorSerializer(vereadores, many=True)
        return Response(serializer.data)
    
from django.core.exceptions import ValidationError
    
class VereadoresByMesaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vereador.objects.all()
    serializer_class = VereadorSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, mesa_id=None):
        vereadores = Vereador.objects.exclude(id=1).exclude(mesa_id=mesa_id)
        serializer = VereadorSerializer(vereadores, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET'])
    def vereadores_in_mesa(self, request, mesa_id=None):
        vereadores = Vereador.objects.filter(mesa_id=mesa_id)
        serializer = VereadorSerializer(vereadores, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['POST'])
    def add_vereador_to_mesa(self, request, mesa_id):
        print("Request Data:", request.data)  # Print the incoming data
         # Antes de adicionar o vereador, verifique se já temos um presidente ou vice-presidente
        existing_president = Vereador.objects.filter(mesa_id=mesa_id, funcao_mesa_diretora="Presidente")
        existing_vice = Vereador.objects.filter(mesa_id=mesa_id, funcao_mesa_diretora="Vice-Presidente")

        for vereador_data in request.data:
            if not vereador_data['funcao']:
             return Response({"error": "A função não pode estar vazia."}, status=400)
            if vereador_data['funcao'] == "Presidente" and existing_president.exists():
                return Response({"error": "Já existe um presidente nesta mesa! "}, status=400)
            if vereador_data['funcao'] == "Vice-Presidente" and existing_vice.exists():
                return Response({"error": "Já existe um vice-presidente nesta mesa! "}, status=400)
        try:
            mesa = MesaDiretora.objects.get(id=mesa_id)
            
            for vereador_data in request.data:
                vereador = Vereador.objects.get(id=vereador_data['vereador_id'])
                vereador.funcao_mesa_diretora = vereador_data['funcao']
                vereador.mesa_id = mesa.id
                vereador.save()

            return Response({"message": "Vereadores adicionados com sucesso."})

        except ValidationError as ve:
                print("ValidationError:", ve)
                return Response({"error": "Erro de validação: " + str(ve)}, status=400)

        except Exception as e:
            print("General Exception:", e)
            return Response({"error": "Erro ao adicionar vereadores: " + str(e)}, status=500)

    
from .models import MesaDiretora
from .serializers import MesaDiretoraSerializer
    
class MesaDiretoraViewSet(viewsets.ModelViewSet):

    queryset = MesaDiretora.objects.all()
    serializer_class = MesaDiretoraSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        mesa_diretora = self.get_object()
        serializer = self.get_serializer(mesa_diretora, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        mesa_diretora = self.get_object()
        mesa_diretora.delete()
        return Response({"status": "success"})

    def partial_update(self, request, *args, **kwargs):
        mesa_diretora = self.get_object()
        serializer = self.get_serializer(mesa_diretora, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
from .models import ParametrosVotacao
from .serializers import ParametrosVotacaoSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ParametrosVotacaoViewSet(viewsets.ModelViewSet):

    queryset = ParametrosVotacao.objects.all()
    serializer_class = ParametrosVotacaoSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        parametro = self.get_object()
        serializer = self.get_serializer(parametro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        parametro = self.get_object()
        parametro.delete()
        return Response({"status": "success"})

    def partial_update(self, request, *args, **kwargs):
        parametro = self.get_object()
        serializer = self.get_serializer(parametro, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from .models import TipoAcao  # Certifique-se de importar TipoAcao
from .serializers import TipoAcaoSerializer  # E também o TipoAcaoSerializer

class TipoAcaoViewSet(viewsets.ModelViewSet):

    queryset = TipoAcao.objects.all()
    serializer_class = TipoAcaoSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        tipo_acao = self.get_object()
        serializer = self.get_serializer(tipo_acao, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        tipo_acao = self.get_object()
        tipo_acao.delete()
        return Response({"status": "success"})

    def partial_update(self, request, *args, **kwargs):
        tipo_acao = self.get_object()
        serializer = self.get_serializer(tipo_acao, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from .models import Reuniao  # Importe o modelo Reuniao
from .serializers import ReuniaoSerializer  # E também o ReuniaoSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ReuniaoViewSet(viewsets.ModelViewSet):

    queryset = Reuniao.objects.all()
    serializer_class = ReuniaoSerializer
    permission_classes = [AllowAny]
    def list(self, request, *args, **kwargs):
        # Primeiro, obtenha a lista padrão de reuniões
        response = super(ReuniaoViewSet, self).list(request, *args, **kwargs)
        
        # Adicione o username no cabeçalho da resposta
        response['X-Username'] = request.user.username
        
        return response
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        reuniao = self.get_object()
        serializer = self.get_serializer(reuniao, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        reuniao = self.get_object()
        reuniao.delete()
        return Response({"status": "success"})

    def partial_update(self, request, *args, **kwargs):
        reuniao = self.get_object()
        serializer = self.get_serializer(reuniao, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
from .models import Pauta  # Importe o modelo Pauta
from .serializers import PautaSerializer  # E também o PautaSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# views.py
class PautaPorReuniaoViewSet(viewsets.ReadOnlyModelViewSet):  # ReadOnly porque talvez você só queira listar e recuperar
    serializer_class = PautaSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        reuniao_id = self.kwargs['reuniao_id']
        return Pauta.objects.filter(reuniao=reuniao_id)

class PautaViewSet(viewsets.ModelViewSet):

    queryset = Pauta.objects.all()
    serializer_class = PautaSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        pauta = self.get_object()
        serializer = self.get_serializer(pauta, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        pauta = self.get_object()
        pauta.delete()
        return Response({"status": "success"})

    def partial_update(self, request, *args, **kwargs):
        pauta = self.get_object()
        serializer = self.get_serializer(pauta, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CronometroAPI(APIView):
    permission_classes = [IsAuthenticated]  # Permite apenas usuários autenticados

    def get(self, request, *args, **kwargs):
        # Por exemplo, suponha que você queira enviar algumas configurações padrão:
        data = {
            "theme": "light",
            "language": "pt-BR",
            # ... outras configurações que você possa ter
        }
        return JsonResponse(data)
    
class PainelAPI(APIView):
    permission_classes = [IsAuthenticated]  # Permite apenas usuários autenticados

    def get(self, request, *args, **kwargs):
        # Por exemplo, suponha que você queira enviar algumas configurações padrão:
        data = {
            "theme": "light",
            "language": "pt-BR",
            # ... outras configurações que você possa ter
        }
        return JsonResponse(data)
    
    
from .models import Presenca  # Importe o modelo Pauta
from .serializers import PresencaSerializer  # E também o PautaSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



class PresencaViewSet(viewsets.ModelViewSet):
    
    serializer_class = PresencaSerializer
    permission_classes = [AllowAny]
    queryset = Presenca.objects.all()
    
    def create(self, request, *args, **kwargs):
        username = request.data.get('vereador')
        
        try:
            user = User.objects.get(username=username)
            vereador = Vereador.objects.get(user=user)
        except (User.DoesNotExist, Vereador.DoesNotExist):
            return Response({"error": "Vereador not found"}, status=status.HTTP_400_BAD_REQUEST)

        request.data['vereador'] = vereador.id
            
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # Enviar notificação ao grupo de clientes conectados sobre a criação
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"presenca_{kwargs.get('reuniao_id')}",  # supondo que você está usando o reuniao_id como parte do nome do grupo
                {
                    "type": "presenca.update",
                    "event": "created",
                    "data": serializer.data
                }
            )
            
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='atualizar_em_massa')
    def atualizar_em_massa(self, request, reuniao_id=None):
        data = request.data
        # Lógica para atualizar várias presenças com base nos dados recebidos
        # Por exemplo, iterar sobre os dados e atualizar cada presença
        for presenca_data in data:
            presenca = Presenca.objects.get(id=presenca_data['id'])
            presenca.presenca = presenca_data['presenca']
            presenca.save()

        return Response({'status': 'success'}, status=status.HTTP_200_OK)


    def update(self, request, *args, **kwargs):
        presenca = self.get_object()
        serializer = self.get_serializer(presenca, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        presenca = self.get_object()
        presenca.delete()
        return Response({"status": "success"})
    
    def partial_update(self, request, *args, **kwargs):
        presenca = self.get_object()
        serializer = self.get_serializer(presenca, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"])
    def presenca_por_reuniao(self, request, reuniao_id=None):
        presencas = self.queryset.filter(reuniao_id=reuniao_id)
        serializer = PresencaSerializer(presencas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"])
    def presenca_por_reuniao_painel(self, request, reuniao_id=None):
        presencas = self.queryset.filter(reuniao_id=reuniao_id, presenca=True)
        serializer = PresencaSerializer(presencas, many=True)
        return Response(serializer.data)
        
    @action(detail=False, methods=['get'], url_path='relatorio_presenca/(?P<reuniao_id>\d+)')
    def relatorio_presenca(self, request, reuniao_id=None):
        try:
            # Aqui, você pode implementar a lógica para buscar as presenças da reunião especificada
            presencas = Presenca.objects.filter(reuniao_id=reuniao_id)
            serializer = PresencaSerializer(presencas, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['get'])
    def presenca_por_vereador_e_reuniao(self, request, reuniao_id=None):
        username = request.query_params.get('username')
        
        logger.info(f"Username: {username}, Reuniao ID: {reuniao_id}")
        
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            logger.error(f"User with username {username} does not exist")
            return Response({"error": "User não encontrado"}, status=status.HTTP_404_NOT_FOUND)
            
        try:
            vereador = Vereador.objects.get(user=user)
        except ObjectDoesNotExist:
            logger.error(f"Vereador with user {user} does not exist")
            return Response({"error": "Vereador não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        presenca = Presenca.objects.filter(vereador=vereador, reuniao_id=reuniao_id)
        
        logger.info(f"Presenca QuerySet: {presenca}")
        
        if not presenca.exists():
            logger.info(f"No presence found for Vereador: {vereador} and Reuniao ID: {reuniao_id}")
            return Response({"detail": "Presença não encontrada", "presenca": False}, status=status.HTTP_200_OK)

            
        serializer = self.get_serializer(presenca, many=True)
        return Response(serializer.data)


from django.core.exceptions import ObjectDoesNotExist
    
# Em sua API Django
from django.contrib.auth import authenticate




class VerificarSENHaAPI(APIView):

        permission_classes = [AllowAny]
        queryset = User.objects.all()  # Substitua User pelo modelo correto

        def post(self, request, *args, **kwargs):
            username = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                # A senha está correta, retorne uma resposta de sucesso
                return JsonResponse({'status': 'success'})
            else:
                # A senha está incorreta, retorne uma resposta de erro
                return JsonResponse({'status': 'error', 'message': 'Senha incorreta'}, status=400)
            
            
            
from .serializers import VotoSerializer  # E também o PautaSerializer
from .models import Voto
import logging

logger = logging.getLogger(__name__)

class VotacaoViewSet(viewsets.ModelViewSet):
    serializer_class = VotoSerializer  # Substitua pelo serializer apropriado para Votos
    permission_classes = [AllowAny]
    queryset = Voto.objects.all()  # Substitua pela queryset apropriada para seus votos

    @action(detail=False, methods=["POST"])
    def registrar_voto(self, request):
        reuniao_id = request.data.get("reuniao")
        
        try:
            reuniao = Reuniao.objects.get(pk=reuniao_id)
        except Reuniao.DoesNotExist:
            return Response({"error": "Reunião não encontrada"}, status=status.HTTP_404_NOT_FOUND)

        # Encontre a pauta aberta na reunião
        try:
            pauta_aberta = Pauta.objects.get(reuniao=reuniao, status_votacao=Pauta.STATUS_ABERTA)
        except Pauta.DoesNotExist:
            return Response({"error": "Nenhuma pauta está aberta para votação nesta reunião"}, status=status.HTTP_400_BAD_REQUEST)

        vereador = request.user.vereador
         # Verificação da presença do vereador na reunião
        presenca = Presenca.objects.filter(vereador=vereador, reuniao=reuniao).first()
        if not presenca:
            return Response({"error": "Registre sua presença para votar"}, status=status.HTTP_400_BAD_REQUEST)
        # Verifique se o vereador já registrou um voto para esta pauta
        votos_existentes = Voto.objects.filter(vereador=vereador, pauta=pauta_aberta)
        if votos_existentes.exists():
            return Response({"error": "Voto já registrado para esta pauta"}, status=status.HTTP_400_BAD_REQUEST)

        # Recupere o voto fornecido na solicitação (por exemplo, 'voto' como um campo na solicitação POST)
        voto = request.data.get("voto")

        # Verifique se o voto fornecido é válido
        if voto not in [Voto.VOTO_SIM, Voto.VOTO_NAO, Voto.VOTO_ABSTER]:
            return Response({"error": "Voto inválido"}, status=status.HTTP_400_BAD_REQUEST)

        novo_voto = Voto(vereador=vereador, pauta=pauta_aberta, voto=voto, reuniao=reuniao)
        novo_voto.save()

        # Aqui você pode adicionar a lógica para atualizar o status da pauta
        # Se necessário, dependendo do seu modelo e lógica de negócios.

        return Response({"status": "success", "data": VotoSerializer(novo_voto).data}, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=["PUT"])
    def update_voto(self, request, pk=None):
        try:
            # Encontre o vereador com base no username fornecido
            vereador_username = request.data.get("vereador")
            try:
                vereador = Vereador.objects.get(user__username=vereador_username)
            except Vereador.DoesNotExist:
                return Response({"error": "Vereador não encontrado"}, status=status.HTTP_404_NOT_FOUND)
            
            # Atualize o campo "vereador" com o ID do vereador
            request.data["vereador"] = vereador.id

            voto = self.get_object()
            serializer = self.get_serializer(voto, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Voto {voto.id} atualizado com sucesso")
                return Response({"status": "success", "data": serializer.data})
            else:
                logger.error(f"Erros de validação: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Ocorreu um erro ao atualizar o voto: {str(e)}")
            return Response({"status": "error", "message": "Ocorreu um erro ao atualizar o voto."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



    @action(detail=False, methods=['GET'])
    def buscar_voto_vereador(self, request, vereador_username=None, reuniao_id=None):
        logger.info(f"Buscando voto para vereador_username: {vereador_username}, reuniao_id: {reuniao_id}")

        if not vereador_username or not reuniao_id:
            logger.error("vereador_username e reuniao_id são obrigatórios")
            return Response({"error": "vereador_username e reuniao_id são obrigatórios"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vereador = Vereador.objects.get(user__username=vereador_username)
        except Vereador.DoesNotExist:
            logger.error(f"Vereador com username {vereador_username} não encontrado")
            return Response({"error": "Vereador não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        try:
            reuniao = Reuniao.objects.get(pk=reuniao_id)
        except Reuniao.DoesNotExist:
            logger.error(f"Reunião com id {reuniao_id} não encontrada")
            return Response({"error": "Reunião não encontrada"}, status=status.HTTP_404_NOT_FOUND)

        try:
            pauta_aberta = Pauta.objects.get(reuniao=reuniao, status_votacao=Pauta.STATUS_ABERTA)
        except Pauta.DoesNotExist:
            logger.error(f"Nenhuma pauta está aberta para votação na reunião {reuniao_id}")
            return Response({"error": "Nenhuma pauta está aberta para votação nesta reunião"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            voto = Voto.objects.get(vereador=vereador, pauta=pauta_aberta)
        except Voto.MultipleObjectsReturned:
            logger.error(f"Múltiplos votos encontrados para vereador {vereador_username} e pauta {pauta_aberta.id}")
            voto = Voto.objects.filter(vereador=vereador, pauta=pauta_aberta).first()
        except Voto.DoesNotExist:
            return Response({"error": "Voto não encontrado"}, status=status.HTTP_404_NOT_FOUND)


        serializer = VotoSerializer(voto)
        logger.info(f"Voto encontrado: {serializer.data}")
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    @action(detail=False, methods=['GET'])
    def buscar_votos_todos(self, request, reuniao_id=None):


        if not reuniao_id:
            return Response({"error": "reuniao_id é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reuniao = Reuniao.objects.get(pk=reuniao_id)
            pauta_aberta = Pauta.objects.get(reuniao=reuniao, status_votacao=Pauta.STATUS_ABERTA)
            votos = Voto.objects.filter(pauta=pauta_aberta)
            
            serializer = VotoSerializer(votos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Reuniao.DoesNotExist:
            return Response({"error": "Reunião não encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Pauta.DoesNotExist:
            return Response({"error": "Nenhuma pauta está aberta para votação nesta reunião"}, status=status.HTTP_400_BAD_REQUEST)

class VotacaoRelatorioView(APIView):
    """
    View para gerar relatórios de votação.
    """

    permission_classes = []

    def get(self, request, pauta_id):
        try:
            votos = Voto.objects.filter(pauta_id=pauta_id).select_related('vereador')
            serializer = VotoSerializer(votos, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#SE FOSSE TODO O FOMRULARIO
#def edit_parlamentar(request):
    #if request.method == 'POST':
        #vereador_id = request.POST.get('vereador_id')
        #vereador = get_object_or_404(Vereador, id=vereador_id)

        #form = VereadorForm(request.POST, instance=vereador)
       # if form.is_valid():
           # print("Formulário é válido!")
           # form.save()
        #else:
            #print(form.errors)
            # Redirecionar ou fazer outra ação após salvar, se necessário
       # return render(request, 'configuracao.html', {'vereador': vereador, 'form': form})

    # Se o método não for POST, retorne um erro ou outro comportamento desejado.
    #return HttpResponseBadRequest("Método inválido")