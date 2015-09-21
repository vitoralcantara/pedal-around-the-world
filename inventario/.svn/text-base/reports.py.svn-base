# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

from geraldo import Report, ReportBand, Label, ObjectValue, SystemField,\
                    BAND_WIDTH, landscape

class RelatorioInventarioGeralPDF(Report):
    title = 'Relatório Geral dos Inventários'
    author = 'CBTU - Companhia Brasileira de Trens Urbanos'
    
    print_if_empty = True
    page_size = landscape(A4)

    class band_page_header(ReportBand):
        height = 1.75*cm
        elements = [
            SystemField(expression='%(report_title)s', top=0, left=0, width=BAND_WIDTH,
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
            Label(text="Nº PATRIM", top=1.2*cm, left=0*cm, width=3*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
            Label(text="DESCRIÇÃO DETALHADA", top=1.2*cm, left=3.1*cm, width=11.6*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
            Label(text="LOCALIZAÇÃO", top=1.2*cm, left=14.8*cm, width=4*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
            Label(text="MARCA", top=1.2*cm, left=18.9*cm, width=3*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
            Label(text="MODELO", top=1.2*cm, left=22*cm, width=3*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
            Label(text="Nº DE SÉRIE", top=1.2*cm, left=25.1*cm, width=2.6*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
        ]

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            SystemField(expression='%(report_author)s', top=0.1*cm, left=0, width=30*cm),
            SystemField(expression='Página # %(page_number)d de %(page_count)d', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
        ]
        borders = {'top': True}

    class band_detail(ReportBand):
        auto_expand_height = True
        elements = [
            ObjectValue(attribute_name='numero_patrimonio', left=0*cm, width=3*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
            ObjectValue(attribute_name='descricao', left=3.1*cm, width=11.6*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
            ObjectValue(attribute_name='localizacao', left=14.8*cm, width=4*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
            ObjectValue(attribute_name='marca', left=18.9*cm, width=3*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
            ObjectValue(attribute_name='modelo', left=22*cm, width=3*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
            ObjectValue(attribute_name='numero_serie', left=25.1*cm, width=2.6*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
        ]

class RelatorioInventarioPDF(Report):
    
    author = 'CBTU - Companhia Brasileira de Trens Urbanos'
    
    print_if_empty = True
    page_size = landscape(A4)

    class band_page_header(ReportBand):
        height = 1.75*cm
        elements = [
            SystemField(expression='%(var:titulo)s', top=0, left=0, width=BAND_WIDTH,
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}),
            Label(text="Nº PATRIM", top=1.2*cm, left=0*cm, width=3*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
            Label(text="DESCRIÇÃO DETALHADA", top=1.2*cm, left=3.1*cm, width=11.6*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
            Label(text="LOCALIZAÇÃO", top=1.2*cm, left=14.8*cm, width=4*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
            Label(text="MARCA", top=1.2*cm, left=18.9*cm, width=3*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
            Label(text="MODELO", top=1.2*cm, left=22*cm, width=3*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
            Label(text="Nº DE SÉRIE", top=1.2*cm, left=25.1*cm, width=2.6*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
        ]

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
            SystemField(expression='%(report_author)s', top=0.1*cm, left=0, width=30*cm),
            SystemField(expression='Página # %(page_number)d de %(page_count)d', top=0.1*cm,
                width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
        ]
        borders = {'top': True}

    class band_detail(ReportBand):
        auto_expand_height = True
        elements = [                  
            ObjectValue(attribute_name='numero_patrimonio', left=0*cm, width=3*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
            ObjectValue(attribute_name='descricao', left=3.1*cm, width=11.6*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
            ObjectValue(attribute_name='localizacao', left=14.8*cm, width=4*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
            ObjectValue(attribute_name='marca', left=18.9*cm, width=3*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
            ObjectValue(attribute_name='modelo', left=22*cm, width=3*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
            ObjectValue(attribute_name='numero_serie', left=25.1*cm, width=2.6*cm,
                  style={'alignment':TA_CENTER}, borders={'top': True}),
        ]