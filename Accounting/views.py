from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserProfileForm, WorkExperienceForm, EducationForm
from .models import User, Education, WorkExperience

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
def logoutaccount(request): 
    logout(request) 
    return redirect('landing') 

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

@login_required
def updateAccount(request):
    user = request.user  # Django's user
    user_profile = User.objects.get(user=user) # Our user

    searchTerm = request.GET.get('searchEducation')
    if searchTerm:
        educations = Education.objects.filter(degree__icontains = searchTerm, user = user_profile)
    else:
        educations = Education.objects.filter(user = user_profile)
        
    searchTerm2 = request.GET.get('searchExperience')
    if searchTerm2:
        experiences = WorkExperience.objects.filter(role__icontains = searchTerm2, user = user_profile)
    else:
        experiences = WorkExperience.objects.filter(user = user_profile)
    
    return render(request, 'update.html', {'educations': educations, 'experiences': experiences})

@login_required
def delete_work_experience(request, experience_id):
    experience = get_object_or_404(WorkExperience, id=experience_id)
    experience.delete()
    messages.success(request, "La experiencia ha sido eliminada correctamente.")
    return redirect('updateAccount')

@login_required
def delete_education(request, education_id):
    education = get_object_or_404(Education, id=education_id)
    education.delete()
    messages.success(request, "La educación ha sido eliminada correctamente.")
    return redirect('updateAccount')