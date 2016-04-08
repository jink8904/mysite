__author__ = 'Julio'

from reportlab.graphics.charts.textlabels import Label
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import io


class PdfPrint:
    # initialize class
    def __init__(self, buffer, pageSize):
        self.buffer = buffer
        # default format is A4
        if pageSize == 'A4':
            self.pageSize = A4
        elif pageSize == 'Letter':
            self.pageSize = letter
        self.width, self.height = self.pageSize

    def pageNumber(self, canvas, doc):
        number = canvas.getPageNumber()
        canvas.drawCentredString(100 * mm, 15 * mm, str(number))

    def title_draw(self, x, y, text):
        chart_title = Label()
        chart_title.x = x
        chart_title.y = y
        chart_title.fontName = 'FreeSansBold'
        chart_title.fontSize = 16
        chart_title.textAnchor = 'middle'
        chart_title.setText(text)
        return chart_title

    def generar_pdf(self, options):
        heading = options.get("headings")
        data = options.get("data")
        title = options.get("title")
        ruc = options.get("ruc")
        empresa = options.get("empresa")
        table_style = options.get("table_style")
        top_title = ruc + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + empresa
        buff = io.BytesIO()
        doc = SimpleDocTemplate(
            buff,
            pagesize=self.pageSize,
            rightMargin=40,
            leftMargin=40,
            topMargin=60,
            bottomMargin=18,
        )
        template = []
        styles = getSampleStyleSheet()

        styles.add(ParagraphStyle(
            name="titulo", alignment=TA_CENTER, fontName='Times-Roman', spaceAfter=15,
        spaceBefore=6, fontSize=12))

        top_title = Paragraph(top_title, styles['Normal'])
        header = Paragraph(title, styles['titulo'])

        template.append(top_title)
        template.append(header)

        t = Table(heading + data)
        t.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.75, colors.black),
                ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke)
            ]
        ))
        if(table_style):
            t.setStyle(TableStyle(table_style))
        template.append(t)
        doc.build(template)
        pdf = buff.getvalue()
        buff.close()
        return pdf
