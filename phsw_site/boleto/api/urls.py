from django.urls import path
from phsw_site.boleto.api.views import gen_boleto

app_name = "boleto"
urlpatterns = [
    path('gerar/', gen_boleto, name="gen_boleto")
]