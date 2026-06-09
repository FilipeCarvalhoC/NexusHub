from django import forms
from django.contrib.auth.models import User, Group

from .models import Funcionario


class FuncionarioCadastroForm(forms.ModelForm):

    first_name = forms.CharField(
        label='Nome',
        max_length=100
    )

    last_name = forms.CharField(
        label='Sobrenome',
        max_length=100
    )

    username = forms.CharField(
        label='Usuário',
        max_length=100
    )

    email = forms.EmailField(
        label='Email'
    )

    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput,
        required=False
    )

    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label='Cargo de Acesso',
        required=False
    )

    class Meta:

        model = Funcionario

        fields = [
            'cargo',
            'funcao',
            'telefone',
            'data_nascimento',
            'foto',
            'setor',
            'superior'
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # MODO EDIÇÃO
        if self.instance and self.instance.pk:

            self.fields['first_name'].initial = (
                self.instance.usuario.first_name
            )

            self.fields['last_name'].initial = (
                self.instance.usuario.last_name
            )

            self.fields['username'].initial = (
                self.instance.usuario.username
            )

            self.fields['email'].initial = (
                self.instance.usuario.email
            )

            # senha opcional na edição
            self.fields['password'].required = False

        else:

            # senha obrigatória no cadastro
            self.fields['password'].required = True

        
        self.fields['data_nascimento'].widget = forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        )
        # bootstrap
        for field in self.fields.values():

            field.widget.attrs.update({
                'class': 'form-control'
            })

    def clean_username(self):

        username = self.cleaned_data.get('username')

        usuario_existente = User.objects.filter(
            username=username
        ).first()

        # CADASTRO
        if not self.instance.pk:

            if usuario_existente:

                raise forms.ValidationError(
                    'Este nome de usuário já existe.'
                )

        # EDIÇÃO
        else:

            if (
                usuario_existente and
                usuario_existente != self.instance.usuario
            ):

                raise forms.ValidationError(
                    'Este nome de usuário já existe.'
                )

        return username

class MeuPerfilForm(forms.ModelForm):

    first_name = forms.CharField(
        label='Nome',
        max_length=100
    )

    last_name = forms.CharField(
        label='Sobrenome',
        max_length=100
    )

    email = forms.EmailField(
        label='Email'
    )

    class Meta:

        model = Funcionario

        fields = [
            'telefone',
            'foto'
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:

            self.fields['first_name'].initial = (
                self.instance.usuario.first_name
            )

            self.fields['last_name'].initial = (
                self.instance.usuario.last_name
            )

            self.fields['email'].initial = (
                self.instance.usuario.email
            )

        for field in self.fields.values():

            field.widget.attrs.update({
                'class': 'form-control'
            })