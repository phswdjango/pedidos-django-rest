from django.urls import path
from phsw_site.pedidos.api.views import (
    # Item
    ItemApi,
    SpecificItemApi,

    # Order
    OrderApi,
    SpecificOrderApi,

    # Category
    CategoryApi, SpecificCategoryApi,

)

app_name = 'pedidos'
urlpatterns = [
    # Order
    path('order/', OrderApi.as_view(), name='api_order'),
    path('order/<code>/', SpecificOrderApi.as_view(), name='api_specific_order'),

    # Item
    path('item/', ItemApi.as_view(), name='api_item'),
    path('item/<code>/', SpecificItemApi.as_view(), name='api_specific_item'),

    # Category
    path('category/', CategoryApi.as_view(), name='api_category'),
    path('category/<code>/', SpecificCategoryApi.as_view(), name='api_specific_category'),

    # Price list

]
