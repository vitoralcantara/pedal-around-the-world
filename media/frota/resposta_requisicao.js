/**
 * @author hugo
 */

$(document).ready(function(){
	if($("input[name=status]:checked").val() == undefined){
		$("#id_status_0").attr('checked', true);
	}
	if($("input[name=status]:checked").val() == "Aceita"){
		$("#id_status_0").attr('checked', true);
		$("select[name=viatura]").parent().parent().show();
	}
	if($("input[name=status]:checked").val() == "Recusada"){
		$("#id_status_1").attr('checked', true);
		$("select[name=viatura]").parent().parent().hide();				
	}
	$("#id_status_0").change(function(){		
		$("select[name=viatura]").parent().parent().show();
		//clean_value($(this).prev().prev())
				
	});
	$("#id_status_1").change(function(){
		//clean_value($("input[name=viatura]").prev().prev())
		$("select[name=viatura]").val([""]);
		$("select[name=viatura]").removeClass("filled");
		$("select[name=viatura]").next().hide();
		$("select[name=viatura]").parent().parent().hide();		
	});	
})
