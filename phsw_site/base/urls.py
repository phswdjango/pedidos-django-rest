from django.urls import path
from phsw_site.base import views

app_name = 'base'
urlpatterns = [
    path('', views.home, name='home'),
    path('criar-empresa/', views.criar_empresa, name='criar_empresa'),
    path('editar-empresa/', views.editar_empresa, name='editar_empresa'),
    path('criar-usuario/', views.criar_usuario, name='criar_usuario'),
    path('editar-usuarios/', views.editar_usuarios, name='editar_usuario'),
]
