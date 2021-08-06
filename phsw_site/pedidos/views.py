from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from phsw_site.pedidos.models import Pedido



@login_required
def pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedidos/pedidos.html', context={'pedidos': pedidos})
