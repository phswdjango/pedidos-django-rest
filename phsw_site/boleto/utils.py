from io import BytesIO
from wsgiref.util import FileWrapper
import pdfkit
from django.http import HttpResponse
import os
from barcode import ITF
from barcode.writer import SVGWriter
from jinja2 import FileSystemLoader, Environment
from rest_framework import status
from rest_framework.response import Response

options = {
    'enable-local-file-access': None,
}

modelos = {
    '1': 'modelo-boleto.html',
}


def create_barcode(code):
    with open("barcode.svg", "wb") as f:
        ITF(code, writer=SVGWriter()).write(f)


def gerar_boleto(modelo, campos):

    if campos['banco'] == 'sicoob':
        campos['banco'] = 'file://' + os.path.join(
            os.path.dirname(__file__)) + '/templates/logo-banco/sicoob.png'
    else:
        return Response({"response": f"O banco '{campos['banco']}' nao existe."}, status=status.HTTP_400_BAD_REQUEST)
    if campos['codigo_barras']:
        codigo_barra_svg = ITF(campos['codigo_barras'], writer=SVGWriter())
        codigo_barra = codigo_barra_svg.render(writer_options=None, text='')
        codigo_barra = str(codigo_barra)
        codigo_barra = codigo_barra.replace("b'", "").replace(r"\n", "").removesuffix("'")
        campos['barcode_svg'] = f'{codigo_barra}'
    else:
        return Response({"response": "Nenhum codigo de barras foi informado."}, status=status.HTTP_400_BAD_REQUEST)
    if modelo == '1':
        myloader = FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates/'))
        env = Environment(loader=myloader)
        template = env.get_template(modelos['1'])
        bolelo_html = template.render(campos)
        boleto_gerado = BytesIO(pdfkit.from_string(bolelo_html, output_path=False, options=options))
        return HttpResponse(FileWrapper(boleto_gerado), content_type="application/pdf")
    else:
        return Response({"response": f"O modelo '{modelo}' não existe."}, status=status.HTTP_400_BAD_REQUEST)
