from django.contrib import admin
from phsw_site.pedidos.models import Item, TabelaPreco, ItemPreco, Pedido, ItemPedido, CategoriaItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo_item', 'fk_categoria', 'verbose_name', 'descricao', 'unidade', 'codigo_barras', 'ativado')
    # list_filter = ('CategoriaItem.verbose_name', 'status')
    list_filter = ('fk_categoria', 'ativado')
    # prepopulated_fields = {'slug': ('title',)}
    search_fields = ('verbose_name', 'ativado')
    ordering = ('fk_categoria', 'verbose_name')
    list_editable = ('ativado', 'verbose_name')  # editavel ao acessar a pagina ItemAdmin
    list_display_links = ('id', 'codigo_item')  # link para acessar o registro.


@admin.register(ItemPreco)
class ItemPrecoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fk_tabelaPreco', 'fk_item', 'preco_unit', 'data')


class ItemPrecoInline(admin.TabularInline):
    model = ItemPreco


@admin.register(TabelaPreco)
class TabelaPrecoAdmin(admin.ModelAdmin):
    list_display = ('id', 'verbose_name', 'codigo_tabela')
    ordering = ('verbose_name',)
    inlines = [
        ItemPrecoInline
    ]


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fk_empresa', 'fk_usuario', 'status', 'data_pedido', 'data_faturamento', 'valor_total')
    list_filter = ('fk_empresa', 'fk_usuario', 'data_pedido', 'status')
    ordering = ('data_pedido',)
    inlines = [
        ItemPedidoInline
    ]


@admin.register(CategoriaItem)
class CategoriaItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo_categoria', 'descricao', 'verbose_name')
