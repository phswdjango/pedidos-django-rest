from datetime import time, timezone

from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
class ItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['fk_categoria', 'verbose_name', 'descricao', 'unidade', 'codigo_barras', 'ativado', 'imagem']

# ---------------------/ Bulk Update Serializer /----------------------------


class ModelObjectidField(serializers.Field):
    """
        We use this when we are doing bulk create/update. Since multiple instances share
        many of the same fk objects we validate and query the objects first, then modify the request data
        with the fk objects. This allows us to pass the objects in to be validated.
    """

    def to_representation(self, value):
        # return value.id
        return value.id

    def to_internal_value(self, data):
        return data


class BulkCreateUpdateListSerializer(serializers.ListSerializer):
    def create(self, validated_data):

        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise ValidationError(e)

        # update_project_last_modified(result)

        return result

    def to_representation(self, instances):

        start = time.time()
        fk_categoria = instances[0].fk_categoria.pk
        rep_list = []
        for instance in instances:
            rep_list.append(
                dict(
                    id_item=instance.pk,
                    fk_categoria=fk_categoria,
                    verbose_name=instance.verbose_name,
                    descricao=instance.descricao,
                    unidade=instance.unidade,
                    codigo_barras=instance.codigo_barras,
                    ativado=instance.ativado,
                )
            )

        print("to_rep", time.time() - start)

        return rep_list

    def update(self, instances, validated_data):
        start = time.time()

        instance_hash = {index: instance for index, instance in enumerate(instances)}
        print("instance hash", time.time() - start)
        start = time.time()
        result = [
            self.child.update(instance_hash[index], attrs)
            for index, attrs in enumerate(validated_data)
        ]
        # print("update instance", time.time() - start)
        # start = time.time()

        print(self.child.Meta.read_only_fields)
        writable_fields = [
            x
            for x in self.child.Meta.fields
            if x not in self.child.Meta.read_only_fields + ("fk_categoria",)
        ]
        # bulk update doesn't modify auto_now fields in django
        # if "last_modified" in self.child.Meta.fields:
        #     writable_fields += ["last_modified"]
        #     last_modified = timezone.now()
        #     for instance in result:
        #         instance.last_modified = last_modified
        # print("lst modified", time.time() - start)
        # start = time.time()

        try:
            self.child.Meta.model.objects.bulk_update(result, writable_fields)
        except IntegrityError as e:
            raise ValidationError(e)

        # print("bulk update", time.time() - start)
        # start = time.time()

        # update_project_last_modified(result)
        # print("project lm", time.time() - start)
        # start = time.time()

        return result


class BulkItemUpdateSerializer(serializers.ModelSerializer):
    fk_categoria = ModelObjectidField()

    def create(self, validated_data):
        instance = Item(**validated_data)

        if isinstance(self._kwargs["data"], dict):
            instance.save()

        return instance

    def update(self, instance, validated_data):
        instance.fk_categoria = validated_data["fk_categoria"]
        instance.verbose_name = validated_data["verbose_name"]
        instance.descricao = validated_data["descricao"]
        instance.unidade = validated_data["unidade"]
        instance.codigo_barras = validated_data["codigo_barras"]
        instance.ativado = validated_data["ativado"]

        if isinstance(self._kwargs["data"], dict):
            instance.save()

        return instance

    class Meta:
        model = Item
        fields = ('id_item', 'fk_categoria', 'verbose_name', 'descricao', 'unidade', 'codigo_barras', 'ativado')
        list_serializer_class = BulkCreateUpdateListSerializer

# ---------------------------------------------------------------------

class BulkItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id_item', 'fk_categoria', 'verbose_name', 'descricao', 'unidade', 'codigo_barras', 'ativado', 'imagem']

    def create(self, validated_data):
        instance = Item(**validated_data)
        instance.save()
        return instance