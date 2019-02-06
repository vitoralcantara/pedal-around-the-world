# -*- coding: utf-8 -*-

from decimal import Decimal
from django import forms
from django.conf import settings
from django.forms import widgets
from django.forms.util import flatatt
from django.template.loader import render_to_string
from django.utils import simplejson
from django.utils.datastructures import MultiValueDict
from django.utils.safestring import mark_safe
from djtools.utils import randomic, has_change_permission, has_add_permission, \
    mask_cpf, mask_money, mask_placa, mask_cnpj, mask_empenho, mask_horas_cursos
from sre_parse import isdigit
import re

# TODO: gerar id's para os widgets (funcionar com label for)
# TODO: pegar max_length do models
# TODO: melhorar visualizacao do field required

# This code avoid conflicts by duplicate jquery import
if getattr(settings, 'DJTOOLS_JQUERY_IN_SUPER_TEMPLATE', False):
    BASE_JS_MEDIA = ()
else:
    BASE_JS_MEDIA = (settings.DJTOOLS_MEDIA_URL + 'js/jquery.js',)


class Masked:
    class Media:
        js = BASE_JS_MEDIA + (
            settings.DJTOOLS_MEDIA_URL + 'js/jquery.maskedinput.js',
            settings.DJTOOLS_MEDIA_URL + 'js/widgets-core.js',
        )

class MaskedInput(forms.TextInput, Masked):
    pass


class BrDataWidget(forms.DateTimeInput, Masked):
    """
    Define o ``format`` e aplica a máscara javascript a partir da classe.
    """
    format = '%d/%m/%Y'
    
    def __init__(self, attrs=None, format=None, show_label=True):
        attrs = attrs or {}
        if show_label:
            attrs.update({'class': 'br-data-widget', 'size': '10', 'maxlength': '10'})
        else:
            attrs.update({'class': 'br-data-widget labeless', 'size': '10', 'maxlength': '10'})
        super(forms.DateTimeInput, self).__init__(attrs)
        if format:
            self.format = format


class TimeWidget(forms.TimeInput, Masked):
    """
    Aplica a máscara javascript a partir da classe.
    """
    def __init__(self, attrs=None, format=None):
        attrs = attrs or {}
        attrs.update({'class': 'time-widget', 'size': '8', 'maxlength': '8'})
        super(forms.TimeInput, self).__init__(attrs)
        if format:
            self.format = format


class BrDataHoraWidget(forms.DateTimeInput, Masked):
    """
    Define o ``format`` e aplica a máscara javascript a partir da classe.
    """
    format = '%d/%m/%Y %H:%M:%S'

    def __init__(self, attrs=None, format=None, show_label=True):
        attrs = attrs or {}
        if show_label:
            attrs.update({'class': 'br-datahora-widget', 'size': '19', 'maxlength': '19'})
        else:
            attrs.update({'class': 'br-datahora-widget labeless', 'size': '19', 'maxlength': '19'})
        super(forms.DateTimeInput, self).__init__(attrs)
        if format:
            self.format = format


class BrTelefoneWidget(MaskedInput):
    
    def __init__(self, attrs={}):
        attrs.update({'class': 'br-phone-number-widget', 'size': '14', 'maxlength': '14'})
        super(BrTelefoneWidget, self).__init__(attrs=attrs)


class BRCpfWidget(MaskedInput):
    
    def __init__(self, attrs={}):
        attrs.update({'class': 'br-cpf-widget', 'size': '14', 'maxlength': '14'})
        super(self.__class__, self).__init__(attrs=attrs)
    
    def render(self, name, value, attrs=None):
        if value and value.isdigit() and len(value) == 11:
            value = mask_cpf(value)
        return super(self.__class__, self).render(name, value, attrs=attrs)


class BrCnpjWidget(MaskedInput):
    
    def __init__(self, attrs={}):
        attrs.update({'class': 'br-cnpj-widget', 'size': '18', 'maxlength': '18'})
        super(self.__class__, self).__init__(attrs=attrs)
    
    def render(self, name, value, attrs=None):
        if value and value.isdigit() and len(value) == 14:
            value = mask_cnpj(value)
        return super(self.__class__, self).render(name, value, attrs=attrs)


class BrDinheiroWidget(MaskedInput):

    def __init__(self, attrs={}):
        attrs.update({'class': 'br-dinheiro-widget', 'size': '15', 'maxlength': '15'})
        super(BrDinheiroWidget, self).__init__(attrs=attrs)
    
    def _format_value(self, value):
        if value is None:
            value = u''
        expected_types = (basestring, Decimal)
        if not isinstance(value, expected_types):
            raise ValueError('Value type must be in %s' % expected_types)
        if isinstance(value, basestring) and (value == u'' or ',' in value):
            # value is blank or already formatted
            return value
        else:
            return mask_money(value)
    
    def render(self, name, value, attrs=None):
        value = self._format_value(value)
        return super(BrDinheiroWidget, self).render(name, value, attrs=attrs)
    

class BRDateRangeWidget(forms.MultiWidget):

    def __init__(self, widgets=[BrDataWidget, BrDataWidget], attrs={}):
        super(self.__class__, self).__init__(widgets, attrs)

    def decompress(self, value):
        if not value:
            return ['', '']
        return value

    def render(self, name, value, attrs=None):
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i)) 
            output.append(widget.render(name + '_%s' % i, widget_value, final_attrs))
            if i == 0:
                output.append(u'<span style="padding: 0px 10px 0px 4px">até</span>')
        return mark_safe(self.format_output(output))


class NumEmpenhoWidget(MaskedInput):
    
    def __init__(self, attrs={}):
        attrs.update({'class': 'empenho-widget', 'size': '14', 'maxlength': '12'})
        super(self.__class__, self).__init__(attrs=attrs)
    
    def render(self, name, value, attrs=None):
        if value and len(value) == 10:
            value = mask_empenho(value)
        return super(self.__class__, self).render(name, value, attrs=attrs)


class HorasCursosWidget(MaskedInput):
    
    def __init__(self, attrs={}):
        attrs.update({'class': 'horas-cursos-widget', 'size': '7', 'maxlength': '5'})
        super(self.__class__, self).__init__(attrs=attrs)
        
    def _format_value(self, value):
        if value is None:
            value = u''
        expected_types = (basestring, float)
        if not isinstance(value, expected_types):
            raise ValueError('Value type must be in %s' % expected_types)
        if isinstance(value, basestring) and (value == u'' or ('.' in value and len(filter(isdigit, value.split('.')))==2)):
            # value is blank or already formatted
            return value
        else:
            return mask_horas_cursos(value)
    
    def render(self, name, value, attrs=None):
        value = self._format_value(value)
        return super(HorasCursosWidget, self).render(name, value, attrs=attrs)


    

class BrPlacaVeicularWidget(MaskedInput):
    
    def __init__(self, attrs={}):
        attrs.update({'class': 'placa-widget', 'size': '10', 'maxlength': '8'})
        super(self.__class__, self).__init__(attrs=attrs)
    
    def render(self, name, value, attrs=None):
        if value and len(value) == 7:
            value = mask_placa(value)
        return super(self.__class__, self).render(name, value, attrs=attrs)
  
  
class BrCepWidget(MaskedInput):
    
    def __init__(self, attrs={}):
        attrs.update({'class': 'br-cep-widget', 'size': '9', 'maxlength': '9'})
        super(self.__class__, self).__init__(attrs=attrs)
    
    
class IntegerWidget(MaskedInput):
    
    def __init__(self, attrs={}):
        attrs.update({'class': 'integer-widget'})
        super(self.__class__, self).__init__(attrs=attrs)
    

class AlphaNumericWidget(MaskedInput):
    
    def __init__(self, attrs={}):
        attrs.update({'class': 'alpha-widget'})
        super(self.__class__, self).__init__(attrs=attrs)


class AlphaNumericUpperCaseWidget(MaskedInput):
    
    def __init__(self, attrs={}):
        attrs.update({'class': 'upper-text-widget'})
        super(self.__class__, self).__init__(attrs=attrs)


class CapitalizeTextWidget(MaskedInput):
    
    def __init__(self, attrs={}):
        attrs.update({'class': 'capitalize-text-widget'})
        super(self.__class__, self).__init__(attrs=attrs)

###############
# Autocomplete Configuration
###############

BASE_SEARCH_URL = 'autocompletar'
def get_search_url(cls):
    data = dict(base_search_url=BASE_SEARCH_URL, app_label=cls._meta.app_label,
                model_label=cls.__name__.lower())
    return '/%(base_search_url)s/%(app_label)s/%(model_label)s/' % data

def get_change_list_url(cls):
    data = dict(app_label=cls._meta.app_label, model_name=cls.__name__.lower())
    return '/admin/%(app_label)s/%(model_name)s/' % data

def get_add_another_url(cls):
    data = dict(app_label=cls._meta.app_label, model_name=cls.__name__.lower())
    return '/admin/%(app_label)s/%(model_name)s/add/' % data

ALL_AUTOCOMPLETE_OPTIONS = (
    'matchCase',
    'matchContains',
    'mustMatch',
    'minChars',
    'selectFirst',
    'extraParams',
    'formatItem',
    'formatMatch',
    'formatResult',
    'multiple',
    'multipleSeparator',
    'width',
    'autoFill',
    'max',
    'highlight',
    'scroll',
    'scrollHeight'
)

DEFAULT_AUTOCOMPLETE_OPTIONS = dict(autoFill=True, minChars=2, scroll=False, extraParams=dict())

def set_autocomplete_options(obj, options):
    options = options or dict()
    for option in options.keys():
        if option not in ALL_AUTOCOMPLETE_OPTIONS:
            raise ValueError(u'Autocomplete option error: "%s" not in %s' \
                % (option, ALL_AUTOCOMPLETE_OPTIONS))
    new_options = DEFAULT_AUTOCOMPLETE_OPTIONS.copy()
    new_options.update(options)
    obj.options = simplejson.dumps(new_options)


###############
# AutocompleteWidget 
# http://jannisleidel.com/2008/11/autocomplete-form-widget-foreignkey-model-fields/) 
###############

class AutocompleteWidget(forms.TextInput):
    """
    Widget desenvolvido para ser utilizado com field ``forms.ModelChoiceField``.
    """
    # TODO: mover scripts do template ``autocomplete_widget.html`` para arquivo js.
    class Media:
        js = BASE_JS_MEDIA + (
            settings.DJTOOLS_MEDIA_URL + "autocomplete/jquery.autocomplete.js",
            settings.DJTOOLS_MEDIA_URL + "autocomplete/jquery.bgiframe.min.js",
            settings.ADMIN_MEDIA_PREFIX + "js/admin/RelatedObjectLookups.js",
        )
        css = {'all': (settings.DJTOOLS_MEDIA_URL + "autocomplete/jquery.autocomplete.css",)}
    
    def __init__(self, url=None, id_=None, attrs=None, show=True, help_text=None, readonly=False,
                 side_html=None, label_value=None, **options):
        # TODO: o `label_value` poderia passar uma funcao como parametro, o que
        # retiraria a obrigação de fazer um método na classe de modelo.
        """
        ``id_``: autocomplete input id (default: randomic).
        ``url``: autocomplete search url (if not supplied, autocomplete will be 
                 readonly); this url must return "<label>|<id>\n<label>|<id>..".
        """
        self.help_text = help_text
        self.show = show
        self.attrs = attrs and attrs.copy() or {}
        self.id_ = id_ or randomic()
        self.url = url
        self.readonly = readonly
        self.side_html = side_html
        if label_value:
            extraParams = options.get('extraParams', {})
            extraParams['label_value'] = label_value
            options['extraParams'] = extraParams
        set_autocomplete_options(self, options)
        super(AutocompleteWidget, self).__init__(self.attrs)
    
    def render(self, name, value=None, attrs={}):
        model_cls = self.choices.queryset.model
        value = value or ''
        if not isinstance(value, (basestring, int, model_cls)):
            raise ValueError('value must be basestring, int or a models.Model instance. Got %s.' % value)
        if isinstance(value, model_cls):
            value = value.pk
        self.url = self.url or get_search_url(model_cls)
        context = dict(id=self.id_,
                       value=value,
                       options=self.options,
                       name=name,
                       url=self.url,
                       change_list_url=get_change_list_url(model_cls),
                       add_another_url=get_add_another_url(model_cls),
                       has_change_permission=has_change_permission(model_cls),
                       has_add_permission=has_add_permission(model_cls),
                       side_html=self.side_html,
                       readonly=self.readonly,
                       attrs=self.attrs,
                       show=self.show,
                       help_text=self.help_text)
        output = render_to_string('djtools/templates/autocomplete_widget.html',
                                  context)
        return mark_safe(output)


class AjaxMultiSelect(widgets.Widget):
    class Media:
        js = BASE_JS_MEDIA + (
            settings.DJTOOLS_MEDIA_URL + "autocomplete/jquery.autocomplete.js",
            settings.DJTOOLS_MEDIA_URL + "autocomplete/jquery.bgiframe.min.js",
        )
        css = {'all': (settings.DJTOOLS_MEDIA_URL + "autocomplete/jquery.autocomplete.css",
                       settings.DJTOOLS_MEDIA_URL + "m2m/m2m.css",)}

    def __init__(self, auto_url=None, app_name=None, class_name=None, attrs=None,
                 **options):
        self.auto_url = auto_url
        set_autocomplete_options(self, options)
        super(self.__class__, self).__init__(attrs)

    def build_attrs(self, extra_attrs=None, **kwargs):
        ret = super(AjaxMultiSelect, self).build_attrs(extra_attrs=None, **kwargs)
        return ret

    def render(self, name, value, attrs=None, choices=()):
        self.auto_url = self.auto_url or get_search_url(self.choices.queryset.model)
        final_attrs = self.build_attrs(attrs)
        final_attrs.setdefault('id', 'id_' + name)
        if value:
            items = [self.choices.queryset.model.objects.get(pk=id_) for id_ in value]
        else:
            items = []
        context = dict(name=name,
                       attrs=flatatt(final_attrs),
                       url=self.auto_url,
                       options=self.options,
                       items=items)
        output = render_to_string('djtools/templates/multipleautocomplete_widget.html',
                                  context)
        return mark_safe(output)

    def value_from_datadict(self, data, files, name):
        if isinstance(data, MultiValueDict):
            return data.getlist(name)
        return data.get(name, None)


###############
# TreeWidget
###############

class TreeWidget(forms.TextInput):
    class Media:
        js = BASE_JS_MEDIA + (
            settings.DJTOOLS_MEDIA_URL + "jstree/_lib.js",
            settings.DJTOOLS_MEDIA_URL + "jstree/tree_component.min.js",)
        css = {'all': (settings.DJTOOLS_MEDIA_URL + "jstree/tree_component.css",
                       settings.DJTOOLS_MEDIA_URL + "jstree/style.css",)}
    
    def __init__(self, id_=None, root_nodes=None, attrs={}):
        self.id_ = id_ or randomic()
        super(TreeWidget, self).__init__(attrs)
        self.root_nodes = root_nodes
    
    def get_parent_field(self):
        cls = self.choices.queryset.model
        for field in cls._meta.fields:
            if field.get_internal_type() == 'ForeignKey' and field.rel.to == cls:
                return field
        raise Exception(u'Class %s has no self relation' % (cls.__name__))

    def get_root_nodes(self):
        cls = self.choices.queryset.model
        args = {self.get_parent_field().name: None}
        return self.choices.queryset.filter(**args)
    
    def get_children(self, node):
        args = {self.get_parent_field().name: node}
        return self.choices.queryset.filter(**args)

    def get_tree_as_ul(self, node):
        nodes = []
        nodes.append('<ul>')
        self.__get_descendents_helper(node, nodes)
        nodes.append('</ul>')
        return nodes

    def __get_descendents_helper(self, node, nodes):
        # FIXME: deixar o ``title`` mais flexível
        nodes.append('<li id="%(pk)s"><a href="#" title="%(title)s">%(label)s</a>' \
            % dict(pk=node.pk, title=unicode(node), label=unicode(node)))
        node_children = self.get_children(node)
        if node_children:
            nodes.append('<ul>')
        for c in node_children:
            self.__get_descendents_helper(c, nodes)
        if node_children:
            nodes.append('</ul>')
        nodes.append('</li>')
        return nodes
    
    def render(self, name, value=None, attrs={}):
        # FIXME: deixar ``context`` mais flexível
        value = value or ''
        self.root_nodes = self.root_nodes or self.get_root_nodes()
        tree_as_ul = []
        for root_node in self.root_nodes:
            tree_as_ul += self.get_tree_as_ul(root_node)
        tree_as_ul = ''.join(tree_as_ul)
        output = u"""\
        <div class="tree-container" id="tree-%(name)s">
            %(tree_as_ul)s
        </div>
        <input type="hidden" name="%(name)s" value="%(value)s"/>
        <script type="text/javascript">
            root_nodes = $("#tree-%(name)s > ul");
            root_nodes.addClass("tree-ul-root");
            for (i=0; i<root_nodes.length; i++) {
                root_node = $(root_nodes[i]);
                root_node.attr("id", "root-node-"+(i+1));
            }
            $("#tree-%(name)s > ul").css("padding", "0");
            $("#tree-%(name)s > ul.tree-ul-root").tree({
                ui: {
                    theme_name: "default", 
                    theme_path: "%(DJTOOLS_MEDIA_URL)sjstree/themes/",
                    context     : [ 
                        {
                            id      : "open-branch",
                            label   : "Open Branch", 
                            visible : function (NODE, TREE_OBJ) { return true }, 
                            action  : function (NODE, TREE_OBJ) { 
                                
                            } 
                        }
                    ]
                },
                callback: {
                    onselect: function(node, tree_obj) {
                        value = node.getAttribute("id")
                        $("input[name=%(name)s]").val(value)
                    },
                },
            });
            
            function select_node(node_id) {
                for (i=0; i<root_nodes.length; i++) {
                    root_node = $(root_nodes[i]);
                    $.tree_reference(root_node.attr("id")).select_branch($('#'+node_id));
                }
            }
        </script>""" % dict(
            name=name, value=value, tree_as_ul=tree_as_ul,
            DJTOOLS_MEDIA_URL=settings.DJTOOLS_MEDIA_URL)
        if value:
            output += u"""\
            <script>
                select_node('%(value)s');
            </script>
            """ % dict(value=value)
        return mark_safe(output)
