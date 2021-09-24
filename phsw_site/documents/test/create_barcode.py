from barcode import ITF
from barcode.writer import SVGWriter


def create_barcode(code):
    with open("barcode.svg", "wb") as f:
        ITF(code, writer=SVGWriter()).write(f)