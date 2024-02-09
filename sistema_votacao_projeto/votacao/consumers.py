# consumers.py

from channels.db import database_sync_to_async
from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DeleteModelMixin,
    RetrieveModelMixin,
)
from votacao.models import Presenca, User, Vereador,Voto
from votacao.serializers import PresencaSerializer,VotoSerializer
import logging
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from rest_framework.renderers import JSONRenderer


# Configure o logger
logger = logging.getLogger(__name__)

specificStatusCodeMappings = {
    '1000': 'Normal Closure',
    '1001': 'Going Away',
    '1002': 'Protocol Error',
    '1003': 'Unsupported Data',
    '1004': '(For future)',
    '1005': 'No Status Received',
    '1006': 'Abnormal Closure',
    '1007': 'Invalid frame payload data',
    '1008': 'Policy Violation',
    '1009': 'Message too big',
    '1010': 'Missing Extension',
    '1011': 'Internal Error',
    '1012': 'Service Restart',
    '1013': 'Try Again Later',
    '1014': 'Bad Gateway',
    '1015': 'TLS Handshake'
}

def getStatusCodeString(code):
    if code is None:
        return "Código de status desconhecido"
    if (code >= 0 and code <= 999):
        return '(Unused)'
    elif (code >= 1016):
        if (code <= 1999):
            return '(For WebSocket standard)'
        elif (code <= 2999):
            return '(For WebSocket extensions)'
        elif (code <= 3999):
            return '(For libraries and frameworks)'
        elif (code <= 4999):
            return '(For applications)'
    return specificStatusCodeMappings.get(code, '(Unknown)')

class PresencaConsumer(
    GenericAsyncAPIConsumer
):   
    
    

    async def connect(self):
        logger.info("Conexão estabelecida.")
        print("Método connect chamado!")
        
        # Verificar se reuniao_id está na URL. Se não, definir um padrão (por exemplo, "global").
        reuniao_id = self.scope['url_route']['kwargs'].get('reuniao_id', 'global')
        
        self.room_group_name = f"presenca_{reuniao_id}"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        await super().connect()
        logger.info(f"Conexão estabelecida. Conectado ao grupo {self.room_group_name}.")

    async def disconnect(self, close_code):
        status_message = getStatusCodeString(close_code)
        logger.info(f"Desconexão com código: {close_code} - {status_message}")
        await self.channel_layer.group_discard(
            self.room_group_name,  # use a variável de nome de grupo dinâmico
            self.channel_name
        )
        await super().disconnect(close_code)




    queryset = Presenca.objects.all()
    serializer_class = PresencaSerializer
    queryset_votos = Voto.objects.all()  # Suponho que o modelo seja chamado Voto
    serializer_class_votos = VotoSerializer  # Suponho que o serializer seja chamado VotoSerializer
    permission_classes = (permissions.AllowAny, )
    
    @database_sync_to_async
    def get_serialized_data_votos(self):
        queryset = self.queryset_votos
        serializer = self.serializer_class_votos(queryset, many=True)
        return serializer.data

    async def voto_por_reuniao(self, content):
        logger.info(f"Processando mensagem: {content}")
        try:

            serializer_data = await self.get_serialized_data_votos()
            targetComponent = content['targetComponent']
       
            message = {
                'type': 'voto.update',
                'data': 'voto.update',
                'targetComponent':targetComponent,
                
            }
            await self.channel_layer.group_send(self.room_group_name, message)
        except Exception as e:
            logger.error(f"Erro ao processar voto por reunião: {str(e)}")

    
    async def presenca_update(self, event):
        await self.send_json({
            'type': event['type'],
            'data': event['data'],
            'targetComponent': event['targetComponent'],
        })


    async def abrir_submenu_votacao_update(self, event):
        await self.send_json({
            'type': event['type'],
            'data': event['data'],
            'targetComponent': event['targetComponent'],

        })
    
    async def abrir_submenu_parlamentares_update(self, event):
        await self.send_json({
            'type': event['type'],
            'data': event['data'],
            'targetComponent': event['targetComponent'],
        })
     

    
    async def limpar_update(self, event):
       # processar a mensagem aqui
        await self.send_json({
            'type': event['type'],
            'data': event['data'],
            'targetComponent': event['targetComponent'],
        })
     
    async def voto_update(self, event):
        await self.send_json({
            'type': event['type'],
            'data': event['data'],
            'targetComponent': event['targetComponent'],
        })
      
    async def sorteio_update(self, event):

        await self.send_json({
            'type': event['type'],
            'data': event['data'],
            'targetComponent': event['targetComponent'],
        })

      
    async def sorteio_por_reuniao(self, content):
        # Processa a atualização do sorteio
        try:
            targetComponent = content['targetComponent']

            rankedParlamentares = content['data']
            message = {
                'type': 'sorteio.update',
                'data': rankedParlamentares,
                'targetComponent':targetComponent,
            }
            await self.channel_layer.group_send(self.room_group_name, message)
        except Exception as e:
            logger.error(f"Erro ao processar atualização de sorteio com conteúdo: {content}. Erro: {str(e)}")



    async def editar_all_cronometro(self, content):
        # Processa a atualização do cronometro
        try:
            defaultDuration = content['data']
            targetComponent = content['targetComponent']
    
            message = {
                'type': 'editar_all_cronometro.update',   # Isso é usado para determinar a função de manipulação quando a mensagem é recebida
                'data': defaultDuration,
                'targetComponent':targetComponent,

            }
            await self.channel_layer.group_send(self.room_group_name, message)
        except Exception as e:
            logger.error(f"Erro ao processar atualização de cronometro com conteúdo: {content}. Erro: {str(e)}")

    async def editar_all_cronometro_update(self, event):
        await self.send_json({
            'type': event['type'],
            'data': event['data'],
            'targetComponent': event['targetComponent'],
        })

    async def iniciar_cronometro(self, content):
        # Processa a atualização do cronometro
        try:
            tempoRestante = content['data']
            vereadorId = content['vereadorId']
            targetComponent = content['targetComponent']
            message = {
                'type': 'iniciar_cronometro.update',   # Isso é usado para determinar a função de manipulação quando a mensagem é recebida
                'data': tempoRestante,
                'vereadorId':vereadorId,
                'targetComponent':targetComponent,
            }
            await self.channel_layer.group_send(self.room_group_name, message)
        except Exception as e:
            logger.error(f"Erro ao processar atualização de cronometro com conteúdo: {content}. Erro: {str(e)}")

    async def iniciar_cronometro_update(self, event):
        await self.send_json({
            'type': event['type'],
            'data': event['data'],
            'vereadorId': event['vereadorId'],
            'targetComponent': event['targetComponent'],
            
        })

    async def preparar_cronometro(self, content):
        # Processa o "preparo" ou "set" do cronometro
        try:
            logger.info(f"Processando mensagem: {content}")
            tempoRestante = content['data']
            vereadorId = content['vereadorId']
            targetComponent = content['targetComponent']
            message = {
                'type': 'preparar_cronometro.update',   
                'data': tempoRestante,
                'vereadorId':vereadorId,
                'targetComponent':targetComponent,
            }
            await self.channel_layer.group_send(self.room_group_name, message)
        except Exception as e:
            logger.error(f"Erro ao processar atualização de cronometro com conteúdo: {content}. Erro: {str(e)}")

    async def preparar_cronometro_update(self, event):
        await self.send_json({
            'type': event['type'],
            'data': event['data'],
            'vereadorId': event['vereadorId'],
            'targetComponent': event['targetComponent'],
        })

    async def editar_cronometro(self, content):
        # Processa o "preparo" ou "set" do cronometro
        try:
            logger.info(f"Processando mensagem: {content}")
            tempoRestante = content['data']
            vereadorId = content['vereadorId']
            targetComponent = content['targetComponent']
            message = {
                'type': 'editar_cronometro.update',   
                'data': tempoRestante,
                'vereadorId':vereadorId,
                'targetComponent':targetComponent,
            }
            await self.channel_layer.group_send(self.room_group_name, message)
        except Exception as e:
            logger.error(f"Erro ao processar atualização de cronometro com conteúdo: {content}. Erro: {str(e)}")

    async def editar_cronometro_update(self, event):
        await self.send_json({
            'type': event['type'],
            'data': event['data'],
            'vereadorId': event['vereadorId'],
            'targetComponent': event['targetComponent'],
        })


    async def ajustar_cronometro(self, content):
        # Processa o "preparo" ou "set" do cronometro
        try:
            logger.info(f"Processando mensagem: {content}")
            tempoVereador1 = content['tempoVereador1']
            tempoVereador2 = content['tempoVereador2']
            vereadorId1 = content['vereadorId1']
            vereadorId2 = content['vereadorId2']
            targetComponent = content['targetComponent']
            message = {
                'type': 'ajustar_cronometro.update',   
                'tempoVereador1': tempoVereador1,
                'tempoVereador2': tempoVereador2,
                'vereadorId1':vereadorId1,
                'vereadorId2':vereadorId2,
                'targetComponent':targetComponent,
            }
            await self.channel_layer.group_send(self.room_group_name, message)
        except Exception as e:
            logger.error(f"Erro ao processar atualização de cronometro com conteúdo: {content}. Erro: {str(e)}")

    async def ajustar_cronometro_update(self, event):
        await self.send_json({
            'type': event['type'],
            'tempoVereador1': event['tempoVereador1'],
            'tempoVereador2': event['tempoVereador2'],
            'vereadorId1': event['vereadorId1'],
            'vereadorId2': event['vereadorId2'],
            'targetComponent': event['targetComponent'],
        })
    async def zerar_cronometro(self, content):
        # Processa o "preparo" ou "set" do cronometro
        vereadorId = content['vereadorId']
        targetComponent = content['targetComponent']
        try:

            message = {
                'type': 'zerar_cronometro.update',   
                'data': 'zerar_cronometro.update',
                'vereadorId':vereadorId,
                'targetComponent':targetComponent,
            }
            await self.channel_layer.group_send(self.room_group_name, message)
        except Exception as e:
            logger.error(f"Erro ao processar atualização de cronometro com conteúdo: {content}. Erro: {str(e)}")

    async def zerar_cronometro_update(self, event):
        await self.send_json({
            'type': event['type'],
            'data': event['data'],
            'vereadorId': event['vereadorId'],
            'targetComponent': event['targetComponent'],
        })


    async def pausar_cronometro(self, content):
        # Processa a "pausa" ou "set" do cronometro
        try:
            vereadorId = content['vereadorId']
            tempoRestante = content['data']
            targetComponent = content['targetComponent']

            message = {
                'type': 'pausar_cronometro.update',   
                'data': tempoRestante,
                'vereadorId':vereadorId,
                'targetComponent':targetComponent,
            }
            await self.channel_layer.group_send(self.room_group_name, message)
        except Exception as e:
            logger.error(f"Erro ao processar pausa de cronometro com conteúdo: {content}. Erro: {str(e)}")

    async def pausar_cronometro_update(self, event):
        await self.send_json({
            'type': event['type'],
            'data': event['data'],
            'vereadorId': event['vereadorId'],
            'targetComponent': event['targetComponent'],
        })


    async def limpar_votos(self, content):
        try:
            targetComponent = content['targetComponent']
            message = {
                'type': 'limpar_votos.update',
                'data': 'limpar_votos.update',
                'targetComponent':targetComponent,
            }
            await self.channel_layer.group_send(self.room_group_name, message)
        except Exception as e:
            logger.error(f"Erro ao processar voto por reunião: {str(e)}")


    async def limpar_votos_update(self, event):
        await self.send_json({
            'type': event['type'],
            'data': event['data'],
            'targetComponent': event['targetComponent'],
        })






    @database_sync_to_async
    def get_serialized_data(self):
        queryset = self.get_queryset()  # Substitua pelo método adequado para obter os objetos que você quer serializar
        serializer = PresencaSerializer(queryset, many=True)  # Use o nome correto do seu serializer
        return serializer.data

    # Adicione este método
    async def send_json(self, content, close=False):
        try:
            logger.info(f"Preparando para enviar mensagem para o grupo {self.room_group_name}. Mensagem: {content}")
            await super().send_json(content, close)
            logger.info(f"Mensagem enviada com sucesso para o grupo {self.room_group_name}. ")
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem para o grupo {self.room_group_name}. . Erro: {str(e)}")

    async def pauta_update_reuniao(self, content):
        logger.info(f"Processando presença por reunião com conteúdo: {content}")
        try:
            targetComponent = content['targetComponent']
            # substituir serializer_data pela sua mensagem específica
            message = {
                'type': 'pauta.update',
                'data': "pauta.update",
                'targetComponent':targetComponent,
            }
            logger.info(f"Preparando para enviar mensagem para o grupo {self.room_group_name}.")
            await self.channel_layer.group_send(self.room_group_name, message)

            logger.info(f"Mensagem enviada com sucesso para o grupo {self.room_group_name}.")
        except Exception as e:
            logger.error(f"Erro ao processar presença por reunião com conteúdo: {content}. Erro: {str(e)}")

    async def pauta_update(self, event):
        await self.send_json({
            'type': event['type'],
            'data': event['data'],
            'targetComponent': event['targetComponent'],
        })

    async def presenca_por_reuniao(self, content):
        logger.info(f"Processando presença por reunião com conteúdo: {content}")
        try:
            targetComponent = content['targetComponent']
            # substituir serializer_data pela sua mensagem específica
            message = {
                'type': 'presenca.update',
                'data': "presenca.update",
                'targetComponent':targetComponent,
            }
            logger.info(f"Preparando para enviar mensagem para o grupo {self.room_group_name}.")
            await self.channel_layer.group_send(self.room_group_name, message)

            logger.info(f"Mensagem enviada com sucesso para o grupo {self.room_group_name}.")
        except Exception as e:
            logger.error(f"Erro ao processar presença por reunião com conteúdo: {content}. Erro: {str(e)}")
            
    async def limpar_lista_sorteio(self, content):
        logger.info(f"Processando presença por reunião com conteúdo: {content}")
        try:
            # substituir serializer_data pela sua mensagem específica
            targetComponent = content['targetComponent']
            message = {
                'type': 'limpar.update',
                'data': "limpar.update",
                'targetComponent':targetComponent,
            }
            logger.info(f"Preparando para enviar mensagem para o grupo {self.room_group_name}.")
            await self.channel_layer.group_send(self.room_group_name, message)

            logger.info(f"Mensagem enviada com sucesso para o grupo {self.room_group_name}.")
        except Exception as e:
            logger.error(f"Erro ao processar presença por reunião com conteúdo: {content}. Erro: {str(e)}")


    async def abrir_submenu_votacao(self, content):
        logger.info(f"Processando mensagem: {content}")


        try:
            # substituir serializer_data pela sua mensagem específica
            targetComponent = content['targetComponent']
            message = {
                'type': 'abrir_submenu_votacao.update',
                'data': "abrir_submenu_votacao.update",
                'targetComponent':targetComponent,

            }
            logger.info(f"Preparando para enviar mensagem para o grupo {self.room_group_name}.")
            await self.channel_layer.group_send(self.room_group_name, message)

            logger.info(f"Mensagem enviada com sucesso para o grupo {self.room_group_name}.")
        except Exception as e:
            logger.error(f"Erro ao processar presença por reunião com conteúdo: {content}. Erro: {str(e)}")


    async def abrir_submenu_parlamentares(self, content):
        logger.info(f"Processando mensagem: {content}")
        try:
            targetComponent = content['targetComponent']
            # substituir serializer_data pela sua mensagem específica
            message = {
                'type': 'abrir_submenu_parlamentares.update',
                'data': "abrir_submenu_parlamentares.update",
                'targetComponent':targetComponent,
            }
            logger.info(f"Preparando para enviar mensagem para o grupo {self.room_group_name}.")
            await self.channel_layer.group_send(self.room_group_name, message)

            logger.info(f"Mensagem enviada com sucesso para o grupo {self.room_group_name}.")
        except Exception as e:
            logger.error(f"Erro ao processar presença por reunião com conteúdo: {content}. Erro: {str(e)}")

    
    async def votacoes(self, content):
        logger.info(f"Processando mensagem: {content}")
        try:
            # substituir serializer_data pela sua mensagem específica
            targetComponent = content['targetComponent']
            message = {
                'type': 'votacoes.update',
                'data': "votacoes.update",
                'targetComponent':targetComponent,
            }
            logger.info(f"Preparando para enviar mensagem para o grupo {self.room_group_name}.")
            await self.channel_layer.group_send(self.room_group_name, message)

            logger.info(f"Mensagem enviada com sucesso para o grupo {self.room_group_name}.")
        except Exception as e:
            logger.error(f"Erro ao processar presença por reunião com conteúdo: {content}. Erro: {str(e)}")
        
    async def votacoes_update(self, event):
        await self.send_json({
            'type': event['type'],
            'data': event['data'],
            'targetComponent': event['targetComponent'],
        })



    async def reunioes(self, content):
        logger.info(f"Processando mensagem: {content}")
        try:
            # substituir serializer_data pela sua mensagem específica
            targetComponent = content['targetComponent']
            message = {
                'type': 'reunioes.update',
                'data': "reunioes.update",
                'targetComponent':targetComponent,
            }
            logger.info(f"Preparando para enviar mensagem para o grupo {self.room_group_name}.")
            await self.channel_layer.group_send(self.room_group_name, message)

            logger.info(f"Mensagem enviada com sucesso para o grupo {self.room_group_name}.")
        except Exception as e:
            logger.error(f"Erro ao processar presença por reunião com conteúdo: {content}. Erro: {str(e)}")
        
    async def reunioes_update(self, event):
        await self.send_json({
            'type': event['type'],
            'data': event['data'],
            'targetComponent': event['targetComponent'],
        })



    async def receive_json(self, content, **kwargs):
        action = content.get('action')
        if action == 'presenca_por_reuniao':
            await self.presenca_por_reuniao(content)
        elif action == 'pauta_update_reuniao':
            await self.pauta_update_reuniao(content)
        elif action == 'voto_por_reuniao':
            await self.voto_por_reuniao(content)
        elif action == 'sorteio_por_reuniao':  # Ação para tratar a atualização do sorteio
            await self.sorteio_por_reuniao(content)
        elif action == 'limpar_lista_sorteio':  # Ação para tratar a atualização do sorteio
            await self.limpar_lista_sorteio(content)

        elif action == 'abrir_submenu_votacao':  # Ação para tratar da alteração dos submenus de parlamentares e de votações
            await self.abrir_submenu_votacao(content)

        elif action == 'abrir_submenu_parlamentares':  # Ação para tratar da alteração dos submenus de parlamentares e de votações
            await self.abrir_submenu_parlamentares(content)

        elif action == 'editar_all_cronometro':  # Atualiza todos cronometros após a ação
            await self.editar_all_cronometro(content)

        elif action == 'iniciar_cronometro':  # Atualiza todos cronometros após a ação
            await self.iniciar_cronometro(content)

        elif action == 'preparar_cronometro':  # Prepara todos cronometros após a ação
            await self.preparar_cronometro(content)


        elif action == 'editar_cronometro':  # Prepara todos cronometros após a ação
            await self.editar_cronometro(content)

        elif action == 'ajustar_cronometro':  # Prepara todos cronometros após a ação
            await self.ajustar_cronometro(content)

        elif action == 'zerar_cronometro':  # Zera todos cronometros após a ação
            await self.zerar_cronometro(content)

        elif action == 'pausar_cronometro':  # Zera todos cronometros após a ação
            await self.pausar_cronometro(content)
        elif action == 'votacoes':  
            await self.votacoes(content)
        elif action == 'reunioes':  
            await self.reunioes(content)
        elif action == 'limpar_votos':
            await self.limpar_votos(content)
        else:
            await super().receive_json(content, **kwargs)



