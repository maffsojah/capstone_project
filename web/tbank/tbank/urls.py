"""tbank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from material.frontend import urls as frontend_urls

from . import forms, widget_forms, admin_forms
from services import urls

def index_view(request):
    context = {
        'login': forms.LoginForm(),
        'registration': forms.RegistrationForm(),
    }
    return render(request, 'index.html', context)


urlpatterns = [
    url(r'^$', index_view),

    # services
    url(r'^services/login/$', generic.FormView.as_view(
        form_class=forms.LoginForm, success_url='/services/login/', template_name="services.html")),
    url(r'^services/registration/$', generic.FormView.as_view(
        form_class=forms.RegistrationForm, success_url='/services/registration/', template_name="services.html")),
    url(r'^services/bank/$', generic.FormView.as_view(
        form_class=forms.BankForm, success_url='/services/bank/', template_name="services.html")),
    url(r'^services/', include('services.urls', namespace='services')),
    url(r'^admin/', admin.site.urls),

    # frontend
    url(r'^frontend/$', generic.RedirectView.as_view(url='/frontend/services/', permanent=False), name="index"),
    url(r'', include(frontend_urls)),
]


if 'material_frontend' not in settings.INSTALLED_APPS:
    urlpatterns += [url(r'^admin/', include(admin.site.urls))]