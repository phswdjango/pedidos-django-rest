from . models import Pedido
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch


def buscar_pedidos_do_usuario(request):
    return Pedido.objects.order_by('-data_pedido').filter(fk_usuario=request.user).select_related(
        'fk_empresa', 'fk_status')


def buscar_pedidos_do_agente_admin(request):
    return Pedido.objects.order_by('-data_pedido').filter(fk_empresa=request.user.fk_empresa).select_related(
        'fk_empresa', 'fk_status', 'fk_usuario')






    # usuario = User.objects.
    # empresa =
    # status =
    # pedidos = Pedido.objects.order_by('data_pedido').prefetch_related(
    #     Prefetch(), Prefetch(), Prefetch()
    # ).all()
    # def trazer_modulos_com_aulas():  # prefetch_related serve pra evitar o N+1 em busca do lado 'N' pro lado '1'
    #     aulas_ordenadas = Aula.objects.order_by('order')
    #     return Modulo.objects.order_by('order').prefetch_related(
    #         Prefetch('aula_set', queryset=aulas_ordenadas, to_attr='aulas')).all()