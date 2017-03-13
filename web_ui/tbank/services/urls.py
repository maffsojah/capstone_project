from django.conf.urls import url

from services import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^active_users', views.active_users, name='active_users'),
]
