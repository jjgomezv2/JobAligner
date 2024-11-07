from django.shortcuts import render
from .models import Suggestion

import os
from openai import OpenAI
import json
import markdown
from dotenv import load_dotenv, find_dotenv

from Accounting.models import WorkExperience, Education

def compute_probability(cv):

    _ = load_dotenv('openAI.env')

    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get('openAI_api_key'),
    )

    workExperience = ""
    i = 1
    
    workExperienceList = WorkExperience.objects.filter(user=cv.user)

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

    educationList = Education.objects.filter(user=cv.user)

    for item in educationList:
        education += f""" Education {i}:

        Degree: {item.degree}
        Institution: {item.institution}
        Start Date: {item.start_date}
        End Date: {item.end_date}
        Achievements: {item.achievements}\n"""

        i += 1

    prompt = f"""Calcula la probabilidad de obtener el empleo descrito en la vacante según la información laboral y educativa del aplicante en la siguiente información:

        Detalles personales:
        Nombre: {cv.user.name}
        Correo electrónico: {cv.user.email}
        LinkedIn: {cv.user.linkedin}

        Habilidades:
        {cv.user.skills}

        Experiencia laboral:

        {workExperience}
        
        Educación:

        {education}
        
        Detalles de la vacante:
        Título: {cv.vacancy.title}
        Descripción: {cv.vacancy.description}
        Requisitos: {cv.vacancy.requirements}
        Ubicación: {cv.vacancy.location}
        Empresa: {cv.vacancy.company_name}

        Teniendo en cuenta para la respuesta lo siguiente:
        1. La respuesta es ÚNICAMENTE un número entero sin el símbolo de porcentaje
        2. Esta debe ser lógica y acorde con lo que solicita la vacante y su concordancia con la educación y experiencia del solicitante
        
        """


    model="gpt-4o-mini"

    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature = 0.5,
        max_tokens = 1000,
    )

    probability = response.choices[0].message.content
    
    return int(probability)
    

def generate_suggestions(cv):

    _ = load_dotenv('openAI.env')

    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get('openAI_api_key'),
    )

    workExperience = ""
    i = 1
    
    workExperienceList = WorkExperience.objects.filter(user=cv.user)

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

    educationList = Education.objects.filter(user=cv.user)

    for item in educationList:
        education += f""" Education {i}:

        Degree: {item.degree}
        Institution: {item.institution}
        Start Date: {item.start_date}
        End Date: {item.end_date}
        Achievements: {item.achievements}\n"""

        i += 1
        
    probability = compute_probability(cv)

    prompt = f"""Da sugerencias para la obtención del empleo según la vacante, la información laboral y educativa del aplicante en la siguiente información:

        Detalles personales:
        Nombre: {cv.user.name}
        Correo electrónico: {cv.user.email}
        LinkedIn: {cv.user.linkedin}

        Habilidades:
        {cv.user.skills}

        Experiencia laboral:

        {workExperience}
        
        Educación:

        {education}
        
        Detalles de la vacante:
        Título: {cv.vacancy.title}
        Descripción: {cv.vacancy.description}
        Requisitos: {cv.vacancy.requirements}
        Ubicación: {cv.vacancy.location}
        Empresa: {cv.vacancy.company_name}

        Teniendo en cuenta para la respuesta lo siguiente:
        1. Que sea lógica y congruente con lo solicitado en la vacante y la información de la persona
        2. Que además se base en la probabilidad calculada de obtención del empleo la cual es: {probability}
        
        """


    model="gpt-4o-mini"

    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature = 0.5,
        max_tokens = 1000,
    )

    suggestions = response.choices[0].message.content
    suggestionsFormated = markdown.markdown(suggestions)
    
    new_suggestion = Suggestion.objects.create(
        cv = cv,
        suggestions = suggestionsFormated,
        probability = probability,
    )