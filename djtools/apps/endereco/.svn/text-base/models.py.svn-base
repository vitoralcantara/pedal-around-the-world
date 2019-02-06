# -*- coding: utf-8 -*-

"""
Forma de implantação:
    psql -U postgres <DB_NAME> cep_app_endereco.sql
    ./manage.py syncdb (Para criar tabela ``endereco_endereco``)
    ./manage.py sqlsequencereset endereco
"""

from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from djtools.dbfields import BrCepField, BrEstadoBrasileiroField


def get_models_to_audit():
    models_to_audit = []
    app_endereco = models.get_app('endereco')
    for model_cls in models.get_models(app_endereco):
        models_to_audit.append('endereco.%s' % (model_cls.__name__.lower()))
    models_to_audit.remove('endereco.endereco')
    return models_to_audit


class Endereco(models.Model):
    # Tabela de CEPs
    local_content_type = models.ForeignKey(ContentType, null=True,
            related_name='local_set_for_%(class)s')
    local_pk = models.PositiveIntegerField(null=True)
    local = generic.GenericForeignKey('local_content_type', 'local_pk')
    
    # Dono do ``Endereco``
    objeto_content_type = models.ForeignKey(ContentType, null=True,
            related_name='objeto_set_for_%(class)s')
    objeto_pk = models.PositiveIntegerField(null=True)
    objeto = generic.GenericForeignKey('objeto_content_type', 'objeto_pk')
    
    # Campos opcionais, réplica da tabela de CEPs ou caso a base_cep seja `None`
    cep = BrCepField(u'CEP', null=True, blank=True)
    tp_logradouro = models.CharField(u'Tipo Logradouro', 
                                     max_length=20, null=True, blank=True,
                                     help_text=u'Ex: Rua, Travessa, Vila, Avenida, Praça etc')
    logradouro = models.CharField(max_length=70, null=True, blank=True)
    bairro = models.CharField(max_length=72, null=True, blank=True)
    cidade = models.CharField(max_length=50, null=True, blank=True)
    uf = BrEstadoBrasileiroField(u'UF', max_length=2, null=True, blank=True)
    
    # Campos opcionais
    numero = models.CharField(u'Nº', max_length=20, null=True, blank=True)
    complemento = models.CharField(u'Comp.', max_length=50, null=True, blank=True)
    
    class Meta:
        ordering = ['id']
    
    @classmethod
    def get_lista_por_objeto(cls, objeto):
        """
        """
        content_type = ContentType.objects.get_for_model(objeto.__class__)
        content_types = [content_type]
        
        model_class = content_type.model_class()
        while model_class.__base__.__name__ != 'Model':
            content_type = ContentType.objects.get_for_model(model_class)
            content_types.append(content_type)
            model_class = model_class.__base__
        
        return cls.objects.filter(objeto_content_type__in=content_types,
                                  objeto_pk=objeto.pk)
    
    def sincronizar_dados_com_local(self, local):
        """
        """
        self.local = local
        self.cidade = local.cidade
        if isinstance(local, CepUnico):
            self.uf = local.uf
        else:
            self.tp_logradouro = local.tp_logradouro
            self.logradouro= local.logradouro
            self.bairro = local.bairro
    
    def save(self):
        """
        Se o CEP existe na base local, a relação será feita.
        """
        from endereco.utils import get_endereco
        local = get_endereco(self.cep)
        if local:
            self.sincronizar_dados_com_local(local)
        models.Model.save(self)
    
    def __unicode__(self):
        return u'(CEP %s) %s %s %s %s, %s, %s/%s' \
            %(self.cep, self.tp_logradouro, self.logradouro, self.numero,
              self.complemento, self.bairro, self.cidade, self.uf)
    

###############
# Tabelas para os estados brasileiros
###############

class EstadoBrasileiro:
    
    @property
    def uf(self):
        return self.__class__.__name__.upper()
    
    def __unicode__(self):
        return self.cep
    
    def to_dict(self):
        return dict(tp_logradouro = self.tp_logradouro,
                    logradouro    = self.logradouro,
                    bairro        = self.bairro,
                    cidade        = self.cidade,
                    uf            = self.uf)

class Ac(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Al(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Am(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Ap(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Ba(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Ce(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Df(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Es(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Go(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Ma(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Mg(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Ms(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Mt(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Pa(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Pb(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Pe(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Pi(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Pr(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Rj(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Rn(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Ro(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Rr(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Rs(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Sc(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Se(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class Sp(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class To(models.Model, EstadoBrasileiro):
    cidade = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=70)
    bairro = models.CharField(max_length=72)
    cep = models.CharField(max_length=9)
    tp_logradouro = models.CharField(max_length=20)

class CepUnico(models.Model):
    cidade = models.CharField(max_length=50)
    nomesemacento = models.CharField(max_length=50)
    cep = models.CharField(max_length=9)
    uf = models.CharField(max_length=2)
    
    def to_dict(self):
        return dict(tp_logradouro = '',
                    logradouro    = '',
                    bairro        = '',
                    cidade        = self.cidade,
                    uf            = self.uf)

