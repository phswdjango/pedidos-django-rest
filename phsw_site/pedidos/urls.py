from django.urls import path

from phsw_site.pedidos import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.pedidos, name='pedidos'),
]
