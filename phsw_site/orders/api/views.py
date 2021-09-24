from rest_framework import status, mixins, generics
from rest_framework.response import Response
from phsw_site.orders.api.serializers import ItemSerializer, ItemUpdateSerializer, \
    BulkItemCreateSerializer, CategorySerializer, OrderSerializer, PriceTableSerializerPost, \
    PriceTableSerializerGet, ItemPriceSerializerGet, ItemPriceSerializerPost
from phsw_site.orders.models import Order, Item, ItemCategory, PriceTable, PriceItem
from rest_framework.views import APIView


# --------------------------/ Item / --------------------------------------------

class ItemApi(APIView):
    def get(self, request):
        if request.user.all_api_permissions:
            try:
                itens = Item.objects.all()
            except Item.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ItemSerializer(itens, many=True)
            return Response(serializer.data)

        return Response({'response': 'Nao possui permissoes para acessar esse recurso.'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
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
                item = Item.objects.get(item_code=code)
            except Item.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ItemSerializer(item)
            return Response(serializer.data)

        return Response({'response': 'Nao possui permissoes para acessar esse recurso.'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, code):
        if request.user.all_api_permissions:
            try:
                item = Item.objects.get(item_code=code)
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

    def delete(self, request, code):
        if request.user.all_api_permissions:
            try:
                item = Item.objects.get(item_code=code)
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
            if request.data.get('status'):
                try:
                    orders = Order.objects.filter(status=request.data['status'])
                except Order.DoesNotExist:
                    return Response({"response": "Error"}, status=status.HTTP_404_NOT_FOUND)
                serializer = OrderSerializer(orders, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'response': "Parameter 'status' is missing."},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'response': 'Nao possui permissoes para acessar esse recurso.'},
                        status=status.HTTP_401_UNAUTHORIZED)


class SpecificOrderApi(APIView):
    def get(self, request, code):
        if request.user.all_api_permissions:
            try:
                order = Order.objects.get(id=code)
            except Order.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        return Response({'response': 'Nao possui permissoes para acessar esse recurso.'},
                        status=status.HTTP_401_UNAUTHORIZED)


# -----------------------------------/ Category / ----------------------

class CategoryApi(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = CategorySerializer
    queryset = ItemCategory.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SpecificCategoryApi(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                          generics.GenericAPIView):
    serializer_class = CategorySerializer
    queryset = ItemCategory.objects.all()
    lookup_url_kwarg = 'code'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# -----------------------------------/ Price Table / ----------------------

class PriceTableApi(APIView):
    # create
    def get(self, request):
        if request.data.get('code'):
            tables = PriceTable.objects.filter(table_code=request.data['code'])
            serializer = PriceTableSerializerGet(tables, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"response": "The 'code' field was not informed."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = PriceTableSerializerPost(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------/ ItemPrice /-----------------------------


class ItemPriceApi(APIView):
    def get(self, request):
        if request.user.all_api_permissions:
            item_code = request.data.get('item_code')
            table_code = request.data.get('table_code')
            if not item_code or not table_code:
                return Response({"response": "Por favor envie os valores de 'item_code' e 'table_code'."},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                priceitem = PriceItem.objects.get(pricetable__table_code=table_code, item__item_code=item_code)

            except PriceItem.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if not priceitem:
                return Response({"response": "Item preco nao encontrado."},
                                status=status.HTTP_404_NOT_FOUND)
            serializer = ItemPriceSerializerGet(priceitem)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'response': 'Nao possui permissoes para acessar esse recurso.'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        item_code = request.data.get('item_code')
        table_code = request.data.get('table_code')
        if not item_code or not table_code:
            return Response({"response": "Por favor envie os valores de 'item_code' e 'table_code'."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            pricetable = PriceTable.objects.get(table_code=table_code)
        except PriceTable.DoesNotExist:
            return Response({"response":"A tabela informada nao existe."}, status=status.HTTP_404_NOT_FOUND)
        try:
            item = Item.objects.get(item_code=item_code)
        except Item.DoesNotExist:
            return Response({"response": "O item informado nao existe."}, status=status.HTTP_404_NOT_FOUND)
        copy_data = request.data.copy()
        copy_data['item'] = item.pk
        copy_data['pricetable'] = pricetable.pk

        serializer = ItemPriceSerializerPost(data=copy_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        item_code = request.data.get('item_code')
        table_code = request.data.get('table_code')
        if not item_code or not table_code:
            return Response({"response": "Por favor envie os valores de 'item_code' e 'table_code'."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            pricetable = PriceTable.objects.get(table_code=table_code)
        except PriceTable.DoesNotExist:
            return Response({"response":"A tabela informada nao existe."}, status=status.HTTP_404_NOT_FOUND)
        try:
            item = Item.objects.get(item_code=item_code)
        except Item.DoesNotExist:
            return Response({"response": "O item informado nao existe."}, status=status.HTTP_404_NOT_FOUND)
        copy_data = request.data.copy()
        copy_data['item'] = item.pk
        copy_data['pricetable'] = pricetable.pk
        try:
            instance = PriceItem.objects.get(item=copy_data['item'], pricetable=copy_data['pricetable'])
        except PriceItem.DoesNotExist:
            return Response({"response": "O PriceItem imformado nao existe."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ItemPriceSerializerPost(instance, data=copy_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if request.user.all_api_permissions:
            item_code = request.data.get('item_code')
            table_code = request.data.get('table_code')
            if not item_code or not table_code:
                return Response({"response": "Por favor envie os valores de 'item_code' e 'table_code'."},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                priceitem = PriceItem.objects.get(pricetable__table_code=table_code, item__item_code=item_code)

            except PriceItem.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if not priceitem:
                return Response({"response": "Item preco nao encontrado."},
                                status=status.HTTP_404_NOT_FOUND)
            operation = priceitem.delete()
            data = {}
            if operation:
                data['success'] = 'deleted successful'
            else:
                data['failure'] = 'delete failed'
            return Response(data, status=status.HTTP_200_OK)

        return Response({'response': 'Nao possui permissoes para acessar esse recurso.'},
                        status=status.HTTP_401_UNAUTHORIZED)
