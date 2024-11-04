from django.contrib import admin
from .models import User, WorkExperience, Education

# Register your models here.

admin.site.register(User)
admin.site.register(WorkExperience)
admin.site.register(Education)