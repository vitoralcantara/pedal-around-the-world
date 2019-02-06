/**
 * @author henrique
 */


$(document).ready(function(){
	if($("input[name=categoria]:checked").val() == undefined){
		$("#id_categoria_0").attr('checked', true);
	}
	if($("input[name=categoria]:checked").val() == "Viatura"){
		$("#id_categoria_0").attr('checked', true);
		$("input[name=inventario]").parent().parent().parent().show();
		$("#ajaxmultiselect_input_pessoas_add").parent().parent().parent().parent().parent().hide();
	}
	if($("input[name=categoria]:checked").val() == "VeiculoComum"){
		$("#id_categoria_1").attr('checked', true);
		$("#ajaxmultiselect_input_pessoas_add").parent().parent().parent().parent().parent().show();
		$("input[name=inventario]").parent().parent().parent().hide();		
	}
	
	$("#id_categoria_0").change(function(){
		$("input[name=inventario]").parent().parent().parent().show();
		$("#ajaxmultiselect_input_pessoas_add").parent().parent().parent().parent().parent().hide();
	});
	$("#id_categoria_1").change(function(){
		$("#ajaxmultiselect_input_pessoas_add").parent().parent().parent().parent().parent().show();
		$("input[name=inventario]").parent().parent().parent().hide();		
	});	
})
