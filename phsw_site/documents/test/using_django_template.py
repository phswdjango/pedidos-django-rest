# from django.template.loaders.filesystem import Loader
from django.template.loader import get_template
import os
import pdfkit as pdf


my_loader = Loader()


options = {
    'enable-local-file-access': None,

}

modelos = {
    '1': 'modelo-boleto.html'
}


def convercao_pdf(html, output_path):
    pdf.from_string(html, output_path=output_path, options=options)


myloader = FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates/'))
env = Environment(loader=myloader)


def gerar_boleto(modelo, outputpath, campos):
    if campos['banco'] == 'sicoob':
        campos['banco'] = 'file://' + os.path.join(
            os.path.dirname(__file__)) + '/templates/logo-banco/sicoob.png'
    else:
        raise Exception(f"O banco informado {campos['banco']} não existe.")

    if campos['codigo_barras']:
        campos['codigo_barras'] = 'file://' + os.path.join(
            os.path.dirname(__file__)) + '/templates/componentes/codigo-barras.png'

    if modelo == '1':
        template = env.get_template(modelos['1'])
        bolelo_html = template.render(**campos)
        convercao_pdf(bolelo_html, outputpath)
    else:
        raise Exception(f'O modelo "{modelo}" não existe. Passe um valor valido para esse campo.')
