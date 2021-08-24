from .models import Pedido, Item, CategoriaItem, ItemPedido
from django.db.models import Q, Value, Prefetch
from django.db.models.functions import Concat
from django.contrib import messages


def buscar_pedidos(request):
    """
    Se houver um 'termo' no querydict do request vai fazer uma pesquisa pelo termo.
    Se não houver, vai buscar os pedidos do usuário ou os pedidos da empresa do usuario, caso este usuario seja
    'agente administrador'.
    """

    if request.GET.get('termo') is not None and request.GET.get('termo') != '':
        termo = request.GET.get('termo')
        campos = Concat('fk_usuario__first_name', Value(' '), 'fk_usuario__last_name')  # precisa do value pra simuar o ' '
        if request.user.is_agente_admin:
            return Pedido.objects.annotate(nome_completo=campos).order_by('-data_pedido').filter(
                Q(fk_status__verbose_name__icontains=termo) | Q(fk_empresa__nome_empresa__icontains=termo) |
                Q(valor_total__icontains=termo) | Q(fk_usuario__first_name__icontains=termo) | Q(fk_usuario__last_name__icontains=termo)
                | Q(nome_completo__icontains=termo), fk_empresa=request.user.fk_empresa).select_related(
                'fk_empresa', 'fk_status', 'fk_usuario')
        return Pedido.objects.annotate(nome_completo=campos).order_by('-data_pedido').filter(
            Q(fk_status__verbose_name__icontains=termo) | Q(fk_empresa__nome_empresa__icontains=termo) |
            Q(valor_total__icontains=termo) | Q(fk_usuario__first_name__icontains=termo) | Q(fk_usuario__last_name__icontains=termo)
            | Q(nome_completo__icontains=termo), fk_usuario=request.user).select_related(
            'fk_empresa', 'fk_status')

    if request.user.is_agente_admin:
        return Pedido.objects.order_by('-data_pedido').filter(fk_empresa=request.user.fk_empresa_id).select_related(
            'fk_empresa', 'fk_status', 'fk_usuario')
    return Pedido.objects.order_by('-data_pedido').filter(fk_usuario=request.user).select_related(
        'fk_empresa', 'fk_status')


def buscar_itens_por_categoria():
    itens_ativados = Item.objects.filter(ativado=True)
    return CategoriaItem.objects.prefetch_related(
        Prefetch('item_set', queryset=itens_ativados, to_attr='itens')).all()


def buscar_todos_os_itens_por_categoria():
    itens = Item.objects.all()
    return CategoriaItem.objects.prefetch_related(
        Prefetch('item_set', queryset=itens, to_attr='itens')).all()


def buscar_pedido(request):
    return ItemPedido.objects.filter(fk_pedido_id=request.POST.get('id_pedido')).all()


def fazer_pedido(request):
    pass


def editar_itens(request):
    pass