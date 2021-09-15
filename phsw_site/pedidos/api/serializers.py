from rest_framework import serializers
from phsw_site.pedidos.models import Pedido, Item


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['fk_empresa', 'fk_usuario', 'fk_status', 'data_pedido', 'data_faturamento', 'valor_total']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['imagem', 'id_item', 'fk_categoria', 'verbose_name', 'descricao', 'unidade', 'codigo_barras', 'ativado']


# cannot update itens if Serializer have the primary key field
class ItemSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['imagem', 'fk_categoria', 'verbose_name', 'descricao', 'unidade', 'codigo_barras', 'ativado']
