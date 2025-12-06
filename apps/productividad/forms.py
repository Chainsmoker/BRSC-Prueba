from django import forms
from .models import DailyActivity


class ActivityForm(forms.ModelForm):
    class Meta:
        model = DailyActivity
        fields = ('date', 'title', 'description')
        labels = {
            'date': 'Fecha',
            'title': 'Título',
            'description': 'Descripción',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['autocomplete'] = 'off'



class ScoreForm(forms.Form):
    score = forms.ChoiceField(choices=DailyActivity.SCORE_CHOICES)