import io
from PyPDF2 import PdfFileMerger, PdfFileReader


def merge_pdf(pdf1, pdf2, output):
    merger = PdfFileMerger()
    merger.append(PdfFileReader(io.BytesIO(pdf1)))
    merger.append(io.BytesIO(pdf2))
    merger.write(output)