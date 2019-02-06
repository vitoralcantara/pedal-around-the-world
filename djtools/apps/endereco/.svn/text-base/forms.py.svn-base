# -*- coding: utf-8 -*-

from django import forms
from endereco.models import Endereco
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from django.conf import settings
from djtools.formfields import BrCepField
from django.template.loader import render_to_string

class BRCepModWidget(forms.TextInput):
    
    class Media:
        js = (settings.MEDIA_URL + "js/jquery.js", 
              settings.MEDIA_URL + "js/mask.js",)
    
    def __init__(self, attrs={}):
        super(self.__class__, self).__init__(attrs=dict(size='9', maxlength='9'))
    
    def render(self, name, value, attrs=None):
        c = super(self.__class__, self).render(name, value, attrs=None)
        extra = u"""
        <span id="resultado-busca-cep"></span>
        <script type="text/javascript">
            $("input[name=%s]").keypress(function(){
                mask(this, mask_cep);
            });
            
            function travar_campos(travar) {
                acao = travar ? "readonly" : null;
                campos = ["bairro", "cidade", "uf", "logradouro", "tp_logradouro"]
                for (i=0; i<campos.length; i++) {
                    input = $("*[name="+campos[i]+"]");
                    if (!travar) {
                        input.val("");
                    }
                    input.attr("readonly", acao);
                }
            }
            
            $("input[name=%s]").keyup(function(){
                if ($(this).val().length == 9) {
                    // CEP completo, buscar dados
                    $("#resultado-busca-cep").html("Buscando endereço...");
                    $.getJSON('/endereco/get_dados_por_cep/', {'cep': $(this).val()},
                        function(data) {
                            $("#resultado-busca-cep").html(data['msg']);
                            if (data['ok']) {
                                for (i in data) {
                                    $("*[name="+i+"]").val(data[i]);
                                }
                                $("*[rel=endereco-nao-cep]").show();
                            } else {
                                if (data['cep_valido']) {
                                    $("*[rel=endereco-nao-cep]").show();
                                } else {
                                    travar_campos(true);
                                }
                            }
                        }
                    );
                }
            });
        </script>
        """ % (name, name)
        return c + mark_safe(extra)

def get_falses_in_dict(dic, keys=None):
    """
    """
    keys = keys or dic.items()
    falses = []
    for key in keys:
        value = dic[key]
        if not value:
            falses.append(key)
    return falses

class EnderecoAdminInlineForm(forms.ModelForm):
    class Meta:
        model = Endereco
        exclude = ['local_pk', 'local_content_type']
    cep = BrCepField(widget=BRCepModWidget, required=False)
    objeto_content_type = forms.ModelChoiceField(queryset=ContentType.objects.all(),
                                               widget=forms.HiddenInput, required=False)
    objeto_pk = forms.IntegerField(widget=forms.HiddenInput, required=False)
    tp_logradouro = forms.CharField(widget=forms.TextInput(attrs={'size':10}),
                                    required=False)
    logradouro = forms.CharField(widget=forms.TextInput(attrs={'size':30}),
                                 required=False)
    numero = forms.CharField(widget=forms.TextInput(attrs={'size':5}),
                             required=False)
    complemento = forms.CharField(widget=forms.TextInput(attrs={'size':10}),
                                  required=False)
    
    def __unicode__(self):
        return render_to_string('endereco/templates/form.html', 
                                dict(form_endereco=self))
    
    def is_valid(self):
        if self.data['cep']: 
            # Se preencheu CEP tem que preencher os demais campos
            keys = ['tp_logradouro', 'logradouro', 'bairro', 'cidade', 'uf']
            falses = get_falses_in_dict(self.data, keys=keys)
            if falses:
                for i in falses:
                    self.errors[i] = ['Este campo deve ser preenchido.']
        return super(EnderecoAdminInlineForm, self).is_valid()
