# -*- coding: utf-8 -*-

from django.db import models, transaction
from django.contrib import admin
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.forms.formsets import all_valid
from django.contrib.admin import helpers
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.utils.html import escape
from djtools.utils import mask_cep
import urllib
import cgi
import re

# Expressões regulares adaptadas de: 
# http://plasoft.wordpress.com/2007/05/11/validacao-de-cep-por-estado/
estados_re = dict(
    SP = re.compile(r'^([1][0-9]{3}|[01][0-9]{4})[0-9]{3}$'),
    RJ = re.compile(r'^[2][0-8][0-9]{3}[0-9]{3}$'),
    MS = re.compile(r'^[7][9][0-9]{3}[0-9]{3}$'),
    MG = re.compile(r'^[3][0-9]{4}[0-9]{3}$'),
    MT = re.compile(r'^[7][8][8][0-9]{2}[0-9]{3}$'),
    AC = re.compile(r'^[6][9]{2}[0-9]{2}[0-9]{3}$'),
    AL = re.compile(r'^[5][7][0-9]{3}[0-9]{3}$'),
    AM = re.compile(r'^[6][9][0-8][0-9]{2}[0-9]{3}$'),
    AP = re.compile(r'^[6][89][9][0-9]{2}[0-9]{3}$'),
    BA = re.compile(r'^[4][0-8][0-9]{3}[0-9]{3}$'),
    CE = re.compile(r'^[6][0-3][0-9]{3}[0-9]{3}$'),
    DF = re.compile(r'^[7][0-3][0-6][0-9]{2}[0-9]{3}$'),
    ES = re.compile(r'^[2][9][0-9]{3}[0-9]{3}$'),
    GO = re.compile(r'^[7][3-6][7-9][0-9]{2}[0-9]{3}$'),
    MA = re.compile(r'^[6][5][0-9]{3}[0-9]{3}$'),
    PA = re.compile(r'^[6][6-8][0-8][0-9]{2}[0-9]{3}$'),
    PB = re.compile(r'^[5][8][0-9]{3}[0-9]{3}$'),
    PE = re.compile(r'^[5][0-6][0-9]{3}[0-9]{3}$'),
    PI = re.compile(r'^[6][4][0-9]{3}[0-9]{3}$'),
    PR = re.compile(r'^[8][0-7][0-9]{3}[0-9]{3}$'),
    RN = re.compile(r'^[5][9][0-9]{3}[0-9]{3}$'),
    RO = re.compile(r'^[7][8][9][0-9]{2}[0-9]{3}$'),
    RR = re.compile(r'^[6][9][3][0-9]{2}[0-9]{3}$'),
    RS = re.compile(r'^[9][0-9]{4}[0-9]{3}$'),
    SC = re.compile(r'^[8][89][0-9]{3}[0-9]{3}$'),
    SE = re.compile(r'^[4][9][0-9]{3}[0-9]{3}$'),
    TO = re.compile(r'^[7][7][0-9]{3}[0-9]{3}$')
)

def get_sigla_estado_por_cep(cep):
    """
    Recebe o cep e retorna a sigla do estado correspondente.
    """
    cep = re.sub('\D', '', cep)
    for estado, re_exp in estados_re.items():
        if re_exp.match(cep):
            return estado
    raise ValueError('O CEP "%s" está inválido' % cep)

def get_classe_modelo_por_cep(cep):
    """
    Recebe o cep e retorna a classe de modelo correspondente.
    """
    return models.get_model('endereco', get_sigla_estado_por_cep(cep))

def get_endereco_base_local(cep):
    """
    """
    cls = get_classe_modelo_por_cep(cep)
    try:
        return cls.objects.get(cep=cep)
    except cls.DoesNotExist:
        return None

def get_endereco_webservice(cep, salvar_local=True):
    """
    Web Service utilizado: http://www.republicavirtual.com.br/cep/index.php
    """
    cep = re.sub('\D', '', cep)
    cep_mascarado = mask_cep(cep)
    url = "http://cep.republicavirtual.com.br/web_cep.php?cep=" + cep + \
        "&formato=query_string"
    WS_ENCODING = 'latin-1'
    pagina = urllib.urlopen(url)
    conteudo = pagina.read()
    resultado = cgi.parse_qs(conteudo)
    
    # CEP Normal
    if resultado['resultado'][0] == '1':
        # resultado.keys(): ['tipo_logradouro', 'resultado', 'bairro', 'cidade', 
        #                    'logradouro', 'resultado_txt', 'uf']
        resultado.pop('resultado')
        resultado.pop('resultado_txt')
        resultado['tp_logradouro'] = resultado.pop('tipo_logradouro')
        local = dict()
        for key, value in resultado.items():
            local[key] = value[0].decode(WS_ENCODING)
        
        # Caso o CEP não exista localmente, será criado
        cls = get_classe_modelo_por_cep(cep)
        if not cls.objects.filter(cep=cep_mascarado):
            local['cep'] = cep_mascarado
            return cls.objects.create(**local)
        else:
            return cls.objects.get(cep=cep_mascarado)
    
    # CEP Único
    elif resultado['resultado'][0] == '2':
        local = dict(
            cidade=resultado['cidade'][0].decode(WS_ENCODING),
            uf=resultado['uf'][0].decode(WS_ENCODING),
            cep=cep_mascarado,
        )
        
        # Caso o CEP não exista localmente, será criado
        cls = models.get_model('endereco', 'cepunico')
        if not cls.objects.filter(cep=cep_mascarado):
            return cls.objects.create(**local)
        else:
            return cls.objects.get(cep=cep_mascarado)
    
    # CEP Inexistente
    else:
        return None

def get_endereco(cep):
    """
    Função utilizada no formulário de cadastro de endereços.
    Busca na base local e, se não encontrar, no WebService.
    Retorna None se não encontrar em nenhum dos dois.
    """
    cep_local = get_endereco_base_local(cep)
    if cep_local:
        return cep_local
    else:
        cep_ws = get_endereco_webservice(cep)
        if cep_ws:
            return cep_ws
        else:
            return None


###############
# EnderecoAdmin
###############

def get_endereco_form(obj=None, data=None, obrigar_ter_endereco=False):
    from endereco.forms import EnderecoAdminInlineForm
    if data:
        # Formulário submetido
        if obj:
            data = data.copy() # tornando ``data`` mutável
            data['objeto_content_type'] = ContentType.objects.get_for_model(obj.__class__).pk
            data['objeto_pk'] = obj.pk
        form = EnderecoAdminInlineForm(data)
    else:
        # Formulário limpo
        form = EnderecoAdminInlineForm()
        if obj:
            obj_content_type = ContentType.objects.get_for_model(obj.__class__)
            form.initial = {'objeto_content_type': obj_content_type.pk, 
                            'objeto_pk': obj.pk}
    if obrigar_ter_endereco:
        if obj:
            Endereco = models.get_model('endereco', 'Endereco')
            if Endereco.get_lista_por_objeto(obj):
                form.fields['cep'].required = False
            else:
                form.fields['cep'].required = True
        else:
            form.fields['cep'].required = True
    return form


class ObjetoComEnderecoAdmin(admin.ModelAdmin):
    
    change_form_template = 'endereco/templates/add_endereco.html'
    obrigar_ter_endereco = False
    
    def render_change_form(self, request, context, add=False, change=False, 
                           form_url='', obj=None):
        Endereco = models.get_model('endereco', 'endereco')
        if 'form_endereco' not in context:
            form_endereco = get_endereco_form(
                obj=obj, obrigar_ter_endereco=self.obrigar_ter_endereco)
            context['form_endereco'] = form_endereco
        if obj:
            context['enderecos'] = Endereco.get_lista_por_objeto(obj)
        context['show_delete'] = True
        return super(ObjetoComEnderecoAdmin, self).render_change_form(
            request, context, add=False, change=False, form_url='', obj=None)
    
    def add_view(self, request, form_url='', extra_context=None):
        model = self.model
        opts = model._meta

        if not self.has_add_permission(request):
            raise PermissionDenied

        ModelForm = self.get_form(request)
        formsets = []
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES)
            form_endereco = get_endereco_form(None, request.POST, 
                                              self.obrigar_ter_endereco)
            extra_context = {'form_endereco': form_endereco}
            if form.is_valid() and form_endereco.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=False)
            else:
                form_validated = False
                new_object = self.model()
            for FormSet in self.get_formsets(request):
                formset = FormSet(data=request.POST, files=request.FILES,
                                  instance=new_object,
                                  save_as_new=request.POST.has_key("_saveasnew"))
                formsets.append(formset)
            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, change=False)
                form.save_m2m()
                for formset in formsets:
                    self.save_formset(request, form, formset, change=False)
                
                self.log_addition(request, new_object)
                # Salvando o endereço
                form_endereco = get_endereco_form(new_object, request.POST, 
                                                  self.obrigar_ter_endereco)
                form_endereco.save()
                # Fim de 'Salvando o endereco'
                return self.response_add(request, new_object)
        else:
            # Prepare the dict of initial data from the request.
            # We have to special-case M2Ms as a list of comma-separated PKs.
            initial = dict(request.GET.items())
            for k in initial:
                try:
                    f = opts.get_field(k)
                except models.FieldDoesNotExist:
                    continue
                if isinstance(f, models.ManyToManyField):
                    initial[k] = initial[k].split(",")
            form = ModelForm(initial=initial)
            for FormSet in self.get_formsets(request):
                formset = FormSet(instance=self.model())
                formsets.append(formset)

        adminForm = helpers.AdminForm(form, list(self.get_fieldsets(request)), self.prepopulated_fields)
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(self.inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset, fieldsets)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media

        context = {
            'title': _('Add %s') % force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'is_popup': request.REQUEST.has_key('_popup'),
            'show_delete': False,
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, add=True)
    add_view = transaction.commit_on_success(add_view)

    def change_view(self, request, object_id, extra_context=None):
        "The 'change' admin view for this model."
        model = self.model
        opts = model._meta

        try:
            obj = model._default_manager.get(pk=object_id)
        except model.DoesNotExist:
            # Don't raise Http404 just yet, because we haven't checked
            # permissions yet. We don't want an unauthenticated user to be able
            # to determine whether a given object exists.
            obj = None

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') \
                          % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})

        if request.method == 'POST' and request.POST.has_key("_saveasnew"):
            return self.add_view(request, form_url='../../add/')

        ModelForm = self.get_form(request, obj)
        formsets = []
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=True)
            else:
                form_validated = False
                new_object = obj
            for FormSet in self.get_formsets(request, new_object):
                formset = FormSet(request.POST, request.FILES,
                                  instance=new_object)
                formsets.append(formset)

            if all_valid(formsets) and form_validated:
                form_endereco = get_endereco_form(new_object, request.POST,
                                                  self.obrigar_ter_endereco)
                if form_endereco.is_valid():
                    self.save_model(request, new_object, form, change=True)
                    form.save_m2m()
                    for formset in formsets:
                        self.save_formset(request, form, formset, change=True)
                    
                    change_message = self.construct_change_message(request, form, formsets)
                    self.log_change(request, new_object, change_message)
                    if form_endereco.cleaned_data['cep']:
                        form_endereco.save()
                    return self.response_change(request, new_object)
                else:
                    extra_context = dict(form_endereco=form_endereco)
                
        else:
            form = ModelForm(instance=obj)
            for FormSet in self.get_formsets(request, obj):
                formset = FormSet(instance=obj)
                formsets.append(formset)

        adminForm = helpers.AdminForm(form, self.get_fieldsets(request, obj), self.prepopulated_fields)
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(self.inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request, obj))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset, fieldsets)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media
        
        context = {
            'title': _('Change %s') % force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'object_id': object_id,
            'original': obj,
            'is_popup': request.REQUEST.has_key('_popup'),
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, change=True, obj=obj)
    change_view = transaction.commit_on_success(change_view)
