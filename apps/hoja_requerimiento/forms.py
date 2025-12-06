from django import forms
from .models import Anios, Q1_T1

class AniosForm(forms.ModelForm):
    class Meta:
        model = Anios
        fields = '__all__'
        widgets = {
            'anio': forms.TextInput(attrs={
                'class': 'form-control w-100',
                'style': 'margin-bottom: 10px;'
            }),
        }

class Q1_T1Form(forms.ModelForm):
    class Meta:
        model = Q1_T1
        fields = '__all__'
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'