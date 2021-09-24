from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from phsw_site.documents.api.serializers import BoletoSerializer
from phsw_site.documents.utils import make_boleto

post_body = {
    "comando": "boleto",
    "modelo": "1",
    "campos": {
        "banco": "sicoob",
        "codigo_banco": "756-0",
        "linha_digitavel": "75691.33007 01048.049504 00003.470010 4 87390000590618",
        "codigo_barras": "02193819023801283932",
        "CNPJ_beneficiario": "CNPJ:01.493.752/0001-02",
        "beneficiario": "Soluma Solucoes em Inform Corpor Ltda",
        "agencia": "3300",
        "codigo_cedente": "480495",
        "endereco_beneficiario": "AV. SAO PAULO, QD.01 LT.08 AP.02 - VILA BRASILIA - AP. DE GOIANIA-GO - 74905-770",
        "pagador": "ALUCENTRO CENTRAL DE ALUMINIO LTDA",
        "nosso_numero": "0000034-7",
        "documento": "007675",
        "parcela": "1 / 1",
        "vencimento": "10/09/2021",
        "valor_documento": "5.906,18",
        "local_pagamento": "PAGAVEL PREFERENCIALMENTE NO SICOOB",
        "codigo_beneficiario": "123456",
        "especie_documento": "DM",
        "aceite": "N",
        "data_processamento": "10/01/2002",
        "data_documento": "10/10/2002",
        "carteira": "1",
        "quantidade": "",
        "xvalor": "",
        "especie": "0,00",
        "instrucoes_responsabilidade": "asldjflk alsdjflk alsjdflk alsdkfjal dfladjflaj ldsflajdflkj laldjfladjf lorem",
        "desconto_abatimento": "",
        "outras_deducoes": "",
        "mora_multa": "",
        "outros_acrescimos": "",
        "valor_cobrado": "",
        "CNPJ_pagador": "3908240984208402",
        "endereco_pagador": "asjdflkaj alfdjlfdja afdljfadljfda alfjalfdj fljj",
    }
}


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def gen_boleto(request):
    if request.user.all_api_permissions:
        serializer = BoletoSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data["comando"] == 'boleto':
                boleto = make_boleto(serializer.validated_data['modelo'], serializer.validated_data['campos'])
                return boleto
            else:
                return Response({"response": f"O comando passado '{serializer.validated_data['comando']}', não é valido. Passe um valor valido para esse campo."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'response': 'Nao possui permissoes para acessar esse recurso.'},
                    status=status.HTTP_401_UNAUTHORIZED)
