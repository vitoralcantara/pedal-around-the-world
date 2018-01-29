# -*- coding: utf-8 -*-

from datetime import date, datetime
from decimal import Decimal
from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group, Permission
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, TemplateDoesNotExist
from django.utils import simplejson
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe
from djtools.templatetags.djtools_templatetags import in_group
from operator import or_
from random import choice
from unicodedata import normalize
import csv
import os
import re


class BrModelAdmin(admin.ModelAdmin):
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        # TODO: automatizar esta função
        
        from djtools.dbfields import BrCpfField, BrCepField, BrTelefoneField, BrDinheiroField
        from djtools.formwidgets import BrDataWidget, BRCpfWidget, BrCepWidget, BrTelefoneWidget, BrDinheiroWidget
        
        if isinstance(db_field, models.DateField): # DateField
            kwargs['widget'] = BrDataWidget
            return db_field.formfield(**kwargs)
        if isinstance(db_field, BrCpfField): # CPF

            kwargs['widget'] = BRCpfWidget
            return db_field.formfield(**kwargs)
        if isinstance(db_field, BrCepField): # CEP

            kwargs['widget'] = BrCepWidget
            return db_field.formfield(**kwargs)
        if isinstance(db_field, BrTelefoneField): # CEP
            kwargs['widget'] = BrTelefoneWidget
            return db_field.formfield(**kwargs)
        if isinstance(db_field, BrDinheiroField): # BrDinheiroField
            kwargs['widget'] = BrDinheiroWidget
            return db_field.formfield(**kwargs)
        return super(BrModelAdmin, self).formfield_for_dbfield(db_field, **kwargs)

class BrTabularInline(admin.TabularInline):

    def formfield_for_dbfield(self, db_field, **kwargs):
        # TODO: automatizar esta função
        
        from djtools.dbfields import BrCpfField, BrCepField, BrTelefoneField, BrDinheiroField
        from djtools.formwidgets import BrDataWidget, BRCpfWidget, BrCepWidget, BrTelefoneWidget, BrDinheiroWidget
        
        if isinstance(db_field, models.DateField): # DateField
            kwargs['widget'] = BrDataWidget
            return db_field.formfield(**kwargs)
        if isinstance(db_field, BrCpfField): # CPF

            kwargs['widget'] = BRCpfWidget
            return db_field.formfield(**kwargs)
        if isinstance(db_field, BrCepField): # CEP

            kwargs['widget'] = BrCepWidget
            return db_field.formfield(**kwargs)
        if isinstance(db_field, BrTelefoneField): # CEP
            kwargs['widget'] = BrTelefoneWidget
            return db_field.formfield(**kwargs)
        if isinstance(db_field, BrDinheiroField): # BrDinheiroField
            kwargs['widget'] = BrDinheiroWidget
            return db_field.formfield(**kwargs)
        return super(BrTabularInline, self).formfield_for_dbfield(db_field, **kwargs)

class DjangoUtilsAdmin(admin.ModelAdmin):
    
    def queryset(self, request):
        """
        Converts the search param to ascii to make searches.
        """
        if 'q' in request.GET:
            request.GET._mutable = True
            request.GET['q'] = to_ascii(request.GET['q'])
        return admin.ModelAdmin.queryset(self, request)


class JsonResponse(HttpResponse):
    def __init__(self, data):
        content=simplejson.dumps(data)
        HttpResponse.__init__(self, content=content,
                              mimetype='application/json')

class PdfResponse(HttpResponse):
    
    def __init__(self, content, name=u'relatorio', attachment=True):
        HttpResponse.__init__(self, content, mimetype='application/pdf')
        if attachment:
            self['Content-Disposition'] = 'attachment; filename="%s.pdf"' \
                % name.encode('utf-8')

def human_str(val, encoding='utf-8', blank=u''):
    """
    Retorna uma representação humana para o objeto.
    
    human_basestring(True) -> 'Sim'
    human_basestring(False) -> 'Não'
    human_basestring(User.objects.get(id=1)) -> 'admin'
    human_basestring(None) -> ''
    human_basestring(None, blank=u'-') -> '-'
    """
    if val is None:
        val = blank
    elif not isinstance(val, basestring):
        if isinstance(val, bool):
            val = val and u'Sim' or u'Não'
        else:
            val = unicode(val)
    return val.encode(encoding)

def CsvResponse(rows, name=u'report', attachment=True, encoding='utf-8', value_for_none=u'-'):
    """
    Retorna uma resposta no formato csv. ``rows`` deve ser lista de listas cujos 
    valores serão convertidos com ``human_str``.
    """
    if not isinstance(rows, list) or \
        (len(rows) and not isinstance(rows[0], list)):
        raise ValueError('``rows`` must be a list of lists')
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' \
        % name.encode('utf-8')
    writer = csv.writer(response)
    for row in rows:
        row = [human_str(i, encoding=encoding, blank=u'-') for i in row]
        writer.writerow(row)
    return response

def get_tl():
    """
    Retorna threadlocals.
    """
    tl = None
    exec 'from %s.djtools.middleware import threadlocals as tl' % settings.PROJECT_NAME
    return tl

def autocomplete_view(request, app_name, class_name):
    """
    Gereric autocomplete view
    =========================
    `request.GET` expected args: 'q', 'manager_name', 'force_generic_seacrh'
    """
    SEARCH_FUNCTION_NAME = 'buscar'
    cls = models.get_model(app_name, class_name)
    if cls is None:
        raise Exception(u'Invalid Class')
    if 'pk' in request.GET:
        # Retorna apenas a representação unicode do objeto. É utilizado na 
        # escolha do objeto via change_list do admin.
        return HttpResponse(unicode(cls.objects.get(pk=request.GET['pk'])))
    if 'force_generic_search' not in request.GET and \
            hasattr(cls, SEARCH_FUNCTION_NAME):
        args = dict(autocomplete=True)
        for key, value in request.GET.items():
            args[str(key)] = value
        return HttpResponse(cls.buscar(**args))
    else:
        args = dict(
            autocomplete_format = True,
            q                   = request.GET.get('q', ''),
            manager_name        = request.GET.get('manager_name', None),
            label_value         = request.GET.get('label_value', None)
        )
        return HttpResponse(generic_search(cls, **args))

def generic_search(cls, q, autocomplete_format=True, manager_name=None,
                   label_value=None):
    """
    Generic search for `cls` class with manager `manager_name`
    ==========================================================
    Every charfield/textfield or the one SearchField will be in search params
    """
    def get_queryset(cls, manager_name=None): 
        if not manager_name:
            return cls.objects
        else:
            return getattr(cls, manager_name)
        
    def construct_search(field_name):
        return "%s__icontains" % field_name
    
    def get_search_fields(cls):
        search_fields = []
        for f in cls._meta.fields:
            if f.__class__.__name__ == 'SearchField':
                return [f.name]
            if f.get_internal_type() in ['CharField', 'TextField']:
                search_fields.append(f.name)
        if not search_fields:
            raise Exception(u'Class %s don\'t have CharField or TextField.' \
                % cls.__name__)
        return search_fields
    
    or_queries = [models.Q(**{construct_search(field_name): q}) \
                  for field_name in get_search_fields(cls)]
    objs = get_queryset(cls, manager_name).filter(reduce(or_, or_queries))
    
    label_value = label_value or '__unicode__'
    if autocomplete_format:
        out = []
        for obj in objs:
            label = eval_attr(obj, label_value).strip()
            out.append('%s|%s\n' % (label.replace('|', '/'), obj.pk))
        return ''.join(out)
    else:
        return objs

def get_search_field(model_class):
    for f in model_class._meta.fields:
        if f.__class__.__name__ == 'SearchField':
            return f

def to_ascii(txt, codif='utf-8'):
    if not isinstance(txt, basestring):
        txt = unicode(txt)
    if isinstance(txt, unicode):
        txt = txt.encode('utf-8')
    return normalize('NFKD', txt.decode(codif)).encode('ASCII', 'ignore')

def get_app_name(function):
    """Receives a function and returns the app name"""
    function_path = function.__module__.split('.')
    if len(function_path) == 2: # function is on the project
        return function_path[0]
    else: # function is on the app
        return function_path[1]

def get_template_path(function):
    """Returns the default template based on function"""
    app_name = get_app_name(function)
    if app_name == settings.PROJECT_NAME:
        return 'templates/%s.html' %(function.__name__)
    else:
        return '%s/templates/%s.html' %(app_name, function.__name__)

def rtr(template=None):
    """
    Deve ser usado como decorador de função.
    """
    def receive_function(function):
        def receive_function_args(request, *args, **kwargs):
            f_return = function(request, *args, **kwargs)
            if isinstance(f_return, HttpResponse):
                return f_return
            return render(template or get_template_path(function), f_return)
        return receive_function_args
    return receive_function

def render(template_name, ctx=None):
    """
    É o substituto do ``render_to_response``, só que já inclui as informações
    do RequestContext no contexto.
    """
    DEFAULT_TEMPLATE = 'djtools/templates/default.html'
    ctx = ctx or dict()
    try:
        return render_to_response(template_name, ctx, 
            context_instance=RequestContext(get_tl().get_request()))
    except TemplateDoesNotExist:
        return render_to_response(DEFAULT_TEMPLATE, ctx, 
            context_instance=RequestContext(get_tl().get_request()))

def httprr(url, message=''):
    """
    É um ``HttpResponseRedirect`` com a possibilidade de passar uma mensagem.
    """
    if url == '.':
        url = get_tl().get_request().path
    if message:
        # FIXME: AttributeError: 'AnonymousUser' object has no attribute 'message_set'
        get_tl().get_user().message_set.create(message=message)
    return HttpResponseRedirect(url)

def not_permitted(template=None, title=None, msg=None):
    template = template or 'djtools/templates/default.html'
    title = title or u'Ação não permitida'
    msg = msg or u'A ação desejada não pode ser feita.'
    return render(template, dict(h1=title, content=msg))

def sync_groups_and_permissions(data):
    """
    Syncronize groups and permissions.
    
    ``data`` format:
    {'<group_name>': ['<ct_app_label>.<ct_model>.<p_codename>']}
    
    Example of ``data``:
    {'operators': [
        'blog.article.add_article', ''blog.article.change_article'],
     'admins': 
        ['blog.article.add_article', 'blog.article.change_article', 'blog.article.delete_article']
    }
    """
    def get_perm(p):
        """
        ``p`` format: '<ct_app_label>.<ct_model>.<p_codename>'
        """
        try:
            ct_app_label, ct_model, p_codename = p.split('.')
        except ValueError:
            raise ValueError(u'Value must be in format "<ct_app_label>.<ct_model>.<p_codename>". Got "%s"' % p)
        try:
            return Permission.objects.get(content_type__app_label = ct_app_label,
                                          content_type__model     = ct_model,
                                          codename                = p_codename)
        except Permission.DoesNotExist:
            raise Permission.DoesNotExist(u'Permission "%s" does not exist. ' \
                u'You can try "./manage.py syncdb" to fix this.' % p)
    
    for group_name, perms in data.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if not created:
            group.permissions.clear()
        for p in perms:
            group.permissions.add(get_perm(p))

def client_is_server(request=None):
    request = request or get_tl().get_request()
    ip = request.META['REMOTE_ADDR'].split(':')[0]
    if ip in ['localhost', '127.0.0.1']:
        return True
    return False

def user_has_profile(user=None):
    user = user or get_tl().get_user()
    if user is None:
        raise ValueError('User is ``None``')
    try:
        user.get_profile()
        return True
    except:
        return False

def group_required(group, login_url=None):
    """
    Must be used as decorator.
    See ``djtools.templatetags.template_utils.in_group``.
    """
    return user_passes_test(lambda u: in_group(u, group), login_url=login_url)
    
###############################
# django.contrib.auth helpers #
###############################

def has_add_permission(model_cls, user=None):
    user = user or get_tl().get_user()
    opts = model_cls._meta
    return user.has_perm(opts.app_label + '.' + opts.get_add_permission())

def has_change_permission(model_cls, user=None):
    user = user or get_tl().get_user()
    opts = model_cls._meta
    return user.has_perm(opts.app_label + '.' + opts.get_change_permission())

def get_admin_model_url(model_cls, sufix=None):
    """
    Returns admin list or add link to ``model_cls``.
    """
    assert sufix in [None, 'add']
    base_url = u'/admin/%(app)s/%(model)s/'
    if sufix:
        base_url += sufix + u'/'
    params = dict(app=model_cls._meta.app_label, model=model_cls._meta.module_name)
    return base_url % params

def get_admin_object_url(obj):
    """
    Returns admin edit link for ``obj``.
    """
    base_url = get_admin_model_url(obj.__class__)
    return base_url + str(obj.pk) + '/'

def has_related_objects(obj):
    for rel_obj in obj._meta.get_all_related_objects():
        if obj.__getattribute__(rel_obj.get_accessor_name()).select_related().count():
            return True
    return False

def get_related_objects(obj):
    related_objects = []
    acessor_names = [r.get_accessor_name() for r in obj._meta.get_all_related_objects()]
    for acessor_name in acessor_names:
        related_objects += getattr(obj, acessor_name).all()
    return related_objects

def form_to_fieldset(form, fieldsets):
    out = []
    if form.errors:
        out.append('<p class="errornote">Por favor, corrija os erros abaixo.</p><br/>')
    
    for fieldset in fieldsets:
        fieldset_label = fieldset[0]
        field_rows = fieldset[1]['fields']
    
        out.append('<fieldset><legend>%s</legend>' % (fieldset_label))
    
        for row in field_rows:
            
            label_area = None
            if isinstance(row, dict):
                label_area = row.keys()[0]
                row = row.values()[0]
            
            out.append('<div class="form-row">')
            
            if label_area:
                out.append('<div class="form-section">%s</div>' % label_area)
            
            for key in row:
                
                field = form.fields[key]
                value = form.data.get(key, form.initial.get(key, ''))
                
                if isinstance(field.widget, forms.HiddenInput):
                    out.append(field.widget.render(key, value, attrs={'id': key}))
                    continue
                
                label = '<label class="%s" for="%s">%s</label>' % \
                    (field.required and 'required' or '', key, field.label)
                
                input_ = field.widget.render(key, value, attrs={'id': key})
                out.append('<div class="field %s">' %(key != row[0] and 'not-first' or ''))
                
                # label
                out.append('<div class="label">')
                out.append(label)
                out.append('</div>')
                
                # input
                out.append('<div class="input">')
                
                if key in form.errors:
                    out.append('<div class="errorlist">')
                    for error in form.errors[key]:
                        out.append('<li>%s</li>' % unicode(error))
                    out.append('</div>')
                out.append(input_)
                out.append('<div class="help_text">')
                out.append(field.help_text)
                out.append('</div>')
                out.append('</div>') # div.input
                
                out.append('</div>')
            
            out.append('</div>') # div.form-row
            
        out.append('</fieldset>')
        
    return ''.join(out)

def set_initial_for_fields(FormClass, initials):
    for key, value in initials.items():
        FormClass.base_fields[key].initial = value

class OverwriteStorage(FileSystemStorage):
    
    def get_available_name(self, name):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(self.path(name))
        return name

def get_field_by_name(form_class, field_name):
    for field in form_class._meta.fields:
        if field.name == field_name:
            return field

def get_model_object(app_label, model_name, object_pk):
    """Useful for avoid imports from another apps"""
    return models.get_model(app_label, model_name)._base_manager.get(pk=object_pk)

def get_profile_model():
    """Returns the profile model based on AUTH_PROFILE_MODULE"""
    if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
        raise ValueError('settings.AUTH_PROFILE_MODULE does not exist')
    try:
        app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
        return models.get_model(app_label, model_name)
    except:
        raise ValueError('settings.AUTH_PROFILE_MODULE is invalid')

def get_profile(username):
    """Returns the profile instance based on AUTH_PROFILE_MODULE setting."""
    return get_profile_model().objects.get(username=username)

def get_or_create_user_link(profile):
    if profile.user:
        return u'<a href="%s">%s</a>' % (get_admin_object_url(profile.user), profile.user)
    elif profile.username:
        return u'<a href="/djtools/create_user/%s/">Criar Usuário "%s"</a>' \
            % (profile.pk, profile.username)
    else:
        return u'("username" não definido)'


####################
# Non-Django Utils
####################

def eval_attr(obj, attr):
    """
    eval_attr(<Person Túlio>, 'city.country.name') --> 'Brazil'
    """
    path = attr.split('.')
    current_val = obj
    for node in path:
        current_val = getattr(current_val, node)
        if callable(current_val):
            current_val = current_val.__call__()
    return current_val

def randomic(size=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
    """Returns a randomic string."""
    return ''.join([choice(allowed_chars) for i in range(size)])

def get_duplicated_values(l):
    duplicated_values = dict()
    for i in set(l):
        qtd = l.count(i)
        if qtd > 1:
            duplicated_values[i] = qtd
    return duplicated_values 

def br_title(value, strip=True):
    value_list = []
    pattern = r'\b(d?[a|e|i|o]s?|por|com)\b'
    if strip:
        value = value.strip()
    for word in value.lower().split():
        if not re.match(pattern, word):
            word = word.title()
        value_list.append(word)
    return ' '.join(value_list)

def diff_dicts(old, new, include_orfan_keys=True, compare_as_string=False):
    """
    Returns a diff dict in format:
        {'modified_key': [u'old_value', u'new_value']}
    -----
    ``old``: old object or dict
    ``new``: new object or dict
    ``include_orfan_keys``: include keys that exists in old but doesn't exists in new
    ``compare_as_string``:  convert to string before comparing values
    """
    if not isinstance(old, dict):
        old = old.__dict__
    if not isinstance(new, dict):
        new = new.__dict__
    diff = dict()
    for key in old.keys():
        if (not include_orfan_keys) and (key not in new):
            continue
        val1, val2 = old[key], new[key]
        cmp1, cmp2 = val1, val2
        if compare_as_string:
            if not isinstance(val1, basestring):
                cmp1 = str(val1)
            if not isinstance(val2, basestring):
                cmp2 = str(val2)
        if cmp1 != cmp2:
            diff[key] = [val1, val2]
    return diff

def dict_from_keys_n_values(keys, values):
    assert len(keys) == len(values)
    data = dict()
    for i in range(len(keys)):
        data[keys[i]] = values[i]
    return data

def str_to_dateBR(value, force_4_digits_year=True):
    """
    '01/01/2000' -> date(2000, 1, 1)
    """
    date_list = value.split('/')
    if len(date_list) != 3:
        raise ValueError(u'Data inválida.')
    if force_4_digits_year and len(date_list[2]) != 4:
        raise ValueError(u'O ano deve ter 4 dígitos.')
    date_list = [int(i) for i in date_list]
    date_list.reverse()
    return date(*date_list)

def str_money_to_decimal(value):
    """
    '1.010,10' -> Decimal('1010.00')
    """
    value_float = float(value.replace('.', '').replace(',', '.'))
    return Decimal(str(value_float))

def split_thousands(value, sep='.'):
    """
    split_thousands('1000000000') -> '1.000.000.000'
    """
    if not isinstance(value, basestring):
        value = str(value)
    if len(value) <= 3:
        return value
    return split_thousands(value[:-3], sep) + sep + value[-3:]

def mask_money(value):
    """
    mask_money(1) -> '1,00'
    mask_money(1000) -> '1.000,00'
    mask_money(1000.99) -> '1.000,99'
    """
    value = str(value)
    if '.' in value:
        reais, centavos = value.split('.')
    else:
        reais = value
        centavos = '00'
    reais = split_thousands(reais)
    return reais + ',' + centavos

def cpf_valido(value):
    from djtools.formfields import BrCpfField
    cpf_field = BrCpfField()
    try:
        cpf_field.clean(value)
        return True
    except ValidationError:
        return False

def mask_cpf(value):
    """
    '00000000000' -> '000.000.000-00'
    """
    value = mask_numbers(value)
    return value[:3] + '.' + value[3:6] + '.' + value[6:9] + '-' + value[9:11]

def mask_cnpj(value):
    """
    'XXXXXXXXXXXXXX' -> 'XX.XXX.XXX/XXXX-XX'
    """
    value = mask_numbers(value)
    return value[:2] + '.' + value[2:5] + '.' + value[5:8] + '/' + value[8:12] + \
        '-' + value[12:14]

def mask_cep(value):
    """
    '99999999' -> '99999-999'
    """
    value = mask_numbers(value)
    return value[:5] + '-' + value[5:]

def mask_numbers(value):
    """
    '012abc345def' -> '012345'
    """
    return re.sub('\D', '', str(value))

def mask_placa(value):
    """
    'AAA1111' -> 'AAA-1111'
    """
    value = str(value)
    return value[:3] + '-' + value[3:]

def mask_horas_cursos(value):
    """
    '1111' -> '111.1'
    """
    value = str(value)
    return value 


def mask_empenho(value):
    """
    '1234123456' -> '1234NE123456'
    """
    value = str(value)
    return value[:4] + 'NE' + value[4:]

def lists_to_csv(lists, as_response=False, filename='report.csv'):
    """
    lists: list of lists

    The reader is hard-coded to recognise either '\r' or '\n' as end-of-line, 
    and ignores lineterminator. This behavior may change in the future.
    """
    if as_response:
        target = HttpResponse(mimetype='text/csv')
        target['Content-Disposition'] = 'attachment; filename=%s' % filename
    else:
        target = open(filename, 'w')
    
    new_lists = []
    for row in lists:
        new_row = [smart_str(i).replace('\n', '').replace('\r', '') for i in row]
        new_lists.append(new_row)
    
    writer = csv.writer(target)
    writer.writerows(new_lists)
    if as_response:
        return target
    else:
        target.close()

def range_float(start, stop, step):
    """
    Provides a range for float values; builtin ``range`` only supports int values.
    ----------
    >>> range_float(0, 2.5, 0.5)
    >>> [0, 0.5, 1.0, 1.5, 2.0]
    """
    if step == 0:
        raise ValueError('Step must not be 0')
    if start < stop and step < 0:
        raise ValueError('Step must positive for start %s and step %s' % (start, stop))
    if start > stop and step > 0:
        raise ValueError('Step must negative for start %s and step %s' % (start, stop))
    l = [start]
    current = start + step
    while current < stop:
        l.append(current)
        current += step
    return l

def date2datetime(date_):
    return datetime(date_.year, date_.month, date_.day)

def get_age(begin, end=None):
    # adapted from 
    # http://stackoverflow.com/questions/765797/python-timedelta-in-years
    def yearsago(years, from_date=None):
        if from_date is None:
            from_date = datetime.now()
        try:
            return from_date.replace(year=from_date.year - years)
        except:
            # Must be 2/29!
            assert from_date.month == 2 and from_date.day == 29 # can be removed
            return from_date.replace(month=2, day=28,
                                     year=from_date.year-years)
    
    if isinstance(begin, date):
        begin = date2datetime(begin)
    if end is None:
        end = datetime.now()
    num_years = int((end - begin).days / 365.25)
    if begin > yearsago(num_years, end):
        return num_years - 1
    else:
        return num_years


###########################################################################
# ReadOnlyForm (Adaptado de http://www.djangosnippets.org/snippets/1340/) #
###########################################################################

class SpanWidget(forms.Widget):
    """
    Renders a value wrapped in a <span> tag.

    Requires use of specific form support. (see ReadonlyForm 
    or ReadonlyModelForm)
    """

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(u'<span%s >%s</span>' % (
            forms.util.flatatt(final_attrs), self.original_value))

    def value_from_datadict(self, data, files, name):
        return self.original_value

class SpanField(forms.Field):
    """
    A field which renders a value wrapped in a <span> tag.

    Requires use of specific form support. (see ReadonlyForm 
    or ReadonlyModelForm)
    """

    def __init__(self, *args, **kwargs):
        kwargs['widget'] = kwargs.get('widget', SpanWidget)
        super(SpanField, self).__init__(*args, **kwargs)

class Readonly(object):
    """
    Base class for ReadonlyForm and ReadonlyModelForm

    Use example:
        class MyForm(ReadonlyModelForm):
            _readonly = ('foo',)
    """
    def __init__(self, *args, **kwargs):
        super(Readonly, self).__init__(*args, **kwargs)
        readonly_fieldnames = getattr(self, '_readonly', None)
        if not readonly_fieldnames:
            return
        for name, field in self.fields.items():
            if name in readonly_fieldnames:
                field.widget = SpanWidget()
            elif not isinstance(field, SpanField):
                continue
            field.widget.original_value = unicode(getattr(self.instance, name))

class ReadonlyForm(Readonly, forms.Form):
    pass

class ReadonlyModelForm(Readonly, forms.ModelForm):
    pass
