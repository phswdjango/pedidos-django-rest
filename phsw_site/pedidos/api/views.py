from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from phsw_site.pedidos.api.serializers import PedidoSerializer, ItemSerializer, ItemUpdateSerializer, \
    BulkItemCreateSerializer, BulkItemUpdateSerializer
from phsw_site.pedidos.models import Pedido, Item, CategoriaItem
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

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
        item = Item.objects.get(codigo_item=slug)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ItemSerializer(item)
    return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes([IsAuthenticated])
def api_update_item(request, slug):
    if request.user.all_api_permissions:
        try:
            item = Item.objects.get(codigo_item=slug)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ItemUpdateSerializer(item, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = 'update successful'
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'response': 'Nao possui permissoes para acessar esse recurso.'}, status=status.HTTP_401_UNAUTHORIZED)


# ----------------------------------/ BULK /----------------------------------

def validate_ids(data, field="id", unique=True):

    if isinstance(data, list):
        id_list = [int(x[field]) for x in data]

        if unique and len(id_list) != len(set(id_list)):
            raise ValidationError("Multiple updates to a single {} found".format(field))

        return id_list

    return [data]

class Api_Bulk_Item_Update(generics.ListCreateAPIView):

    serializer_class = BulkItemUpdateSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(Api_Bulk_Item_Update, self).get_serializer(
            *args, **kwargs
        )

    def get_queryset(self, ids=None):
        if ids:
            return Item.objects.filter(
                id__in=ids,
                # project__pk=self.kwargs["project_id"], id__in=ids,
            )
        # return Item.objects.filter(project__id=self.kwargs["project_id"],)
        return Item.objects.filter(id=self.kwargs["id"])

    def post(self, request, *args, **kwargs):

        fk_categoria = CategoriaItem.objects.get(id=kwargs["fk_categoria_id"])
        # editado ^
        if isinstance(request.data, list):
            for item in request.data:
                item["fk_categoria"] = fk_categoria
        else:
            raise ValidationError("Invalid Input")

        return super(Api_Bulk_Item_Update, self).post(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):

        fk_categoria = CategoriaItem.objects.get(id=kwargs["fk_categoria_id"])

        ids = validate_ids(request.data)

        if isinstance(request.data, list):
            for item in request.data:
                item["fk_categoria"] = fk_categoria
        else:
            raise ValidationError("Invalid Input")

        instances = self.get_queryset(ids=ids)

        serializer = self.get_serializer(
            instances, data=request.data, partial=False, many=True
        )

        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        data = serializer.data
        return Response(data)

    def perform_update(self, serializer):
        serializer.save()

# --------------------------------------------

@api_view(['DELETE', ])
@permission_classes([IsAuthenticated])
def api_delete_item(request, slug):
    if request.user.all_api_permissions:
        try:
            item = Item.objects.get(codigo_item=slug)
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


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def api_bulk_item_create(request):
    if request.user.all_api_permissions:
        serializer = BulkItemCreateSerializer(data=request.data, many=True)
        data = {}
        if serializer.is_valid():
            data['success'] = 'criado com sucesso'
            serializer.save()
            return Response(data=data)
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
