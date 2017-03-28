from django.conf.urls import url, include
from django.views import generic

from . import views

urlpatterns = [
    url('^', generic.TemplateView.as_view(template_name="home.html"), name="index"),
    # ex: /
    url(r'^', views.active_customer_list, name='active_customers'),
    # ex: /services/1
    url(r'^services/(?P<active_customer_id>[0-9]+)/$', views.customer_details, name='active_customer_details'),
    # ex: /
    url(r'^', views.inactive_customer_list, name='inactive_customers'),
    # ex: /services/1
    url(r'^services/(?P<inactive_customer_id>[0-9]+)/$', views.customer_details, name='inactive_customer_details'),
    # ex: /level
    url(r'^level', views.services_list, name='services_list'),
    # ex: /level/5
    url(r'^level/(?P<service_level_id>[0-9]+)/$', views.service_level_details, name='service_level_details'),
    # ex: /services/user - get services for the logged users
    url(r'^services/user/(?P<username>\w+)/', views.active_customer_list, name='active_customer_list'),
    url(r'^services/user/', views.active_customer_list, name='active_customer_list'),

    # url(r'^active_users', views.active_users, name='active_users'),
    # url(r'^inactive_users', views.inactive_users, name='inactive_users'),
]
