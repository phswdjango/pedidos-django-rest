from django.urls import path
from phsw_site.base import views

app_name = 'base'
urlpatterns = [
    path('', views.home, name='home'),
    path('criar-empresa/', views.create_company, name='create_company'),
    path('editar-empresa/', views.edit_company, name='edit_company'),
    path('criar-usuario/', views.create_user, name='create_user'),
    path('editar-usuarios/', views.edit_user, name='edit_user'),
]
