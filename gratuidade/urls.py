# -*- coding: utf-8 -*

from django.conf.urls.defaults import patterns

urlpatterns = patterns('gratuidade.views',
           (r'^pessoagratuidade/cartao_gratuidade/(?P<obj_pk>\d+)/$', 'cartao_gratuidade'),
)
    
    
    