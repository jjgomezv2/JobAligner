"""
URL configuration for jobaligner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from jobalignment import views as jobAlignmentViews
from Accounting import views as accountingViews

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', accountingViews.landing, name='landing'),
    path('admin/', admin.site.urls),
    path('account/', include('Accounting.urls')),
    path('success/', jobAlignmentViews.success, name='success'),
    path('vacancy/', jobAlignmentViews.vacancy, name='vacancy'),
    path('home/', jobAlignmentViews.home, name='home'),
    path('cv/<int:cv_id>/', jobAlignmentViews.cv, name='cv'),
    path('cv/delete/<int:cv_id>/', jobAlignmentViews.delete_cv, name='delete_cv'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
