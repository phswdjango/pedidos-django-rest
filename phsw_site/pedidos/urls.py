from django.urls import path

from phsw_site.pedidos import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.fazer_pedido, name='fazer_pedido'),
    path('ver-pedido/', views.ver_pedidos, name='ver_pedidos')
]
