from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

# This class maintains which URLs map to which pages


app_name = 'coach'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^result$', views.result, name='result'),
    url(r'^upload$', views.upload, name='upload'),
    url(r'^userdocs$', views.userdocs, name='userdocs'),
    url(r'^login$', views.login, name='login'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
