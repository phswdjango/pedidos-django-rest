from jinja2 import FileSystemLoader, Environment
import os
import pdfkit as pdf
from barcode import ITF
from barcode.writer import SVGWriter
from create_barcode import create_barcode

options = {
    'enable-local-file-access': None,

}

modelos = {
    '1': 'modelo-boleto.html'
}

myloader = FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates/'))
env = Environment(loader=myloader)


def convercao_pdf(html, output_path):
    pdf.from_string(html, output_path=output_path, options=options)


def gerar_boleto(modelo, outputpath, campos):
    if campos['banco'] == 'sicoob':
        campos['banco'] = 'file://' + os.path.join(
            os.path.dirname(__file__)) + '/templates/logo-banco/sicoob.png'
    else:
        raise Exception(f"O banco informado {campos['banco']} não existe.")

    if campos['codigo_barras']:
        codigo_barra_svg = ITF(campos['codigo_barras'], writer=SVGWriter())
        codigo_barra = codigo_barra_svg.render(writer_options=None, text='')
        codigo_barra = str(codigo_barra)
        codigo_barra = codigo_barra.replace("b'", "").replace(r"\n", "").removesuffix("'")
        campos['barcode_svg'] = f'{codigo_barra}'
    else:
        raise Exception(f'Nenhum codigo de barras foi informado.')

    if modelo == '1':
        template = env.get_template(modelos['1'])
        bolelo_html = template.render(**campos)
        convercao_pdf(bolelo_html, outputpath)
    else:
        raise Exception(f'O modelo "{modelo}" não existe. Passe um valor valido para esse campo.')
