"""
URL configuration for nexusHub project.
"""

from django.contrib import admin # type: ignore
from django.urls import path # type: ignore

from django.conf import settings # type: ignore
from django.conf.urls.static import static # type: ignore

from django.contrib.auth import views as auth_views # type: ignore

from funcionarios.views import (
    perfil,
    cadastrar_funcionario,
    editar_funcionario,
    excluir_funcionario,
    organograma,
    editar_meu_perfil
)

from setores.views import (
    home,
    detalhe_setor,
    cadastrar_setor,
    editar_setor,
    excluir_setor
)

from relatorios.views import (
    criar_relatorio,
    feed_relatorios,
    detalhe_relatorio,
    assistente_ia,
    excluir_relatorio,
    editar_relatorio
)

urlpatterns = [

    # ADMIN
    path(
        'admin/',
        admin.site.urls
    ),

    # LOGIN
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ),
        name='login'
    ),

    # LOGOUT
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # HOME
    path(
        '',
        home,
        name='home'
    ),

    # PERFIL
    path(
        'perfil/',
        perfil,
        name='perfil'
    ),

    path(
        'perfil/editar/',
        editar_meu_perfil,
        name='editar_meu_perfil'
    ),

    # SETORES
    path(
        'setor/<int:setor_id>/',
        detalhe_setor,
        name='detalhe_setor'
    ),

    path(
        'setores/cadastrar/',
        cadastrar_setor,
        name='cadastrar_setor'
    ),

    path(
        'setores/editar/<int:setor_id>/',
        editar_setor,
        name='editar_setor'
    ),

    path(
        'setores/excluir/<int:setor_id>/',
        excluir_setor,
        name='excluir_setor'
    ),

    # FUNCIONÁRIOS
    path(
        'funcionarios/cadastrar/',
        cadastrar_funcionario,
        name='cadastrar_funcionario'
    ),

    path(
        'funcionarios/editar/<int:funcionario_id>/',
        editar_funcionario,
        name='editar_funcionario'
    ),

    path(
        'funcionarios/excluir/<int:funcionario_id>/',
        excluir_funcionario,
        name='excluir_funcionario'
    ),

    # ORGANOGRAMA
    path(
        'organograma/',
        organograma,
        name='organograma'
    ),

    # RELATORIO

    path(
        'relatorios/novo/',
        criar_relatorio,
        name='criar_relatorio'
    ),

    path(
        'relatorios/',
        feed_relatorios,
        name='feed_relatorios'
    ),
    path(
        'relatorios/<int:relatorio_id>/',
        detalhe_relatorio,
        name='detalhe_relatorio'
    ),
    path(
        'assistente/',
        assistente_ia,
        name='assistente_ia'
    ),  
    path(
        'relatorios/editar/<int:relatorio_id>/',
        editar_relatorio,
        name='editar_relatorio'
    ),

    path(
        'relatorios/excluir/<int:relatorio_id>/',
        excluir_relatorio,
        name='excluir_relatorio'
    ),                                  

]

# MEDIA FILES
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)