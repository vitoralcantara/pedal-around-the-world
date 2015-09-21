# -*- coding: utf-8 -*-

from django.db import models
from django.utils.dates import WEEKDAYS
from django.contrib.localflavor.br.br_states import STATE_CHOICES
from djtools import formfields
from djtools.utils import to_ascii, eval_attr
from djtools.utils import randomic


class SearchField(models.TextField):
    """Admin Site Integration: See djtools.utils.DjangoUtilsAdmin"""
    def pre_save(self, model_instance, add):
        search_text = []
        for attr_name in self.search_attrs:
            val = unicode(to_ascii(eval_attr(model_instance, attr_name))).upper().strip()
            search_text.append(val)
        return u' '.join(search_text)
    
    def __init__(self, *args, **kwargs):
        # Django Evolution doesn't give 'search' param
        if 'search' in kwargs:
            self.search_attrs = kwargs.pop('search')
        kwargs.setdefault('editable', False)
        super(self.__class__, self).__init__(*args, **kwargs)
        
        
class BuscaField(models.CharField):
    """Admin Site Integration: See djtools.utils.DjangoUtilsAdmin"""
    def pre_save(self, model_instance, add):
        search_text = []
        for attr_name in self.search_attrs:
            val = unicode(to_ascii(eval_attr(model_instance, attr_name))).upper().strip()
            search_text.append(val)
        return u' '.join(search_text)
    
    def __init__(self, *args, **kwargs):
        # Django Evolution doesn't give 'search' param
        if 'search' in kwargs:
            self.search_attrs = kwargs.pop('search')
        kwargs.setdefault('editable', False)
        kwargs.setdefault('max_length', 90)
        kwargs.setdefault('db_index', True)
        super(self.__class__, self).__init__(*args, **kwargs)        


class RandomField(models.CharField):
    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.name)
        if value:
            return value
        if self.unique:
            values = model_instance.__class__.objects.values_list(self.name, flat=True)
        else:
            values = []
        value = randomic(self.max_length)
        while value in values:
            value = randomic(self.max_length)
        return value
    
    def __init__(self, *args, **kwargs):
        # Django Evolution doesn't give 'search' param
        if 'search' in kwargs:
            self.search_attrs = kwargs.pop('search')
        kwargs.setdefault('editable', False)
        kwargs.setdefault('max_length', 10)
        kwargs.setdefault('unique', True)
        super(self.__class__, self).__init__(*args, **kwargs)


class BrSexoField(models.CharField):
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 1)
        kwargs.setdefault('choices', (('M', 'Masculino'), ('F', 'Feminino')))
        super(self.__class__, self).__init__(*args, **kwargs)


class BrEstadoCivilField(models.CharField):
    
    choices = (
        (u'Solteiro', u'Solteiro'), (u'Casado', u'Casado'),
        (u'Divorciado', u'Divorciado'), (u'Separado', u'Separado'),
        (u'Viúvo', u'Viúvo')
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 50)
        kwargs.setdefault('choices', self.choices)
        super(self.__class__, self).__init__(*args, **kwargs)


class BrDiaDaSemanaField(models.CharField):

    choices = [(unicode(WEEKDAYS[i]), unicode(WEEKDAYS[i])) for i in range(7)]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 50)
        kwargs.setdefault('choices', self.choices)
        super(BrDiaDaSemanaField, self).__init__(*args, **kwargs)


class BrDinheiroField(models.DecimalField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('decimal_places', 2)
        kwargs.setdefault('max_digits', 12)
        super(self.__class__, self).__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', formfields.BrDinheiroField)
        return super(self.__class__, self).formfield(**kwargs)


class PostgresBinaryField(models.Field):
    
    def db_type(self):
        return 'bytea'
    
    def get_db_prep_value(self, value):
        if value:
            import psycopg2
            if isinstance(value, file):
                file_ = value
                value = file_.read()
                file_.close()
            return psycopg2.Binary(value)
        else:
            return value


class BrCpfField(models.CharField):
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 14)
        kwargs.setdefault('verbose_name', u'CPF')
        super(self.__class__, self).__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', formfields.BrCpfField)
        return super(self.__class__, self).formfield(**kwargs)


class BrCnpjField(models.CharField):
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 18)
        super(self.__class__, self).__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', formfields.BrCnpjField)
        return super(self.__class__, self).formfield(**kwargs)


class BrCepField(models.CharField):
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 9)
        #kwargs.setdefault('verbose_name', u'CEP')
        super(self.__class__, self).__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', formfields.BrCepField)
        return super(self.__class__, self).formfield(**kwargs)


class BrTelefoneField(models.CharField):
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 14)
        super(self.__class__, self).__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', formfields.BrTelefoneField)
        return super(self.__class__, self).formfield(**kwargs)


class BrDataField(models.DateField):
    
    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', formfields.BrDataField)
        return super(self.__class__, self).formfield(**kwargs)


class BrDataHoraField(models.DateTimeField):
    
    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', formfields.BrDataHoraField)
        return super(self.__class__, self).formfield(**kwargs)


class BrEstadoBrasileiroField(models.CharField):
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 2)
        kwargs.setdefault('choices', STATE_CHOICES)
        super(self.__class__, self).__init__(*args, **kwargs)

