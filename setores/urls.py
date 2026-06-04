from django.urls import path
from django.contrib.auth import views as auth_views


from .views import (
    home,
    detalhe_setor,
    cadastrar_setor,
    editar_setor,
    excluir_setor
)

urlpatterns = [

    path(
        '',
        home,
        name='home'
    ),

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
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
]

