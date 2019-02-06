function formataValor(valor) {
    valor = '' + valor.toFixed(2);
    x = valor.split('.');
    x1 = x[0];
    x2 = x.length > 1 ? ',' + (x[1].length >= 2 ? x[1] : x[1] + '0') : ',00';
    var rgx = /(\d+)(\d{3})/;
    while (rgx.test(x1)) {
        x1 = x1.replace(rgx, '$1' + '.' + '$2');
    }
    return x1 + x2;
}

function total() {
	qtd = $("#id_quantidade").val();
	vlr = $("#id_valor_unitario").val();
		
	if (qtd.length > 0 && vlr.length > 0) {
		$("#id_valor_total").val(formataValor(Number(qtd) * Number(vlr.replace('.','').replace(',','.'))));
	} else {
		$("#id_valor_total").val('');
	} 
}

function ocultarExibirForm() {
	$("#acaoproposta_form").parent().toggle();
	$("#btn_cadastrar").toggle();
	$("#btn_reset_forms").toggle();
}

$(document).ready(function(){
	$("#btn_cadastrar").click(function(){
		ocultarExibirForm();
	});
	
	$("#btn_reset_forms").click(function(){
		ocultarExibirForm();
	});
	
	$("#id_quantidade").change(function(){
		total();
	});
	
	$("#id_valor_unitario").change(function(){
		total()
	});
	
	$(function() {
		var total = 0;
		$(".col_valor").each(function() {
			total += Number($(this).text().replace('.', '').replace(',', '.'));
		})
		$(".col_valor_total").html(formataValor(total));
	});
	
	total();
})