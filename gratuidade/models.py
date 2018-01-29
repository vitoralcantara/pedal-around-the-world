# -*- coding: utf-8 -*-
from django.db import models

from comum.models import Pessoa
from string import upper

class PessoaGratuidade(Pessoa):
    numero_carteira = models.IntegerField(u'Número da Carteira', unique=True)
    validade = models.DateField(u'Validade')
    situacao = models.CharField(u'Situação', max_length=15)
    via_carteira = models.CharField(u'Via Carteira', max_length=2)
    tipo = models.CharField(u'Tipo de Pessoa', max_length=15)

    # Numero antigo da carteira de Gratuidade
    carteira_antigo = models.CharField(u'Número Antigo da Carteira', max_length=35, blank=True)
    
    class Meta:
        verbose_name = u'Gratuidade'
        verbose_name_plural = u'Gratuidades'

    def __unicode__(self):
        return '%s (%s)' %(self.nome, self.numero_carteira)
    
    def _endereco_cidade(self):
        return upper(self.endereco.municipio)
    
    def _endereco_cep(self):
        return self.endereco.cep
    
    def _nome_pessoa(self):
        return self.nome
    
    def _tipo_pessoa(self):
        if self.tipo == 'tratmedico':
            return u'Trat. médico'
        elif self.tipo == 'tratmedacom':
            return u'Trat. méd. c/ acomp.'
        elif self.tipo == 'defiacom':
            return 'Deficiente c/ acomp.'
        else:
            return self.tipo.title()

class CarteirasAntigas(models.Model):
    pessoa_id = models.ForeignKey(PessoaGratuidade,on_delete=models.CASCADE)
    numero_carteira = models.IntegerField(u'Número da Carteira')
    data_desativada = models.DateField(u'Data expirada')

    class Meta:
        unique_together = (("pessoa_id","numero_carteira"),)

