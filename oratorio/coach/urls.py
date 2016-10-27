from django.conf.urls import url

from . import views

app_name = 'coach'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
