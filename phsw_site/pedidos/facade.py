from .models import Pedido, Item, CategoriaItem, ItemPedido, TabelaPreco
from django.db.models import Q, Value, Prefetch
from django.db.models.functions import Concat
from django.contrib import messages

# ----------------------------/ Orders /-----------------------------

def buscar_pedidos(request):
    """
    Se houver um 'termo' no querydict do request vai fazer uma pesquisa pelo termo.
    Se não houver, vai buscar os pedidos do usuário ou os pedidos da empresa do usuario, caso este usuario seja
    'agente administrador'.
    """

    if request.GET.get('termo') is not None and request.GET.get('termo') != '':
        termo = request.GET.get('termo')
        for status in Pedido.status_choices:
            if termo.lower() in status[1].lower():
                return Pedido.objects.filter(status=status[0]).all()
        campos = Concat('fk_usuario__first_name', Value(' '), 'fk_usuario__last_name')  # precisa do value pra simuar o ' '
        if request.user.is_agente_admin:
            return Pedido.objects.annotate(nome_completo=campos).order_by('-data_pedido').filter(
                Q(status=termo) | Q(fk_empresa__nome_empresa__icontains=termo) |
                Q(valor_total__icontains=termo) | Q(fk_usuario__first_name__icontains=termo) | Q(fk_usuario__last_name__icontains=termo)
                | Q(nome_completo__icontains=termo), fk_empresa=request.user.fk_empresa).select_related(
                'fk_empresa', 'fk_usuario')
        return Pedido.objects.annotate(nome_completo=campos).order_by('-data_pedido').filter(
            Q(status__icontains=termo) | Q(fk_empresa__nome_empresa__icontains=termo) |
            Q(valor_total__icontains=termo) | Q(fk_usuario__first_name__icontains=termo) | Q(fk_usuario__last_name__icontains=termo)
            | Q(nome_completo__icontains=termo), fk_usuario=request.user).select_related('fk_empresa')

    if request.user.is_agente_admin:
        return Pedido.objects.order_by('-data_pedido').filter(fk_empresa=request.user.fk_empresa_id).select_related(
            'fk_empresa', 'fk_usuario')
    return Pedido.objects.order_by('-data_pedido').filter(fk_usuario=request.user).select_related(
        'fk_empresa')


def buscar_pedido(request):
    return ItemPedido.objects.filter(fk_pedido_id=request.POST.get('id_pedido')).all()


def fazer_pedido(request):
    pass


# ------------------------------/ Items /--------------------------------------

def buscar_itens_por_categoria():
    itens_ativados = Item.objects.filter(ativado=True)
    return CategoriaItem.objects.prefetch_related(
        Prefetch('item_set', queryset=itens_ativados, to_attr='itens')).all()


def user_category_items_queryset(request):
    # items = request.user.fk_empresa.fk_tabelaPreco.itens_preco.select_related('fk_item')
    # items = request.user.fk_empresa.fk_tabelaPreco.itens.prefetch_related('item_code')
    # items = Item.objects.prefetch_related('item_code').filter(tabelapreco=request.user.fk_empresa.fk_tabelaPreco)
    # itemspreco = request.user.fk_empresa.fk_tabelaPreco.itens_preco.all()
    # items = Item.objects.prefetch_related(Prefetch('item_code', queryset=itemspreco, to_attr='itempreco'))

    tabelaornone = request.user.fk_empresa.fk_tabelaPreco
    if not request.user.fk_empresa or not tabelaornone:
        return None

    items = Item.objects.filter(ativado=True).filter(tabelapreco__pk=tabelaornone.id)
    return CategoriaItem.objects.prefetch_related(
        Prefetch('item_set', queryset=items, to_attr='itens')).all()

    # if not request.user.fk_empresa or not request.user.fk_empresa.fk_tabelaPreco:
    #     return None
    #
    # items = Item.objects.filter(ativado=True).filter(tabelapreco__pk=request.user.fk_empresa.fk_tabelaPreco_id)
    # return CategoriaItem.objects.prefetch_related(
    #     Prefetch('item_set', queryset=items, to_attr='itens')).all()


def buscar_todos_os_itens_por_categoria():
    itens = Item.objects.all()
    return CategoriaItem.objects.prefetch_related(
        Prefetch('item_set', queryset=itens, to_attr='itens')).all()


def editar_itens(request):
    pass