from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import facade
from django.core.paginator import Paginator


@login_required
def pedidos(request):
    if request.user.is_agente_admin:
        pedidos_do_usuario = facade.buscar_pedidos_do_agente_admin(request)
        paginator = Paginator(pedidos_do_usuario, 3)
        page = request.GET.get('page')
        pedidos_paginator = paginator.get_page(page)

        return render(request, 'pedidos/pedidos_agente_admin.html', context={'pedidos': pedidos_paginator})
    pedidos_do_usuario = facade.buscar_pedidos_do_usuario(request)
    paginator = Paginator(pedidos_do_usuario, 3)
    page = request.GET.get('page')
    pedidos_paginator = paginator.get_page(page)
    return render(request, 'pedidos/pedidos.html', context={'pedidos': pedidos_paginator})


