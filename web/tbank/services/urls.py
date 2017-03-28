# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.views import generic
from . import views

from services import urls


urlpatterns = [
    url('^$', generic.RedirectView.as_view(url='./services/'), name="index"),
    url('^customers/', include(views.CustomerViewSet().urls)),
    url('^services/', include(views.ServiceLevelViewSet().urls)),
    # url('^mymodel/', include(views.MyModelViewSet().urls)),
    # ex: /
   # url(r'^$', views.active_customer_list, name='customer_list'),
    # ex: /review/5/
    # url(r'^customers/(?P<customer_id>[0-9]+)/$', views.customer_detail, name='customer_detail'),
    # # ex: /wine/
    # url(r'^service_level$', views.service_list, name='service_list'),
    # # ex: /wine/5/
    # url(r'^service_level/(?P<service_id>[0-9]+)/$', views.service_detail, name='service_detail'),
]