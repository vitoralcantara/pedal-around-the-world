# -*- coding: utf-8 -*-

from django.utils.safestring import mark_safe
from django.template import Library, TemplateSyntaxError, Node, NodeList, \
    Variable, VariableDoesNotExist
import re
from django.template.loader import render_to_string
from djtools import formutils
import traceback

register = Library()

@register.tag
def render_form(parser, token):
    tag_name, form_name = token.split_contents()
    return RenderFormNode(form_name)

class RenderFormNode(Node):
    def __init__(self, form_name):
        self.form_name = form_name
    
    def render(self, context):
        try:
            form = context[self.form_name]
            form.rendered = formutils.render_form(form)
            form.ID = form.__class__.__name__.lower().replace('form', '_form')
        except Exception, e:            
            return '<pre>'+'<br/>'.join(traceback.format_exc().splitlines())+'</pre>'
        return render_to_string('djtools/templates/form.html', dict(form=form))

@register.filter
def getattr (obj, args):
    """ Try to get an attribute from an object.

    Example: {% if block|getattr:"editable,True" %}

    Beware that the default is always a string, if you want this
    to return False, pass an empty second argument:
    {% if block|getattr:"editable," %}
    """
    splitargs = args.split(',')
    try:
        (attribute, default) = splitargs
    except ValueError:
        (attribute, default) = args, ''
    
    try:
        return obj.__getitem__(attribute)
    except:
        pass
    
    try:
        attr = obj.__getattribute__(attribute)
    except AttributeError:
        attr = obj.__dict__.get(attribute, default)
    except:
        attr = default
    
    if hasattr(attr, '__call__'):
        return attr.__call__()
    else:
        return attr


class IfInNode(Node):
    # http://www.djangosnippets.org/snippets/721/
    def __init__(self, var1, var2, nodelist_true, nodelist_false, negate):
        self.var1, self.var2 = Variable(var1), Variable(var2)
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.negate = negate

    def __repr__(self):
        return "<IfInNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        try:
            val2 = self.var2.resolve(context)
        except VariableDoesNotExist:
            val2 = None
        try:
            if (self.negate and val1 not in val2) or (not self.negate and val1 in val2):
                return self.nodelist_true.render(context)
            return self.nodelist_false.render(context)
        except TypeError:
            raise ValueError, "Second arg to ifin or ifnotin must be iterable"

def do_ifin(parser, token, negate):
    bits = list(token.split_contents())
    if len(bits) != 3:
        raise TemplateSyntaxError, "%r takes two arguments" % bits[0]
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return IfInNode(bits[1], bits[2], nodelist_true, nodelist_false, negate)

def ifin(parser, token):
    return do_ifin(parser, token, False)
register.tag('ifin', ifin)

def ifnotin(parser, token):
    return do_ifin(parser, token, True)
register.tag('ifnotin', ifnotin)


def list_of_dicts_2_list_of_lists(data):
    attrs = data[0].keys()
    list_of_lists = [attrs]
    for i in data:
        item = [unicode(i[attr]) for attr in attrs]
        list_of_lists.append(item)
    return list_of_lists

def list_of_lists_to_table(data):
    head, body = data[0], data[1:]
    out = [u'<table cellspacing="0"><thead><tr>']
    for i in head:
        out.append(u'<th>%s</th>' % unicode(i))
    out.append(u'</tr></thead>')
    out.append(u'<tbody>')
    for index, i in enumerate(body):
        out.append(u'<tr class="%s">' % (index%2 and 'row2' or 'row1'))
        for val in i:
            align =  isinstance(val, basestring) and u'left' or u'right'
            val = unicode(val)
            out.append(u'<td align="%s">%s</td>' % (align, val))
        out.append(u'</tr>')
    out.append(u'</tbody></table>')
    return u''.join(out)   

def list_of_dicts_to_table(data):
    return list_of_lists_to_table(list_of_dicts_2_list_of_lists(data))

@register.filter
def to_table(data):
    """
    `data` can be in 2 formats:
        1. List of lists:
            The first item is the header, later items are rows.
        2. List of dicts:
            Each item is a row.
    """
    if not data:
        return mark_safe(u'<p>Nennhum registro</p>')
    else:
        if len(data) == 1 and isinstance(data[0], list):
            return mark_safe(u'<p>Nennhum registro</p>')
    if isinstance(data[0], list):
        return mark_safe(list_of_lists_to_table(data))
    elif isinstance(data[0], dict):
        return mark_safe(list_of_dicts_to_table(data))

@register.filter
def in_group(user, group):
    # Adapted from http://www.djangosnippets.org/snippets/895/
    """Returns True/False if the user is in the given group(s).
    Usage::
        {% if user|in_group:"Friends" %}
        or
        {% if user|in_group:"Friends,Enemies" %}
        ...
        {% endif %}
    You can specify a single group or comma-delimited list.
    No white space allowed.
    """
    if isinstance(group, basestring):
        if re.search(',', group): 
            group_list = re.sub('\s+','',group).split(',')
        elif re.search(' ', group): 
            group_list = group.split()
        else: 
            group_list = [group]
    elif isinstance(group, list):
        group_list = [i.strip() for i in group]
    user_groups = []
    for group in user.groups.all(): 
        user_groups.append(str(group.name))
    if filter(lambda x:x in user_groups, group_list): 
        return True
    else:
        return False
in_group.is_safe = True

@register.filter
def indice(value, arg):
    """Retorna elemento de lista com indice arg"""
    return value[arg]