
/* Syncronize Widgets */

function sync_widgets() {
    
    // BrDataWidget
    $("input.br-data-widget").unmask();
    $("input.br-data-widget").mask("99/99/9999", {placeholder:" "});
    
    // TimeWidget
    $("input.time-widget").unmask();
    $("input.time-widget").mask("99:99:99", {placeholder:" "});
    
    // BrDateTimeWidget
    $("input.br-datahora-widget").unmask();
    $("input.br-datahora-widget").mask("99/99/9999 99:99:99", {placeholder:" "});
    
    // BrTelefoneWidget
    $("input.br-phone-number-widget").unmask()
    $("input.br-phone-number-widget").mask("(99) 9999-9999", {placeholder:" "});
    
    // BrCepWidget
    $("input.br-cep-widget").unmask()
    $("input.br-cep-widget").mask("99999-999", {placeholder:" "});
	
	// HorasCursosWidget
    $("input.horas-cursos-widget").unbind('keypress');
    $("input.horas-cursos-widget").keypress(function () {
        mask(this, mask_float)
    });
    
    // BrCpfWidget
    $("input.br-cpf-widget").unmask()
    $("input.br-cpf-widget").mask("999.999.999-99", {placeholder:" "});
    
    // BrCnpjWidget
    $("input.br-cnpj-widget").unmask()
    $("input.br-cnpj-widget").mask("99.999.999/9999-99", {placeholder:" "});
    
	// BrPlacaVeicularWidget
    $("input.placa-widget").unmask()
    $("input.placa-widget").mask("aaa-9999", {placeholder:" "});
	$("input.placa-widget").blur(function () {
		this.value = this.value.toUpperCase();
	});
	
	// EmpenhoWidget
    $("input.empenho-widget").unmask()
	//$.mask.definitions['~']='[Nn]';
	//$.mask.definitions['/']='[Ee]';  
    //$("#eyescript").mask("~9.99 ~9.99 999"); 
    $("input.empenho-widget").mask("9999NE999999", {placeholder:" "});
	$("input.empenho-widget").blur(function () {
		this.value = this.value.toUpperCase();
	});
	
	// IntegerWidget
	$("input.integer-widget").unmask('keypress')
	$("input.integer-widget").keypress(function () {
        mask(this, mask_only_numbers)
    });
	
	// AlphaNumericWidget
    $("input.alpha-widget").unmask('keypress')
    $("input.alpha-widget").keypress(function () {
        mask(this, mask_alpha)
    });
	
    // AlphaNumericUpperTextWidget
    $("input.upper-text-widget").unbind('keypress')
    $("input.upper-text-widget").keypress(function () {
        mask(this, mask_upper_text)
    });
	
	// CapitalizeTextWidget
    $("input.capitalize-text-widget").unbind('keypress')
    $("input.capitalize-text-widget").keypress(function () {
        mask(this, mask_camel_case)
    });    
	
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

function mask_upper_text(v){ // by andersonbraulio
    texto = v.replace(/[^a-zA-Z0-9]/g,"");
	textoFormatado = "";

    for (i = 0; i < texto.length; i++) {
        char = texto.charAt(i);
        if (i == 0)
            if (char == ' ')
               textoFormatado = texto.substr(1);
            else
                textoFormatado = char.toUpperCase();
        else
              textoFormatado += char.toUpperCase();
    }
    return textoFormatado;
}

function mask_alpha(v){ // by andersonbraulio
    return v.replace(/[^a-zA-Z0-9]/g,"")
}

function mask_camel_case(v){ // by andersonbraulio
    texto = v.replace(/[^a-zA-ZÁ-Ûá-û0-9.\'\s\-]/g,"");
	textoFormatado = "";

	for (i = 0; i < texto.length; i++) {
        char = texto.charAt(i);
		if (i == 0) {
	        if (char == ' ')
	           textoFormatado = texto.substr(1);
	        else
	            textoFormatado = char.toUpperCase();
		} else {
		  prevChar = textoFormatado.charAt(i-1);
		  if (prevChar == ' ')
		      textoFormatado = texto.substr(0,i).concat(char.toUpperCase());
		  else
		      textoFormatado += char.toLowerCase();
		}
	}
	return textoFormatado;
}

function mask_float(v){
	textoNumerico = v.replace(/\D/g,"");
    textoNumerico = textoNumerico.replace(/^0/,"");
   
	if (textoNumerico.length == 1) {
		return "0." + textoNumerico;
	} else
	if (textoNumerico.length == 2) {
		return textoNumerico[0] + "." + textoNumerico[1];
	} else 
	if (textoNumerico.length == 3){
		return textoNumerico.slice(0,2) + "." + textoNumerico.slice(2)
	} else {
		return textoNumerico.slice(0,3) + "." + textoNumerico.slice(3)
	}

	
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
