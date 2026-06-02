from django.contrib import admin
from .models import Funcionario


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):

    list_display = (
        'usuario',
        'cargo',
        'setor'
    )