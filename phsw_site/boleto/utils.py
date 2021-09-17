from io import BytesIO
from wsgiref.util import FileWrapper

from django.http import HttpResponse
from jinja2 import FileSystemLoader, Environment
import os
import pdfkit as pdf
from barcode import ITF
from barcode.writer import SVGWriter
from rest_framework import status
from rest_framework.response import Response

options = {
    'enable-local-file-access': None,
}

modelos = {
    '1': 'modelo-boleto.html',
}

myloader = FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates/'))
env = Environment(loader=myloader)


def create_barcode(code):
    with open("barcode.svg", "wb") as f:
        ITF(code, writer=SVGWriter()).write(f)


# def convercao_pdf(html, output_path):
#     pdf.from_string(html, output_path=output_path, options=options)

def gerar_boleto(modelo, campos):
    outputpath = '/home/phsw/Documents/boleto2.pdf'

    if campos['banco'] == 'sicoob':
        campos['banco'] = 'file://' + os.path.join(
            os.path.dirname(__file__)) + '/templates/logo-banco/sicoob.png'
    else:
        # raise Exception(f"O banco informado {campos['banco']} não existe.")
        return Response({"response": f"O banco '{campos['banco']}' nao existe."}, status=status.HTTP_400_BAD_REQUEST)
    if campos['codigo_barras']:
        codigo_barra_svg = ITF(campos['codigo_barras'], writer=SVGWriter())
        codigo_barra = codigo_barra_svg.render(writer_options=None, text='')
        codigo_barra = str(codigo_barra)
        codigo_barra = codigo_barra.replace("b'", "").replace(r"\n", "").removesuffix("'")
        campos['barcode_svg'] = f'{codigo_barra}'
    else:
        # raise Exception(f'Nenhum codigo de barras foi informado.')
        return Response({"response": "Nenhum codigo de barras foi informado."}, status=status.HTTP_400_BAD_REQUEST)
    if modelo == '1':
        template = env.get_template(modelos['1'])
        bolelo_html = template.render(**campos)
        # convercao_pdf(bolelo_html, outputpath)
        # return Response({"response": f"Boleto criado com sucesso."}, status=status.HTTP_200_OK)
        boleto_gerado = BytesIO(pdf.from_string(bolelo_html, output_path=False, options=options))
        return HttpResponse(FileWrapper(boleto_gerado), content_type="application/pdf")
    else:
        # raise Exception(f'O modelo "{modelo}" não existe. Passe um valor valido para esse campo.')
        return Response({"response": f"O modelo '{modelo}' não existe."}, status=status.HTTP_400_BAD_REQUEST)
