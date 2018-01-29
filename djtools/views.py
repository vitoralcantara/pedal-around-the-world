# -*- coding: utf-8 -*-

from djtools.utils import JsonResponse, httprr, get_profile_model,\
    get_admin_object_url
from djtools.apps.endereco.utils import get_endereco
from djtools.apps.endereco.models import Endereco
from django.contrib.auth.models import User

def create_user(request, profile_pk):
    profile = get_profile_model().objects.get(pk=profile_pk)
    if profile.user:
        return httprr(get_admin_object_url(profile.user), u'Usuário já criado!')
    else:
        user = User.objects.create_user(profile.username, email='', password=None)
        return httprr('/admin/auth/user/%s/' % user.pk, u'Usuário criado!')

def get_dados_por_cep(request):
    """
    """
    try:
        endereco = get_endereco(request.GET['cep'])
    except ValueError, e:
        return JsonResponse(dict(ok=False, cep_valido=False, msg=str(e)))
    if endereco:
        result = endereco.to_dict()
        result.update(ok=True, msg=u'Endereço encontrado!')
        return JsonResponse(result)
    else:
        return JsonResponse(dict(ok=False, 
                                 cep_valido=True,
                                 msg='Endereço não encontrado! Preencha os dados abaixo.'))

def endereco_deletar(request, objeto_id):
    Endereco.objects.get(pk=objeto_id).delete()
    return httprr(request.META['HTTP_REFERER'], 
                  u'Endereço removido com sucesso!')