from django import forms
from .models import *
from tinymce.widgets import TinyMCE

from django.conf import settings

CUSTOM_TOOLBAR = settings.TINYMCE_DEFAULT_CONFIG.copy()
CUSTOM_TOOLBAR["height"] = 510


class CarpetaFiscalForm(forms.ModelForm):
    class Meta:
        model = CarpetaFiscal
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['autocomplete'] = 'off'
        self.fields['sede'].required = False

class SeguimientoFiscalForm(forms.ModelForm):
    resolucion_tipo = forms.ChoiceField(
        choices=[('Escrito', 'Escrito'),
                ('Resolución', 'Resolución'),
                ('Actualización', 'Actualización'),
                ('Impulso', 'Impulso'),
                ('MAU', 'MAU'),
                ('Contestación de demanda', 'Contestación de demanda'),
                ('Cumplo requerimiento', 'Cumplo requerimiento'),
                ('Subsano omisión', 'Subsano omisión'),
                ('Absuelve traslado', 'Absuelve traslado'),
                ('Recurso de apelación', 'Recurso de apelación'),
                ('Cita con el juez', 'Cita con el juez'),
                ('Oficio', 'Oficio'),
                ('Partida registral', 'Partida registral'),
                ('Disposición', 'Disposición'),
                ('Otros', 'Otros')
                ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    resolucion_texto = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''})
    )

    class Meta:
        model = SeguimientoFiscal
        exclude = ['caso', 'fecha_registro']
        widgets = {
            'fecha_alerta': forms.DateInput(attrs={'type': 'date'}),
            'fecha_seguimiento': forms.DateInput(attrs={'type': 'date'}),
            'fecha_pendiente': forms.DateInput(attrs={'type': 'date'}),
            'inter': forms.CheckboxInput(attrs={
                'class': 'form-check-input switch-color',
                'role': 'switch',
                'id': 'id_inter'
            }),
            'resolucion': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name not in ['inter', 'resolucion_tipo', 'resolucion_texto']:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['autocomplete'] = 'off'

        self.fields['responsable'].required = False
        self.fields['seguimiento'].required = False
        self.fields['fecha_seguimiento'].required = False
        self.fields['pdf'].required = False
        self.fields['inter'].required = False

    def clean(self):
        cleaned_data = super().clean()
        tipo = (cleaned_data.get('resolucion_tipo') or '').strip()
        texto = (cleaned_data.get('resolucion_texto') or '').strip()

        if tipo or texto:
            resolucion_completa = f"{tipo} {texto}".strip()
            cleaned_data['resolucion'] = resolucion_completa
            cleaned_data['inter'] = True if tipo.lower() == 'resolución' else False

        return cleaned_data

class GastoFiscalForm(forms.ModelForm):
    class Meta:
        model = GastoFiscal
        exclude = ['fecha_registro', 'seguimiento'] 
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        self.fields['sustento'].required = False
        self.fields['gastos_dolares'].required = False

#########################################################################################

class CasoJudicialForm(forms.ModelForm):
    class Meta:
        model = CasoJudicial
        fields = '__all__'
        widgets = {
            'fecha_compromiso': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['autocomplete'] = 'off'
        self.fields['sede'].required = False

class SeguimientoForm(forms.ModelForm):
    resolucion_tipo = forms.ChoiceField(
        choices=[('Escrito', 'Escrito'),
                ('Resolución', 'Resolución'),
                ('Actualización', 'Actualización'),
                ('Impulso', 'Impulso'),
                ('MAU', 'MAU'),
                ('Contestación de demanda', 'Contestación de demanda'),
                ('Cumplo requerimiento', 'Cumplo requerimiento'),
                ('Subsano omisión', 'Subsano omisión'),
                ('Absuelve traslado', 'Absuelve traslado'),
                ('Recurso de apelación', 'Recurso de apelación'),
                ('Cita con el juez', 'Cita con el juez'),
                ('Oficio', 'Oficio'),
                ('Partida registral', 'Partida registral'),
                ('Lectura de expediente', 'Lectura de expediente'),
                ('Otros', 'Otros')
                ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    resolucion_texto = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''})
    )

    class Meta:
        model = Seguimiento
        exclude = ['caso', 'fecha_registro']
        widgets = {
            'fecha_seguimiento': forms.DateInput(attrs={'type': 'date'}),
            'fecha_pendiente': forms.DateInput(attrs={'type': 'date'}),
            'fecha_alerta': forms.DateInput(attrs={'type': 'date'}),
            'resolucion': forms.HiddenInput(), 
            'seguimiento': TinyMCE(mce_attrs=CUSTOM_TOOLBAR),
            'pendiente': TinyMCE(mce_attrs=CUSTOM_TOOLBAR),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name not in ['resolucion_tipo', 'resolucion_texto']:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['autocomplete'] = 'off'

        self.fields['responsable'].required = False
        self.fields['seguimiento'].required = False
        self.fields['fecha_seguimiento'].required = False
        self.fields['pdf'].required = False

    def clean(self):
        cleaned_data = super().clean()
        tipo = (cleaned_data.get('resolucion_tipo') or '').strip()
        texto = (cleaned_data.get('resolucion_texto') or '').strip()

        if tipo or texto:
            resolucion_completa = f"{tipo} {texto}".strip()
            cleaned_data['resolucion'] = resolucion_completa

        return cleaned_data


class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        exclude = ['fecha_registro', 'seguimiento'] 
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['sustento'].required = False
        self.fields['gastos_dolares'].required = False

