from django import forms
from .models import JobVacancy

class JobVacancyForm(forms.ModelForm):
    class Meta:
        model = JobVacancy
        fields = '__all__'
        labels = {
            'title': 'Título de la vacante',
            'decription': 'Descripción de la vacante',
            'requirements': 'Requisitos de la vacante',
            'location': 'Localización del lugar',
            'company_name': 'Nombre de la compañía',
        }

