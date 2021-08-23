from django.urls import path

from phsw_site.pedidos import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.fazer_pedido, name='fazer_pedido'),
    path('ver-pedidos/', views.ver_pedidos, name='ver_pedidos'),
    path('ver-pedido/', views.ver_pedido, name='ver_pedido'),
    path('editar-itens/', views.editar_itens, name='editar_itens'),
]
