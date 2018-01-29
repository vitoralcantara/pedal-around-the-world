# -*- coding: utf-8 -*-

from django.utils.encoding import StrAndUnicode, force_unicode, smart_unicode
from django.utils.html import conditional_escape
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django import forms
from xml.dom.minidom import parseString
from django.forms.util import flatatt
from django.conf import settings


def pretty_name(name):
    "Converts 'first_name' to 'First name'"
    name = name[0].upper() + name[1:]
    return name.replace('_', ' ')

class BoundField(StrAndUnicode):
    "A Field plus data"
    def __init__(self, form, field, name):
        self.form = form
        self.field = field
        self.name = name
        self.html_name = form.add_prefix(name)
        self.html_initial_name = form.add_initial_prefix(name)
        if self.field.label is None:
            self.label = pretty_name(name)
        else:
            self.label = self.field.label
        self.help_text = field.help_text or ''

    def __unicode__(self):
        """Renders this field as an HTML widget."""
        if self.field.show_hidden_initial:
            return self.as_widget() + self.as_hidden(only_initial=True)
        return self.as_widget()

    def _errors(self):
        """
        Returns an ErrorList for this field. Returns an empty ErrorList
        if there are none.
        """
        return self.form.errors.get(self.name, self.form.error_class())
    errors = property(_errors)

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        """
        Renders the field by rendering the passed widget, adding any HTML
        attributes passed as attrs.  If no widget is specified, then the
        field's default widget will be used.
        """
        if not widget:
            widget = self.field.widget
        attrs = attrs or {}
        auto_id = self.auto_id
        if auto_id and 'id' not in attrs and 'id' not in widget.attrs:
            attrs['id'] = auto_id
        if not self.form.is_bound:
            data = self.form.initial.get(self.name, self.field.initial)
            if callable(data):
                data = data()
        else:
            if isinstance(self.field, forms.FileField) and self.data is None:
                data = self.form.initial.get(self.name, self.field.initial)
            else:
                data = self.data
        if not only_initial:
            name = self.html_name
        else:
            name = self.html_initial_name
        return widget.render(name, data, attrs=attrs)

    def as_text(self, attrs=None, **kwargs):
        """
        Returns a string of HTML for representing this as an <input type="text">.
        """
        return self.as_widget(forms.TextInput(), attrs, **kwargs)

    def as_textarea(self, attrs=None, **kwargs):
        "Returns a string of HTML for representing this as a <textarea>."
        return self.as_widget(forms.Textarea(), attrs, **kwargs)

    def as_hidden(self, attrs=None, **kwargs):
        """
        Returns a string of HTML for representing this as an <input type="hidden">.
        """
        return self.as_widget(self.field.hidden_widget(), attrs, **kwargs)

    def _data(self):
        """
        Returns the data for this BoundField, or None if it wasn't given.
        """
        return self.field.widget.value_from_datadict(self.form.data, self.form.files, self.html_name)
    data = property(_data)

    def label_tag(self, contents=None, attrs=None):
        """
        Wraps the given contents in a <label>, if the field has an ID attribute.
        Does not HTML-escape the contents. If contents aren't given, uses the
        field's HTML-escaped label.

        If attrs are given, they're used as HTML attributes on the <label> tag.
        """
        contents = contents or conditional_escape(self.label)
        widget = self.field.widget
        id_ = widget.attrs.get('id') or self.auto_id
        if id_:
            attrs = attrs and flatatt(attrs) or ''
            contents = u'<label for="%s"%s>%s</label>' % (widget.id_for_label(id_), attrs, unicode(contents))
        return mark_safe(contents)

    def _is_hidden(self):
        "Returns True if this BoundField's widget is hidden."
        return self.field.widget.is_hidden
    is_hidden = property(_is_hidden)

    def _auto_id(self):
        """
        Calculates and returns the ID attribute for this BoundField, if the
        associated Form has specified auto_id. Returns an empty string otherwise.
        """
        auto_id = self.form.auto_id
        if auto_id and '%s' in smart_unicode(auto_id):
            return smart_unicode(auto_id) % self.html_name
        elif auto_id:
            return self.html_name
        return ''
    auto_id = property(_auto_id)

def render_field(form, field_name):
    normal_row = u'''%(errors)s%(label)s%(field)s%(help_text)s'''
    error_row = u'<div>%s</div>'
    row_ender = u'</td></tr>'
    help_text_html = u'<p class="help">%s</p>'
    errors_on_separate_row = False
    
    "Helper function for outputting HTML. Used by as_table(), as_ul(), as_p()."
    top_errors = form.non_field_errors() # Errors that should be displayed above all fields.
    output, hidden_fields = [], []
    field = form.fields[field_name]
    bf = BoundField(form, field, field_name)
    bf_errors = form.error_class([conditional_escape(error) for error in bf.errors]) # Escape and cache in local variable.
    if bf.is_hidden:
        if bf_errors:
            top_errors.extend([u'(Hidden field %s) %s' % (field_name, force_unicode(e)) for e in bf_errors])
        hidden_fields.append(unicode(bf))
    else:
        if errors_on_separate_row and bf_errors:
            output.append(error_row % force_unicode(bf_errors))
        if bf.label:
            label = conditional_escape(force_unicode(bf.label))
            # Only add the suffix if the label does not end in
            # punctuation.
            if form.label_suffix:
                if label[-1] not in ':?.!':
                    label += form.label_suffix
            label = bf.label_tag(label) or ''
        else:
            label = ''
        if field.help_text:
            help_text = help_text_html % force_unicode(field.help_text)
        else:
            help_text = u''
        output.append(normal_row % {'errors': force_unicode(bf_errors), 
                                    'label': force_unicode(label), 
                                    'field': unicode(bf), 
                                    'help_text': help_text})
    #if top_errors:
    #    output.insert(0, error_row % force_unicode(top_errors))
    if hidden_fields: # Insert any hidden fields in the last row.
        str_hidden = u''.join(hidden_fields)
        if output:
            last_row = output[-1]
            # Chop off the trailing row_ender (e.g. '</td></tr>') and
            # insert the hidden fields.
            if not last_row.endswith(row_ender):
                # This can happen in the as_p() case (and possibly others
                # that users write): if there are only top errors, we may
                # not be able to conscript the last row for our purposes,
                # so insert a new, empty row.
                last_row = normal_row % {'errors': '', 'label': '', 'field': '', 'help_text': ''}
                output.append(last_row)
            output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
        else:
            # If there aren't any rows in the output, just append the
            # hidden fields.
            output.append(str_hidden)
    return mark_safe(u''.join(output))

def indent_xml(xml, indent=' '*4):
    """Indent and return XML."""
    return parseString(xml).toprettyxml(indent)

def render_form(form):    
#    fieldsets = (
#        (None, {
#            'fields': ('url', 'title', 'content', 'sites')
#        }),
#        ('Advanced options', {
#            'fields': (('enable_comments', 'registration_required'), ('template_name',))
#        }),
#    )
    
    fieldsets = hasattr(form, 'fieldsets') and form.fieldsets or \
        [(None, {'fields': form.base_fields.keys()})]
    
    out = [u'<div>']
    for fieldset_name, options in fieldsets:
        
        lines = options['fields']
        classes = ' '.join(options.get('classes', ()))
        fieldset_description = options.get('description', None)
        
        # Fieldset
        out.append(u'<fieldset class="module aligned %(classes)s">' % dict(classes=classes))
        if fieldset_name:
            out.append(u'<h2>%(fieldset_name)s</h2>' % dict(fieldset_name=fieldset_name))
        if fieldset_description:
            out.append(u'<div class="description">%(fieldset_description)s</div>' \
                       % dict(fieldset_description=fieldset_description)) 
            
        for line in lines:
            if isinstance(line, basestring):
                if isinstance(form.base_fields[line].widget, forms.HiddenInput):
                    # Hidden field has no div.form-row
                    out.append(render_field(form, line))
                    continue
                else:
                    line = [line]
            
            out.append(u'<div class="form-row %(line_classes)s ">' \
                       % dict(line_classes=u' '.join(line)))
            
            for field_name in line:
                
                try:
                    form.base_fields[field_name]
                except KeyError:
                    raise KeyError('Field "%s" not in form.' % field_name)
                
                field_classes = []
                if len(line) > 1:
                    field_classes.append(u'field-box')
                if field_name is line[0]:
                    field_classes.append(u'field-box-first')
                else:
                    field_classes.append(u'field-box-later')
                if form.base_fields[field_name].required:
                    field_classes.append(u'required')
                out.append(u'<div class="%(field_classes)s">' \
                           % dict(field_classes=' '.join(field_classes)))
                
                out.append(render_field(form, field_name))
                
                out.append(u'</div>')
            
            out.append(u'</div>')
        
        out.append(u'</fieldset>')
    
    out.append(u'</div>')
    out = u''.join(out)
    return mark_safe(out)
    #return indent_xml(out)[22:] # retirar o ``<?xml version="1.0" ?>``


def show_form_data(form, data=None):    
    data = data or form.data    
    fieldsets = hasattr(form, 'fieldsets') and form.fieldsets or \
        [(None, {'fields': form.base_fields.keys()})]
    #fieldsets = normalize_fieldsets(fieldsets)
    
    out = [u'<div>']
    for fieldset_name, options in fieldsets:
        
        lines = options['fields']
        classes = ' '.join(options.get('classes', ()))
        fieldset_description = options.get('description', None)
        
        # Fieldset
        out.append(u'<fieldset class="module aligned %(classes)s">' % dict(classes=classes))
        if fieldset_name:
            out.append(u'<h2>%(fieldset_name)s</h2>' % dict(fieldset_name=fieldset_name))
        if fieldset_description:
            out.append(u'<div class="description">%(fieldset_description)s</div>' \
                       % dict(fieldset_description=fieldset_description)) 
            
        for line in lines:
            if isinstance(line, basestring):
                if isinstance(form.base_fields[line].widget, forms.HiddenInput):
                    continue
                else:
                    line = [line]
            
            out.append(u'<div class="form-row %(line_classes)s ">' \
                       % dict(line_classes=u' '.join(line)))
            
            for field_name in line:
                field_classes = []
                if len(line) > 1:
                    field_classes.append(u'field-box')
                if field_name is line[0]:
                    field_classes.append(u'field-box-first')
                else:
                    field_classes.append(u'field-box-later')
                if form.base_fields[field_name].required:
                    field_classes.append(u'required')
                out.append(u'<div class="%(field_classes)s">' \
                           % dict(field_classes=' '.join(field_classes)))
                
                template = u'<label style="padding-top: 0">%(label)s</label><span>%(value)s</span>'
                
                field = form.base_fields[field_name] 
                label = field.label
                
                if isinstance(field, forms.BooleanField):
                    value = form.data.get(field_name) == 'on' and _(u'Yes') or _(u'No')
                else:
                    value = form.data[field_name] or u'<em class="scarletred1">Não Informado</em>'
                if hasattr(field, 'choices'):
                    for c_id, c_val in field.choices:
                        if c_id == form.data[field_name]:
                            value = c_val
                out.append(template % dict(label=label,
                                           value=value))
                
                out.append(u'</div>')
            
            out.append(u'</div>')
        
        out.append(u'</fieldset>')
    
    out.append(u'</div>')
    out = u''.join(out)
    return mark_safe(out)


class FormPlus:
    
    class Media:
        css = {
            'all': ('%scss/forms.css' % settings.ADMIN_MEDIA_PREFIX,
                    '%scss/form-with-fieldsets.css' % settings.DJTOOLS_MEDIA_URL,)
        }

    def render_fieldsets(self):
        return render_form(self)
    
    def pre_fields(self, fields):
        """
        Validates a value for each field in ``fields`` at ``self.cleaned_data``.
        """
        blank_fields = []
        for field_name in fields:
            if field_name not in self.cleaned_data:
                blank_fields.append('"%s"' % self.base_fields[field_name].label)
        if blank_fields:
            raise forms.ValidationError(u'O(s) campo(s) %s deve(m) ser preenchido(s).' % ', '.join(blank_fields))
    