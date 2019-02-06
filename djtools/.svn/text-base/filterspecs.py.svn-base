from django.contrib.admin.filterspecs import FilterSpec, ChoicesFilterSpec
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

class RelatedPlusFilterSpec(ChoicesFilterSpec):

    def __init__(self, f, label, request, model):
        self.label = label
        self.lookup_kwarg = '%s__exact' % f
        self.lookup_val = request.GET.get(self.lookup_kwarg, None)
        self.lookup_choices = list(model.objects.values_list(f, flat=True).order_by(f).distinct())
        self.lookup_choices.sort()

    def choices(self, cl):
        yield {'selected': self.lookup_val is None,
               'query_string': cl.get_query_string({}, [self.lookup_kwarg]),
               'display': _('All')}
        for val in self.lookup_choices:
            yield {'selected': smart_unicode(val) == self.lookup_val,
                   'query_string': cl.get_query_string({self.lookup_kwarg: val}),
                   'display': smart_unicode(val).upper()}
    
    def title(self):
        return self.label