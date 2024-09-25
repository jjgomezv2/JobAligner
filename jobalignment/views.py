from django.shortcuts import render, redirect
from .forms import UserProfileForm, EducationForm, WorkExperienceForm
from .models import User

def home(request):
    if request.method == 'POST':
        if 'user_profile_id' in request.POST:
            # Handle modal form submission
            user_profile_id = request.POST.get('user_profile_id')
            user_profile = User.objects.get(id=user_profile_id)

            education_form = EducationForm(request.POST)
            work_experience_form = WorkExperienceForm(request.POST)
            if education_form.is_valid() and work_experience_form.is_valid():

                if work_experience_form:
                    work_experience = work_experience_form.save(commit=False)
                    work_experience.user = user_profile
                    work_experience.save()
                
                if education_form:
                    education = education_form.save(commit=False)
                    education.user = user_profile
                    education.save()

            return redirect('success')  # Redirect to success URL

        else:
            # Handle user profile form submission
            user_profile_form = UserProfileForm(request.POST)
            if user_profile_form.is_valid():
                # Save UserProfile and pass the ID to the context for the modal
                user_profile = user_profile_form.save()
                return render(request, 'home.html', {
                    'education': EducationForm(),
                    'experience': WorkExperienceForm(),
                    'userData': user_profile_form,
                    'user_profile_id': user_profile.id
                })
    
    else:
        user_profile_form = UserProfileForm()
        work_experience_form = WorkExperienceForm()
        education_form = EducationForm()

    return render(request, 'home.html', {
        'education': education_form,
        'experience': work_experience_form,
        'userData': user_profile_form,
        'user_profile_id': None
    })

def success(request):
    return render(request, 'success.html')
