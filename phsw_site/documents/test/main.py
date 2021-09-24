from boleto import gerar_boleto

if __name__ == '__main__':

    parametros = {
        'comando': 'boleto',
        'modelo': '1',
        'outputpath': '/home/phsw/Documents/boleto2.pdf',
        'campos': {
            'banco': 'sicoob',
            'codigo_banco': '756-0',
            'linha_digitavel': '75691.33007 01048.049504 00003.470010 4 87390000590618',
            'codigo_barras': '02193819023801283932',
            'CNPJ_beneficiario': 'CNPJ:01.493.752/0001-02',
            'beneficiario': 'Soluma Solucoes em Inform Corpor Ltda',
            'agencia': '3300',
            'codigo_cedente': '480495',
            'endereco_beneficiario': 'AV. SAO PAULO, QD.01 LT.08 AP.02 - VILA BRASILIA - AP. DE GOIANIA-GO - 74905-770',
            'pagador': 'ALUCENTRO CENTRAL DE ALUMINIO LTDA',
            'nosso_numero': '0000034-7',
            'documento': '007675',
            'parcela': '1 / 1',
            'vencimento': '10/09/2021',
            'valor_documento': '5.906,18',
            'local_pagamento': 'PAGAVEL PREFERENCIALMENTE NO SICOOB',
            'codigo_beneficiario': '123456',
            'especie_documento': 'DM',
            'aceite': 'N',
            'data_processamento': '10/01/2002',
            'carteira': '1',
            'quantidade': '',
            'xvalor': '',
            'especie': '0,00',
            'instrucoes_responsabilidade': 'asldjflk alsdjflk alsjdflk alsdkfjal dfladjflaj ldsflajdflkj laldjfladjf lorem',
            'desconto_abatimento': '',
            'outras_deducoes': '',
            'mora_multa': '',
            'outros_acrescimos': '',
            'valor_cobrado': '',
            'CNPJ_pagador': '3908240984208402',
            'endereco_pagador': 'asjdflkaj alfdjlfdja afdljfadljfda alfjalfdj fljj',
        }
    }

    if parametros['comando'] == 'boleto':
        gerar_boleto(parametros['modelo'], parametros['outputpath'], parametros['campos'])
    else:
        raise Exception(f"O comando passado {parametros['comando']}, não é valido. Passe um valor valido para esse campo.")
