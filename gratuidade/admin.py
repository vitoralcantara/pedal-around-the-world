# -*- coding: utf-8 -*-
from django.contrib import admin

from gratuidade.models import PessoaGratuidade
from gratuidade.forms import PessoaGratuidadeForm
from djtools.utils import rtr, httprr
from datetime import date
from django.contrib.admin.views import main
import pdb

#admin.site.register(PessoaGratuidade)

class PessoaGratuidadeAdmin(admin.ModelAdmin):

    form = PessoaGratuidadeForm

    def __init__(self, *args, **kwargs):
        super(PessoaGratuidadeAdmin, self).__init__(*args, **kwargs)
        main.EMPTY_CHANGELIST_VALUE = '-'



    search_fields = ['nome', 'numero_carteira', 'cpf', 'carteira_antigo']
    list_display = ['editar', 'carteira','situacao', 'nome', 'cpf', 'num_carteira', 'validade', 'tipagem']

    fieldsets = [
        ('Dados Pessoais', {'fields': ['nome', 'cpf','data_nascimento','telefone','rg', 'via_documento', 'uf','naturalidade','estado_civil','nacionalidade','nome_mae','nome_pai','email']}),
        ('Dados da Carteira', {'fields': ['validade','situacao','via_carteira','tipo']}),
        (u'Endereço', {'fields': ['logradouro','numero','complemento','bairro','municipio','cep']}),
    ]

    def editar(self, obj):
        return '<img src="/media/img/16x16/editar.png" title="Editar" />'
    editar.allow_tags = True
    editar.short_description = 'Editar'
    #editar.attrs = {'width': '1px'}


    def tipagem(self, obj):
        if obj.tipo == 'tratmedico':
            return u'Trat. médico'
        elif obj.tipo == 'tratmedacom':
            return u'Trat. méd. c/ acomp.'
        elif obj.tipo == 'defiacom':
            return 'Deficiente c/ acomp.'
        else:
            return obj.tipo.title()

    tipagem.allow_tags = True
    tipagem.short_description = 'Tipo de Pessoa'

    def carteira(self, obj):
        if obj.situacao.upper() == "ATIVO" or obj.situacao.upper() == "INATIVO":
            return '<a href="/gratuidade/pessoagratuidade/cartao_gratuidade/%s/"><img src="/media/img/16x16/cartao_yes.png" title="Imprimir Cartão" /></a>' % (
        obj.pk)
        else:
            return '<img src="/media/img/16x16/cartao_no.png" title="Sem Cartão" />'

    carteira.allow_tags = True
    carteira.short_description = 'Cartão'

    def num_carteira(self,obj):
        return obj.numero_carteira
    num_carteira.admin_order_field = 'numero_carteira'
    num_carteira.short_description = 'Carteira'





admin.site.register(PessoaGratuidade, PessoaGratuidadeAdmin)
