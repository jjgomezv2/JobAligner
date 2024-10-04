from django.shortcuts import render, redirect
from .forms import UserProfileForm, EducationForm, WorkExperienceForm, JobVacancyForm
from .models import User, WorkExperience, Education, JobVacancy

import os
from openai import OpenAI
import json
import markdown
from dotenv import load_dotenv, find_dotenv

def home(request):
    return render(request, 'home.html')

def success(request):
    return render(request, 'success.html')

def cv(request, user_id, vacancy_id):

    user_profile = User.objects.get(user_ident = user_id)
    vacancy = JobVacancy.objects.get(id = vacancy_id)

    _ = load_dotenv('openAI.env')

    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get('openAI_api_key'),
    )

    workExperience = ""
    i = 1
    
    workExperienceList = WorkExperience.objects.filter(user=user_profile)

    for item in workExperienceList:
        
        workExperience += f""" Work Experience {i}:

        Company Name: {item.company_name}
        Role: {item.role}
        Start Date: {item.start_date}
        End Date: {item.end_date}
        Achievements: {item.achievements}\n"""

        i += 1

    
    education = ""
    i = 1

    educationList = Education.objects.filter(user=user_profile)

    for item in educationList:
        education += f""" Education {i}:

        Degree: {item.degree}
        Institution: {item.institution}
        Start Date: {item.start_date}
        End Date: {item.end_date}
        Achievements: {item.achievements}\n"""

        i += 1

    prompt = f"""Genera un currículum optimizado para un sistema de seguimiento de candidatos (ATS) utilizando la siguiente información:

        Detalles personales:
        Nombre: {user_profile.name}
        Correo electrónico: {user_profile.email}
        LinkedIn: {user_profile.linkedin}

        Habilidades:
        {user_profile.skills}

        Experiencia laboral:

        {workExperience}
        
        Educación:

        {education}
        
        Detalles de la vacante:
        Título: {vacancy.title}
        Descripción: {vacancy.description}
        Requisitos: {vacancy.requirements}
        Ubicación: {vacancy.location}
        Empresa: {vacancy.company_name}

        Optimiza el CV enfocándote en lo siguiente:

        1. Alinea las habilidades y logros del usuario con los requisitos de la vacante.
        2. Destaca las experiencias y logros educativos relevantes que coincidan con la descripción y el título del puesto.
        3. Asegúrate de que las principales calificaciones y habilidades del perfil del usuario se presenten de manera que maximicen su visibilidad en el sistema ATS.
        4. Estructura el CV en un formato claro y conciso que cumpla con los estándares ATS, incluyendo secciones como 'Experiencia laboral', 'Educación' y 'Habilidades'.
        5. Usa viñetas para enfatizar logros y verbos de acción para describir las tareas realizadas.
        6. Asegúrate de que el CV cumpla con los requisitos de palabras clave de la vacante para aumentar las posibilidades de pasar el filtro ATS."""


    model="gpt-4o-mini"

    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature = 0,
        max_tokens = 1000,
    )

    cvNotFormated = response.choices[0].message.content
    cv = markdown.markdown(cvNotFormated)

    return render(request, 'cv.html', {'hoja': cv})

def vacancy(request, user_id):
    if request.method == 'POST':
        form = JobVacancyForm(request.POST)
        if form.is_valid():
            vacancy = form.save()
            return redirect('cv', user_id=user_id, vacancy_id=vacancy.id)
    else:
        form = JobVacancyForm()

    return render(request, 'vacancy.html', {'vacancyForm': form})

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
            return redirect('vacancy', user_id=user_id)
        

        educationform = EducationForm()
        experienceForm = WorkExperienceForm()
        
    else:
        educationform = EducationForm()
        experienceForm = WorkExperienceForm()
            
    return render(request, 'experience.html', {'education': educationform, 'experience': experienceForm})
