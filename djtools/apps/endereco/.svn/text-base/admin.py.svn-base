# -*- coding: utf-8 -*-

from django.contrib import admin
from endereco.models import Endereco

class EnderecoAdmin(admin.ModelAdmin):
    list_display = ['id', '__unicode__']
admin.site.register(Endereco, EnderecoAdmin)