from django import forms

from .models import Setor


class SetorForm(forms.ModelForm):

    class Meta:

        model = Setor

        fields = [
            'nome',
            'descricao'
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({
                'class': 'form-control'
            })