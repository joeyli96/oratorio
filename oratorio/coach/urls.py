from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'coach'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^result$', views.result, name='result'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)