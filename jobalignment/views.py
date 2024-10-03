from django.shortcuts import render, redirect
from .forms import UserProfileForm, EducationForm, WorkExperienceForm
from .models import User

def home(request):
    return render(request, 'home.html')

def success(request):
    return render(request, 'success.html')

def vacancy(request):
    return render(request, 'vacancy.html')

def signUp(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile = form.save()
            return redirect('experience', user_id = user_profile.user_ident)
    else:
        form = UserProfileForm()

    return render(request, 'signup.html', {'userData': form})


def experience(request, user_id):
    user_profile = User.objects.get(user_ident = user_id)
    
    if request.method == 'POST':
        if 'formEducation' in request.POST:
            educationform = EducationForm(request.POST)
            if educationform.is_valid():
                education = educationform.save(commit=False)
                education.user = user_profile
                education.save()
            
        elif 'formExperience' in request.POST:
            experienceForm = WorkExperienceForm(request.POST)
            if experienceForm.is_valid():
                experience = experienceForm.save(commit=False)
                experience.user = user_profile
                experience.save()
                

        elif 'continueBtn' in request.POST:  # Manejo del botón "Continuar"
            return redirect('success')  # Redirige a la página de éxito
        

        educationform = EducationForm()
        experienceForm = WorkExperienceForm()
        
    else:
        educationform = EducationForm()
        experienceForm = WorkExperienceForm()
            
    return render(request, 'experience.html', {'education': educationform, 'experience': experienceForm})
