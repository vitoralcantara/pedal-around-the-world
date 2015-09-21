
$(document).ready(function(){
	
	// O empenho s— Ž necess‡rio se o contrato for de despesa, ent‹o este campo dever‡ aparecer como obrigatorio quando for despesa
	var empenho = $("label[for=id_empenho]").parent().parent()
	empenho.addClass("required");
	empenho.hide();
	
	var processo = $("label[for=id_processo]").parent().parent()
	processo.addClass("required");
	processo.hide();
	
	$("#id_tipo").change(function(){
		
        var tipo = $("#id_tipo").val();
        // TODO arrumar um jeito de deixar esse valor dinamico, pegando do model Contrato.TIPO_DESPESA e similares
        switch (tipo) {
            case "1": // despesa
                empenho.show();
                processo.hide();
                break;
            case "2": // receita
                empenho.hide();
                processo.show();
                break;
            default:
                empenho.hide();
                processo.hide();
        }
	})
	
	$("#id_tipo").change();
})