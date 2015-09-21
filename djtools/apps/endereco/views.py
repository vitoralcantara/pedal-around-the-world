# -*- coding: utf-8 -*-

from django_utils.utils import JsonResponse, httprr
from endereco.utils import get_endereco
from endereco.models import Endereco

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