# -*- coding: utf-8 -*-
from django.contrib import admin

from gratuidade.models import PessoaGratuidade
from gratuidade.forms import PessoaGratuidadeForm
from djtools.utils import rtr, httprr

#admin.site.register(PessoaGratuidade)

class PessoaGratuidadeAdmin(admin.ModelAdmin):
    
#    def get_urls(self):
#        from django.conf.urls.defaults import patterns
#        urls = super(PessoaGratuidadeAdmin, self).get_urls()
#        my_urls = patterns('', 
#                           (r'^(.+)/add/$', self.gratuidade_add),                           
#                           )
#        return my_urls + urls
#    
#    @rtr()
#    def gratuidade_add(self, request, object_id):
#        if request.method == 'POST':
#            form = PessoaGratuidadeForm(request.POST)
#            if form.is_valid():
#                form.save()
#                return httprr('', u'Inscrição realizada com sucesso!')
#        else:
#            form = PessoaGratuidadeForm()
#        return locals()
    
    form = PessoaGratuidadeForm
    
    search_fields = ['nome', 'numero_carteira', 'cpf', 'carteira_antigo']
    list_display = ['editar', 'carteira', 'nome', 'cpf', 'numero_carteira', 'qtd_vale', 'tipagem']  
    
    fieldsets = [
        ('Dados Pessoais', {'fields': ['nome', 'cpf','data_nascimento','telefone','rg', 'via_documento', 'uf','naturalidade','estado_civil','nacionalidade','nome_mae','nome_pai','email']}),
        ('Dados da Carteira', {'fields': ['qtd_vale','situacao','via_carteira','tipo']}),
        (u'Endereço', {'fields': ['logradouro','numero','complemento','bairro','municipio','cep']}),
    ]

    def editar(self, obj):
        return '<img src="/media/img/16x16/editar.png" title="Editar" />'
    editar.allow_tags = True
    editar.short_description = ''
    editar.attrs = {'width': '10px'}

    def tipagem(self, obj):
        if obj.tipo == 'tratmedico':
            return 'Trat. medico'
        elif obj.tipo == 'tratmedacom':
            return 'Trat. med. c/ acomp.'
        elif obj.tipo == 'defiacom':
            return 'Deficiente c/ acomp.'
        else:
            return obj.tipo.title()

    tipagem.allow_tags = True
    tipagem.short_description = 'Tipo de Pessoa'

    def carteira(self, obj):        
        return '<a href="/gratuidade/pessoagratuidade/cartao_gratuidade/%s/"><img src="/media/img/16x16/cartao_yes.png" title="Imprimir Cartão" /></a>' % (obj.pk)        
    carteira.allow_tags = True
    carteira.short_description = 'Cartão'
    carteira.attrs = {'width': '10px'}

    
admin.site.register(PessoaGratuidade, PessoaGratuidadeAdmin)
