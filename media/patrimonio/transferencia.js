/**
 * @author henrique
 */

$(document).ready(function(){
	
	if($("input[name=transferencia_tipo]:checked").val() == undefined){
		$("#id_transferencia_tipo_0").attr('checked', true);
	}
	if($("input[name=transferencia_tipo]:checked").val() == "inventario"){
		$("#id_transferencia_tipo_0").attr('checked', true);
		$("input[name=inventario]").parent().parent().show();
		$("input[name=carga_atual]").parent().parent().hide();
		$("input[name=rotulo]").parent().parent().hide();
	}		
	if($("input[name=transferencia_tipo]:checked").val() == "carga"){
		$("#id_transferencia_tipo_1").attr('checked', true);
		$("input[name=inventario]").parent().parent().hide();
		$("input[name=carga_atual]").parent().parent().show();
		$("input[name=rotulo]").parent().parent().hide();
	}
	if($("input[name=transferencia_tipo]:checked").val() == "rotulo"){
		$("#id_transferencia_tipo_2").attr('checked', true);
		$("input[name=inventario]").parent().parent().hide();
		$("input[name=carga_atual]").parent().parent().hide();
		$("input[name=rotulo]").parent().parent().show();
	}	
	
	$("#id_transferencia_tipo_0").change(function(){
		$("input[name=inventario]").parent().parent().show();
		$("input[name=carga_atual]").parent().parent().hide();
		$("input[name=rotulo]").parent().parent().hide();
	});
	
	$("#id_transferencia_tipo_1").change(function(){
		$("input[name=inventario]").parent().parent().hide();
		$("input[name=carga_atual]").parent().parent().show();
		$("input[name=rotulo]").parent().parent().hide();
	});
	
	$("#id_transferencia_tipo_2").change(function(){
		$("input[name=inventario]").parent().parent().hide();
		$("input[name=carga_atual]").parent().parent().hide();
		$("input[name=rotulo]").parent().parent().show();
	});
})