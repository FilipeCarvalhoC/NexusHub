from django.contrib import admin # type: ignore

# Register your models here.

from .models import (
    Relatorio,
    Comentario,
    Avaliacao,
    Curtida,
    Tag
)

admin.site.register(Relatorio)
admin.site.register(Comentario)
admin.site.register(Avaliacao)
admin.site.register(Curtida)
admin.site.register(Tag)