from rest_framework import status, mixins, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from phsw_site.pedidos.api.serializers import ItemSerializer, ItemUpdateSerializer, \
    BulkItemCreateSerializer, CategorySerializer, OrderSerializer
from phsw_site.pedidos.models import Pedido, Item, CategoriaItem
from rest_framework.views import APIView


# --------------------------/ Item / --------------------------------------------

class ItemApi(APIView):
    def get(self, request, format=None):
        if request.user.all_api_permissions:
            try:
                itens = Item.objects.all()
            except Item.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ItemSerializer(itens, many=True)
            return Response(serializer.data)

        return Response({'response': 'Nao possui permissoes para acessar esse recurso.'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, format=None):
        if request.user.all_api_permissions:
            if isinstance(request.data, dict):
                item = Item()
                serializer = ItemSerializer(item, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            if isinstance(request.data, list):
                serializer = BulkItemCreateSerializer(data=request.data, many=True)
                data = {}
                if serializer.is_valid():
                    data['success'] = 'criado com sucesso'
                    serializer.save()
                    return Response(data=data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'response': 'Nao possui permissoes para acessar esse recurso.'},
                        status=status.HTTP_401_UNAUTHORIZED)


class SpecificItemApi(APIView):
    def get(self, request, code):

        if request.user.all_api_permissions:
            try:
                item = Item.objects.get(codigo_item=code)
            except Item.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ItemSerializer(item)
            return Response(serializer.data)

        return Response({'response': 'Nao possui permissoes para acessar esse recurso.'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, code, format=None):
        if request.user.all_api_permissions:
            try:
                item = Item.objects.get(codigo_item=code)
            except Item.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ItemUpdateSerializer(item, data=request.data)
            data = {}
            if serializer.is_valid():
                serializer.save()
                data['success'] = 'update successful'
                return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'response': 'Nao possui permissoes para acessar esse recurso.'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, code, format=None):
        if request.user.all_api_permissions:
            try:
                item = Item.objects.get(codigo_item=code)
            except Item.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            operation = item.delete()
            data = {}
            if operation:
                data['success'] = 'deleted successful'
            else:
                data['failure'] = 'delete failed'
            return Response(data=data)
        return Response({'response': 'Nao possui permissoes para acessar esse recurso.'},
                        status=status.HTTP_401_UNAUTHORIZED)


# --------------------------------/ Orders /---------------------------------/


class OrderApi(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = OrderSerializer

    def get(self, request):
        if request.user.all_api_permissions:
            if request.data.get('filter'):
                try:
                    pedidos = Pedido.objects.filter(status=request.data['filter'])
                except Pedido.DoesNotExist:
                    return Response({"response": "Passe um valor correto para o campo 'filter'"}, status=status.HTTP_404_NOT_FOUND)
                serializer = OrderSerializer(pedidos, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'response': "Parameter 'filter' is missing."},
                        status=status.HTTP_400_BAD_REQUEST)
        return Response({'response': 'Nao possui permissoes para acessar esse recurso.'},
                                status=status.HTTP_401_UNAUTHORIZED)


class SpecificOrderApi(APIView):
    def get(self, request, code):
        if request.user.all_api_permissions:
            try:
                pedido = Pedido.objects.get(id=code)
            except Pedido.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = OrderSerializer(pedido)
            return Response(serializer.data)
        return Response({'response': 'Nao possui permissoes para acessar esse recurso.'},
                        status=status.HTTP_401_UNAUTHORIZED)


# -----------------------------------/ Category / ----------------------

class CategoryApi(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = CategorySerializer
    queryset = CategoriaItem.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SpecificCategoryApi(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = CategorySerializer
    queryset = CategoriaItem.objects.all()
    lookup_url_kwarg = 'code'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# -----------------------------------/ Sales Table / ----------------------

class CategoryApi(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = CategorySerializer
    queryset = CategoriaItem.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SpecificCategoryApi(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = CategorySerializer
    queryset = CategoriaItem.objects.all()
    lookup_url_kwarg = 'code'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
