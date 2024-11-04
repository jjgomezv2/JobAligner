from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signUp, name='signup'),
    path('login/', views.loginacc, name='login'),
    path('experience/', views.experience, name='experience'),
]