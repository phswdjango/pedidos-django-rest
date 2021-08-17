from . models import Pedido
# from django.shortcuts import get_object_or_404
from django.db.models import Q, Value
from django.db.models.functions import Concat

def buscar_pedidos(request):
    """
    Se houver um 'termo' no querydict do request vai fazer uma pesquisa pelo termo (try na linha 11).
    Se não houver, vai buscar os pedidos do usuário ou os pedidos da empresa do usuario, caso este usuario seja
    'agente administrador'.
    """
    if request.GET.get('termo') is not None and request.GET.get('termo') != '':
        termo = request.GET.get('termo')
        campos = Concat('fk_usuario__first_name', Value(' '), 'fk_usuario__last_name')  # precisa do value pra simuar o ' '
        print("termo recebido: ", termo)
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

    # if request.GET.get('termo'):
    #     termo = request.GET.get('termo')
    #     print("termo recebido: ", termo)
    #     if request.user.is_agente_admin:
    #         return Pedido.objects.order_by('-data_pedido').filter(fk_empresa=request.user.fk_empresa, fk_status__verbose_name=termo).select_related(
    #             'fk_empresa', 'fk_status', 'fk_usuario')
    #     return Pedido.objects.order_by('-data_pedido').filter(fk_usuario=request.user).select_related(
    #         'fk_empresa', 'fk_status')




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