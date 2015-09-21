# -*- coding: utf-8 -*-
from django.http import HttpResponse
from djtools.utils import rtr

from inventario.reports import RelatorioInventarioPDF, RelatorioInventarioGeralPDF
from geraldo.generators import PDFGenerator
from inventario.models import ItensPatrimoniais, StatusItens, Inventarios
from inventario.forms import InventarioBuscaForm



def relatorio_geral(request):
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=relatorio.pdf'

    itenspatrim = ItensPatrimoniais.objects.order_by('id')
    
    report = RelatorioInventarioGeralPDF(queryset=itenspatrim)
    report.generate_by(PDFGenerator, filename=response)

    return response
@rtr()
def inventario_busca(request):
    form = InventarioBuscaForm(request.GET or None)
    if form.is_valid():
# FIXME: Adicionar o campo descrição na busca!!!
#        descricao = form.cleaned_data['descricao']
        descricao = ''
        ano = form.cleaned_data['ano']
        status = form.cleaned_data['status']
        
        inventarios = ItensPatrimoniais.objects.filter(campo_busca__icontains=descricao)
        if status:
            inventarios = inventarios.filter(status=status)
        if ano:
            inventarios = inventarios.filter(inventario=ano)
        
        if request.GET.has_key('pdf'):
            return relatorio(request, inventarios)
    return locals()

def relatorio(request, inventarios):
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=relatorio.pdf'

    ano = request.GET.get('ano')
    status = request.GET.get('status')
    
    if status:
        status = StatusItens.objects.get(pk = status)
    if ano:
        ano = Inventarios.objects.get(pk = ano)
    
    if not status and not ano:
        return relatorio_geral(request)
    if not status:
        titulo = 'Relatório - Inventário %s' % ano
    elif not ano:
        titulo = 'Relatório %s - Inventário' % status
    else:
        titulo = 'Relatório %s - Inventário %s' %(status, ano)
    
    report = RelatorioInventarioPDF(queryset=inventarios)
    report.generate_by(PDFGenerator, filename=response, variables={'titulo': titulo})

    return response