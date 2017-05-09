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
from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.shortcuts import render
from django.views import generic

from formtools.wizard.views import SessionWizardView
from material.frontend import urls as frontend_urls

from tbank import forms
from . import forms, widget_forms, admin_forms
#, widget_forms, admin_forms

def index_view(request):
    context = {
        #'login': forms.LoginForm(),
        #'registration': forms.RegistrationForm(),
    }
    return render(request, 'index.html', context)

# class Wizard(SessionWizardView):
#     form_list = [forms.WizardForm1, forms.WizardForm2]
#
#     def done(self, form_list, **kwargs):
#         return render(self.request, 'formtools/wizard/wizard_done.html', {
#             'form_data': [form.cleaned_data for form in form_list],
#         })
#
class WidgetFormView(generic.FormView):
    template_name = 'widgets_tbank.html'

    def form_valid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))

#
class AdminFormView(generic.FormView):
    template_name = 'admin_tbank.html'

    @classmethod
    def as_view(cls, *args, **kwargs):
        return login_required(super(AdminFormView, cls).as_view(*args, **kwargs))

    def form_valid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))
#

urlpatterns = [
    url(r'^$', index_view),

    # services
    # url(r'^tbank/login/$', generic.FormView.as_view(
    #     form_class=forms.LoginForm, success_url='/tbank/login/', template_name="tbank.html")),
    # url(r'^tbank/registration/$', generic.FormView.as_view(
    #     form_class=forms.RegistrationForm, success_url='/tbank/registration/', template_name="tbank.html")),
    # url(r'^tbank/bank/$', generic.FormView.as_view(
    #     form_class=forms.BankForm, success_url='/tbank/bank/', template_name="tbank.html")),
    # url(r'^services/', include('services.urls', namespace='services')),


    # frontend
    url(r'^frontend/$', generic.RedirectView.as_view(url='/frontend/customers/', permanent=False), name="index"),
    url(r'', include(frontend_urls)),
]


if 'material_frontend' not in settings.INSTALLED_APPS:
    urlpatterns += [url(r'^admin/', include(admin.site.urls))]
