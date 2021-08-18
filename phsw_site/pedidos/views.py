from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import facade
from django.core.paginator import Paginator


@login_required
def ver_pedidos(request):
    pedidos_queryset = facade.buscar_pedidos(request)
    paginator = Paginator(pedidos_queryset, 3)
    page = request.GET.get('page')
    pedidos_paginator = paginator.get_page(page)
    return render(request, 'pedidos/ver_pedidos.html', context={'pedidos': pedidos_paginator})


def fazer_pedido(request):
    itens_queryset = facade.buscar_itens_por_categoria()
    return render(request, 'pedidos/fazer_pedido.html', context={'itens': itens_queryset})


