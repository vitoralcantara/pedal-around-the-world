
/* Syncronize Widgets */

function sync_widgets() {
    
    // BrDataWidget
    $("input.br-date-widget").unmask();
    $("input.br-date-widget").mask("99/99/9999", {placeholder:" "});
    
    // TimeWidget
    $("input.br-date-widget").unmask();
    $("input.br-date-widget").mask("99/99/9999", {placeholder:" "});
    
    // BrTelefoneWidget
    $("input.br-phone-number-widget").unmask()
    $("input.br-phone-number-widget").mask("(99) 9999-9999", {placeholder:" "});
    
    // BrCepWidget
    $("input.br-cep-widget").unmask()
    $("input.br-cep-widget").mask("99999-999", {placeholder:" "});
    
    // BrCpfWidget
    $("input.br-cpf-widget").unmask()
    $("input.br-cpf-widget").mask("999.999.999-99", {placeholder:" "});
    
    // BrCnpjWidget
    $("input.br-cnpj-widget").unmask()
    $("input.br-cnpj-widget").mask("99.999.999/9999-99", {placeholder:" "});
    
    // BrDinheiroWidget
    $("input.br-dinheiro-widget").unbind('keypress');
    $("input.br-dinheiro-widget").keypress(function () {
        mask(this, mask_money)
    });
    
}

var v_obj = null
var v_fun = null

function mask(o,f){
    v_obj=o
    v_fun=f
    setTimeout("execmask()",1)
}

function execmask(){
    v_obj.value=v_fun(v_obj.value)
}

function mask_only_numbers(v){
    return v.replace(/\D/g,"")
}

function mask_money(v){ // by paivatulio
    textoNumerico = v.replace(/\D/g,"");
    textoNumerico = textoNumerico.replace(/^0/,"")
	textoFormatado = "";
	if (textoNumerico.length == 1) {
		return "0,0"+textoNumerico;
	} else
	if (textoNumerico.length == 2) {
		return "0,"+textoNumerico;
	} else {
	for (i=0; i<textoNumerico.length; i++) {
		if (i == textoNumerico.length - 2) {
			textoFormatado += ",";
		}
		if ((i!= 0 && textoNumerico.length-i >= 5) && ((textoNumerico.length-i+1) % 3 == 0)) {
			textoFormatado += ".";
		}
		textoFormatado += textoNumerico.charAt(i);
	}
	return textoFormatado;
	}
}

$(document).ready(function(){
   sync_widgets(); 
});
