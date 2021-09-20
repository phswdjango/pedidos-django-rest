from rest_framework import serializers
from phsw_site.pedidos.models import Pedido, Item, CategoriaItem, TabelaPreco


# -------------------------/ item / --------------------------------


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['imagem', 'codigo_item', 'fk_categoria', 'verbose_name', 'descricao', 'unidade', 'codigo_barras', 'ativado']


# cannot update itens if Serializer have the primary key field
class ItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['fk_categoria', 'verbose_name', 'descricao', 'unidade', 'codigo_barras', 'ativado', 'imagem']


class BulkItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['codigo_item', 'fk_categoria', 'verbose_name', 'descricao', 'unidade', 'codigo_barras', 'ativado', 'imagem']

    def create(self, validated_data):
        instance = Item(**validated_data)
        instance.save()
        return instance

# --------------------------------------/ order / ----------------------------


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pedido
        fields = ['fk_empresa', 'fk_usuario', 'status', 'data_pedido', 'data_faturamento', 'valor_total']
        # read_only_fields = ['fk_empresa', 'fk_usuario', 'status', 'data_pedido', 'data_faturamento', 'valor_total']


# --------------------------------/ Category / ------------------------------------


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaItem
        fields = ['id', 'codigo_categoria', 'verbose_name', 'descricao']


#------------------------------/ sales table / --------------------------------


class SalesTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabelaPreco
        fields = "__all__"