# -*- coding: utf-8 -*-

#XXX: DEPRECATED - Mover funções para comum.utils ou djtools.utils.

from datetime import date, timedelta
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import dateformat
from stunat.djtools.middleware import threadlocals as tl


def get_allowed_apps(user=None):
    """Se o usuário tiver alguma permissão de uma app, ela será permitida."""
    user = user or tl.get_user()
    if user is None:
        return []
    all_apps = [i[0] for i in settings.APP_CONTENT_TYPES]
    return [g.name.split('_')[0] for g in user.groups.all() if all_apps]

def get_allowed_apps_choices(user=None):
    """É o ``get_allowed_apps`` com retorno adaptado para o select html"""
    user = user or tl.get_user()
    if user is None:
        return []
    return [[app_label, app_name] for app_label, app_name in settings.APP_CONTENT_TYPES \
            if app_label in get_allowed_apps(user)]

@login_required
def stunat_context_processor(request):
    if 'current_app' not in request.session: # O usuário acabou de logar
        request.session['current_app'] = 'home'
        request.session['debug'] = settings.DEBUG
        request.session['allowed_apps'] = get_allowed_apps(request.user)
        request.session['allowed_apps_choices'] = get_allowed_apps_choices(request.user)
        request.session['template_menu'] = get_template_menu_name(request)
    
    # Caso a URL pertenca a uma app que não seja a atual, vamos mudar a app
    path = request.path.split('/')
    app_label = path[0] != 'admin' and path[0] or path[1]
    if app_label != request.session.get('current_app') and \
        app_label in request.session.get('allowed_apps'):
            change_app(request, app_label)
        
    return dict(super_template       = 'admin/base.html',
                debug                = request.session['debug'],
                allowed_apps         = request.session.get('allowed_apps'),
                allowed_apps_choices = request.session.get('allowed_apps_choices'),
                current_app          = request.session.get('current_app'),
                template_menu        = request.session.get('template_menu'))

@login_required
def change_app(request, app_label):
    request.session['current_app'] = app_label
    request.session['template_menu'] = get_template_menu_name(request, app_label)

@login_required
def get_template_menu_name(request, app_label='home'):
    """Baseado na app escolhida, o menu adequado será retornado."""
    app_label = app_label
    if app_label == 'home':
        return None
    group = request.user.groups.filter(name__istartswith=app_label)[0]
    return '%(app)s/templates/menu/%(group)s.html' %(dict(app=app_label, group=group.name))


### Conversões de tipos de dados

def tratar_dados(dicionario):
    """
    Estou usando isso para tratar GET/POST de request.
    Essa função pode ser muito melhorada.
    """
    dados_tratados = {}
    for key, value in dicionario.items():
        if value.replace(' ', '') == '':
            dados_tratados[key] = None
        else:
            if value.isdigit():
                dados_tratados[key] = int(value)
            else:
                dados_tratados[key] = value
    return dados_tratados

def str_to_date(value):
    # XXX: Deprecated; usar djtools.utils.str_to_dateBR
    try:
        lista = value.split('/')
        return date(int(lista[2]), int(lista[1]), int(lista[0]))
    except:
        return None

def moeda_to_decimal(value):
    # XXX: Deprecated; usar djtools.utils.str_money_to_decimal
    value_float = float(value.replace('.', '').replace(',', '.'))
    return Decimal(str(value_float))

def float_to_moeda(value):
    # XXX: Deprecated; usar djtools.utils.mask_money
    reaisCentavos = str(value).split('.')
    reais = reaisCentavos[0]
    listaReais = []
    for i in range(len(reais)):
        if i!=0 and (len(reais)-i)%3==0:
            listaReais.append('.')
        listaReais.append(reais[i])
    if len(reaisCentavos) == 2:
        centavos = reaisCentavos[1]
        if len(centavos) == 1:
            centavos += '0'
    else:
        centavos = '00'
    return ''.join(listaReais) + ',' + centavos


### String

def extrair_numeros(value):
    """
    Retorna o `value` somente com os caracteres numéricos.
    Ex: '123abc456' --> '123456'
    """
    value = list(value)
    return ''.join([i for i in value if i.isdigit()])


### Listas

def agrupar_em_pares(lista):
    """
    [0, 1, 2, 3, 4, 5, 6] --> [[0, 1], [2, 3], [4, 5], [6]]
    """
    lista_pares = []
    for index, item in enumerate(lista):
        if index % 2 == 0:
            lista_pares.append([item])
        else:
            lista_pares[-1].append(item)
    return lista_pares


### Datas

def somar_data(data,  qtd_dias):
    # TODO: Mover para djtools.utils
    return data + timedelta(qtd_dias)
    

def data_extenso(data=None):
    # XXX: Função Desnecessária, basta usar dateformat.format
    data = data or date.today()
    return dateformat.format(data, 'd \de F \de Y')

def data_normal(data=None):
    """
    Ex: date(2008, 1, 1) --> '01/01/2008'.
    """
    data = data or date.today()
    return data.strftime('%d/%m/%Y')

def extrair_periodo(data_ini, data_fim):
    """
    Retorna string que representa o período entre as datas passadas.
    Ex: date(2008, 1, 1), date(2008, 2, 1) --> '01/01/2008 até '01/02/2008'.
    """
    return u'%s até %s' %(data_ini.strftime('%d/%m/%Y'),
                          data_fim.strftime('%d/%m/%Y'))

def datas_entre(data_ini, data_fim, sabado=True, domingo=True):
    """
    """
    dias = []
    data_atual = data_ini
    while data_atual <= data_fim:
        if not sabado and data_atual.weekday() == 5:
            data_atual = data_atual + timedelta(1)
            continue
        if not domingo and data_atual.weekday() == 6:
            data_atual = data_atual + timedelta(1)
            continue
        dias.append(data_atual)
        data_atual = data_atual + timedelta(1)
    return dias
### Hora

def formata_segundos(segundos):
    t_hora = segundos /3600
    aux = segundos % 3600
    t_minuto = aux / 60
    t_segundo = aux % 60 
                
    dic_tempo = {'h':t_hora, 'm':t_minuto, 's':t_segundo}
    return dic_tempo

### Matemáticas

def somar_qtd(lista_de_listas, indice):
    """Soma índice numa lista de listas"""
    soma = Decimal('0.0')
    for item in lista_de_listas:
        value = item[indice]
        if value is not None:
            if isinstance(value, str):
                soma += moeda_to_decimal(value)
            elif isinstance(value, float):
                soma += Decimal(str(value))
            elif isinstance(value, Decimal):
                soma += value
    return soma.__int__()

def somar_indice(lista_de_listas, indice):
    """Soma índice numa lista de listas"""
    soma = Decimal('0.0')
    for item in lista_de_listas:
        value = item[indice]
        if value is not None:
            if isinstance(value, str):
                soma += moeda_to_decimal(value)
            elif isinstance(value, float):
                soma += Decimal(str(value))
            elif isinstance(value, Decimal):
                soma += value
    return soma


### SQL

def entre_datas(data_ini, data_fim, coluna='data'):
    data_fim = data_fim + timedelta(1)
    return "%(coluna)s >= '%(data_ini)s' and %(coluna)s < '%(data_fim)s'" \
        %(dict(coluna=coluna, data_ini=data_ini, data_fim=data_fim))


### Máscaras

def mascara_processo(value):
    return u'%s.%s/%s-%s' %(value[:5], value[5:11], value[11:15], value[15:])

global campos
campos = [
    { 'campo': 'cpf', 'alias': 'CPF' },
    { 'campo': 'sexo', 'alias': 'Sexo' },
    { 'campo': 'data_nascimento', 'alias': 'Data de Nascimento' },
    { 'campo': 'nivel_escolaridade', 'alias': 'Escolaridade' },
    { 'campo': 'ingresso_serv_pub', 'alias': 'Ingresso Serv. Pub.' },
    { 'campo': 'ingresso_serv_pub_posse', 'alias': 'Posse Serv. Pub.' },
    { 'campo': 'ingresso_no_orgao', 'alias': 'Ingresso no Órgão' },
    { 'campo': 'tempo_servico', 'alias': 'Tempo de Serviço' },
    { 'campo': 'setor_lotacao', 'alias': u'Setor (Lotação)' },
    { 'campo': 'setor_lotacao_data_ocupacao', 'alias': 'Setor (Ocupação)' },
    { 'campo': 'funcao', 'alias': 'Função' },
    { 'campo': 'funcao_codigo', 'alias': u'Função (Código)' },
    { 'campo': 'funcao_data_ocupacao', 'alias': u'Função (Ocupação)' },
    { 'campo': 'setor_funcao', 'alias': u'Setor (Função)' },
    { 'campo': 'cargo_emprego', 'alias': 'Cargo Emprego' },
    { 'campo': 'cargo_emprego_data_ocupacao', 'alias': u'Cargo Emprego (Ocupação)' },
    { 'campo': 'cargo_emprego_data_saida', 'alias': 'Cargo Emprego(Saída)' },
    { 'campo': 'cargo_classe', 'alias': 'Classe do Cargo' },
    { 'campo': 'jornada_trabalho', 'alias': 'Jornada de Trabalho' },
    { 'campo': 'formacao_completa', 'alias': 'Formação Reconhecida' },
    { 'campo': 'atividade', 'alias': 'Atividade' },
    { 'campo': 'regime_juridico', 'alias': 'Regime Jurídico' },
    { 'campo': 'situacao', 'alias': 'Situação' },
    { 'campo': 'dados_bancarios', 'alias': 'Dados Bancários' },
    { 'campo': 'carteira_de_trabalho', 'alias': 'Carteira de Trabalho' },
    { 'campo': 'afastamento', 'alias': 'Afastamento' },
    { 'campo': 'aposentadoria', 'alias': 'Aposentadoria' },
    { 'campo': 'exclusao_data_ocorrencia', 'alias': 'Ocorrência de Exclusão' },
    { 'campo': 'data_obito', 'alias': 'Data de Óbito' },
    { 'campo': 'categoria', 'alias': 'Categoria' },
    { 'campo': 'nivel_padrao', 'alias': 'Nível Padrão' },
    { 'campo': 'identificacao_unica_siape', 'alias': 'Identificação Única' },
    { 'campo': 'data_cadastro_siape', 'alias': 'Data Cadastro' },
    { 'campo': 'qtde_depend_ir', 'alias': 'Qtde Depend. IR' },
    { 'campo': 'campus', 'alias': 'Campus' },
    { 'campo': 'codigo_vaga', 'alias': u'Código de Vaga' },
    { 'campo': 'titulacao', 'alias': u'Titulação' },
    { 'campo': 'nome_pai', 'alias': u'Nome do Pai' },
    { 'campo': 'nome_mae', 'alias': u'Nome da Mãe' },
    { 'campo': 'titulo_numero', 'alias': u'Titulo Eleitoral' },
    { 'campo': 'titulo_zona', 'alias': u'Titulo (Zona)' },
    { 'campo': 'titulo_secao', 'alias': u'Titulo (Seção)' },
    { 'campo': 'titulo_uf', 'alias': u'Titulo (UF)' },
    { 'campo': 'titulo_data_emissao', 'alias': u'Titulo (Emissão)' },    
    { 'campo': 'rg', 'alias': u'RG' },
    { 'campo': 'rg_data', 'alias': u'RG (Data)' },
    { 'campo': 'rg_naturalidade', 'alias': u'RG (Naturalidade)' },
    { 'campo': 'rg_orgao', 'alias': u'RG (Órgão)' },
    { 'campo': 'rg_uf', 'alias': u'RG (UF)' },
    { 'campo': 'pis_pasep', 'alias': u'PIS/PASEP' },
    { 'campo': 'grupo_sanguineo', 'alias': u'Grupo Sangüineo' },
    { 'campo': 'fator_rh', 'alias': u'Fator RH' },
    { 'campo': 'cnh_carteira', 'alias': u'CNH (Carteira)' },
    { 'campo': 'cnh_registro', 'alias': u'CNH (Registro)' },
    { 'campo': 'cnh_categoria', 'alias': u'CNH (Categoria)' },
    { 'campo': 'cnh_emissao', 'alias': u'CNH (Emissão)' },
    { 'campo': 'cnh_validade', 'alias': u'CNH (Validade)' },
    { 'campo': 'cnh_uf', 'alias': u'CNH (UF)' },
    { 'campo': 'enderecos', 'alias': u'Endereço' },
    { 'campo': 'email', 'alias': u'E-mail' },
    { 'campo': 'estado_civil', 'alias': u'Estado Civil' },
    { 'campo': 'telefones', 'alias': u'Telefone' },
    { 'campo': 'opera_raio_x', 'alias': u'Opera Raio X' },
    { 'campo': 'pensionistas', 'alias': u'Pensionistas' },
    { 'campo': 'pensionistas_matricula', 'alias': u'Pens (Matrícula)' },
    { 'campo': 'pensionistas_rg', 'alias': u'Pens (RG)' },
    { 'campo': 'pensionistas_titulo', 'alias': u'Pens (Título)' },
    { 'campo': 'pensionistas_endereco', 'alias': u'Pens (Endereço)' },
    { 'campo': 'pensionistas_telefone', 'alias': u'Pens (Telefone)' },
    { 'campo': 'pensionistas_sexo', 'alias': u'Pens (Sexo)' },
    { 'campo': 'pensionistas_estado_civil', 'alias': u'Pens (E. Civil)' },
    { 'campo': 'pensionistas_dados_bancarios', 'alias': u'Pens (Banco)' },
    { 'campo': 'pensionistas_data_ultima_pensao_paga', 'alias': u'Pens (Última Pensão)' },
    { 'campo': 'ferias', 'alias': u'Férias' },
    
]


class MesFechadoException(Exception):
    def __init__(self, message=None):
        message = message or u'Impossível cancelar. O mês já foi fechado.'
        self.message = message
    def __str__(self):
        return repr(self.message)

        
####################
# Agrupamento de grupos
####################

OPERADOR_ALMOXARIFADO = [
    'almoxarifado_operador', 'almoxarifado_gerente', 'almoxarifado_gerente_sistemico',
]
OPERADOR_PATRIMONIO = [
    'patrimonio_operador', 'patrimonio_gerente', 'patrimonio_gerente_sistemico',
]

TODOS_GRUPOS_PATRIMONIO = [
    'patrimonio_padrao', 'patrimonio_operador', 'patrimonio_gerente', 'patrimonio_gerente_sistemico',
]

# FIXME: Essa lógica me parece inapropriada. Um gerente deve ter todas as permissoes
# hierarquicamente inferiores. Verificar

GERENTES_RH = ['rh_gerente_sistemico', 'rh_gerente']

OPERADOR_RH = GERENTES_RH + ['rh_operador']

TODOS_GRUPOS_RH = OPERADOR_RH + ['rh_padrao']

TODOS_GRUPOS_PONTO = [
    'ponto_padrao', 'ponto_operador', 'ponto_gerente', 'ponto_gerente_sistemico',
]
OPERADOR_PONTO = [
    'ponto_operador', 'ponto_gerente', 'ponto_gerente_sistemico',
]
QUALQUER_GRUPO_PONTO = OPERADOR_PONTO + ['ponto_padrao']

QUALQUER_GRUPO_PROTOCOLO = ['protocolo_padrao', 'protocolo_operador']

OPERADOR_FROTA = [
    'frota_operador', 'frota_gerente', 'frota_gerente_sistemico', 
]
OPERADOR_ALMOXARIFADO_OU_PATRIMONIO = OPERADOR_ALMOXARIFADO + OPERADOR_PATRIMONIO

