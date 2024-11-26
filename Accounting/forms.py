from django import forms
from .models import User, WorkExperience, Education

class UserProfileForm(forms.ModelForm):
     class Meta:
        model = User
        exclude = ['user']
        labels = {
            'user_ident': 'Número de identificación',
            'name': 'Nombre',
            'email': 'Correo electrónico',
            'linkedin': 'Enlace LinkedIn',
            'skills': 'Habilidades',
        }

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
    
    start_date = forms.DateField(
        label= 'Fecha de inicio',
        widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        label= 'Fecha de fin',
        widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'})
    )
        

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
        
    start_date = forms.DateField(
        label= 'Fecha de inicio',
        widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        label= 'Fecha de fin',
        widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'})
    )