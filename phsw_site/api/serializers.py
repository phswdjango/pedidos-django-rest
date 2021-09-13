from rest_framework import serializers
from phsw_site.pedidos.models import Pedido


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['__all__']