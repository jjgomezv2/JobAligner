from django.db import models
from Accounting.models import User

# Create your models here.
    
class JobVacancy(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    company_name = models.CharField(max_length=200)

class CV(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cvs')
    vacancy = models.ForeignKey(JobVacancy, on_delete=models.CASCADE, related_name='vacancys')
    cvpdf = models.FileField(upload_to='pdfs/', blank=True, null=True)

