from rest_framework import serializers
from phsw_site.orders.models import Order, Item, ItemCategory, PriceTable, PriceItem


# -------------------------/ item / --------------------------------


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['imagem', 'item_code', 'category', 'verbose_name', 'description', 'unit', 'bar_code', 'active']


# cannot update itens if Serializer have the primary key field
class ItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['category', 'verbose_name', 'description', 'unit', 'bar_code', 'active', 'imagem']


class BulkItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['item_code', 'category', 'verbose_name', 'description', 'unit', 'bar_code', 'active']

    def create(self, validated_data):
        instance = Item(**validated_data)
        instance.save()
        return instance

# --------------------------------------/ order / ----------------------------


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['company', 'user', 'status', 'order_date', 'billing_date', 'order_amount']


# --------------------------------/ Category / ------------------------------------


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = ['id', 'category_code', 'verbose_name', 'description']


# ------------------------------/ sales table / --------------------------------

class PriceItemSerializerGet(serializers.ModelSerializer):
    item = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = PriceItem
        fields = ['item', 'price_unit', 'date']


class PriceTableSerializerGet(serializers.ModelSerializer):
    items = PriceItemSerializerGet(many=True)

    class Meta:
        model = PriceTable
        fields = ['table_code', 'verbose_name', 'items']


class PriceItemSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = PriceItem
        fields = ['item', 'price_unit', 'date']


class PriceTableSerializerPost(serializers.ModelSerializer):
    items = PriceItemSerializerPost(many=True)

    class Meta:
        model = PriceTable
        fields = ['table_code', 'verbose_name', 'items']

    # create sales table with itemprice
    def create(self, validated_data):
        print(validated_data)
        price_items = validated_data.pop('items')
        salestable = PriceTable.objects.create(**validated_data)
        for priceitem in price_items:
            PriceItem.objects.create(pricetable=salestable, **priceitem)
        return salestable

    def update(self, instance, validated_data):
        # items_preco = validated_data.pop('items')
        instance.table_code = validated_data.get('table_code', instance.table_code)
        instance.verbose_name = validated_data.get('verbose_name', instance.verbose_name)
        instance.items = validated_data.get('items', instance.items)
        if self.is_valid():
            instance.save()
        return instance

# ---------------------------------/ ItemPrice /-------------------------------


class ItemPriceSerializerGet(serializers.ModelSerializer):
    item = serializers.StringRelatedField(read_only=True)
    pricetable = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = PriceItem
        fields = ['item', 'pricetable', 'price_unit', 'date']


class ItemPriceSerializerPost(serializers.ModelSerializer):

    class Meta:
        model = PriceItem
        fields = ['item', 'pricetable', 'price_unit']

