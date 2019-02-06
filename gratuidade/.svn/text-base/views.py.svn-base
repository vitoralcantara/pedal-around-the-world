# -*- coding: utf-8 -*-
from django.http import HttpResponse

from reports import CarteiraGratuidadePDF
from geraldo.generators import PDFGenerator
from gratuidade.models import PessoaGratuidade


def cartao_gratuidade(request, obj_pk):
    resp = HttpResponse(mimetype='application/pdf')

    pessoagratuidade = PessoaGratuidade.objects.filter(pk = obj_pk)
        
    report = CarteiraGratuidadePDF(queryset=pessoagratuidade)
    report.generate_by(PDFGenerator, filename=resp)

    return resp

