# -*- coding: utf-8 -*-

import os

cur_dir = os.path.dirname(os.path.abspath(__file__))

from geraldo import Image
from geraldo import Report, ReportBand, ObjectValue, landscape, SystemField
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER


class CarteiraGratuidadePDF(Report):
    title = 'Carteira de Gratuidade'
    author = 'CBTU/RN'

    print_if_empty = True
    page_size = landscape(A4)

    class band_detail(ReportBand):
        cur_dir += '/img/'
        elements = (
            Image(left=1.75 * cm, top=0.5 * cm, filename=os.path.join(cur_dir, 'carteira2017.png')),

            ##############
            ## CARTEIRA ##
            ##############
            ObjectValue(attribute_name='_tipo_pessoa', left=5 * cm, top=2.45 * cm,
                        style={'fontSize': 15, 'alignment': TA_CENTER}),
            ObjectValue(attribute_name='numero_carteira', left=5.2 * cm, top=5.5 * cm, ),
            ObjectValue(attribute_name='nome', width=8.5 * cm, left=5.2 * cm, top=4.6 * cm, ),
            ObjectValue(attribute_name='nome_pai', width=8.5 * cm, left=14 * cm, top=1.1 * cm, ),
            ObjectValue(attribute_name='nome_mae', width=8.5 * cm, left=14 * cm, top=1.5 * cm, ),
            ObjectValue(attribute_name='naturalidade', left=14 * cm, top=2.6 * cm,
                        get_value=lambda instance: instance.naturalidade.upper()),
            ObjectValue(attribute_name='data_nascimento', left=19.2 * cm, top=2.6 * cm,
                        get_value=lambda instance: instance.data_nascimento.strftime('%d/%m/%Y')),
            ObjectValue(attribute_name='validade', left=8 * cm, top=3.6 * cm,
                        get_value=lambda instance: instance.validade.strftime('%d/%m/%Y')
                        if instance.validade else ""),
            ObjectValue(attribute_name='nacionalidade', left=14 * cm, top=3.55 * cm,
                        get_value=lambda instance: instance.nacionalidade.upper()),
            ObjectValue(attribute_name='estado_civil', left=18.0 * cm, top=3.55 * cm,
                        get_value=lambda instance: instance.estado_civil.upper()),
            ObjectValue(attribute_name='via_carteira', left=20.5 * cm, top=3.6 * cm, ),
            ObjectValue(attribute_name='cpf', left=14 * cm, top=4.5 * cm, ),
            ObjectValue(attribute_name='rg', left=18.0 * cm, top=4.5 * cm, ),
            ObjectValue(attribute_name='via_documento', left=20.5 * cm, top=4.5 * cm, ),
            SystemField(expression='%(now:%d/%m/%Y)s', left=5.2 * cm, top=3.6 * cm, ),

            #######################
            ## FICHA DE CADASTRO ##
            #######################

            ObjectValue(attribute_name='via_carteira', left=9.9 * cm, top=9.55 * cm, ),
            SystemField(expression='%(now:%d/%m/%Y)s', left=18.15 * cm, top=9.55 * cm, ),
            ObjectValue(attribute_name='_tipo_pessoa', left=12 * cm, top=10.8 * cm,
                        style={'fontSize': 15, 'alignment': TA_CENTER}),
            ObjectValue(attribute_name='numero_carteira', left=5.35 * cm, top=12.33 * cm, ),
            ObjectValue(attribute_name='endereco', left=15.35 * cm, top=12.33 * cm, ),
            ObjectValue(attribute_name='nome', width=8.5 * cm, left=5.1 * cm, top=13 * cm, ),
            ObjectValue(attribute_name='nome_pai', width=8.5 * cm, left=5.35 * cm, top=13.7 * cm, ),
            ObjectValue(attribute_name='nome_mae', width=8.5 * cm, left=5.35 * cm, top=14.1 * cm, ),
            ObjectValue(attribute_name='_endereco_cidade', left=15 * cm, top=13.75 * cm, ),
            ObjectValue(attribute_name='_endereco_cep', left=20.6 * cm, top=13.73 * cm, ),
            ObjectValue(attribute_name='rg', left=5.75 * cm, top=15.6 * cm, ),
            ObjectValue(attribute_name='via_documento', left=9 * cm, top=15.6 * cm, ),
            ObjectValue(attribute_name='data_nascimento', left=15.5 * cm, top=14.9 * cm,
                        get_value=lambda instance: instance.data_nascimento.strftime('%d/%m/%Y')),
            ObjectValue(attribute_name='estado_civil', left=19.9 * cm, top=14.9 * cm,
                        get_value=lambda instance: instance.estado_civil.upper()),
            ObjectValue(attribute_name='cpf', left=5.75 * cm, top=16.1 * cm, ),
            ObjectValue(attribute_name='nacionalidade', left=6.2 * cm, top=16.69 * cm,
                        get_value=lambda instance: instance.nacionalidade.upper()),
            ObjectValue(attribute_name='naturalidade', left=6 * cm, top=17.3 * cm,
                        get_value=lambda instance: instance.naturalidade.upper()),
            ObjectValue(attribute_name='telefone', left=13.1 * cm, top=17.3 * cm, ),
            #ObjectValue(attribute_name='qtd_vale', left=17.5 * cm, top=17.2 * cm, ),
            ObjectValue(attribute_name='validade', left=17.1 * cm, top=17.2 * cm,
                        get_value=lambda instance: instance.validade.strftime('%d/%m/%Y')
                        if instance.validade else ""),
            ObjectValue(attribute_name='situacao', left=18.4 * cm, top=17.2 * cm,
                        get_value=lambda instance: instance.situacao.upper(),
                        style={'alignment': TA_CENTER}),

        )
