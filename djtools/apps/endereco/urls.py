# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns
from endereco.views import get_dados_por_cep

urlpatterns = patterns('',
    
    # Ajax
    (r'^get_dados_por_cep/', get_dados_por_cep),
    (r'^(?P<objeto_id>\d+)/delete/', 'endereco.views.endereco_deletar'),
    
)
