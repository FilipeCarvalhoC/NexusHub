from django.db import models

# Create your models here.

class Setor(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'