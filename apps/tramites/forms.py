from datetime import date
from tinymce.widgets import TinyMCE

from django import forms
from django.contrib.auth import get_user_model

from .models import Tramite, SeguimientoTramite,GastoTramite

User = get_user_model()

class TramiteForm(forms.ModelForm):
    resolucion_tipo = forms.ChoiceField(
        choices=[
            ('Administrativo', 'Administrativo'),
            ('Municipal', 'Municipal'),
            ('Identificación (RENIEC, otros)', 'Identificación (RENIEC, otros)'),
            ('Tributario', 'Tributario'),
            ('Notarial', 'Notarial'),
            ('Registral', 'Registral'),
            ('Otros', 'Otros'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    resolucion_texto = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''})
    )

    class Meta:
        model = Tramite
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'tramite_tipo': forms.HiddenInput(),
            'sumilla': forms.Textarea(attrs={'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'responsable2' in self.fields:
            self.fields['responsable2'].queryset = (
                User.objects.filter(is_active=True)
                .exclude(username__in=['cdiaz', 'plupa', 'Nelly', 'surcodev'])
                .order_by('first_name')
            )


        for name, field in self.fields.items():
            if name not in ['resolucion_tipo', 'resolucion_texto']:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['autocomplete'] = 'off'

        self.fields['destinatario'].required = False
        self.fields['partes_intervinientes'].required = False
        self.fields['sumilla'].required = False
        self.fields['tramite_tipo'].required = False

        self.fields['fecha'].initial = date.today()
        self.fields['fecha'].widget.attrs['readonly'] = True


    def clean(self):
        cleaned_data = super().clean()
        tipo = (cleaned_data.get('resolucion_tipo') or '').strip()
        texto = (cleaned_data.get('resolucion_texto') or '').strip()

        if tipo or texto:
            tramite_completo = f"{tipo} {texto}".strip()
            cleaned_data['tramite_tipo'] = tramite_completo

        return cleaned_data



class SeguimientoTramiteForm(forms.ModelForm):
    class Meta:
        model = SeguimientoTramite
        exclude = ['caso', 'fecha_registro']
        widgets = {
            'fecha_seguimiento': forms.DateInput(attrs={'type': 'date'}),
            'fecha_alerta': forms.DateInput(
                attrs={
                    'type': 'date',
                    'style': 'background-color: #E8F2F7;',
                }
            ),
            'fecha_pendiente': forms.DateInput(attrs={'type': 'date'}),
            'pendiente': TinyMCE(attrs={'cols': 80, 'rows': 10}),
            'sumilla': TinyMCE(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['responsable'].required = False
        self.fields['seguimiento'].required = False
        self.fields['fecha_seguimiento'].required = False
        self.fields['pdf'].required = False

class GastoTramiteForm(forms.ModelForm):
    class Meta:
        model = GastoTramite
        exclude = ['fecha_registro', 'seguimiento']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'detalle': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['sustento'].required = False
        self.fields['gastos_dolares'].required = False
