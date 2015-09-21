# -*- coding: utf-8 -*

from django.conf.urls.defaults import patterns

urlpatterns = patterns('inventario.views',
            (r'^itenspatrimoniais/relatorio_geral/$', 'relatorio_geral'),
#            (r'^itenspatrimoniais/relatorio/$', 'relatorio'),
            
            (r'^inventario_busca/$', 'inventario_busca'),            
)