# from django import forms
# from .models import *

# class ProyectoForm(forms.ModelForm):
#     class Meta:
#         model = Proyecto
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'
#             field.widget.attrs['autocomplete'] = 'off'

#         # Cambiar el tipo del campo 'fecha' a input date
#         if 'fecha' in self.fields:
#             self.fields['fecha'].widget = forms.DateInput(
#                 attrs={
#                     'class': 'form-control',
#                     'type': 'date',
#                     'autocomplete': 'off',
#                 }
#             )


# class ActividadForm(forms.ModelForm):
#     class Meta:
#         model = Actividad
#         # 🔥 Quitamos 'proyecto' de los campos editables
#         fields = [
#             'descripcion',
#             'sustento',
#             'fecha',
#             'debe',
#             'haber',
#             'saldo',
#         ]

#         widgets = {
#             'descripcion': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Ingrese la descripción de la actividad',
#             }),
#             'sustento': forms.ClearableFileInput(attrs={
#                 'class': 'form-control',
#             }),
#             'fecha': forms.DateInput(attrs={
#                 'class': 'form-control',
#                 'type': 'date',
#             }),
#             'debe': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'step': '0.01',
#             }),
#             'haber': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'step': '0.01',
#             }),
#             'saldo': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'step': '0.01',
#                 'readonly': True,
#             }),
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         debe = cleaned_data.get('debe') or 0
#         haber = cleaned_data.get('haber') or 0
#         cleaned_data['saldo'] = debe - haber
#         return cleaned_data
