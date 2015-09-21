# -*- coding: utf-8 -*-
from inventario.models import ItensPatrimoniais, StatusItens, Inventarios
from django import forms

#####################
# ITENSPATRIMONIAIS #
#####################

class ItensPatrimoniaisForm(forms.ModelForm):
    class Meta:
        model = ItensPatrimoniais

    descricao = forms.CharField(label=u'Descrição',
                                widget=forms.Textarea(attrs={'rows':'4', 'columns':'10'}), 
                                help_text=u'Descrição do Item')
    comentario = forms.CharField(label=u'Comentário',
                                widget=forms.Textarea(attrs={'rows':'4', 'columns':'10'}),
                                required = False 
                                )
    
class InventarioBuscaForm(forms.Form):
# FIXME: Adicionar o campo descrição na busca!!!
#    descricao = forms.CharField(label=u'Descrição do Item', required=False, widget=forms.TextInput(attrs={'size':'50'}))
    ano = forms.ModelChoiceField(label=u'Ano do Inventário', empty_label=u'Todos', 
                                        queryset=Inventarios.objects.all(), required=False)
    status = forms.ModelChoiceField(label=u'Status', empty_label=u'Todos', 
                                    queryset=StatusItens.objects.all(), required=False)
    
    METHOD = 'GET'
    TITLE = 'Busca de Inventários'