from django.urls import path
from phsw_site.pedidos.api.views import (
    api_all_pedidos, api_pedido,
    api_get_all_itens, api_get_item, api_update_item, api_delete_item, api_create_item, api_bulk_item_create,
    Api_Bulk_Item_Update
)

app_name = 'pedidos'
urlpatterns = [
    # Orders
    path('all-orders/', api_all_pedidos, name='api_all_orders'),
    path('order/<slug>/', api_pedido, name='api_order'),
    # Items
    path('item/all-items/', api_get_all_itens, name='api_all_items'),
    path('item/details/<slug>/', api_get_item, name='api_item'),
    path('item/update/<slug>/', api_update_item, name='update_item'),
    path('item/delete/<slug>/', api_delete_item, name='delete_item'),
    path('item/create/', api_create_item, name='create_item'),
    path('item/bulk-item-create/', api_bulk_item_create, name='bulk_item_create'),
    path('item/bulk-item-update/<fk_categoria_id>/', Api_Bulk_Item_Update.as_view(), name='bulk_item_update'),
]