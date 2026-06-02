from django.shortcuts import ( # type: ignore
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required # type: ignore
from django.db.models import (# type: ignore
    Q,
    Avg,
    Case,
    When,
    IntegerField,
    Value
) 

from funcionarios.models import Funcionario

from .models import (
    Relatorio,
    Comentario,
    Avaliacao,
    Curtida
)

from .forms import (
    RelatorioForm,
    ComentarioForm,
    AvaliacaoForm
)
from django.contrib import messages # type: ignore

@login_required
def criar_relatorio(request):

    funcionario = get_object_or_404(
        Funcionario,
        usuario=request.user
    )

    if request.method == 'POST':

        form = RelatorioForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            relatorio = form.save(
                commit=False
            )

            relatorio.autor = funcionario

            relatorio.save()

            return redirect(
                'feed_relatorios'
            )

    else:

        form = RelatorioForm()

    return render(

        request,

        'relatorios/criar_relatorio.html',

        {
            'form': form
        }

    )


@login_required
def feed_relatorios(request):

    busca = request.GET.get(
        'busca'
    )

    relatorios = Relatorio.objects.select_related(
        'autor',
        'autor__usuario'
    ).order_by(
        '-criado_em'
    )

    if busca:

        palavras = busca.split()

        sinonimos = {

            'nota':[
                'nf',
                'nfe',
                'nota fiscal'
            ],

            'erro':[
                'falha',
                'problema'
            ],

            'login':[
                'acesso',
                'senha'
            ],

            'certificado':[

                'a1',
                'a3',
                'token'

            ]

        }

        consulta = Q()

        for palavra in palavras:

            termos = [palavra]

            if palavra.lower() in sinonimos:

                termos.extend(

                    sinonimos[
                        palavra.lower()
                    ]

                )

            for termo in termos:

                consulta |= Q(
                    titulo__icontains=termo
                )

                consulta |= Q(
                    categoria__icontains=termo
                )

                consulta |= Q(
                    problema__icontains=termo
                )

                consulta |= Q(
                    solucao__icontains=termo
                )

                consulta |= Q(
                    palavras_chave__icontains=termo
                )

                consulta |= Q(
                    tags__nome__icontains=termo
                )

                consulta |= Q(
                    autor__usuario__first_name__icontains=termo
                )

            relatorios = relatorios.filter(
                consulta
            ).distinct().order_by(
                '-criado_em'
            )

    return render(

        request,

        'relatorios/feed_relatorios.html',

        {
            'relatorios': relatorios,
            'busca': busca
        }

    )

from django.shortcuts import ( # type: ignore
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required # type: ignore
from django.db.models import Q, Avg # type: ignore

from funcionarios.models import Funcionario

from .models import (
    Relatorio,
    Comentario,
    Avaliacao,
    Curtida
)

from .forms import (
    RelatorioForm,
    ComentarioForm,
    AvaliacaoForm
)


@login_required
def criar_relatorio(request):

    funcionario = get_object_or_404(
        Funcionario,
        usuario=request.user
    )

    if request.method == 'POST':

        form = RelatorioForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            relatorio = form.save(
                commit=False
            )

            relatorio.autor = funcionario

            relatorio.save()

            form.save_m2m()

            return redirect(
                'feed_relatorios'
            )

    else:

        form = RelatorioForm()

    return render(
        request,
        'relatorios/criar_relatorio.html',
        {
            'form': form
        }
    )

@login_required
def feed_relatorios(request):

    busca = request.GET.get(
        'busca',
        ''
    )

    relatorios = Relatorio.objects.select_related(
        'autor',
        'autor__usuario'
    ).prefetch_related(
        'tags'
    )

    if busca:

        palavras = busca.split()

        consulta = Q()

        relevancia = Value(
            0,
            output_field=IntegerField()
        )

        for palavra in palavras:

            consulta |= Q(
                titulo__icontains=palavra
            )

            consulta |= Q(
                categoria__icontains=palavra
            )

            consulta |= Q(
                problema__icontains=palavra
            )

            consulta |= Q(
                solucao__icontains=palavra
            )

            consulta |= Q(
                palavras_chave__icontains=palavra
            )

            consulta |= Q(
                tags__nome__icontains=palavra
            )

            relevancia += Case(

                When(
                    titulo__icontains=palavra,
                    then=Value(5)
                ),

                When(
                    tags__nome__icontains=palavra,
                    then=Value(4)
                ),

                When(
                    palavras_chave__icontains=palavra,
                    then=Value(4)
                ),

                When(
                    categoria__icontains=palavra,
                    then=Value(3)
                ),

                When(
                    problema__icontains=palavra,
                    then=Value(2)
                ),

                When(
                    solucao__icontains=palavra,
                    then=Value(1)
                ),

                default=Value(0),

                output_field=IntegerField()

            )

        relatorios = (

            relatorios

            .filter(
                consulta
            )

            .annotate(
                score=relevancia
            )

            .distinct()

            .order_by(
                '-score',
                '-criado_em'
            )

        )

    else:

        relatorios = relatorios.order_by(
            '-criado_em'
        )

    return render(

        request,

        'relatorios/feed_relatorios.html',

        {

            'relatorios': relatorios,

            'busca': busca

        }

    )


@login_required
def detalhe_relatorio(request, relatorio_id):

    relatorio = get_object_or_404(
        Relatorio.objects.prefetch_related(
            'tags'
        ),
        id=relatorio_id
    )

    relatorios_relacionados = Relatorio.objects.filter(

        tags__in=relatorio.tags.all()

    ).exclude(

        id=relatorio.id

    ).distinct()[:5]

    funcionario = get_object_or_404(
        Funcionario,
        usuario=request.user
    )

    comentarios = relatorio.comentarios.all().order_by(
        '-criado_em'
    )

    media = relatorio.avaliacoes.aggregate(
        Avg('nota')
    )

    media_notas = media[
        'nota__avg'
    ]

    curtidas_uteis = relatorio.curtidas.filter(
        tipo='util'
    ).count()

    curtidas_nao_ajudou = relatorio.curtidas.filter(
        tipo='nao_ajudou'
    ).count()

    comentario_form = ComentarioForm()

    avaliacao_form = AvaliacaoForm()

    if request.method == 'POST':

        if 'comentar' in request.POST:

            comentario_form = ComentarioForm(
                request.POST
            )

            if comentario_form.is_valid():

                comentario = comentario_form.save(
                    commit=False
                )

                comentario.autor = funcionario

                comentario.relatorio = relatorio

                comentario.save()

                return redirect(
                    'detalhe_relatorio',
                    relatorio.id
                )

        if 'avaliar' in request.POST:

            avaliacao_form = AvaliacaoForm(
                request.POST
            )

            if avaliacao_form.is_valid():

                nota = avaliacao_form.cleaned_data[
                    'nota'
                ]

                Avaliacao.objects.update_or_create(

                    usuario=funcionario,

                    relatorio=relatorio,

                    defaults={
                        'nota': nota
                    }

                )

                return redirect(
                    'detalhe_relatorio',
                    relatorio.id
                )

        if 'curtir' in request.POST:

            tipo = request.POST.get(
                'tipo'
            )

            Curtida.objects.update_or_create(

                usuario=funcionario,

                relatorio=relatorio,

                defaults={
                    'tipo': tipo
                }

            )

            return redirect(
                'detalhe_relatorio',
                relatorio.id
            )

    return render(
        request,
        'relatorios/detalhe_relatorio.html',
        {

            'relatorio': relatorio,

            'comentarios': comentarios,

            'comentario_form': comentario_form,

            'avaliacao_form': avaliacao_form,

            'media_notas': media_notas,

            'curtidas_uteis': curtidas_uteis,

            'curtidas_nao_ajudou': curtidas_nao_ajudou,

            'relatorios_relacionados': relatorios_relacionados

        }
    )
@login_required
def assistente_ia(request):

    resposta = None

    pergunta = request.GET.get(
        'pergunta'
    )

    if pergunta:

        palavras = pergunta.split()

        consulta = Q()

        for palavra in palavras:

            consulta |= Q(
                titulo__icontains=palavra
            )

            consulta |= Q(
                problema__icontains=palavra
            )

            consulta |= Q(
                solucao__icontains=palavra
            )

            consulta |= Q(
                palavras_chave__icontains=palavra
            )

            consulta |= Q(
                tags__nome__icontains=palavra
            )

        resultados = Relatorio.objects.filter(

            consulta

        ).distinct()[:5]

        resposta = resultados

    return render(

        request,

        'relatorios/assistente_ia.html',

        {

            'resposta': resposta,

            'pergunta': pergunta

        }

    )
@login_required
def editar_relatorio(request, relatorio_id):

    relatorio = get_object_or_404(
        Relatorio,
        id=relatorio_id
    )

    funcionario = Funcionario.objects.get(
        usuario=request.user
    )

    if (
        relatorio.autor != funcionario
        and not request.user.is_superuser
    ):

        messages.error(
            request,
            'Você não possui permissão para editar este relatório.'
        )

        return redirect('feed_relatorios')

    if request.method == 'POST':

        form = RelatorioForm(
            request.POST,
            request.FILES,
            instance=relatorio
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Relatório atualizado com sucesso.'
            )

            return redirect(
                'detalhe_relatorio',
                relatorio.id
            )

    else:

        form = RelatorioForm(
            instance=relatorio
        )

    return render(
        request,
        'relatorios/editar_relatorio.html',
        {
            'form': form,
            'relatorio': relatorio
        }
    )


@login_required
def excluir_relatorio(request, relatorio_id):

    if not request.user.is_superuser:

        messages.error(
            request,
            'Somente administradores podem excluir relatórios.'
        )

        return redirect('feed_relatorios')

    relatorio = get_object_or_404(
        Relatorio,
        id=relatorio_id
    )

    if request.method == 'POST':

        relatorio.delete()

        messages.success(
            request,
            'Relatório removido.'
        )

        return redirect('feed_relatorios')

    return render(
        request,
        'relatorios/excluir_relatorio.html',
        {
            'relatorio': relatorio
        }
    )