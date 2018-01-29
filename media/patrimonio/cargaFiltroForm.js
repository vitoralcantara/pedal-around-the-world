/**
 * @author dennel
 */

$(document).ready(function(){
	
	$("#id_campus").change(function(){
		form = $("form[name=formUO]");
		form.submit();
	})
	
})