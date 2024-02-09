"""
URL configuration for sistema_votacao_projeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, include,re_path
from django.conf import settings
from django.conf.urls.static import static


from rest_framework.routers import DefaultRouter
from votacao.views import (
    LoginAPI, LogoutAPI,VerificarSENHaAPI, HomeAPI, ConfiguracaoAPI, LegislaçaoAPI,GroupViewSet,VereadoresGroupViewSet,GroupConfigViewSet,SpecificGroupViewSet,PaineisGroupViewSet,GroupPainelViewSet,VereadorPhotoAPI,VotacaoRelatorioView,
    ReuniaoViewSet, PautaViewSet, 
    VereadorViewSet, PresencaViewSet,PartidoPoliticoViewSet,VereadoresByPartidoViewSet,MesaDiretoraViewSet,VereadoresByMesaViewSet,ParametrosVotacaoViewSet,TipoAcaoViewSet,PautaViewSet,CronometroAPI,PainelAPI,ReuniaoPlenarioAPI,PautaPorReuniaoViewSet,TelaVotacaoAPI,PresencaViewSet,VotacaoViewSet

)



# Configuração do router do DRF
router = DefaultRouter()
router.register(r'api/groups', GroupViewSet)
router.register(r'api/groups/paineis', GroupPainelViewSet)

router.register(r'api/vereadores', VereadorViewSet)





urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/login/', LoginAPI.as_view(), name='api-login'),
    path('api/logout/', LogoutAPI.as_view(), name='logout_api'),
    path('api/home/', HomeAPI.as_view(), name='api-home'),
    path('api/vereador/photo/', VereadorPhotoAPI.as_view(), name='api-vereador-photo'),
    path('api/telaParlamentar/', TelaVotacaoAPI.as_view(), name='api-home'),
    path('api/reuniao_plenario/', ReuniaoPlenarioAPI.as_view(), name='api-reuniao-plenario'),
    path('api/links_constituicao/', LegislaçaoAPI.as_view(), name='api-links_constituicao'),
    path('api/configuracao/', ConfiguracaoAPI.as_view(), name='api-configuracao'),
    path('api/manage_parlamentar/', VereadorViewSet.as_view({'get': 'composicao_parlamentarAtual', 'post': 'create'}), name='create_parlamentar'),
    path('api/manage_parlamentar/todos/', VereadorViewSet.as_view({'get': 'list', 'post': 'create'}), name='create_parlamentar'),
    re_path(r'^api/manage_parlamentar/(?P<pk>\d+)/$', VereadorViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'}), name='manage_parlamentar'),
    path('api/vereadores/composicao_parlamentar/', GroupViewSet.as_view({'get': 'list'}), name='composicao_parlamentar'), 
    re_path(r'api/groups/(?P<grupo_id>\d+)/vereadores/not_in_group/', VereadoresGroupViewSet.as_view({'get': 'list_not_in_group'}), name='vereadores-not-in-group'),
    re_path(r'api/groups/(?P<grupo_id>\d+)/vereadores/in_group/', VereadoresGroupViewSet.as_view({'get': 'list_in_group'}), name='vereadores-in-group'),
    re_path(r'api/groups/(?P<grupo_id>\d+)/vereadores/add_to_group/', VereadoresGroupViewSet.as_view({'post': 'add_to_group'}), name='add-vereador-to-group'),
    re_path(r'api/groups/(?P<grupo_id>\d+)/vereadores/remove_from_group/', VereadoresGroupViewSet.as_view({'post': 'remove_from_group'}), name='remove-vereador-from-group'),
    re_path(r'api/groups/(?P<grupo_id>\d+)/set-as-current/', GroupConfigViewSet.as_view({'put': 'set_group_as_current'}), name='set_group_as_current'),


    
    path('api/specific-groups/', SpecificGroupViewSet.as_view({'get': 'list'}), name='specific_groups'),
    
    path('api/painelum-groups/', PaineisGroupViewSet.as_view({'get': 'composicao_painelTvUm'}), name='TvUm'),
    path('api/paineldois-groups/', PaineisGroupViewSet.as_view({'get': 'composicao_painelTvDois'}), name='TvDois'),
    path('api/paineltres-groups/', PaineisGroupViewSet.as_view({'get': 'composicao_painelTvTres'}), name='TvTres'),
    
    re_path(r'api/groups/(?P<grupo_id>\d+)/vereadores/list_not_in_group_and_group_atual/', SpecificGroupViewSet.as_view({'get': 'list_not_in_group_and_group_atual'}), name='vereadores-not-in-group'),


    path('api/manage_partido/', PartidoPoliticoViewSet.as_view({'get': 'list', 'post': 'create'}), name='create_partido'),
    re_path(r'^api/manage_partido/(?P<pk>\d+)/$', PartidoPoliticoViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'}), name='manage_partido'),
    re_path(r'^api/vereadores_by_partido/(?P<partido_id>\d+)/$', VereadoresByPartidoViewSet.as_view({'get': 'list'}), name='vereadores_by_partido'),
    re_path(r'^api/vereadores_by_mesa/(?P<mesa_id>\d+)/$', VereadoresByMesaViewSet.as_view({'get': 'list'}), name='vereadores_by_mesa'),
    re_path(r'^api/vereadores_by_mesa/(?P<mesa_id>\d+)/add/$', VereadoresByMesaViewSet.as_view({'post': 'add_vereador_to_mesa'}), name='add_vereador_to_mesa'),
    re_path(r'^api/vereadores_in_mesa/(?P<mesa_id>\d+)/$', VereadoresByMesaViewSet.as_view({'get': 'vereadores_in_mesa'}), name='vereadores_in_mesa'),
    path('api/manage_mesa_diretora/', MesaDiretoraViewSet.as_view({'get': 'list', 'post': 'create'}), name='create_mesa_diretora'),
    re_path(r'^api/manage_mesa_diretora/(?P<pk>\d+)/$', MesaDiretoraViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'}), name='manage_mesa_diretora'),
    path('api/manage_parametro_votacao/', ParametrosVotacaoViewSet.as_view({'get': 'list', 'post': 'create'}), name='create_parametro_votacao'),
    re_path(r'^api/manage_parametro_votacao/(?P<pk>\d+)/$', ParametrosVotacaoViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'}), name='manage_parametro_votacao'),
    path('api/manage_tipo_acao/', TipoAcaoViewSet.as_view({'get': 'list', 'post': 'create'}), name='create_tipo_acao'),
    re_path(r'^api/manage_tipo_acao/(?P<pk>\d+)/$', TipoAcaoViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'}), name='manage_tipo_acao'),
    path('api/manage_reuniao/', ReuniaoViewSet.as_view({'get': 'list', 'post': 'create'}), name='create_reuniao'),
    re_path(r'^api/manage_reuniao/(?P<pk>\d+)/$', ReuniaoViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'}), name='manage_reuniao'),
    path('api/manage_pauta/', PautaViewSet.as_view({'get': 'list', 'post': 'create'}), name='create_pauta'),
    re_path(r'^api/manage_pauta/(?P<pk>\d+)/$', PautaViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'}), name='manage_pauta'),
    re_path(r'^api/reuniao/(?P<reuniao_id>\d+)/votacoes/$', PautaPorReuniaoViewSet.as_view({'get': 'list'}), name='votacoes_por_reuniao'),
    path('api/cronometro/', CronometroAPI.as_view(), name='api-cronometro'),
    path('api/painel/', PainelAPI.as_view(), name='api-painel'),
    path('api/manage_presenca/', PresencaViewSet.as_view({'get': 'list', 'post': 'create'}), name='create_presenca'),
    re_path(r'^api/manage_presenca/(?P<pk>\d+)/$', PresencaViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'}), name='manage_presenca'),
    re_path(r'^api/presenca_por_reuniao/(?P<reuniao_id>\d+)/$', PresencaViewSet.as_view({'get': 'presenca_por_reuniao'}), name='presenca_por_reuniao'),
    re_path(r'^api/presenca_por_reuniao_painel/(?P<reuniao_id>\d+)/$', PresencaViewSet.as_view({'get': 'presenca_por_reuniao_painel'}), name='presenca_por_reuniao_painel'),
    re_path(r'^api/presenca_por_vereador_e_reuniao/(?P<reuniao_id>\d+)/$', PresencaViewSet.as_view({'get': 'presenca_por_vereador_e_reuniao'}), name='presenca_por_vereador_e_reuniao'),
    path('api/votacao/registrar_voto/', VotacaoViewSet.as_view({'post': 'registrar_voto'}), name='registrar_voto'),
    re_path(r'^api/votacao/(?P<pk>\d+)/update/$', VotacaoViewSet.as_view({'put': 'update_voto'}), name='update_voto'),
    path('api/votacao/', VotacaoViewSet.as_view({'get': 'list'}), name='list_votacao'),
    re_path(r'^api/votacao/(?P<pk>\d+)/$', VotacaoViewSet.as_view({'get': 'retrieve'}), name='detail_votacao'),
    path('api/atualizar_em_massa/<int:reuniao_id>/', PresencaViewSet.as_view({'post': 'atualizar_em_massa'}), name='atualizar_em_massa'),
    path('api/votacao/buscar_votos/<str:vereador_username>/<int:reuniao_id>/', VotacaoViewSet.as_view({'get': 'buscar_voto_vereador'}), name='buscar_votos'),
    path('api/votacao/buscar_votos_reuniao/<int:reuniao_id>/', VotacaoViewSet.as_view({'get': 'buscar_votos_todos'}), name='buscar_votos_todos'),
    path('api/presenca/<int:reuniao_id>/relatorio_presenca/', PresencaViewSet.as_view({'get': 'relatorio_presenca'}), name='relatorio_presenca'),
    path('api/votacao/relatorio/<int:pauta_id>/', VotacaoRelatorioView.as_view(), name='votacao_relatorio'),


    path('api/verificar_senha/', VerificarSENHaAPI.as_view(), name='verificar_senha'),
    path('', include(router.urls)),  # Inclui todas as URLs do router do DRF
]
urlpatterns += router.urls
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

    




    #path('api/manage_parlamentar/', ManageParlamentarAPI.as_view(), name='create_parlamentar'),
    #re_path(r'^api/manage_parlamentar/(?P<id>\d+)/$', ManageParlamentarAPI.as_view(), name='manage_parlamentar'),