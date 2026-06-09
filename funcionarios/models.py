from django.db import models
from django.contrib.auth.models import User

from setores.models import Setor


class Funcionario(models.Model):

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    ativo = models.BooleanField(
        default=True
    )

    cargo = models.CharField(
        max_length=100
    )

    funcao = models.TextField()

    telefone = models.CharField(
        max_length=20,
        blank=True
    )

    data_nascimento = models.DateField(
        null=True,
        blank=True
    )

    foto = models.ImageField(
        upload_to='funcionarios/',
        blank=True,
        null=True
    )

    setor = models.ForeignKey(
        Setor,
        on_delete=models.CASCADE
    )

    superior = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):

        return self.usuario.get_full_name()