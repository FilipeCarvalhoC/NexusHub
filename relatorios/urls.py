from django.urls import path

from .views import (
    criar_relatorio,
    feed_relatorios,
    detalhe_relatorio,
    editar_relatorio,
    excluir_relatorio,
    assistente_ia,
    meus_favoritos
)

urlpatterns = [

    path(
        'relatorios/',
        feed_relatorios,
        name='feed_relatorios'
    ),

    path(
        'relatorios/novo/',
        criar_relatorio,
        name='criar_relatorio'
    ),

    path(
        'relatorios/<int:relatorio_id>/',
        detalhe_relatorio,
        name='detalhe_relatorio'
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

    path(
        'favoritos/',
        meus_favoritos,
        name='meus_favoritos'
    ),

    path(
        'assistente/',
        assistente_ia,
        name='assistente_ia'
    ),
]