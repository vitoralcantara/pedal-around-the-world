# -*- coding: utf-8 -*-

from django.contrib import admin

from comum.models import Pessoa, Endereco
from comum.forms import PessoaForm, EnderecoForm

#admin.site.register(Pessoa)
#admin.site.register(Endereco)

##########
# PESSOA #
##########

class PessoaAdmin(admin.ModelAdmin):
    form = PessoaForm    
    search_fields = ['nome', 'cpf']
    list_display = ['nome', 'cpf', 'data_nascimento']    
admin.site.register(Pessoa, PessoaAdmin)

############
# ENDERECO #
############
    
class EnderecoAdmin(admin.ModelAdmin):
    form = EnderecoForm
admin.site.register(Endereco, EnderecoAdmin)