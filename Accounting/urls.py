from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signUp, name='signup'),
    path('login/', views.loginacc, name='login'),
    path('experience/', views.experience, name='experience'),
    path('logout/', views.logoutaccount, name='logoutaccount'),
    path('updateAccount/', views.updateAccount, name='updateAccount'),
    path('work_experience/delete/<int:experience_id>/', views.delete_work_experience, name='delete_work_experience'),
    path('education/delete/<int:education_id>/', views.delete_education, name='delete_education'),
]