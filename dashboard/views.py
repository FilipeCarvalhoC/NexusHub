from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from funcionarios.models import Funcionario
from setores.models import Setor
from relatorios.models import Relatorio, Favorito


@login_required
def dashboard_home(request):

    total_funcionarios = Funcionario.objects.count()

    total_setores = Setor.objects.count()

    total_relatorios = Relatorio.objects.count()

    total_favoritos = Favorito.objects.count()

    ultimos_relatorios = Relatorio.objects.order_by(
        '-criado_em'
    )[:5]

    context = {

        'total_funcionarios': total_funcionarios,

        'total_setores': total_setores,

        'total_relatorios': total_relatorios,

        'total_favoritos': total_favoritos,

        'ultimos_relatorios': ultimos_relatorios,

    }

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )