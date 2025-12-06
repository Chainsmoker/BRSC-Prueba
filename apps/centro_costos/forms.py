from django import forms
from .models import *

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        self.fields['tipo'].required = True
        self.fields['responsable'].required = False

        choices = self.fields['tipo'].choices
        filtered_choices = [choice for choice in choices if choice[0] != '']
        self.fields['tipo'].choices = [('', 'Seleccione tipo de gasto')] + filtered_choices
        #self.fields['responsable'].empty_label = "Seleccione responsable"

class GastoTA2020Form(forms.ModelForm):
    class Meta:
        model = GastoTA2020
        fields = ['actividad', 'item', 'fecha', 'detalle', 'documento', 'debe', 'haber', 'tipo_gasto']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['actividad'].empty_label = "Seleccione actividad"

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class CantaCallaoForm(forms.ModelForm):
    class Meta:
        model = CantaCallao
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
class NuevoGastoForm(forms.ModelForm):
    class Meta:
        model = NuevoGasto
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control w-100',
                'style': 'margin-bottom: 10px;'
            }),
        }

class GastoForm(forms.ModelForm):
    MOVIMIENTO_CHOICES = [
        (False, "Salida"),
        (True, "Ingreso"),
    ]

    es_ingreso = forms.ChoiceField(
        choices=MOVIMIENTO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        label="Movimiento"
    )

    class Meta:
        model = Gasto
        exclude = ['origen', 'fecha_registro', 'ultima_modificacion', 'editor']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'placeholder': 'XX-XXX-XX', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.initial.get('monto_dolares') is None:
            self.initial['monto_dolares'] = ''
        if self.instance and getattr(self.instance, 'monto_dolares', None) is None:
            self.fields['monto_dolares'].initial = ''

        for name, field in self.fields.items():
            if name not in ['es_ingreso', 'codigo', 'fecha']:
                field.widget.attrs['class'] = 'form-control'

class GastoN9Form(forms.ModelForm):
    class Meta:
        model = GastoN9
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('monto_dolares') is None:
            self.initial['monto_dolares'] = ''
        if self.instance and getattr(self.instance, 'monto_dolares', None) is None:
            self.fields['monto_dolares'].initial = ''
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


