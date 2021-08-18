from django.urls import path
from phsw_site.base import views

app_name = 'base'
urlpatterns = [
    path('', views.home, name='home'),
]
