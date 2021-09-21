from rest_framework import serializers
from phsw_site.pedidos.models import Pedido, Item, CategoriaItem, TabelaPreco, ItemPreco


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


# ------------------------------/ sales table / --------------------------------

class ItemPrecoSerializerGet(serializers.ModelSerializer):
    fk_item = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ItemPreco
        fields = ['fk_item', 'preco_unit', 'data']


class PriceTableSerializerGet(serializers.ModelSerializer):
    itens_preco = ItemPrecoSerializerGet(many=True)

    class Meta:
        model = TabelaPreco
        fields = ['codigo_tabela', 'verbose_name', 'itens_preco']


class ItemPrecoSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = ItemPreco
        fields = ['fk_item', 'preco_unit', 'data']


class PriceTableSerializerPost(serializers.ModelSerializer):
    itens_preco = ItemPrecoSerializerPost(many=True)

    class Meta:
        model = TabelaPreco
        fields = ['codigo_tabela', 'verbose_name', 'itens_preco']

    # create sales table with itemprice
    def create(self, validated_data):
        print(validated_data)
        items_preco = validated_data.pop('itens_preco')
        salestable = TabelaPreco.objects.create(**validated_data)
        for itempreco in items_preco:
            ItemPreco.objects.create(fk_tabelaPreco=salestable, **itempreco)
        return salestable

    def update(self, instance, validated_data):
        # items_preco = validated_data.pop('itens_preco')
        instance.codigo_tabela = validated_data.get('codigo_tabela', instance.codigo_tabela)
        instance.verbose_name = validated_data.get('verbose_name', instance.verbose_name)
        instance.itens_preco = validated_data.get('itens_preco', instance.itens_preco)
        if self.is_valid():
            instance.save()
        return instance

# ---------------------------------/ ItemPrice /-------------------------------


class ItemPriceSerializerGet(serializers.ModelSerializer):
    fk_item = serializers.StringRelatedField(read_only=True)
    fk_tabelaPreco = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ItemPreco
        fields = ['fk_item', 'fk_tabelaPreco', 'preco_unit', 'data']


class ItemPriceSerializerPost(serializers.ModelSerializer):

    class Meta:
        model = ItemPreco
        fields = ['fk_item', 'fk_tabelaPreco', 'preco_unit' ]

