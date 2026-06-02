from django.db import models # type: ignore
from funcionarios.models import Funcionario


class Relatorio(models.Model):

    STATUS = [

        ('Aberto', 'Aberto'),
        ('Em andamento', 'Em andamento'),
        ('Resolvido', 'Resolvido')

    ]

    PRIORIDADE = [

        ('Baixa', 'Baixa'),
        ('Média', 'Média'),
        ('Alta', 'Alta'),
        ('Crítica', 'Crítica')

    ]

    autor = models.ForeignKey(
        Funcionario,
        on_delete=models.CASCADE
    )

    titulo = models.CharField(
        max_length=200
    )

    categoria = models.CharField(
        max_length=100
    )

    problema = models.TextField()

    solucao = models.TextField()

    resultado_final = models.TextField(
        blank=True,
        null=True
    )

    observacoes = models.TextField(
        blank=True,
        null=True
    )

    palavras_chave = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )

    prioridade = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    
    tags = models.ManyToManyField(
        'Tag',
        blank=True
    )

    imagem = models.ImageField(
        upload_to='relatorios/',
        blank=True,
        null=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.titulo
    
class Comentario(models.Model):

    relatorio = models.ForeignKey(
        Relatorio,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )

    autor = models.ForeignKey(
        Funcionario,
        on_delete=models.CASCADE
    )

    texto = models.TextField()

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f'{self.autor} - {self.relatorio}'


class Avaliacao(models.Model):

    relatorio = models.ForeignKey(
        Relatorio,
        on_delete=models.CASCADE,
        related_name='avaliacoes'
    )

    usuario = models.ForeignKey(
        Funcionario,
        on_delete=models.CASCADE
    )

    nota = models.IntegerField()

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = [
            ('relatorio','usuario')
        ]

    def __str__(self):

        return f'{self.relatorio} - {self.nota}'

class Curtida(models.Model):

    TIPOS = [

        ('util', 'Útil'),

        ('nao_ajudou', 'Não ajudou')

    ]

    relatorio = models.ForeignKey(
        Relatorio,
        on_delete=models.CASCADE,
        related_name='curtidas'
    )

    usuario = models.ForeignKey(
        Funcionario,
        on_delete=models.CASCADE
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = [
            ('relatorio','usuario')
        ]

    def __str__(self):

        return f'{self.usuario} - {self.tipo}'

class Tag(models.Model):

    nome = models.CharField(
        max_length=50,
        unique=True
    )

    def __str__(self):

        return f'#{self.nome}'
    
