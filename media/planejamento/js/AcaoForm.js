function ocultarExibirForm() {
	$("#acao_form").parent().toggle();
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
})
