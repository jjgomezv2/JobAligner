from django.db import models
from jobalignment.models import CV

# Create your models here.
class Suggestion(models.Model):
    cv = models.OneToOneField(CV, on_delete=models.CASCADE)
    suggestions = models.TextField()
    probability = models.IntegerField()
    