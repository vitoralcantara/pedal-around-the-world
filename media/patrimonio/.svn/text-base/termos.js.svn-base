/**
 * @author dennel
 */

$(document).ready(function(){
	$("label[for=id_periodo_de_movimento_ini]").parent().parent().hide();
    $("label[for=id_periodo_de_movimento_fim]").parent().parent().hide();
    
    if($("#id_tipo").val() == "recebimento"){
		$("label[for=id_periodo_de_movimento_ini]").parent().parent().show();
        $("label[for=id_periodo_de_movimento_fim]").parent().parent().show();
	}
	else{
		$("label[for=id_periodo_de_movimento_ini]").parent().parent().hide();
        $("label[for=id_periodo_de_movimento_fim]").parent().parent().hide();
	}
    
	$("#id_tipo").change(function(){
		if($("#id_tipo").val() == "recebimento"){
			$("label[for=id_periodo_de_movimento_ini]").parent().parent().show();
            $("label[for=id_periodo_de_movimento_fim]").parent().parent().show();
		}
		else{
			$("label[for=id_periodo_de_movimento_ini]").parent().parent().hide();
            $("label[for=id_periodo_de_movimento_fim]").parent().parent().hide();
		}
	})
})
   