from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import facade

@login_required
def pedidos(request):
    pedidos_do_usuario = facade.buscar_pedidos_do_usuario(request)
    return render(request, 'pedidos/pedidos.html', context={'pedidos': pedidos_do_usuario})


