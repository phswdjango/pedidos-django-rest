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

templates = {
    '1': 'boleto.html',
}


def make_boleto(template, fields):

    if fields['banco'] == 'sicoob':
        fields['banco'] = 'file://' + os.path.join(
            os.path.dirname(__file__)) + '/templates/bank-logo/sicoob.png'
    else:
        return Response({"response": f"The bank '{fields['banco']}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    if fields['codigo_barras']:
        barcode_svg = ITF(fields['codigo_barras'], writer=SVGWriter())
        # barcode = barcode_svg.render(writer_options=None, text='')
        barcode = barcode_svg.render(writer_options={'module_width': 0.25, 'module_height': 17}, text='')
        barcode = str(barcode)
        barcode = barcode.replace("b'", "").replace(r"\n", "").removesuffix("'")
        fields['barcode_svg'] = f'{barcode}'
    else:
        return Response({"response": "No barcode was informed."}, status=status.HTTP_400_BAD_REQUEST)
    if template == '1':
        myloader = FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates/'))
        env = Environment(loader=myloader)
        template = env.get_template(templates['1'])
        bolelo_html = template.render(fields)
        generated_boleto = BytesIO(pdfkit.from_string(bolelo_html, output_path=False, options=options))
        return HttpResponse(FileWrapper(generated_boleto), content_type="application/pdf")
    else:
        return Response({"response": f"The template '{template}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)
