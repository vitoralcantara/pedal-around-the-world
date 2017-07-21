# -*- coding: utf-8 -*-
from comum.models import Pessoa, Endereco
from django import forms

from djtools.formfields import BrDataField, BrCepField, BrCepWidget
from djtools.formwidgets import BRCpfWidget, BrDataWidget

from comum import choices

############
# ENDERECO #
############

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
    cep = BrCepField(label=u'CEP', widget=BrCepWidget, required=False)

##########
# PESSOA #
##########

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        
    #cpf = forms.CharField(label=u'CPF', widget=BRCpfWidget, required=True)
    data_nascimento = BrDataField(label=u'Data nascimento', widget=BrDataWidget())
    nacionalidade = forms.ChoiceField(label=u'Nacionalidade', widget=forms.Select(), choices=choices.NACIONALIDADE, required=False)
    estado_civil = forms.ChoiceField(label=u'Estado Civil', widget=forms.Select(), choices=choices.ESTADO_CIVIL, required=False)