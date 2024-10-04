from django import forms
from .models import WorkExperience, Education, User, JobVacancy

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        exclude = ['user']
        labels = {
            'company_name': 'Nombre empresa',
            'role': 'Cargo',
            'start_date': 'Fecha de inicio',
            'end_date': 'Fecha de fin',
            'achievements': 'Logros',
        }
        

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['user']
        labels = {
            'degree': 'Título obtenido',
            'institution': 'Universidad',
            'start_date': 'Fecha de inicio',
            'end_date': 'Fecha de fin',
            'achievements': 'Logros',
        }
        

class UserProfileForm(forms.ModelForm):
     class Meta:
        model = User
        fields = '__all__'
        labels = {
            'user_ident': 'Número de identificación',
            'name': 'Nombre',
            'email': 'Correo electrónico',
            'linkedin': 'Enlace LinkedIn',
            'skills': 'Habilidades',
        }

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

