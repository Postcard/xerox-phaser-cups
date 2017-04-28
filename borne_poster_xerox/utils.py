# -*- coding: utf8 -*-
from urllib2 import urlopen
import io
import tempfile

from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from PyPDF2 import PdfFileMerger, PdfFileReader
import cups

from .constants import A3_PIXELS_HEIGHT, A3_PIXELS_WIDTH, XEROX_7100N, VERSO_POSTER_PDF_PATH, WEBSITE, TICKET_NUMBER


def create_poster(portrait):
    with Color('white') as bg:
        with Image(width=A3_PIXELS_WIDTH, height=A3_PIXELS_HEIGHT, background=bg) as poster:
            poster.units = 'pixelsperinch'
            poster.resolution = 300
            response = urlopen(portrait['picture_with_caption_1280'])
            with Image(file=response) as picture:
                margin_top = 413
                margin_left = 100
                picture_size = A3_PIXELS_WIDTH - 2 * margin_left
                picture.resize(picture_size, picture_size)
                poster.composite(picture, left=margin_left, top=margin_top)
                with Drawing() as draw:
                    draw.font = 'XSWNEBMaisonMonoL'
                    draw.font_size = 50
                    margin_text = 413
                    line_spacing = 83
                    draw.text(margin_text, A3_PIXELS_HEIGHT - margin_text, WEBSITE)
                    ticket_number = TICKET_NUMBER % portrait['code']
                    draw.text(margin_text, A3_PIXELS_HEIGHT - margin_text - line_spacing, ticket_number)
                    draw(poster)
                    response.close()
                    poster_buffer = io.BytesIO()
                    poster.format = 'pdf'
                    poster.save(file=poster_buffer)
                    merger = PdfFileMerger()
                    merger.append(poster_buffer)
                    with open(VERSO_POSTER_PDF_PATH, 'rb') as verso:
                        merger.append(PdfFileReader(verso))
                        temp_file = tempfile.NamedTemporaryFile(delete=False)
                        merger.write(temp_file.name)
                        temp_file.close()
                        return temp_file.name


class PrinterNotFoundException(Exception):
    pass


def print_to_xerox_7100N(filename):

    conn = cups.Connection()
    printers = conn.getPrinters()
    printer = printers.get(XEROX_7100N)
    if not printer:
        raise PrinterNotFoundException()

    options = {
        'media': 'A3',
        'sides': 'two-sided-long-edge',
        'XROutputColor': 'PrintAsGrayscale',
        'XRPrintQuality': 'Photo'
    }
    conn.printFile(XEROX_7100N, filename, 'poster', options)



