# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db import models
from djtools.filterspecs import RelatedPlusFilterSpec
from djtools.formfields import BrDataHoraField, BrDataField
from djtools.formwidgets import BrDataHoraWidget, BrDataWidget

class ModelAdminPlus(admin.ModelAdmin):
    """A admin.ModelAdmin with more features."""
    
    change_list_template = 'djtools/templates/adminutils/change_list.html'
    change_form_template = 'djtools/templates/adminutils/change_form.html'
    
    show_delete_link = True # Force hide "delete link"
    show_save_and_add_another = True # Force hide "save and add another button"
    show_save_and_continue = True # Force hide "save and continue button"
    
    formfield_overrides = {
        models.DateTimeField: {
            'form_class': BrDataHoraField,
            'widget': BrDataHoraWidget},
        models.DateField: {
            'form_class': BrDataField,
            'widget': BrDataWidget},
    }
    
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        # Setting submit_row context
        context.update({
            'onclick_attrib': (self.model._meta.get_ordered_objects() and change
                                and 'onclick="submitOrderForm();"' or ''),
            'show_delete_link': self.show_delete_link and (not context['is_popup'] and self.has_delete_permission(request, obj)
                                  and (change or context['show_delete'])),
            'show_save_as_new': not context['is_popup'] and change and self.save_as,
            'show_save_and_add_another': self.show_save_and_add_another and self.has_add_permission(request) and 
                                not context['is_popup'] and (not self.save_as or add),
            'show_save_and_continue': self.show_save_and_continue and not context['is_popup'] and self.has_change_permission(request, obj),
            'is_popup': context['is_popup'],
            'show_save': True
        })
        return super(ModelAdminPlus, self).render_change_form(
            request, context, add=add, change=change, form_url=form_url, obj=obj)
    
    def changelist_view(self, request, extra_context=None):
        filter_related_plus_specs = []
        if hasattr(self, 'list_filter_plus'):
            for title, lookup in self.list_filter_plus:
                filter_spec = RelatedPlusFilterSpec(lookup, title, request, self.model)
                filter_related_plus_specs.append(filter_spec)
        extra_context = dict(filter_related_plus_specs=filter_related_plus_specs)
        return super(ModelAdminPlus, self).changelist_view(request, extra_context)
