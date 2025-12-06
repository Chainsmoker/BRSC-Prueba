from django import forms
from .models import Partida,Plano

class PartidaForm(forms.ModelForm):
    class Meta:
        model = Partida
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['autocomplete'] = 'off'

        self.fields['responsable'].required = False
        self.fields['centro_costos'].required = False
        self.fields['partida'].required = False

class PlanoForm(forms.ModelForm):
    class Meta:
        model = Plano
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
