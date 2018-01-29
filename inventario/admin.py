# -*- coding: utf-8 -*-

from django.contrib import admin

from inventario.models import StatusItens, Inventarios, ItensPatrimoniais
from inventario.forms import ItensPatrimoniaisForm

admin.site.register(StatusItens)
admin.site.register(Inventarios)

#admin.site.register(ItensPatrimoniais)

#####################
# ITENSPATRIMONIAIS #
#####################

class ItensPatrimoniaisAdmin(admin.ModelAdmin):
    
    form = ItensPatrimoniaisForm
    search_fields = ['numero_patrimonio', 'descricao']
    list_display = ['editar', 'numero_patrimonio', 'descricao'] 
    list_filter = ['inventario']
    
    fieldsets = [
                 ('', {'fields': ['inventario', 'numero_patrimonio', 'descricao', 'desc_cad']}), 
                 ('Localização', {'fields': ['localizacao', 'loc_ant']}),
                 ('Inventário',{'fields': ['marca', 'modelo', 'numero_serie', 'comentario', 'status']}),
                 ]
    
    def editar(self, obj):
        return '<img src="/media/img/16x16/editar.png" title="Editar" />'
    editar.allow_tags = True
    editar.short_description = ''
    editar.attrs = {'width': '10px'}
    
admin.site.register(ItensPatrimoniais, ItensPatrimoniaisAdmin)