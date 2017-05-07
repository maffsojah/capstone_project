# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.views import generic

from . import views


urlpatterns = [
    # url('^$', generic.RedirectView.as_view(url='./mymodel/'), name="index"),
    #url('^$', generic.RedirectView.as_view(url='./customers/'), name="index"),
    url('^$', generic.TemplateView.as_view(template_name="customers/index.html"), name="index"),
    #url('^services/', include(views.ServiceViewSet().urls)),
    #url('^customers/', include(views.CustomerViewSet().urls)),
]
