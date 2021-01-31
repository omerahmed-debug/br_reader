from django.urls import path
from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('read', views.read, name='read'),
        url(r'^.*$', RedirectView.as_view(url='/', permanent=False), name='index')

]