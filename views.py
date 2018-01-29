# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from djtools.templatetags.djtools_templatetags import in_group
from djtools.utils import rtr, httprr, user_has_profile
from comum.utils import change_app

@rtr()
@login_required
def index(request):
    """
    Tela inicial com informações relevantes de cada módulo que o usuário
    autenticado tenha acesso.
    """
    if request.user.is_superuser and not user_has_profile(request.user):
        return httprr('/admin/')
    
    contexto = dict()

    # Gratuidade
    if in_group(request.user, ['gratuidade_operador']) and 'gratuidade' in settings.INSTALLED_APPS:
        contexto['gratuidade'] = dict()
        contexto['gratuidade']['cadastro_pessoagratuidade'] = 'Cadastrar'
        
    # Inventário
    if in_group(request.user, ['inventario_operador']) and 'inventario' in settings.INSTALLED_APPS:
        contexto['inventario'] = dict()
        contexto['inventario']['cadastro_itenspatrimoniais'] = 'Cadastrar'

    return contexto

@login_required
def change_app_and_get_menu_template(request):
    """
    Muda a aplicação atual e retorna o conteúdo do menu apropriado.
    """
    change_app(request, request.GET['app_label'])
    if request.session['template_menu']: 
        return HttpResponse(render_to_string(request.session['template_menu']))
    else:
        return HttpResponse('')