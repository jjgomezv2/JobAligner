from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CombinedForm
from .models import User, WorkExperience, Education

# Create your views here.
def home(request):
    if request.method == 'POST':
        form = CombinedForm(request.POST)
        
        if form.is_valid():
            # Guardar UserProfile
            user_profile = form.cleaned_data['user_profile']
            user_profile.save()
            
            # Guardar WorkExperience
            work_experience = form.cleaned_data['work_experience']
            work_experience.user_profile = user_profile
            work_experience.save()
            
            # Guardar Education
            education = form.cleaned_data['education']
            education.user_profile = user_profile
            education.save()

            return redirect('success_url')  # Redirige a form de vacante
    else:
        form = CombinedForm()

    return render(request, 'home.html', {'form': form})