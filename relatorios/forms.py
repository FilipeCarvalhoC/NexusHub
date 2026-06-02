from django import forms # type: ignore
from django.forms import CheckboxSelectMultiple # type: ignore

from .models import (
    Relatorio,
    Comentario,
    Avaliacao
)


class RelatorioForm(forms.ModelForm):

    class Meta:

        model = Relatorio

        fields = [

            'titulo',
            'categoria',
            'problema',
            'solucao',
            'resultado_final',
            'observacoes',
            'palavras_chave',
            'prioridade',
            'status',
            'tags',
            'imagem'

        ]

        widgets = {

            'tags': CheckboxSelectMultiple()

        }

    def __init__(self,*args,**kwargs):

        super().__init__(*args,**kwargs)

        for field in self.fields.values():

            if field.name != 'tags':

                field.widget.attrs.update({

                    'class':'form-control'

                })

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({

                'class': 'form-control'

            })

        self.fields['tags'].widget.attrs.update({

            'class': 'form-check-input'

        })


class ComentarioForm(forms.ModelForm):

    class Meta:

        model = Comentario

        fields = [
            'texto'
        ]

        widgets = {

            'texto': forms.Textarea(

                attrs={

                    'class':'form-control',

                    'rows':4,

                    'placeholder':'Escreva seu comentário...'

                }

            )

        }


class AvaliacaoForm(forms.ModelForm):

    class Meta:

        model = Avaliacao

        fields = [
            'nota'
        ]

        widgets = {

            'nota': forms.Select(

                choices=[

                    (1,'⭐ 1'),
                    (2,'⭐⭐ 2'),
                    (3,'⭐⭐⭐ 3'),
                    (4,'⭐⭐⭐⭐ 4'),
                    (5,'⭐⭐⭐⭐⭐ 5')

                ],

                attrs={

                    'class':'form-select'

                }

            )

        }