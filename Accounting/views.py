from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserProfileForm, WorkExperienceForm, EducationForm
from .models import User

# Create your views here.

def landing(request):
    return render(request, 'landing.html')

def signUp(request):
    if request.method == 'GET':
        user_form = UserCreationForm()
        profile_form = UserProfileForm()
        return render(request, 'signup.html',
                  {'user_form': user_form, 'profile_form': profile_form})
    else:

        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            if request.POST['password1'] == request.POST['password2']:
                user = user_form.save()
                
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                login(request,user) 
                
                return redirect('experience')
            else:
                return render(request, 'signup.html', 
                              {'user_form': user_form, 'profile_form': profile_form, 'error': 'Passwords do not match'})
        else:
            return render(request, 'signup.html', 
                              {'user_form': user_form, 'profile_form': profile_form, 'error': 'Form Validation Error'})

def loginacc(request): 
    if request.method == 'GET': 
        return render(request, 'login.html', 
            {'form':AuthenticationForm}) 
    else: 
         user = authenticate(request, username=request.POST['username'], 
                            password=request.POST['password']) 
    if user is None: 
        return render(request,'login.html', 
                {'form': AuthenticationForm(), 
                'error': 'username and password do not match'}) 
    else: 
        login(request,user) 
        return redirect('home')
    

@login_required
def experience(request):

    user = request.user  # Django's user
    user_profile = User.objects.get(user=user) # Our user
    
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
            return redirect('home')
        

        educationform = EducationForm()
        experienceForm = WorkExperienceForm()
        
    else:
        educationform = EducationForm()
        experienceForm = WorkExperienceForm()
            
    return render(request, 'experience.html', {'education': educationform, 'experience': experienceForm})

