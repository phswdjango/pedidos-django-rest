from django.contrib import admin
from phsw_site.orders.models import Item, PriceTable, Order, PriceItem, ItemCategory, OrderedItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_code', 'category', 'verbose_name', 'description', 'unit', 'bar_code', 'active')
    # list_filter = ('ItemCategory.verbose_name', 'status')
    list_filter = ('category', 'active')
    # prepopulated_fields = {'slug': ('title',)}
    search_fields = ('verbose_name', 'active')
    ordering = ('category', 'verbose_name')
    list_editable = ('active', 'verbose_name')
    list_display_links = ('id', 'item_code')


@admin.register(PriceItem)
class PriceItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'pricetable', 'item', 'price_unit', 'date')


class PriceItemInline(admin.TabularInline):
    model = PriceItem


@admin.register(PriceTable)
class PriceTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'verbose_name', 'table_code')
    ordering = ('verbose_name',)
    inlines = [
        PriceItemInline
    ]


class OrderedItemInline(admin.TabularInline):
    model = OrderedItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'user', 'status', 'order_date', 'billing_date', 'order_amount')
    list_filter = ('company', 'user', 'order_date', 'status')
    ordering = ('order_date',)
    inlines = [
        OrderedItemInline
    ]


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_code', 'description', 'verbose_name')
