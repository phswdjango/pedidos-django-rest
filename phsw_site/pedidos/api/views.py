from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from phsw_site.pedidos.api.serializers import PedidoSerializer, ItemSerializer, ItemSerializerUpdate
from phsw_site.pedidos.models import Pedido, Item

# ------------------/ Item


@api_view(['GET', ])
def api_get_all_itens(request):
    try:
        itens = Item.objects.all()
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ItemSerializer(itens)
        return Response(serializer.data)


@api_view(['GET', ])
def api_get_item(request, slug):
    try:
        item = Item.objects.get(id_item=slug)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return Response(serializer.data)


@api_view(['PUT', ])
def api_update_item(request, slug):
    try:
        item = Item.objects.get(id_item=slug)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = ItemSerializerUpdate(item, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = 'update successful'
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
def api_delete_item(request, slug):
    try:
        item = Item.objects.get(id_item=slug)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        operation = item.delete()
        data = {}
    if operation:
        data['success'] = 'deleted successful'
    else:
        data['failure'] = 'delete failed'
    return Response(data=data)


@api_view(['POST', ])
def api_create_item(request):
    item = Item()
    if request.method == 'POST':
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------/ Pedidos


@api_view(['GET', ])
def api_all_pedidos(request):
    try:
        pedidos = Pedido.objects.all()
    except Pedido.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PedidoSerializer(pedidos)
        return Response(serializer.data)


@api_view(['GET', ])
def api_pedido(request, slug):
    try:
        pedidos = Pedido.objects.get(id=slug)
    except Pedido.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PedidoSerializer(pedidos)
        return Response(serializer.data)
