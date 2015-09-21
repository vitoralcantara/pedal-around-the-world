# -*- coding: utf-8 -*-

from django.db import models
import urllib
import cgi
import re

# Expressões regulares adaptadas de: 
# http://plasoft.wordpress.com/2007/05/11/validacao-de-cep-por-estado/
estados_re = dict(
    SP = re.compile(r'^([1][0-9]{3}|[01][0-9]{4})[0-9]{3}$'),
    RJ = re.compile(r'^[2][0-8][0-9]{3}[0-9]{3}$'),
    MS = re.compile(r'^[7][9][0-9]{3}[0-9]{3}$'),
    MG = re.compile(r'^[3][0-9]{4}[0-9]{3}$'),
    MT = re.compile(r'^[7][8][8][0-9]{2}[0-9]{3}$'),
    AC = re.compile(r'^[6][9]{2}[0-9]{2}[0-9]{3}$'),
    AL = re.compile(r'^[5][7][0-9]{3}[0-9]{3}$'),
    AM = re.compile(r'^[6][9][0-8][0-9]{2}[0-9]{3}$'),
    AP = re.compile(r'^[6][89][9][0-9]{2}[0-9]{3}$'),
    BA = re.compile(r'^[4][0-8][0-9]{3}[0-9]{3}$'),
    CE = re.compile(r'^[6][0-3][0-9]{3}[0-9]{3}$'),
    DF = re.compile(r'^[7][0-3][0-6][0-9]{2}[0-9]{3}$'),
    ES = re.compile(r'^[2][9][0-9]{3}[0-9]{3}$'),
    GO = re.compile(r'^[7][3-6][7-9][0-9]{2}[0-9]{3}$'),
    MA = re.compile(r'^[6][5][0-9]{3}[0-9]{3}$'),
    PA = re.compile(r'^[6][6-8][0-8][0-9]{2}[0-9]{3}$'),
    PB = re.compile(r'^[5][8][0-9]{3}[0-9]{3}$'),
    PE = re.compile(r'^[5][0-6][0-9]{2}[0-9]{3}$'),
    PI = re.compile(r'^[6][4][0-9]{3}[0-9]{3}$'),
    PR = re.compile(r'^[8][0-7][0-9]{3}[0-9]{3}$'),
    RN = re.compile(r'^[5][9][0-9]{3}[0-9]{3}$'),
    RO = re.compile(r'^[7][8][9][0-9]{2}[0-9]{3}$'),
    RR = re.compile(r'^[6][9][3][0-9]{2}[0-9]{3}$'),
    RS = re.compile(r'^[9][0-9]{4}[0-9]{3}$'),
    SC = re.compile(r'^[8][89][0-9]{3}[0-9]{3}$'),
    SE = re.compile(r'^[4][9][0-9]{3}[0-9]{3}$'),
    TO = re.compile(r'^[7][7][0-9]{3}[0-9]{3}$')
)

def get_estado_sigla(cep):
    cep = re.sub('\D', '', cep)
    for estado, re_exp in estados_re.items():
        if re_exp.match(cep):
            return estado
    return None

def get_classe_modelo(cep):
    return models.get_model('django_extra', get_estado_sigla(cep))

def get_local(cep):
    """
    Busca na base local e, se não encontrar, no WebService.
    Retorna None se não encontrar em nenhum dos dois.
    """
    cep_local = None#get_cep_baselocal(cep)
    if cep_local:
        return cep_local
    else:
        cep_ws = get_cep_webservice(cep)
        if cep_ws:
            return cep_ws
        else:
            return None

def get_cep_baselocal(cep):
    cls = get_classe_modelo(cep)
    cep = '%s-%s' % (''.join(cep[:-3]), ''.join(cep[-3:]))
    try:
        return cls.objects.get(cep=cep)
    except cls.DoesNotExist:
        return None

def get_cep_webservice(cep, salvar_local=True):
    # Web Service utilizado:
    # http://www.republicavirtual.com.br/cep/index.php
    cep = re.sub('\D', '', cep)
    url = "http://cep.republicavirtual.com.br/web_cep.php?cep=" + cep + "&formato=query_string"
    WS_ENCODING = 'latin-1'
    pagina = urllib.urlopen(url)
    conteudo = pagina.read()
    resultado = cgi.parse_qs(conteudo)
    if resultado['resultado'][0] == '1':
        # resultado.keys(): ['tipo_logradouro', 'resultado', 'bairro', 'cidade', 
        #                    'logradouro', 'resultado_txt', 'uf']
        resultado.pop('resultado')
        resultado.pop('resultado_txt')
        resultado['tp_logradouro'] = resultado.pop('tipo_logradouro')
        local = dict()
        for key, value in resultado.items():
            local[key] = value[0].decode(WS_ENCODING)
        if not salvar_local:
            return local
        else:
            cls = get_classe_modelo(cep)
            return cls.objects.create(**local)
    elif resultado['resultado'][0] == '2':
        local = dict(
            cidade=resultado['cidade'][0].decode(WS_ENCODING),
            uf=resultado['uf'][0].decode(WS_ENCODING)
        )
        if not salvar_local:
            return local
        else:
            cls = models.get_model('endereco', 'cepunico')
            return cls.objects.create(**local)
    else:
        return None
