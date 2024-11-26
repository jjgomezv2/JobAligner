from django import forms
from .models import JobVacancy

class JobVacancyForm(forms.ModelForm):
    class Meta:
        model = JobVacancy
        fields = '__all__'
        labels = {
            'title': 'Título de la vacante',
            'description': 'Descripción de la vacante',
            'requirements': 'Requisitos de la vacante',
            'location': 'Localización de la compañía',
            'company_name': 'Nombre de la compañía',
        }

