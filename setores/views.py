from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Setor
from .forms import SetorForm
from funcionarios.models import Funcionario
from funcionarios.utils import (
    is_administrador,
    is_rh
)

@login_required
def home(request):

    busca = request.GET.get('busca')

    setores = Setor.objects.all()

    funcionarios = Funcionario.objects.select_related(
        'usuario',
        'setor'
    )

    if busca:

        funcionarios = funcionarios.filter(

            Q(usuario__first_name__icontains=busca) |

            Q(usuario__last_name__icontains=busca) |

            Q(cargo__icontains=busca) |

            Q(funcao__icontains=busca) |

            Q(usuario__email__icontains=busca) |

            Q(setor__nome__icontains=busca)

        )

    return render(
        request,
        'home.html',
        {
            'setores': setores,
            'funcionarios': funcionarios,
            'busca': busca
        }
    )

@login_required
def detalhe_setor(request, setor_id):

    setor = get_object_or_404(Setor, id=setor_id)

    funcionarios = Funcionario.objects.filter(
        setor=setor
    )

    return render(request, 'setores/detalhe_setor.html', {
        'setor': setor,
        'funcionarios': funcionarios
    })
@login_required
def cadastrar_setor(request):

    if not (
        request.user.is_superuser
        or is_administrador(request.user)
    ):
        return redirect('home')

    if request.method == 'POST':

        form = SetorForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('home')

    else:

        form = SetorForm()

    return render(
        request,
        'setores/cadastrar_setor.html',
        {
            'form': form
        }
    )
@login_required
def editar_setor(request, setor_id):

    if not (
        request.user.is_superuser
        or is_administrador(request.user)
    ):
        return redirect('home')

    setor = get_object_or_404(
        Setor,
        id=setor_id
    )

    if request.method == 'POST':

        form = SetorForm(
            request.POST,
            instance=setor
        )

        if form.is_valid():

            form.save()

            return redirect('home')

    else:

        form = SetorForm(instance=setor)

    return render(
        request,
        'setores/editar_setor.html',
        {
            'form': form,
            'setor': setor
        }
    )
@login_required
def excluir_setor(request, setor_id):

    if not (
        request.user.is_superuser
        or is_administrador(request.user)
    ):
        return redirect('home')

    setor = get_object_or_404(
        Setor,
        id=setor_id
    )

    if request.method == 'POST':

        setor.delete()

        return redirect('home')

    return render(
        request,
        'setores/excluir_setor.html',
        {
            'setor': setor
        }
    )