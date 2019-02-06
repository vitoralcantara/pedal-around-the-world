# -*- coding: utf-8 -*-
from django.db import models
from djtools.dbfields import SearchField

class StatusItens(models.Model):
    descricao = models.CharField(u'Descrição', max_length=50, blank=True)
    
    class Meta:
        verbose_name = u'Status Item'
        verbose_name_plural = u'Status Itens'
        
    def __unicode__(self):
        return self.descricao


class Inventarios(models.Model):    
    ano = models.CharField(u'Ano', max_length=4, blank=True)    
    
    class Meta:
        verbose_name = u'Inventário'
        verbose_name_plural = u'Inventários'
        
    def __unicode__(self):
        return self.ano

class ItensPatrimoniais(models.Model):    
    inventario = models.ForeignKey(Inventarios, blank=True)
    status = models.ForeignKey(StatusItens)
    
    numero_patrimonio = models.IntegerField(u'Número Patrimônio')
    descricao = models.TextField(u'Descrição')
    marca = models.CharField(u'Marca', max_length=165, blank=True)
    modelo = models.CharField(u'Modelo', max_length=165, blank=True)
    numero_serie = models.IntegerField(u'Número de Série', blank=True)
    comentario = models.TextField(u'Comentário', blank=True)
    
    localizacao = models.CharField(u'Localização Atual', max_length=165, blank=True)
    loc_ant = models.CharField(u'Localização Anterior', max_length=165, blank=True)
    desc_cad = models.CharField(u'Descrição do Cadastro', max_length=165, blank=True)
    
    campo_busca = SearchField(search=['inventario', 'descricao'])
    
    class Meta:
        verbose_name = u'Item Patrimonial'
        verbose_name_plural = u'Itens Patrimoniais'
        
    def __unicode__(self):
        return '%s - %s' %(self.numero_patrimonio, self.descricao)
    
    def _status_item(self):
        return self.status.descricao