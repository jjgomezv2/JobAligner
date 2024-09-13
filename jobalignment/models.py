from django.db import models

# Create your models here.
class User(models.Model):
    user_ident = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    linkedin = models.URLField(max_length=100)
    skills = models.TextField()

class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_experiences')
    company_name = models.CharField(max_length=200)
    role = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    achievements = models.TextField(blank=True)
    
class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    achievements = models.TextField(blank=True)
    
class JobVacancy(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    company_name = models.CharField(max_length=200)
