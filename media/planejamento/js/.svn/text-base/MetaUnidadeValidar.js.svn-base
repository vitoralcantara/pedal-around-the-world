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

$(document).ready(function(){
	// Função para gerar a soma automática
	somar = function(quadro) {
		var total = 0;

		quadro.find(".col_valor").each(function() {
			total += Number($(this).text().replace('.', '').replace(',', '.'));
		})
		quadro.find(".col_valor_total").html(formataValor(total));
	}

	$(function(){
		$.each($.find("#dados_acao_validada"), function(index, item) {
			somar($(this));
		});
		
		$.each($.find("#dados_acao_pendente"), function(index, item) {
			somar($(this));
		});
	})
	
	// Função para esconder as ações de acordo com o ChechBox id_check_mostrar_validadas
	esconder_acoes_validadas = function() {
		$.each($.find("#dados_acao_validada"), function(index, item) {
			if (!$("#id_check_mostrar_validadas").val()) {
				$(this).hide().show("slow");
			} else {
				$(this).show().hide("slow");
			}
		});
	}
	
	$("#id_check_mostrar_validadas").click(esconder_acoes_validadas);
	esconder_acoes_validadas();

	// Função para submeter dados ao SUAP	
	deferir_indeferir = function() {
		box = $(this).parent().parent();
		id_acao_pk = box.find("#id_acao_pk").val();
		tipo_acao_pk = "I";

		if ($(this).val() == "Deferir") {
			tipo_acao_pk = "D";
		}

		$.ajax({
			 type: "POST",
			 url: "/planejamento/ajax/acao/salvar/",
			 data: {id_acao: id_acao_pk, tipo_acao: tipo_acao_pk},
			 dataType: "json",
				 success: function(response) {
				 	if (response.situacao) {
						box.find("#id_butoes_box").hide();
						box.attr('id', 'dados_acao_validada');
						
						if (tipo_acao_pk == 'D') {
							box.find("#id_circulo_img").attr('src', '/media/img/green-circle.png');
						} else {
							box.find("#id_circulo_img").attr('src', '/media/img/red-circle.png');
						}
						
						if ($("#id_check_mostrar_validadas").val()) {
							box.show().hide("slow");
						}		
					} else {
						alert("Deu Tilt.");						
					}
				}
		 });
	}	
	
	$.each($.find("#id_button_deferir"), function(index,item) {
		$(this).click(deferir_indeferir);
	});
	
	$.each($.find("#id_button_indeferir"), function(index,item) {
		$(this).click(deferir_indeferir);
	});
	
	// Função para voltar a validação das metas
	$.each($.find("#id_button_voltar"), function(index,item) {
		$(this).click(function(){
			location = "/planejamento/meta/validar/";
		});
	});
})