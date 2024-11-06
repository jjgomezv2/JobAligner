from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import JobVacancyForm
from .models import JobVacancy, CV
from Accounting.models import User, WorkExperience, Education

# AI Libraries
import os
from openai import OpenAI
import json
import markdown
from dotenv import load_dotenv, find_dotenv

#Libraries for pdf
import io
from django.core.files.base import ContentFile
from xhtml2pdf import pisa

@login_required
def home(request):

    user = request.user  # Django's user
    user_profile = User.objects.get(user=user) # Our user

    searchTerm = request.GET.get('searchProduct')
    if searchTerm:
        cvs = CV.objects.filter(vacancy__title__icontains = searchTerm, user = user_profile)
    else:
        cvs = CV.objects.filter(user = user_profile)
    
    return render(request, 'home.html', {'user': user,'searchTerm':searchTerm, 'cvs': cvs})


def success(request):
    return render(request, 'success.html')

@login_required
def vacancy(request):

    user = request.user  # Django's user
    user_profile = User.objects.get(user=user) # Our user

    if request.method == 'POST':
        form = JobVacancyForm(request.POST)
        if form.is_valid():

            vacancy = form.save()

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
            cvFormated = markdown.markdown(cvNotFormated)

            new_cv = CV.objects.create(
                user = user_profile,
                vacancy = vacancy,
                cvpdf = None,
            )

            pdf_file = generateDocumentCV(cvFormated, new_cv.id)

            new_cv.cvpdf = pdf_file

            new_cv.save()
            
            return redirect('cv', cv_id=new_cv.id)
    else:
        form = JobVacancyForm()

    return render(request, 'vacancy.html', {'vacancyForm': form})



def generateDocumentCV(formatedText, idcv):
    # Configura el buffer de memoria para guardar el PDF temporalmente
    buffer = io.BytesIO()

    # Define un HTML básico con el contenido formateado
    html_content = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Helvetica, sans-serif;
                    margin: 20px;
                }}
                h1 {{
                    text-align: center;
                }}
                p {{
                    margin: 10px 0;
                }}
            </style>
        </head>
        <body>
            <h1>Hoja de Vida</h1>
            <div>
                {formatedText}
            </div>
        </body>
    </html>
    """

    # Genera el PDF a partir del contenido HTML
    pisa_status = pisa.CreatePDF(io.BytesIO(html_content.encode("UTF-8")), dest=buffer)

    # Verifica si hubo errores al crear el PDF
    if pisa_status.err:
        print("Error al generar el PDF")

    # Guarda el contenido del buffer como un archivo PDF en el modelo
    buffer.seek(0)
    pdf_content = ContentFile(buffer.read(), name=str(idcv) + ".pdf")
    buffer.close()

    return pdf_content


@login_required
def cv(request, cv_id):
    
    cv = get_object_or_404(CV, id=cv_id)
    print(cv.cvpdf.url)
    return render(request, 'cv.html', {'cv': cv})
