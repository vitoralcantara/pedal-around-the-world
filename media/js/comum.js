$(document).ready(function() {
	// remove o label padrão do django
   	$('input.labeless').prev().remove();
	$('input.labeless').next().addClass('help_marginless');
	$('input.labeless').next().removeClass('help');
	
	// adicionar uma cor padrão que indica que os campos estão desabilitados
	$('input[readonly=true]').css('background-color', '#eee');
	$('textarea[readonly=true]').css('background-color', '#eee');
		
	// reseta o formulário da página
	$('#btn_reset_forms').click(function () {
		$('form').each(function() {
			this.reset();
		});
	});
});

