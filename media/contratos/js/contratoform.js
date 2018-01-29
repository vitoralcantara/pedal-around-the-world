
$(document).ready(function(){
	
	// O empenho só é necessário se o contrato for de despesa, então este campo deverá aparecer como obrigatorio quando for despesa
	var empenho = $("label[for=id_empenho]").parent().parent()
	empenho.addClass("required");
	empenho.hide();
	
	// se não tiver empenho, então o processo passa a ser obrigatório
	var processo = $("label[for=id_processo]").parent().parent()
	processo.addClass("required");
	processo.hide();
	
	$("#id_tipo").change(function(){
		
		// caso essas regras sejam alteradas, verificar se tambem será necessário alterar o termoaditivoform.js
        var tipo = $("#id_tipo").val();
        // TODO arrumar um jeito de deixar esse valor dinamico, pegando do model Contrato.TIPO_DESPESA e similares
        switch (tipo) {
            case "Despesa":
                empenho.show();
                processo.hide();
                break;
            case "Receita": 
                empenho.hide();
                processo.show();
                break;
            default:
				// conferir ser o default deve ser exibir ou esconder os campos
                empenho.hide();
                processo.hide();
        }
	})
	
	$("#id_tipo").change();
})