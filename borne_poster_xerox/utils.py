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
            response = urlopen(portrait['picture_1280'])
            with Image(file=response) as picture:
                margin_top_bottom = 413
                margin_left_picture = 100
                picture_size = A3_PIXELS_WIDTH - 2 * margin_left_picture
                picture.resize(picture_size, picture_size)
                poster.composite(picture, left=margin_left_picture, top=margin_top_bottom)
                with Drawing() as draw:
                    draw.font = 'MaisonMonoL'
                    margin_text = 319
                    # draw caption
                    draw.font_size = 104
                    draw.fill_color = Color('white')

                    caption_x = margin_text
                    caption_y = margin_top_bottom + picture_size - margin_text + margin_left_picture
                    caption_line_height = 167
                    offset = 0

                    def draw_with_shadow(x, y, text):
                        draw.fill_color = Color('black')
                        for i in range(-2, 3):
                            for j in range(-2, 3):
                                if not i == 0 and j == 0:
                                    draw.text(x + i, y + i, text)
                        draw.fill_color = Color('white')
                        draw.text(x, y, text)

                    draw_with_shadow(caption_x, caption_y, portrait['taken_str'])

                    place = portrait['place']
                    if place:
                        offset += caption_line_height
                        draw_with_shadow(caption_x, caption_y - offset, place['name'])

                    event = portrait['event']
                    if event:
                        offset += caption_line_height
                        draw_with_shadow(caption_x, caption_y - offset, event['name'])

                    draw.fill_color = Color('black')
                    draw.font_size = 50
                    line_spacing = 83
                    draw.text(margin_text, A3_PIXELS_HEIGHT - margin_top_bottom, WEBSITE)
                    ticket_number = TICKET_NUMBER % portrait['code']
                    draw.text(margin_text, A3_PIXELS_HEIGHT - margin_top_bottom - line_spacing, ticket_number)


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



