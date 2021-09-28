from rest_framework import serializers


class FieldsBoletoSerializer(serializers.Serializer):
    banco = serializers.CharField(max_length=6)
    codigo_banco = serializers.CharField(max_length=6, required=False)
    linha_digitavel = serializers.CharField(max_length=61)
    codigo_barras = serializers.CharField(max_length=43)
    CNPJ_beneficiario = serializers.CharField(max_length=18, required=False)
    beneficiario = serializers.CharField(max_length=62, required=False)
    agencia = serializers.CharField(max_length=10, required=False)
    codigo_cedente = serializers.CharField(max_length=13, required=False, )
    endereco_beneficiario = serializers.CharField(max_length=85, required=False)
    pagador = serializers.CharField(max_length=75, required=False)
    nosso_numero = serializers.CharField(max_length=17, required=False)
    documento = serializers.CharField(max_length=20, required=False)
    parcela = serializers.CharField(max_length=26, required=False)
    vencimento = serializers.CharField(max_length=10, required=False)
    valor_documento = serializers.CharField(max_length=19, required=False)
    local_pagamento = serializers.CharField(max_length=89, required=False)
    codigo_beneficiario = serializers.CharField(max_length=17, required=False)
    especie_documento = serializers.CharField(max_length=12, required=False)
    aceite = serializers.CharField(max_length=7, required=False)
    data_processamento = serializers.CharField(max_length=16, required=False)
    data_documento = serializers.CharField(max_length=16, required=False)
    carteira = serializers.CharField(max_length=18, required=False)
    quantidade = serializers.CharField(allow_blank=True, max_length=14, required=False)
    xvalor = serializers.CharField(allow_blank=True, max_length=16, required=False)
    especie = serializers.CharField(allow_blank=True, max_length=9, required=False)
    instrucoes_responsabilidade_1 = serializers.CharField(max_length=84, required=False)
    instrucoes_responsabilidade_2 = serializers.CharField(max_length=84, required=False)
    instrucoes_responsabilidade_3 = serializers.CharField(max_length=84, required=False)
    instrucoes_responsabilidade_4 = serializers.CharField(max_length=84, required=False)
    instrucoes_responsabilidade_5 = serializers.CharField(max_length=84, required=False)
    instrucoes_responsabilidade_6 = serializers.CharField(max_length=84, required=False)
    instrucoes_responsabilidade_7 = serializers.CharField(max_length=84, required=False)
    instrucoes_responsabilidade_8 = serializers.CharField(max_length=84, required=False)
    desconto_abatimento = serializers.CharField(allow_blank=True, max_length=23, required=False)
    outras_deducoes = serializers.CharField(allow_blank=True, max_length=23, required=False)
    mora_multa = serializers.CharField(allow_blank=True, max_length=19, required=False)
    outros_acrescimos = serializers.CharField(allow_blank=True, max_length=19, required=False)
    valor_cobrado = serializers.CharField(allow_blank=True, max_length=22, required=False)
    CNPJ_pagador = serializers.CharField(max_length=16, required=False)
    endereco_pagador = serializers.CharField(max_length=115, required=False)

    def validate_codigo_barras(self, value):
        for n in value:
            if not n in '0123456789':
                raise serializers.ValidationError(f"The field 'codigo_barra' must have only integers, but '{n}' was recived.")
        return value


class BoletoSerializer(serializers.Serializer):
    comando = serializers.CharField(max_length=15)
    modelo = serializers.CharField(max_length=15)
    campos = FieldsBoletoSerializer()
