from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import FuncionarioCadastroForm
from .models import Funcionario
from .utils import (
    is_administrador,
    is_rh,
    is_gestor
)


@login_required
def perfil(request):

    funcionario = get_object_or_404(
        Funcionario,
        usuario=request.user
    )

    return render(
        request,
        'funcionarios/perfil.html',
        {
            'funcionario': funcionario
        }
    )


@login_required
def cadastrar_funcionario(request):

    if not (
        request.user.is_superuser
        or is_rh(request.user)
        or is_administrador(request.user)
    ):
        return redirect('home')

    if request.method == 'POST':

        form = FuncionarioCadastroForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            usuario = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )

            funcionario = form.save(commit=False)

            funcionario.usuario = usuario

            grupo = form.cleaned_data['grupo']

            usuario.groups.add(grupo)

            funcionario.save()

            return redirect('home')

        else:

            print(form.errors)

    else:

        form = FuncionarioCadastroForm()

    return render(
        request,
        'funcionarios/cadastrar_funcionario.html',
        {
            'form': form
        }
    )


@login_required
def editar_funcionario(request, funcionario_id):

    if not (
        request.user.is_superuser
        or is_rh(request.user)
        or is_administrador(request.user)
    ):
        return redirect('home')

    funcionario = get_object_or_404(
        Funcionario,
        id=funcionario_id
    )

    if request.method == 'POST':

        form = FuncionarioCadastroForm(
            request.POST,
            request.FILES,
            instance=funcionario
        )

        if form.is_valid():

            funcionario = form.save(commit=False)

            usuario = funcionario.usuario

            usuario.first_name = form.cleaned_data['first_name']

            usuario.last_name = form.cleaned_data['last_name']

            usuario.email = form.cleaned_data['email']

            usuario.username = form.cleaned_data['username']

            # altera senha somente se preencher
            if form.cleaned_data['password']:

                usuario.set_password(
                    form.cleaned_data['password']
                )

            usuario.save()

            funcionario.save()

            return redirect('home')

        else:

            print(form.errors)

    else:

        form = FuncionarioCadastroForm(
            instance=funcionario
        )

    return render(
        request,
        'funcionarios/editar_funcionario.html',
        {
            'form': form,
            'funcionario': funcionario
        }
    )


@login_required
def excluir_funcionario(request, funcionario_id):

    if not (
        request.user.is_superuser
        or is_rh(request.user)
        or is_administrador(request.user)
    ):
        return redirect('home')

    funcionario = get_object_or_404(
        Funcionario,
        id=funcionario_id
    )

    if request.method == 'POST':

        funcionario.usuario.delete()

        return redirect('home')

    return render(
        request,
        'funcionarios/excluir_funcionario.html',
        {
            'funcionario': funcionario
        }
    )


@login_required
def organograma(request):

    funcionarios = Funcionario.objects.select_related(
        'usuario',
        'setor',
        'superior'
    ).all()

    lideres = funcionarios.filter(
        superior__isnull=True
    )

    return render(
        request,
        'funcionarios/organograma.html',
        {
            'lideres': lideres,
            'funcionarios': funcionarios
        }
    )


@login_required
def editar_meu_perfil(request):

    funcionario = get_object_or_404(
        Funcionario,
        usuario=request.user
    )

    if request.method == 'POST':

        form = FuncionarioCadastroForm(
            request.POST,
            request.FILES,
            instance=funcionario
        )

        if form.is_valid():

            funcionario = form.save(commit=False)

            usuario = funcionario.usuario

            usuario.first_name = form.cleaned_data['first_name']

            usuario.last_name = form.cleaned_data['last_name']

            usuario.email = form.cleaned_data['email']

            usuario.username = form.cleaned_data['username']

            if form.cleaned_data['password']:

                usuario.set_password(
                    form.cleaned_data['password']
                )

            usuario.save()

            funcionario.save()

            return redirect('perfil')

        else:

            print(form.errors)

    else:

        form = FuncionarioCadastroForm(
            instance=funcionario
        )

    return render(
        request,
        'funcionarios/editar_meu_perfil.html',
        {
            'form': form,
            'funcionario': funcionario
        }
    )