# -*- coding: utf-8 -*-

#########
# COMUM #
#########

ESTADO_CIVIL = (
                ('solteiro', u'Solteiro'),
                ('casado', u'Casado'),
                ('divorciado', u'Divorciado'),
                ('separado', u'Separado'),
                ('viuvo', u'Viúvo')
                )

NACIONALIDADE = (
                 ('brasileira', 'Brasileira'),
                 ('estrangeira', 'Estrangeira')
                 )

##############
# GRATUIDADE #
##############

TIPO_PESSOA = (
            ('aposentado','Aposentado'),
	        ('provisoria','Provisoria'),
            ('deficiente','Deficiente'),
            ('idoso','Idoso'),
            ('defiacom',   'Deficiente c/ acompanhante'),
            ('tratmedico', 'Trat. médico'),
            ('tratmedacom','Trat. méd. c/ acompanhante')
        )

SITUACAO = (
            ('ATIVO','ATIVO'),
            ('INATIVO','INATIVO'),
            ('EM ANÁLISE',u'EM ANÁLISE'),
            ('INDEFERIDO','INDEFERIDO')
        )
