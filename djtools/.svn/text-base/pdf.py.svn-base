#-*- coding: utf8 -*-

"""
Módulo que torna mais fácil a geração de PDFs com reportlab
"""

from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, TableStyle, \
                               Frame, PageBreak, Image
from reportlab.platypus.tables import LongTable
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas
from StringIO import StringIO
from datetime import datetime
from operator import isNumberType
from djtools.utils import human_str


STYLES = getSampleStyleSheet()


class PagesCountCanvas(canvas.Canvas):
    """
    Imprime "página X de Y" no canto inferior esquerdo de cada página
    Créditos: http://code.activestate.com/recipes/576832/
    """
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 7)
        self.drawRightString(200*mm, 8*mm,
            "Página %d de %d" % (self._pageNumber, page_count))


def para(text, style='BodyText', bulletText=None, caseSensitive=0, **para_args):
    """
    ``text``: texto do parágrafo
    ``style``: estilo do paragrafo
               opções: ['bu', 'df', 'h1', 'h2', 'h3', 'title', 'BodyText', 
                        'Bullet', 'Code', 'Definition', 'Heading1', 'Heading2', 
                        'Heading3', 'Italic', 'Normal', 'Title']
    ``para_args``: dict com atributos e valores para a tag `<para>`
    
    ****************************************************************************
    Class Paragraph:
    
    Paragraph(text, style, bulletText=None, caseSensitive=1) 
    
    text a string of stuff to go into the paragraph. style is a style definition 
    as in reportlab.lib.styles. bulletText is an optional bullet defintion. 
    caseSensitive set this to 0 if you want the markup tags and their attributes 
    to be case-insensitive.
    
    This class is a flowable that can format a block of text into a paragraph with 
    a given style.
    
    The paragraph Text can contain XML-like markup including the tags: 
    <b> ... </b> - bold 
    <i> ... </i> - italics 
    <u> ... </u> - underline
    <strike> ... </strike> - strike through 
    <super> ... </super> - superscript 
    <sub> ... </sub> - subscript 
    <font name=fontfamily/fontname color=colorname size=float> 
    <onDraw name=callable label="a label"/>
    <index [name="callablecanvasattribute"] label="a label"/> 
    <link>link text</link> attributes of links 
        size/fontSize=num
        name/face/fontName=name 
        fg/textColor/color=color 
        backcolor/backColor/bgcolor=color 
        dest/destination/target/href/link=target 
    <a>anchor text</a> attributes of anchors 
        fontSize=num 
        fontName=name 
        fg/textColor/color=color 
        backcolor/backColor/bgcolor=color 
        href=href
    <a name="anchorpoint"/> 
    <unichar name="unicode character name"/> 
    <unichar value="unicode code point"/> 
    <img src="path" width="1in" height="1in" valign="bottom"/>
    The whole may be surrounded by <para> </para> tags
    The <b> and <i> tags will work for the built-in fonts (Helvetica /Times / Courier). 
    For other fonts you need to register a family of 4 fonts using 
    reportlab.pdfbase.pdfmetrics.registerFont; then use the addMapping function to 
    tell the library that these 4 fonts form a family e.g.
        from reportlab.lib.fonts import addMapping 
        addMapping('Vera', 0, 0, 'Vera')	#normal 
        addMapping('Vera', 0, 1, 'Vera-Italic')	#italic 
        addMapping('Vera', 1, 0, 'Vera-Bold')	#bold 
        addMapping('Vera', 1, 1, 'Vera-BoldItalic')	#italic and bold
    It will also be able to handle any MathML specified Greek characters.
    """
    text = human_str(text)
    
    alignments = dict(l='left', r='right', c='center')
    
    if not text.upper().startswith('<PARA'):
        para_args_formatted = []
        for key, value in para_args.items():
            if key.lower() in ['align', 'alignment'] and value in alignments:
                value = alignments[value]
            para_args_formatted.append('%s="%s"' % (key, value))
        text = '<para %s>%s</para>' % (' '.join(para_args_formatted), text)
    
    return Paragraph(text=text, style=STYLES[style], bulletText=bulletText, 
                     caseSensitive=caseSensitive)


def table(rows, w=None, h=None, grid=1, head=0, count=0, zebra=0, 
          auto_align=1, blank=u'-', a=None):
    """
    w: colWidths
    h: rowHeight
    grid: mostrar grades da tabela
    head: indica se a primeira lista de `rows` é o cabeçalho
    count: mostra o contador das linhas
    zebra: a tabela fica zebrada
    auto_align: alinha automaticamente a célula de acordo com seu valor
    blank: valor caso a célula esteja em branco (ou None)
    a: alinhamentos
    """
    number_of_columns = len(rows[0])
    
    # Validating rows
    for row_n, row in enumerate(rows[1:]):
        if len(row) != number_of_columns:
            raise Exception('Rows must have %d columns, got %d on row %d' \
                            % (number_of_columns, len(row), row_n + 2))
    
    # Validating w
    if w:
        if len(w) != number_of_columns:
            raise Exception('Param `w` must have len %d, got %d' \
                            % (number_of_columns, len(w)))
    
    # Validating a
    if a:
        if len(a) != number_of_columns:
            raise Exception('Param `a` must have len %d, got %d' \
                            % (number_of_columns, len(a)))
        
    
    def get_auto_align(value):
        return isNumberType(value) and 'right' or 'left'
    
    fontSize = 8
    formatted_rows = []
    
    for index, row in enumerate(rows): # Body
        # HEAD
        if index == 0 and head:
            if count and w:
                w = [10] + w
            formatted_row = []
            row = count and ([u'#'] + row) or row
            for cell in row:
                text = '<para fontSize="%s" alignment="center"><b>%s</b></para>' % (fontSize, cell)
                formatted_row.append(para(text))
            formatted_rows.append(formatted_row)
            continue
        
        # ROW
        formatted_row = []
        if count:
            order = head and index or index + 1
            text = '<para fontSize="%s" alignment="right">%s</para>' % (fontSize, order)
            formatted_row = [para(text)]
        for row_count, cell in enumerate(row):
            # If cell insn't a reportlab element
            if not cell.__class__.__module__.split('.')[0] == 'reportlab':
                para_args = dict(fontSize=fontSize)
                if not cell: # valor em branco
                    cell = blank
                    para_args['align'] = 'center'
                else:
                    if a:
                        para_args['align'] = a[row_count]
                    elif auto_align:
                        para_args['align'] = get_auto_align(cell)
                cell = para(cell, **para_args)
            formatted_row.append(cell)
        formatted_rows.append(formatted_row)
    
    # Constructor args to table <LongTable>
    constructor_args = {}
    if w:
        constructor_args['colWidths'] = [i*mm for i in w]
    if h:
        constructor_args['rowHeights'] = h*mm
    if head:
        # repeat table header after page breaks
        constructor_args['repeatRows'] = 1
    
    # Creating the table
    table = LongTable(formatted_rows, **constructor_args)
    table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.25, 0.25),
        ('TOPADDING', (0,0), (-1,-1), 0.25, 0.25)
    ]))
    
    if grid:
        table.setStyle(TableStyle([
            ('INNERGRID', (0,0), (-1,-1), 0.1, colors.gray),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ]))
    
    if head:
        table.setStyle(TableStyle([
            ('ROWBACKGROUNDS', (0, 0), (-1, 0), (0xCCCCCC,)),
        ]))
    
    if zebra:
        table.setStyle(TableStyle([
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), (0xEEEEEE, None))
        ]))
    
    return table


def space(height):
    return Spacer(0, height*mm)


def page_break():
    return PageBreak()


def _doNothing(canvas, doc):
    pass


class PdfReport(object):
    
    def __init__(self, body, header_args=None, footer_args=None, paper='A4', 
                 pages_count=1, creation_date=0, filename=None):
        """
        body <list>:
            lista com elementos que compõem o corpo do PDF.
        header_args & footer_args <function|dict>:
            representam elementos que aparecerão em todas as páginas.
            se for <function>:
                a função receber ao menos os parâmetros `canvas` e `doc`, devendo 
                retornar algo como o ``body`` e deve ter o atributo ``height``
            se for <dict>:
                height, story, function, args
        paper <string>:
            uma opção de reportlab.lib.pagesizes (caso tenha um "-" antes da opção,
            será ententido como formato paisagem - o default é retrato): ['A0', 
            'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'B0', 'B1', 'B2', 'B3', 'B4', 
            'B5', 'B6', 'ELEVENSEVENTEEN', 'LEGAL'])
        pages_count <bool>:
            indica se o PDF usará ``PagesCountCanvas`` para mostrar o contador de 
            páginas
        """
        self._set_paper(paper)
        self.body = body
        self.show_pages_count = pages_count
        self.show_creation_date = creation_date
        self.creation_date = datetime.now()
        self.filename = filename
        # header_args
        self.header_args = header_args
        self._set_header_or_footer_args('header')
        # footer_args
        self.footer_args = footer_args
        self._set_header_or_footer_args('footer')
    
    def _set_paper(self, paper):
        paper = paper.upper()
        if paper.startswith('-'):
            landscape = True
            paper = paper[1:]
        else:
            landscape = False
        self.pagesize = getattr(pagesizes, paper)
        if landscape:
            self.pagesize = pagesizes.landscape(self.pagesize)
            
    def _set_header_or_footer_args(self, option):
        assert option in ('header', 'footer')
        args_name = option + '_args'
        args = getattr(self, args_name)
        if args:
            if callable(args): # args é uma função
                try:
                    height = args.height
                except AttributeError:
                    raise AttributeError('Função `%s` deve ter atributo `height`' % args_name)
            elif isinstance(args, dict): # args é um dicionário
                if 'function' in args: # args tem chave `function`
                    if not callable(args['function']):
                        raise ValueError('Chave `function` de %s deve ser uma função' % args_name)
                    if hasattr(args['function'], 'height'):
                        if 'height' in args:
                            raise ValueError('Chave `height` é inválida porque `function` tem atributo `height`')
                        height = args['function'].height
                else: # args não tem chave `function`
                    if 'story' not in args:
                        raise ValueError('%s args_name deve ter chave `story` quando não tem `function`')
                    height = args['height']
        else:
            height = 0
        setattr(self, option + '_height', height*mm)

    def _get_header_or_footer_story(self, option, canvas, doc):
        assert option in ('header', 'footer')
        args = getattr(self, option+'_args')
        if args:
            if callable(args) or 'function' in args:
                func_args = dict(canvas=canvas, doc=doc)
                if callable(args):
                    function = args
                elif 'function' in args:
                    function = args['function']
                    func_args.update(args['args'])
                story = function(**func_args)
                if not isinstance(story, list):
                    raise ValueError('Função deve retornar lista')
                return story
            else:
                return args['story']
        else:
            return []

    def has_header(self):
        return self.header_height > 0*mm

    def has_footer(self):
        return self.footer_height > 0*mm
    
    def set_header(self, canvas, doc):
        if not self.has_header():
            return

        f = Frame( # (x1,y1) <-- lower left corner
            x1                   = doc.leftMargin, 
            y1                   = doc.pagesize[1] - self.header_height - 10*mm,
            width                = doc.width, # doc.width = doc.pagesize[1] - doc.leftMargin - doc.rightMargin 
            height               = self.header_height, 
            leftPadding          = 1, 
            bottomPadding        = 1, 
            rightPadding         = 1, 
            topPadding           = 1, 
            id                   = None, 
            showBoundary         = 1, 
            overlapAttachedSpace = None, 
            _debug               = None
        )
        f.addFromList(self._get_header_or_footer_story('header', canvas, doc)[:], canvas)
    
    def set_footer(self, canvas, doc):
        if not self.has_footer():
            return

        f = Frame( # (x1,y1) <-- lower left corner
            x1                   = doc.leftMargin, 
            y1                   = doc.bottomMargin - self.footer_height, 
            width                = doc.width, # doc.width = doc.pagesize[1] - doc.leftMargin - doc.rightMargin 
            height               = self.footer_height, 
            leftPadding          = 1, 
            bottomPadding        = 1, 
            rightPadding         = 1, 
            topPadding           = 1, 
            id                   = None, 
            showBoundary         = 1, 
            overlapAttachedSpace = None, 
            _debug               = None
        )
        f.addFromList(self._get_header_or_footer_story('footer', canvas, doc)[:], canvas)
    
    def onFirstPage(self, canvas, doc):
        canvas.saveState()
        self.set_header(canvas, doc)
        self.set_footer(canvas, doc)
        if self.show_creation_date:
            self.set_creation_date(canvas, doc)
        canvas.restoreState()

    def onLaterPages(self, canvas, doc):
        canvas.saveState()
        self.set_header(canvas, doc)
        self.set_footer(canvas, doc)
        if self.show_creation_date:
            self.set_creation_date(canvas, doc)
        canvas.restoreState()
    
    def set_creation_date(self, canvas, doc):
        canvas.setFont('Helvetica', 7)
        horario = self.creation_date.strftime('%d/%m/%Y %H:%M:%S')
        canvas.drawString(10*mm, 8*mm, u'PDF gerado em %s' % horario)
    
    def generate(self):
        """
        SimpleDocTemplate extends BaseDocTemplate
        
        BaseDocTemplate(self, filename, pagesize=defaultPageSize,
            pageTemplates=[], showBoundary=0, leftMargin=inch, rightMargin=inch, topMargin=inch, 
            bottomMargin=inch, allowSplitting=1, title=None, author=None, _pageBreakQuick=1, encrypt=None)
        """
        pdf_file = StringIO()
        doc = SimpleDocTemplate(
            pdf_file, 
            pagesize = self.pagesize,
            # Margens que delimitam a área útil (sem header e footer)
            leftMargin   = 10*mm,
            rightMargin  = 10*mm,
            topMargin    = 10*mm + self.header_height,
            bottomMargin = 10*mm + self.footer_height
        )
        story = []
        for item in self.body:    
            story.append(item)
        
        # Preparing to build()
        build_args = dict(
            flowables    = story, 
            onFirstPage  = self.onFirstPage, 
            onLaterPages = self.onLaterPages,
        )
        if self.show_pages_count:
            build_args['canvasmaker'] = PagesCountCanvas
        doc.build(**build_args)
        
        if self.filename:
            f = open(self.filename, 'w')
            f.write(pdf_file.getvalue())
            f.close()
        else:
            return pdf_file.getvalue()

def header_or_footer_example(canvas, doc):
    return [para('Nome: _______________     Data: _______________', alignment='center')]
header_or_footer_example.height = 10

def img_and_title(title_text, img_field_file, img_w=40, useful_w=190):
    """
    img_field_file: atributo ImageField de um objeto de modelo
    useful_w: largura útil do papel (190 para A4 com margens de 10mm)
    """
    img_h = (img_w / float(img_field_file.width)) * img_field_file.height
    image = Image(img_field_file.path, width=img_w*mm, height=img_h*mm)
    return table(rows = [[image, title_text]], 
                 w    = [img_w, useful_w-img_w], 
                 grid = 0)

if __name__ == '__main__':
    # PDF report example
    rows = [['thead1', 'thead2']]
    for i in range(100):
        rows.append(['val1', 'val2'])
    body=[
        para('<para align="center" size="16">Meu Título</para>'), 
        para('<para align="right">Meu nome é <b>Chuck Noris</b></para>'),
        para('<u>Texto underline</ul>'),
        table(rows=rows, head=True, zebra=True),
        para('<br/>foo bar ')
    ]
    
    doc = PdfReport(body=body, header_args=header_or_footer_example, footer_args=header_or_footer_example, 
        filename='/tmp/relatorio.pdf', show_pages_count=True, show_creation_date=True)
    import os
    os.system('open /tmp/relatorio.pdf')
