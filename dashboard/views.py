from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count
from datetime import date

from funcionarios.models import Funcionario
from setores.models import Setor
from relatorios.models import Relatorio, Favorito


@login_required
def dashboard_home(request):

    # INDICADORES

    total_funcionarios = Funcionario.objects.filter(
        ativo=True
    ).count()

    total_inativos = Funcionario.objects.filter(
        ativo=False
    ).count()

    total_setores = Setor.objects.count()

    total_relatorios = Relatorio.objects.count()

    total_favoritos = Favorito.objects.count()

    # ANIVERSARIANTES DO MÊS

    mes_atual = date.today().month

    aniversariantes = Funcionario.objects.filter(
        ativo=True,
        data_nascimento__month=mes_atual
    ).order_by(
        'data_nascimento__day'
    )

    hoje = date.today()

    aniversariante_do_dia = Funcionario.objects.filter(
        ativo=True,
        data_nascimento__day=hoje.day,
        data_nascimento__month=hoje.month
    ).first()

    # ÚLTIMOS RELATÓRIOS

    ultimos_relatorios = Relatorio.objects.order_by(
        '-criado_em'
    )[:5]

    # TOP CONTRIBUIDORES

    top_contribuidores = Funcionario.objects.filter(
        ativo=True
    ).annotate(
        total_relatorios=Count(
            'relatorio'
        )
    ).order_by(
        '-total_relatorios'
    )[:5]

    # RELATÓRIOS POR SETOR

    dados_setores = []

    for setor in Setor.objects.all():

        total = Relatorio.objects.filter(
            autor__setor=setor
        ).count()

        dados_setores.append({

            'setor': setor.nome,
            'total': total

        })

    context = {

        'total_funcionarios': total_funcionarios,
        'total_inativos': total_inativos,
        'total_setores': total_setores,
        'total_relatorios': total_relatorios,
        'total_favoritos': total_favoritos,

        'ultimos_relatorios': ultimos_relatorios,

        'top_contribuidores': top_contribuidores,

        'dados_setores': dados_setores,

        'aniversariantes': aniversariantes,

    }

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )