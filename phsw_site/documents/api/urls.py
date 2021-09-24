from django.urls import path
from phsw_site.documents.api.views import gen_boleto

app_name = "boleto"
urlpatterns = [
    path('boleto/', gen_boleto, name="gen_boleto")
]