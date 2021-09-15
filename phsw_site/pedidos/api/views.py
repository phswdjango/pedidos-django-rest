from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from phsw_site.pedidos.api.serializers import PedidoSerializer, ItemSerializer, ItemSerializerUpdate
from phsw_site.pedidos.models import Pedido, Item
from rest_framework.permissions import IsAuthenticated

# ------------------/ Item


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def api_get_all_itens(request):
    try:
        itens = Item.objects.all()
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ItemSerializer(itens, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def api_get_item(request, slug):
    try:
        item = Item.objects.get(id_item=slug)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ItemSerializer(item)
    return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes([IsAuthenticated])
def api_update_item(request, slug):
    if request.user.all_api_permissions:
        try:
            item = Item.objects.get(id_item=slug)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ItemSerializerUpdate(item, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = 'update successful'
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'response': 'Nao possui permissoes para acessar esse recurso.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE', ])
@permission_classes([IsAuthenticated])
def api_delete_item(request, slug):
    if request.user.all_api_permissions:
        try:
            item = Item.objects.get(id_item=slug)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        operation = item.delete()
        data = {}
        if operation:
            data['success'] = 'deleted successful'
        else:
            data['failure'] = 'delete failed'
        return Response(data=data)
    return Response({'response': 'Nao possui permissoes para acessar esse recurso.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def api_create_item(request):
    if request.user.all_api_permissions:
        item = Item()
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'response': 'Nao possui permissoes para acessar esse recurso.'}, status=status.HTTP_401_UNAUTHORIZED)

# -------------/ Pedidos


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def api_all_pedidos(request):
    try:
        pedidos = Pedido.objects.all()
    except Pedido.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PedidoSerializer(pedidos, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def api_pedido(request, slug):
    try:
        pedidos = Pedido.objects.get(id=slug)
    except Pedido.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PedidoSerializer(pedidos)
    return Response(serializer.data)
