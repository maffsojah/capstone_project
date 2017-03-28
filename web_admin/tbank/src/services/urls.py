from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^clients/active_users$', views.Clients.as_view(), name='active_users'),
    url(r'^clients/inactive_users$', views.Clients.as_view(), name='inactive_users'),
]
