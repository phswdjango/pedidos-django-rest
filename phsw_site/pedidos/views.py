from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from phsw_site.pedidos.models import Pedido
from django.db.models import Prefetch

@login_required
def pedidos(request):
    usuario = User.objects.all()
    empresa = 
    status = 
    pedidos = Pedido.objects.order_by('data_pedido').prefetch_related(
        Prefetch(), Prefetch(), Prefetch()
    ).all()
    return render(request, 'pedidos/pedidos.html', context={'pedidos': pedidos})


# def trazer_modulos_com_aulas():  # prefetch_related serve pra evitar o N+1 em busca do lado 'N' pro lado '1'
#     aulas_ordenadas = Aula.objects.order_by('order')
#     return Modulo.objects.order_by('order').prefetch_related(
#         Prefetch('aula_set', queryset=aulas_ordenadas, to_attr='aulas')).all()