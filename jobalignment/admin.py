from django.contrib import admin
from .models import User, WorkExperience, Education, JobVacancy

# Register your models here.

admin.site.register(User)
admin.site.register(WorkExperience)
admin.site.register(Education)
admin.site.register(JobVacancy)
