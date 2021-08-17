from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import facade
from django.core.paginator import Paginator


@login_required
def pedidos(request):
    pedidos_queryset = facade.buscar_pedidos(request)
    paginator = Paginator(pedidos_queryset, 3)
    page = request.GET.get('page')
    pedidos_paginator = paginator.get_page(page)
    return render(request, 'pedidos/pedidos.html', context={'pedidos': pedidos_paginator})
