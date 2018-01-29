# -*- coding: utf-8 -*-

from decimal import Decimal
from django import forms
from django.forms.fields import EMPTY_VALUES
from django.utils.encoding import smart_unicode, force_unicode
from django.utils.translation import ugettext_lazy as _
from djtools.formwidgets import BrDataWidget, BrTelefoneWidget, BRCpfWidget, \
    BrDinheiroWidget, BrDataHoraWidget, BrCnpjWidget, BRDateRangeWidget, \
    BrPlacaVeicularWidget, BrCepWidget, IntegerWidget, AlphaNumericWidget, \
    AlphaNumericUpperCaseWidget, CapitalizeTextWidget, NumEmpenhoWidget, \
    HorasCursosWidget
from djtools.utils import mask_cpf, mask_cnpj, mask_placa, range_float, \
    mask_empenho, mask_horas_cursos
from itertools import izip
import re
from django.template import Template, Context
from django.utils.safestring import mark_safe


class ModelChoiceFieldPlus(forms.ModelChoiceField):
    
    def __init__(self, queryset, empty_label=u"---------", cache_choices=False,
                 required=True, widget=None, label=None, initial=None,
                 help_text=None, to_field_name=None, *args, **kwargs):
        self.label_template = kwargs.pop('label_template')
        super(ModelChoiceFieldPlus, self).__init__(
            queryset, empty_label, cache_choices,
            required, widget, label, initial,
            help_text, to_field_name, *args, **kwargs)
    
    def label_from_instance(self, obj):
        if not self.label_template:
            return super(ModelChoiceFieldPlus, self).label_from_instance(obj)
        t = Template(self.label_template)
        return mark_safe(t.render(Context({'obj': obj })).replace(' ', '&nbsp;'))


class BrDataField(forms.DateField):
    
    default_error_messages = {
        'max_value': _(u'Ensure this value is less than or equal to %s.'),
        'min_value': _(u'Ensure this value is greater than or equal to %s.'),
    }

    widget = BrDataWidget

    def __init__(self, input_formats=None, *args, **kwargs):
        self.min_value = kwargs.pop('min_value', None)
        self.max_value = kwargs.pop('max_value', None)
        super(forms.DateField, self).__init__(*args, **kwargs)
        self.input_formats = ('%d/%m/%Y',)
    
    def clean(self, value):
        value = super(BrDataField, self).clean(value)
        if value in EMPTY_VALUES:
            return None
        if self.max_value is not None and value > self.max_value:
            raise forms.ValidationError(self.error_messages['max_value'] % self.max_value.strftime('%d/%m/%Y'))
        if self.min_value is not None and value < self.min_value:
            raise forms.ValidationError(self.error_messages['min_value'] % self.min_value.strftime('%d/%m/%Y'))
        return value


class BrDataHoraField(forms.DateTimeField):

    widget = BrDataHoraWidget

    def __init__(self, input_formats=None, *args, **kwargs):
        super(forms.DateTimeField, self).__init__(*args, **kwargs)
        self.input_formats = ('%d/%m/%Y %H:%M:%S',)


class BrTelefoneField(forms.Field):
    
    widget = BrTelefoneWidget
    
    def __init__(self, *args, **kwargs):
        kwargs.pop('max_length')
        super(self.__class__, self).__init__(*args, **kwargs)
        self.help_text = kwargs.get('help_text', u'Formato: "(99) 9999-9999"')
    
    default_error_messages = {
        'invalid': u'O número deve estar no formato (XX) XXXX-XXXX.',
    }

    def clean(self, value):
        super(BrTelefoneField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        value = re.sub('(\(|\)|\s+)', '', smart_unicode(value))
        phone_digits_re = re.compile(r'^(\d{2})[-\.]?(\d{4})[-\.]?(\d{4})$')
        m = phone_digits_re.search(value)
        if m:
            return u'(%s) %s-%s' % (m.group(1), m.group(2), m.group(3))
        raise forms.ValidationError(self.error_messages['invalid'])


class BrCepField(forms.RegexField):

    widget = BrCepWidget
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('help_text', u'Formato: "99999-999"')
        kwargs['max_length'] = 9
        super(BrCepField, self).__init__(r'^\d{5}-\d{3}$', *args, **kwargs)
    
    def clean(self, value):
        value = super(BrCepField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        if not re.match('\d\d\d\d\d-\d\d\d', value):
            raise forms.ValidationError(self.error_messages['invalid'])
        return value


def DV_maker(v):
    if v >= 2:
        return 11 - v
    return 0


class BrCpfField(forms.CharField):
    
    default_error_messages = {
        'invalid': _("Invalid CPF number."),
        'max_digits': _("This field requires at most 11 digits or 14 characters."),
        'digits_only': _("This field requires only numbers."),
    }

    widget = BRCpfWidget
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', 'CPF')
        super(self.__class__, self).__init__(*args, **kwargs)
        self.help_text = kwargs.get('help_text', u'Formato: "XXX.XXX.XXX-XX"')
    
    def clean(self, value):
        value = super(BrCpfField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        if len(value) == 11: # formato "99999999999"
            value = mask_cpf(value)
        if len(value) != 14: # formato "999.999.999-99"
            raise forms.ValidationError(self.error_messages['invalid'])
        if not re.match('\d\d\d.\d\d\d.\d\d\d-\d\d', value):
            raise forms.ValidationError(self.error_messages['invalid'])
        orig_value = value[:]
        if not value.isdigit():
            value = re.sub("[-\.]", "", value)
        try:
            int(value)
        except ValueError:
            raise forms.ValidationError(self.error_messages['digits_only'])
        if len(value) != 11:
            raise forms.ValidationError(self.error_messages['max_digits'])
        orig_dv = value[-2:]

        new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(10, 1, -1))])
        new_1dv = DV_maker(new_1dv % 11)
        value = value[:-2] + str(new_1dv) + value[-1]
        new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(11, 1, -1))])
        new_2dv = DV_maker(new_2dv % 11)
        value = value[:-1] + str(new_2dv)
        if value[-2:] != orig_dv:
            raise forms.ValidationError(self.error_messages['invalid'])

        return orig_value


class BrCnpjField(forms.CharField):
    
    default_error_messages = {
        'invalid': _("Invalid CNPJ number."),
        'digits_only': _("This field requires only numbers."),
        'max_digits': _("This field requires at least 14 digits"),
    }
    
    widget = BrCnpjWidget
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', 'CNPJ')
        super(self.__class__, self).__init__(*args, **kwargs)
        self.help_text = kwargs.get('help_text', u'Formato: "XX.XXX.XXX/XXXX-XX"')

#    def clean(self, value):
#        """
#        Value can be either a string in the format XX.XXX.XXX/XXXX-XX or a
#        group of 14 characters.
#        """
#        value = super(BrCnpjField, self).clean(value)
#        if value in EMPTY_VALUES:
#            return u''
#        if len(value) == 14: # formato "XXXXXXXXXXXXXX"
#            value = mask_cnpj(value)
#        if len(value) != 18: # formato "XX.XXX.XXX/XXXX-XX"
#            raise forms.ValidationError(self.error_messages['invalid'])
#        orig_value = value[:]
#        if not value.isdigit():
#            value = re.sub("[-/\.]", "", value)
#        try:
#            int(value)
#        except ValueError:
#            raise forms.ValidationError(self.error_messages['digits_only'])
#        if len(value) != 14:
#            raise forms.ValidationError(self.error_messages['max_digits'])
#        orig_dv = value[-2:]
#
#        new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(5, 1, -1) + range(9, 1, -1))])
#        new_1dv = DV_maker(new_1dv % 11)
#        value = value[:-2] + str(new_1dv) + value[-1]
#        new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(6, 1, -1) + range(9, 1, -1))])
#        new_2dv = DV_maker(new_2dv % 11)
#        value = value[:-1] + str(new_2dv)
#        if value[-2:] != orig_dv:
#            raise forms.ValidationError(self.error_messages['invalid'])
#
#        return orig_value

    def clean(self, value):
        """
        Value can be either a string in the format XX.XXX.XXX/XXXX-XX or a
        group of 14 characters.
        """
        value = super(BrCnpjField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        if len(value) == 14: # formato "XXXXXXXXXXXXXX"
            value = mask_cnpj(value)
        if len(value) != 18: # formato "XX.XXX.XXX/XXXX-XX"
            raise forms.ValidationError(self.error_messages['invalid'])
        if not re.match('\d\d.\d\d\d.\d\d\d/\d\d\d\d-\d\d', value):
            raise forms.ValidationError(self.error_messages['invalid'])
        orig_value = value[:]
#        grupo1 = value.split('-')
#        grupo2 = grupo1.split('/')
#        grupo3 = grupo2.split('.')
#        if not grupo1[1].isdigit():
#            raise forms.ValidationError(self.error_messages['invalid'])
#        if not grupo2[1].isdigit():  
#            raise forms.ValidationError(self.error_messages['invalid'])
#        if not grupo3[1].isdigit():  
#            raise forms.ValidationError(self.error_messages['invalid'])
        if not value.isdigit():
            value = re.sub("[-\./]", "", value)
        try:
            int(value)
        except ValueError:
            raise forms.ValidationError(self.error_messages['digits_only'])
        if len(value) != 14:
            raise forms.ValidationError(self.error_messages['max_digits'])
        orig_dv = value[-2:]

        new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(5, 1, -1) + range(9, 1, -1))])
        new_1dv = DV_maker(new_1dv % 11)
        value = value[:-2] + str(new_1dv) + value[-1]
        new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(6, 1, -1) + range(9, 1, -1))])
        new_2dv = DV_maker(new_2dv % 11)
        value = value[:-1] + str(new_2dv)
        if value[-2:] != orig_dv:
            raise forms.ValidationError(self.error_messages['invalid'])

        return orig_value


class BrDinheiroField(forms.DecimalField):

    widget = BrDinheiroWidget
    
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.help_text = kwargs.get('help_text', u'Formato: "9.999,99"')
    
    def clean(self, value):
        if not self.required and not value:
            return None
        value = value.replace('.', '').replace(',', '.')
        try:
            return Decimal(value)
        except:
            raise forms.ValidationError(self.error_messages['invalid'])
        

#class NumericoField(forms.IntegerField):
#    
#    widget = NumericoWidget
#    
#    def __init__(self, *args, **kwargs):
#        super(self.__class__, self).__init__(*args, **kwargs)
#        self.help_text = kwargs.get('help_text', u'Formato: "1111111"')
#        
#    default_error_messages = {
#        'invalid': u'O campo deve ser preenchido apenas com números',
#    }
#    
#    def clean(self, value):
#        value = super(NumericoField, self).clean(value)
#        if value in EMPTY_VALUES:
#            return u''
#        if value:
#            teste = re.compile(r'[0-9]')
#            for numero in value :
#                if not teste.match(numero):
#                    return False               
##        if not value.isdigit():
##            raise forms.ValidationError(self.error_messages['invalid'])
#        return value

# utilizado para campos de texto com máscara para aceitar apenas inteiros. O campo no banco é texto
class NumericField(forms.CharField):
    
    widget = IntegerWidget
    
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        
    default_error_messages = {
        'invalid': u'O campo deve ser preenchido apenas com números',
    }
    

# utilizado para campos de texto com márcaras de inteiros. O campo no banco é inteiro
class IntegerField(forms.CharField):
    
    widget = IntegerWidget
    
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        
    default_error_messages = {
        'invalid': u'O campo deve ser preenchido apenas com números',
    }
      
    def clean(self, value):
        if not self.required and not value:
            return None
        try:
            return int(value)
        except:
            raise forms.ValidationError(self.error_messages['invalid'])


class AlphaNumericField(forms.CharField):
    
    widget = AlphaNumericWidget
    
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        
    default_error_messages = {
        'invalid': u'O campo pode ser preenchido apenas com números ou letras',
    }
    
    
class AlphaNumericUpperCaseField(forms.CharField):
    
    widget = AlphaNumericUpperCaseWidget
    
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        
    default_error_messages = {
        'invalid': u'O campo pode ser preenchido apenas com números ou letras maiúsculas',
    }
    

class CapitalizeTextField(forms.CharField):
    
    widget = CapitalizeTextWidget
    
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        
    default_error_messages = {
        'invalid': u'O campo pode ser preenchido apenas com números ou letras',
    }

class NumEmpenhoField(forms.CharField):
    
    widget = NumEmpenhoWidget
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', u'Número de empenho')
        super(self.__class__, self).__init__(*args, **kwargs)
        self.help_text = kwargs.get('help_text', u'Formato: "9999NE123456"')
        
    default_error_messages = {
        'invalid': u'O número de empenho deve estar no formato 9999NE123456',
    }
    
    def clean(self, value):
        value = super(NumEmpenhoField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        if len(value) == 10: # formato "9999123456"
            value = mask_empenho(value)
        if len(value) != 12: # formato "9999NE123456"
            raise forms.ValidationError(self.error_messages['invalid'])
        grupos = value.split('NE')
        if not grupos[0].isdigit():
            raise forms.ValidationError(self.error_messages['invalid'])
        if not grupos[1].isdigit():  
            raise forms.ValidationError(self.error_messages['invalid'])
        return grupos[0] + 'NE' + grupos[1]
    
class HorasCursosField(forms.FloatField):
    
    widget = HorasCursosWidget
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', u'Horas')
        super(self.__class__, self).__init__(*args, **kwargs)
        self.help_text = kwargs.get('help_text', u'Formato: "999.9"')
        
    default_error_messages = {
        'invalido' : u'O campo deve estar no formato 999.9'
    }
    
    def clean(self, value):
        if not self.required and not value:
            return None
        try:
            return float(value)
        except:
            raise forms.ValidationError(self.error_messages['invalid'])        


class BrPlacaVeicularField(forms.CharField):
    
    widget = BrPlacaVeicularWidget
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', 'Placa')
        super(self.__class__, self).__init__(*args, **kwargs)
        self.help_text = kwargs.get('help_text', u'Formato: "AAA-1111"')
        
    default_error_messages = {
        'invalid': u'A placa deve estar no formato AAA-1111',
    }
    
    def clean(self, value):
        value = super(BrPlacaVeicularField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        if len(value) == 7: # formato "AAA1111"
            value = mask_placa(value)
            pass
        if len(value) != 8: # formato "AAA-1111"
            raise forms.ValidationError(self.error_messages['invalid'])
        grupos = value.split('-')
        if not grupos[0].isalpha():
            raise forms.ValidationError(self.error_messages['invalid'])
        else:
            letras = grupos[0].upper()
        if not grupos[1].isdigit():  
            raise forms.ValidationError(self.error_messages['invalid'])
        return letras + '-' + grupos[1]


class BRDateRangeField(forms.MultiValueField):

    widget = BRDateRangeWidget

    def __init__(self, fields=(BrDataField, BrDataField), sum_end_date=False, *args, **kwargs):
        super(forms.MultiValueField, self).__init__(*args, **kwargs)
        # Set 'required' to False on the individual fields, because the
        # required validation will be handled by MultiValueField, not by those
        # individual fields.
        for f in fields:
            f.required = False
        self.fields = fields

    def clean(self, value):
        """
        Retorna [(data), (data+1 dia)], pois o formato facilita as pesquisas
        em banco de dados: .filter(date__gt=start_date, date__lt=end_date)
        """
        datefield = BrDataField()
        try:
            start_date, end_date = [datefield.clean(i) for i in value]
        except:
            raise forms.ValidationError(u'A faixa de datas está inválida.')
        if start_date > end_date:
            raise forms.ValidationError(u'A data final é menor que a inicial.')
        return [start_date, end_date]


class RangeFloatField(forms.FloatField):
    
    def __init__(self, max_value=None, min_value=None, *args, **kwargs):
        self.step = kwargs.pop('step')
        self.max_value, self.min_value = max_value, min_value
        
        if self.step:
            choices = range_float(self.min_value, self.max_value + self.step, self.step)
            choices = [unicode(i) for i in choices]
            choices = list(izip(choices, choices))
            self.widget = forms.Select(choices=choices)
        
        forms.Field.__init__(self, *args, **kwargs)
    
    def widget_attrs(self, widget):
        if self.step: # forms.Select widget
            return {}
        else: # forms.TextInput widget
            return {'size': 5}


class SmartModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """
    A classe deixa a mensagem de erro mais amigável: indica o ``unicode(obj)`` 
    em vez de ``obj.pk``.
    """
    
    def clean(self, value):
        if self.required and not value:
            raise forms.ValidationError(self.error_messages['required'])
        elif not self.required and not value:
            return []
        if not isinstance(value, (list, tuple)):
            raise forms.ValidationError(self.error_messages['list'])
        for pk in value:
            try:
                self.queryset.filter(pk=pk)
            except ValueError:
                raise forms.ValidationError(self.error_messages['invalid_pk_value'] % pk)
        qs = self.queryset.filter(pk__in=value)
        pks = set([force_unicode(o.pk) for o in qs])
        for val in value:
            if force_unicode(val) not in pks:
                val = unicode(self.queryset.model._default_manager.get(pk=val))
                raise forms.ValidationError(self.error_messages['invalid_choice'] % val)
        return qs
