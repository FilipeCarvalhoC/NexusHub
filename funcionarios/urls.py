from django.urls import path

from .views import (
    perfil,
    cadastrar_funcionario,
    editar_funcionario,
    excluir_funcionario,
    organograma,
    editar_meu_perfil
)

urlpatterns = [

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

    path(
        'organograma/',
        organograma,
        name='organograma'
    ),

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
]