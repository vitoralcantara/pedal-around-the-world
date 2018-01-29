# -*- coding: utf-8 -*-
from django.db import models
from djtools.dbfields import BrEstadoBrasileiroField, BrTelefoneField


class Endereco(models.Model):        
    logradouro = models.CharField(u'Logradouro', max_length=50)
    numero = models.CharField(u'Número', max_length=10, blank=True)
    complemento = models.CharField(u'Complemento', max_length=50, blank=True)
    bairro = models.CharField(u'Bairro', max_length=30, blank=True)
    municipio = models.CharField(u'Município', max_length=30, blank=True)
    
    cep = models.CharField(u'CEP', max_length=9, blank=True)
    
    uf = BrEstadoBrasileiroField(u'UF', max_length=2, blank=True)
    
    class Meta:
        db_table = 'endereco'
        verbose_name = u'Endereço'
        verbose_name_plural = u'Endereços'
    
    def __unicode__(self):
        return '%s, %s' % (self.logradouro.upper(), self.numero)
        

class Pessoa(models.Model):
    nome = models.CharField(u'Nome', max_length=200)
    
    cpf = models.CharField(u'CPF', max_length=20, blank=True,unique=True)
    data_nascimento = models.DateField(u'Data nascimento')
    nacionalidade = models.CharField(u'Nacionalidade', max_length=40, blank=True)
    estado_civil = models.CharField(u'Estado Civil', max_length=20, blank=True)
    
    telefone = BrTelefoneField(u'Telefone', blank=True)
    uf = BrEstadoBrasileiroField(u'UF', max_length=2, blank=True)
    
    naturalidade = models.CharField(u'Naturalidade', max_length=50, blank=True)    
    rg = models.CharField(u'Identidade', max_length=20, blank=True)
    via_documento = models.CharField(u'Via Documento', max_length=2, blank=True)
    nome_mae = models.CharField(u'Nome da mãe', max_length=100, blank=True)
    nome_pai = models.CharField(u'Nome do pai', max_length=100, blank=True)
    email = models.CharField(u'E-Mail', max_length=50, blank=True)
    excluido = models.BooleanField(u'Excluído', default=False)
    
    endereco = models.ForeignKey(Endereco, verbose_name=u'Endereço')
    
    class Meta:
        db_table = 'pessoa'
        verbose_name = u'Pessoa'
        verbose_name_plural = u'Pessoas'
        
    def __unicode__(self):
        return self.nome