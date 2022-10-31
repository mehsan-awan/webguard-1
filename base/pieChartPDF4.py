import os

from reportlab.lib.colors import blue, red, HexColor, green, white
from reportlab.lib.utils import ImageReader

from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import Paragraph, Spacer, Image, PageBreak
from reportlab.platypus.doctemplate import BaseDocTemplate, PageTemplate, NextPageTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.platypus.frames import Frame
from datetime import datetime

from . import views


class MyDocTemplate(BaseDocTemplate):

    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)
        self.pagesize = defaultPageSize

    def afterFlowable(self, flowable):
        "Registers TOC entries."
        if flowable.__class__.__name__ == 'Paragraph':

            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Heading1' or style == 'h1_reportguide':
                level = 0
            elif style == 'Heading2' or style == "H_Centered":
                level = 1
            elif style == 'Heading3':
                level = 2
            else:
                return
            E = [level, text, self.page]
            # if we have a bookmark name, append that to our notify data
            bn = getattr(flowable, '_bookmarkName', None)
            if bn is not None: E.append(bn)
            self.notify('TOCEntry', tuple(E))


class pdfReport:
    def __init__(self, url, request):
        self.elements = []
        self.date = datetime.now().date()
        self.time = datetime.now().time().strftime("%H:%M:%S")
        print(self.date)
        print(self.time)
        self.url = url
        self.PAGE_HEIGHT = defaultPageSize[1]
        self.PAGE_WIDTH = defaultPageSize[0]
        mydir = os.getcwd() + "/base/"
        self.logo = mydir + "NCSAEL.jpg"
        PS = ParagraphStyle

        self.h1 = PS(
            name='Heading1',
            fontSize=18,
            font="Times-Bold",
            leading=35,
            textColor=HexColor("#6A7EBD")
        )
        self.h1_reportguide = PS(
            name='h1_reportguide',
            fontSize=16,
            font="Times-Bold",
            leading=35,
            alignment=TA_CENTER,
            textColor=HexColor("#000")
        )

        self.h2 = PS(name='Heading2',
                     fontSize=14,
                     leading=22,
                     textColor=HexColor("#6A7EBD")
                     )

        self.h3 = PS(name='Heading3',
                     fontSize=12,
                     leading=22,
                     textColor=HexColor("#6A7EBD")
                     )

        self.H_Centered = PS(name='H_Centered',
                             fontSize=14,
                             leading=22,
                             alignment=TA_CENTER,
                             )

        self.bodyGreen = PS(name='bodyGreen',
                            fontSize=12,
                            leading=16,
                            alignment=TA_LEFT,
                            textColor=green,
                            )

        self.bodyBlue = PS(name='bodyBlue',
                           fontSize=12,
                           leading=16,
                           leftIndent=20,
                           alignment=TA_JUSTIFY,
                           textColor=blue
                           )

        self.bodyRed = PS(name='bodyRed',
                          fontSize=12,
                          leading=16,
                          alignment=TA_LEFT,
                          textColor=red
                          )
        self.bodyWhite = PS(name='bodyWhite',
                            fontSize=12,
                            leading=16,
                            leftIndent=20,
                            alignment=TA_JUSTIFY,
                            textColor=white
                            )

        self.body_Centered = PS(name='body_Centered',
                                fontSize=12,
                                leading=16,
                                alignment=TA_CENTER,
                                )

        self.bodyStyle = PS(name='bodyStyle',
                            fontSize=12,
                            leading=16,
                            alignment=TA_JUSTIFY
                            )
        self.body_heading = PS(name='body_heading',
                               font="Times-Bold",
                               fontSize=12,
                               leading=22,
                               textColor=HexColor("#6A7EBD")
                               )

        self.myPagebreak = PageBreak()

        self.graph_pos = 0

        path = views.GetCodeDirectory(request) + "Reports/"
        self.pdf_filename = path + self.url + "$" + str(self.date) + "$" + str(self.time) + '$Report.pdf'
        self.doc = MyDocTemplate(self.pdf_filename)
        # os.system(path + "Report.pdf")

    def make_drawing(self, total_tested, total_detected):
        from reportlab.lib import colors
        from reportlab.graphics.shapes import Drawing
        from reportlab.graphics.charts.barcharts import HorizontalBarChart
        drawing = Drawing(300, 100)

        data = [
            (total_tested, total_detected)
        ]

        names = ["Total Tested Entities", "Compromised Entities"]

        bc = HorizontalBarChart()
        bc.x = 90
        bc.y = 50
        bc.height = 30
        bc.width = 350
        bc.data = data
        bc.strokeColor = colors.white
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = total_tested + 10

        bc.valueAxis.valueStep = total_tested / 10
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = -10
        bc.categoryAxis.labels.fontName = 'Helvetica'
        bc.categoryAxis.categoryNames = names
        bc.bars[(0, 0)].fillColor = colors.blue

        drawing.add(bc)
        return drawing

    def titlePage(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Bold', 20)
        canvas.drawCentredString(self.PAGE_WIDTH / 2, self.PAGE_HEIGHT / 2 + 4 * 12, "A Web Guard Report on")
        # canvas.setFont('Times-Bold', 20)
        canvas.drawCentredString(self.PAGE_WIDTH / 2, self.PAGE_HEIGHT / 2 + 2 * 12, self.url)
        canvas.setFont('Times-Roman', 16)
        canvas.drawCentredString(self.PAGE_WIDTH / 2, self.PAGE_HEIGHT / 2 - 0 * 12, str(self.date))
        canvas.drawCentredString(self.PAGE_WIDTH / 2, self.PAGE_HEIGHT / 2 - 2 * 12, str(self.time))

        canvas.restoreState()

    def contentPage(self, canvas, doc):
        canvas.saveState()
        canvas.setTitle("Report")
        # Header
        canvas.line(66, 780, LETTER[0] - 66, 780)
        canvas.setFont('Times-Roman', 14)
        text_width = stringWidth("A Web Guard Report on", 'Times-Roman', 14)
        x = (self.PAGE_WIDTH - text_width) / 2.0
        canvas.drawString(x, 810, "A Web Guard Report on")
        text_width = stringWidth(self.url, 'Times-Roman', 14)
        x = (self.PAGE_WIDTH - text_width) / 2.0
        canvas.drawString(x, 790, self.url)
        logo = ImageReader(self.logo)
        canvas.drawImage(logo, 70, 785, 50, 50, mask='auto')

        # Footer
        canvas.line(66, 78, LETTER[0] - 66, 78)
        canvas.setFont('Times-Roman', 12)
        page = "NATIONAL CYBER SECURITY AUDITING AND EVALUATION LAB (NCSAEL)"
        email = "csael-nust@mcs.edu.pk                                                                         "
        phone = "+92-51-8731584-5"
        canvas.drawString(90, 65, page)
        canvas.drawString(240, 50, email)
        canvas.drawString(250, 35, phone)
        canvas.drawString(500, 30, "Page %d" % doc.page)

        # canvas.drawString(inch, 0.75 * inch, "Page %d | Dated: %s" % (doc.page, self.date))
        canvas.restoreState()

    def reportguide(self, canvas, doc):
        canvas.saveState()
        # Header
        canvas.line(66, 780, LETTER[0] - 66, 780)
        canvas.setFont('Times-Roman', 14)
        text_width = stringWidth("A Web Guard Report on", 'Times-Roman', 14)
        x = (self.PAGE_WIDTH - text_width) / 2.0
        canvas.drawString(x, 810, "A Web Guard Report on")
        text_width = stringWidth(self.url, 'Times-Roman', 14)
        x = (self.PAGE_WIDTH - text_width) / 2.0
        canvas.drawString(x, 790, self.url)
        logo = ImageReader(self.logo)
        canvas.drawImage(logo, 70, 785, 50, 50, mask='auto')
        # body
        canvas.setFont('Times-Bold', 16)
        # canvas.drawString(240, 750, "Report Guidelines")
        # canvas.line(240, 748, 365, 748)
        canvas.drawString(80, 710, "Color Key:")
        canvas.line(80, 708, 155, 708)

        canvas.setFillColorRGB(1, 0, 0)
        canvas.drawString(110, 680, "Red:")
        canvas.setFont('Times-Roman', 16)
        canvas.drawString(170, 680, "Current Copy Data")

        canvas.setFillColorRGB(0, 102, 0)
        canvas.setFont('Times-Bold', 16)
        canvas.drawString(110, 655, "Green:")
        canvas.setFont('Times-Roman', 16)
        canvas.drawString(170, 655, "Trusted Copy Data")

        canvas.setFillColorRGB(0, 0, 1)
        canvas.setFont('Times-Bold', 16)
        canvas.drawString(110, 630, "Blue:")
        canvas.setFont('Times-Roman', 16)
        canvas.drawString(170, 630, "Changes in DOM")

        canvas.setFillColorRGB(0, 0, 0)
        canvas.setFont('Times-Bold', 16)
        canvas.drawString(80, 590, "Line no Details:")
        canvas.line(80, 588, 185, 588)

        canvas.drawString(110, 560, "0a1:")
        canvas.setFont('Times-Roman', 16)
        canvas.drawString(170, 560, "It indicates that line no 1 is added.")

        canvas.setFont('Times-Bold', 16)
        canvas.drawString(110, 535, "1c1:")
        canvas.setFont('Times-Roman', 16)
        canvas.drawString(170, 535, "It indicates the change in text at line no 1.")

        canvas.setFont('Times-Bold', 16)
        canvas.drawString(110, 510, "1c5:")
        canvas.setFont('Times-Roman', 16)
        canvas.drawString(170, 510, "It indicates that text in line 1 is changed and moved to line 5.")

        canvas.setFont('Times-Bold', 16)
        canvas.drawString(110, 485, "5d4:")
        canvas.setFont('Times-Roman', 16)
        canvas.drawString(170, 485, "It indicates that line no 5 is deleted.")

        canvas.setFont('Times-Bold', 16)
        canvas.drawString(110, 460, "1,5d1:")
        canvas.setFont('Times-Roman', 16)
        canvas.drawString(170, 460, "It indicates that line no 1 to 5 are deleted.")

        canvas.setFont('Times-Bold', 16)
        canvas.drawString(110, 435, "1d1,5:")
        canvas.setFont('Times-Roman', 16)
        canvas.drawString(170, 435, "It indicates that line no 1 to 5 are added.")

        canvas.setFont('Times-Bold', 16)
        canvas.drawString(80, 395, "Images Details:")
        canvas.line(80, 393, 180, 393)

        canvas.drawString(110, 365, "New Images:")
        canvas.setFont('Times-Roman', 16)
        canvas.drawString(260, 365, "New images are added to the page.")

        canvas.setFont('Times-Bold', 16)
        canvas.drawString(110, 340, "Deleted Images:")
        canvas.setFont('Times-Roman', 16)
        canvas.drawString(260, 340, "Some images are deleted.")

        canvas.setFont('Times-Bold', 16)
        canvas.drawString(110, 315, "Tempered Images:")
        canvas.setFont('Times-Roman', 16)
        canvas.drawString(260, 315, "Image xyz.png is tempered.")

        # Footer
        canvas.line(66, 78, LETTER[0] - 66, 78)
        canvas.setFont('Times-Roman', 12)
        page = "NATIONAL CYBER SECURITY AUDITING AND EVALUATION LAB (NCSAEL)"
        email = "csael-nust@mcs.edu.pk                                                                         "
        phone = "+92-51-8731584-5"
        canvas.drawString(90, 65, page)
        canvas.drawString(240, 50, email)
        canvas.drawString(250, 35, phone)
        canvas.drawString(500, 30, "Page %d" % (doc.page))

        canvas.restoreState()

    def doHeading(self, text, sty):
        from hashlib import sha1
        # create bookmarkname
        a = (text + sty.name).encode('utf-8')
        bn = sha1(a).hexdigest()
        # modify paragraph text to include an anchor point with name bn
        h = Paragraph(text + '<a name="%s"/>' % bn, sty)
        # store the bookmark name on the flowable so afterFlowable can see this
        h._bookmarkName = bn
        return h
        # self.elements.append(h)

    def generate_pdf(self):
        # doc = SimpleDocTemplate('Report.pdf')
        # doc = MyDocTemplate('Report.pdf')
        frameT = Frame(self.doc.leftMargin, self.doc.bottomMargin, self.doc.width, self.doc.height, id='normal')

        self.doc.addPageTemplates([PageTemplate(id='TitlePage', frames=frameT, onPage=self.titlePage),
                                   PageTemplate(id='ContentPage', frames=frameT, onPage=self.contentPage),
                                   PageTemplate(id='reportguide', frames=frameT, onPage=self.reportguide)
                                   ])
        toc = TableOfContents()

        PS = ParagraphStyle

        # ***Title Page***#

        im1 = Image(self.logo, 112.5, 112.5)
        im1.hAlign = 'CENTER'
        self.elements.append(im1)

        self.elements.append(NextPageTemplate('ContentPage'))
        self.elements.append(PageBreak())

        self.elements.append(Paragraph('<b>Table of Contents</b>', self.body_Centered))
        toc.levelStyles = [
            PS(fontName='Times-Bold', fontSize=14, name='TOCHeading1',
               leftIndent=20, firstLineIndent=-20, spaceBefore=5, leading=16),
            PS(fontSize=12, name='TOCHeading2',
               leftIndent=40, firstLineIndent=-20, spaceBefore=0, leading=12),
            PS(fontSize=10, name='TOCHeading3',
               leftIndent=60, firstLineIndent=-20, spaceBefore=0, leading=12),
            PS(fontSize=10, name='TOCHeading4',
               leftIndent=100, firstLineIndent=-20, spaceBefore=0, leading=12),
        ]
        self.elements.append(toc)
        self.elements.append(PageBreak())

        # self.elements.append(NextPageTemplate('reportguide'))
        # self.elements.append(PageBreak())
        # self.elements.append(self.doHeading("<u><b>Report Guidelines</b></u>", self.h1_reportguide))

        self.elements.append(NextPageTemplate('ContentPage'))
        self.elements.append(PageBreak())

        self.elements.append(self.doHeading('Executive Summary', self.h1))
        self.elements.append(self.doHeading('Introduction', self.h2))
        self.elements.append(Paragraph('WebGuard is a Website Defacement Agent designed to detect any type of Web '
                                       'Defacement attempts and to minimize the response time of CERT team. WebGuard '
                                       'is capable of screening multiple websites 24/7 for continuous monitoring. If '
                                       'any irregularities are detected, the owner of the website is notified.',
                                       self.bodyStyle))
        self.elements.append(Spacer(1, 12))
        self.elements.append(self.doHeading('Findings', self.h2))
        self.elements.append(Paragraph('WebGuard found that following entities are changed.', self.bodyStyle))
        self.graph_pos = len(self.elements)
        self.elements.append(PageBreak())

