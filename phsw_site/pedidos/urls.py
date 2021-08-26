from django.urls import path

from phsw_site.pedidos import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.fazer_pedido, name='fazer_pedido'),
    path('ver-pedidos/', views.ver_pedidos, name='ver_pedidos'),
    path('ver-pedido/', views.ver_pedido, name='ver_pedido'),
    path('criar-item/', views.criar_item, name='criar_item'),
    path('editar-itens/', views.editar_itens, name='editar_itens'),
    path('criar-tabela-preco/', views.criar_tabela_preco, name='criar_tabela_preco'),
    path('editar-tabelas-preco/', views.editar_tabelas_preco, name='editar_tabelas_preco'),
    path('criar-categoria/', views.criar_categoria, name='criar_categoria'),
    path('editar-categoria/', views.editar_categoria, name='editar_categoria'),



]
