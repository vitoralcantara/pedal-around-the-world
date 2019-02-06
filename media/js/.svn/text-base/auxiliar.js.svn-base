
function check_item(checkbox, focus_element, toggle_enable_inputs) {
	/*
	 * Adiciona a classe highlight na TR pai do ``checkbox``.
	 * ``focus_element`` elemento que terá o foco após checkar.
	 * ``toggle_enable_inputs`` alterna o atributo "disabled" dos inputs.
	 */
	focus_element = focus_element || null;
    toggle_enable_inputs = toggle_enable_inputs || false;
	if (checkbox.checked) {
		$(checkbox).parents("tr").addClass("highlight");
		if (toggle_enable_inputs) {
			$(checkbox).parents("tr").find(":input[type!=checkbox]").attr("disabled", false);
		}
		if (focus_element) {
			focus_element.focus();
		}
	}
	else {
		$(checkbox).parents("tr").removeClass("highlight");
		if (toggle_enable_inputs) {
			$(checkbox).parents("tr").find(":input[type!=checkbox]").attr("disabled", true);			
		}
	}
}

function mostrar_totais(args) {
    /*
     * ``valores``: lista de valores (cada item deve ter atributo "value")
     * ``qtds``: lista de quantidades (cada item deve ter atributo "value")
     * ``alvos_parciais``
     * ``alvo_final``
    */
    var valor_total = 0.00;
    for (var i=0; i<args.valores.length; i++) {
        valor = $(args.valores.eq(i)).attr("value");
        qtd = $(args.qtds.eq(i)).attr("value");
        if (valor == null || valor == "" || qtd == null || qtd == "") {
            if (args.alvos_parciais != null) {
                args.alvos_parciais.eq(i).html("0,00");
            }
        } else {
            valor_parcial = (parseFloat(mask_numbers(valor))/100) * parseFloat(qtd);
            if (args.alvos_parciais != null) {
                args.alvos_parciais.eq(i).html(mask_cash(valor_parcial.toFixed(2))+"");
            }
            valor_total += valor_parcial;
        }
    }
    valor_final = mask_cash(valor_total.toFixed(2))+"";
    if (args.alvo_final != null) {
        args.alvo_final.attr("value", valor_final);
        args.alvo_final.html(valor_final);
    }
    return valor_final;
};

function marcar(elem) {
    /*
    Adiciona ou remove classe highlight no primeiro ancestral tr.
    */
    elem = $(elem);
    if (elem.attr("checked") == true) {
        elem.parents("tr:first").addClass("highlight");
    } else {
        elem.parents("tr:first").removeClass("highlight");
    }
}

/*
add_item = function(button, container_id, tipo_material, onclick) {
    
    //utilizada na tela de edição de empenho.
    
    var container = $("#"+container_id);
    if (container.css("display") == "block" && $("#"+container_id+" table").length >= 1) {
        container.hide();
        $(button).html("(Adicionar)");
        return;
    }
    var container = $("#"+container_id);
    if ($("#"+container_id+" table").length == 0) {
        container.append("<form><table><tr'><td id='td_item'></td>"+
	        "<td><input type='text' style='width: 350px' name='item' id='item' value=''/></td>"+
	        "<td>Qtd: <input type='text' name='qtd' size='5' maxlength='5' onkeypress='mascara(this,somenteNumeros)'/></td>"+
	        "<td>R$: <input type='text' name='preco' size='11' maxlength='12' onkeypress='mascara(this,mascara_dinheiro)'/></td></tr>"+
            "<tr id='tr_descricao'><td align='right'>Descrição:</td><td colspan = '5'><textarea class='input_text' rows='1' cols='80' name='descricao'></textarea></td></tr></table></form>");
        if (tipo_material == 'permanente') {
            $('#td_item').html('ED:');
            $("input[name=item]").autocomplete("/buscar_categoriamaterialpermanente/");
	    } 
        else if (tipo_material == 'consumo') {
            $('#tr_descricao').hide();
            $('#td_item').html('Material:');
            $("input[name=item]").autocomplete("/buscar_materialconsumo/", {"minChars": 3});
        }
        container.append("<input style='margin-top: 0px; margin-bottom: 10px' type='button' value='Salvar' onclick='"+onclick+"'/>");
    }
    container.show();
    $(button).html("(Cancelar adição)");
};
*/


function ismaxlength(obj){
    var mlength=obj.getAttribute? parseInt(obj.getAttribute("maxlength")) : ""
    if (obj.getAttribute && obj.value.length>mlength)
    obj.value=obj.value.substring(0,mlength)
}

getDataHoje = function() {
    data = new Date();
    var dia = data.getDate() + "";
    var mes = parseInt(data.getMonth()+1) + ""
    var ano = data.getFullYear();
    if (dia.length == 1) {
        dia = "0" + dia;
    }
    if (mes.length == 1) {
        mes = "0" + mes;
    }
    return dia+"/"+mes+"/"+ano;
};

atualizarValorTotal = function() { //ATUALIZA O VALOR POR ITEM E O VALOR TOTAL NA ENTRADA
    var valorTotal = 0.00;
    var existeItemIncompleto = false;
    for (numero=0; numero<divItensNumeroItens(); numero++) {
        qtd = $("#qtd_"+numero).attr("value");
        valor = $("#preco_"+numero).attr("value");
        if (qtd == null || valor == null) {
            $("span#valor_item_"+numero).html("0,00");
            $("span#valor_total").html("0,00");
            existeItemIncompleto = true;
        } else {
            valorItem = (parseFloat(somenteNumeros(valor))/100) * parseFloat(qtd);
            $("span#valor_item_"+numero).html(mascara_dinheiro(valorItem.toFixed(2))+"");
            valorTotal += valorItem;
        }
    }
    if (!existeItemIncompleto) {
        $("span#valor_total").html(mascara_dinheiro(valorTotal.toFixed(2))+"");
    }
};



function atualizarValorTotalNovo() { //ATUALIZA O VALOR POR ITEM E O VALOR TOTAL NA ENTRADA
	var valorTotal = 0.00;
	var existeItemIncompleto = false;
	for (numero=0; numero <= numeroUltimoItem(); numero++) {
	if ( $("div#item_"+numero).length != 0 ){ //caso o item exista na relacao
		qtd = $("#qtd_"+numero).attr("value");
		valor = $("#preco_"+numero).attr("value");
		if (qtd == null || valor == null) {
			$("#total_"+numero).attr("value","0,00");
			$("span#valor_total").html("0,00");
			existeItemIncompleto = true;
		} else {
			valorItem = (parseFloat(somenteNumeros(valor))/100) * parseFloat(qtd);
			$("#total_"+numero).attr("value",mascara_dinheiro(valorItem.toFixed(2))+"");
			valorTotal += valorItem;
		}
	}
	}
	if (!existeItemIncompleto) {
		$("span#valor_total").html(mascara_dinheiro(valorTotal.toFixed(2))+"");
	}
}


atualizarValorTotalCombustivel = function() { //ATUALIZA O VALOR TOTAL DO COMBUSTIVEL
    var qtd = $("#qtd").attr("value");
    var valor = $("#vl_unit").attr("value");
    if (qtd == null || valor == null) {
        $("#total").attr("value","0,00");
    } else {
        valorItem = (parseFloat(somenteNumeros(valor))/100) * parseFloat(qtd);
        $("#total").attr("value",mascara_dinheiro(valorItem.toFixed(2))+"");
    }
};


atualizarValorTotalManutencao = function() { //ATUALIZA O VALOR POR ITEM E O VALOR TOTAL DA MANUTENCAO
    var valorTotal = 0.00
    for (numero=1; numero <= numeroUltimoItem(); numero++) {
	 	if ( $("div#item_"+numero).length != 0 ){ //caso o item exista na relacao
			valor = $("#preco_"+numero).attr("value")
			if (valor == null) {
		    	valorItem = 0
			} else {
		   	valorItem = (parseFloat(somenteNumeros(valor))/100)
			}
		   valorTotal += valorItem;
		}
		var valorTotalPeca = 0.00
      for (numeropeca=1; numeropeca <= numeroUltimoItemPeca(numero); numeropeca++) {
	   	if ( $("tr#item_peca_"+numero+"_"+numeropeca).length != 0 ){ //caso o item exista na relacao
		     valorpeca = $("#total_peca_"+numero+"_"+numeropeca).attr("value")
		     if (valorpeca == null) {
		        valorItemPeca = 0
		     } else {
		        valorItemPeca = (parseFloat(somenteNumeros(valorpeca))/100)
		     }
		     valorTotalPeca += valorItemPeca
		   }
	   }
	   valorTotal = valorTotal + valorTotalPeca
    }
    $("span#valor_total").html(mascara_dinheiro(valorTotal.toFixed(2))+"")
};


atualizarValorTotalPeca = function(numeroItem) { //ATUALIZA O VALOR POR ITEM E O VALOR TOTAL DA MANUTENCAO
    var valorTotal = 0.00;
    var existeItemIncompleto = false;
    for (numero=0; numero <= numeroUltimoItemPeca(numeroItem); numero++) {
	   if ( $("tr#item_peca_"+numeroItem+"_"+numero).length != 0 ){ //caso o item exista na relacao
		  qtd = $("#qtd_peca_"+numeroItem+"_"+numero).attr("value");
		  valor = $("#preco_peca_"+numeroItem+"_"+numero).attr("value");
		  if (valor == null) {
		    $("#total_peca_"+numeroItem+"_"+numero).attr("value","0,00");
		    $("span#valor_total_peca_"+numeroItem).html("0,00");
		    existeItemIncompleto = true;
		  } else {
		    valorItem = (parseFloat(somenteNumeros(valor))/100) * parseFloat(qtd);
		    $("#total_peca_"+numeroItem+"_"+numero).attr("value",mascara_dinheiro(valorItem.toFixed(2))+"");
		    valorTotal += valorItem;
		  }
	   }
    }
    if (!existeItemIncompleto) {
        $("span#valor_total_peca_"+numeroItem).html(mascara_dinheiro(valorTotal.toFixed(2))+"");
    }
    atualizarValorTotalManutencao();
};

setHighlight = function(elementId, checked) {
	if (checked) {
		$("#"+elementId).addClass("highlight");
	} else {
		$("#"+elementId).removeClass("highlight");
	}
};

checkQuantidade = function(id) {
	qtd = document.getElementById("qtd"+id);
	if (document.getElementById("cb"+id).checked) {		
		qtd.removeAttribute("disabled");
		qtd.focus()
	} else {
		qtd.setAttribute("disabled", "");
	}
};

showDestino = function(bool) {	
	if (!bool) {
		document.getElementById("tr_destino").style.display = "none";
	}
	else {
		document.getElementById("tr_destino").style.display = "table-row";
	}
};


/* ==========
   SUAP: Entrada
============= */

setTipoEntrada = function(item) {
	tipo = item.value;
	if (tipo == "compra") {
        $("#radio_recursoproprio").click();
        $("#tr_origemrecurso").css("display", "table-row");
        $("#tr_numeronotafiscal").css("display", "table-row");
		$("#tr_datanotafiscal").css("display", "table-row");
		$("#tr_empenho").css("display", "table-row");
	}
	else if (tipo == "doacao") {
            $("#tr_origemrecurso").css("display", "none");
			$("#tr_projetoespecial").css("display", "none");
            $("#tr_numeronotafiscal").css("display", "none");
			$("#tr_datanotafiscal").css("display", "none");
			$("#tr_empenho").css("display", "none");			
    }
};

setOrigemRecurso = function(item) {
    tipo = item.value;
    if (tipo == 'proprio') {
        $("#tr_projetoespecial").css("display", "none");
    } else if (tipo == 'projetoespecial') {
        $("#tr_projetoespecial").css("display", "table-row");
    }
};

limparItens = function() {
    $("div#itens").remove();
    $("<div id='itens' style='display: none'></div>").insertBefore($("div#addItem"));
};

setTipoMaterial = function(tipo) {
    if ($("#tipoMaterial").attr("value") != null) {
        limparItens();
    }
    $("#tipoMaterial").attr("value", tipo);
};

setTipoMaterialNovo = function(tipo) {

	if ($("#tipoMaterial").attr("value") != null) {
		$("#tipoMaterial").attr("value", tipo);
		limparItensNovo();
	}
	else{
		$("#tipoMaterial").attr("value", tipo);
	}

	var container = $("<fieldset class='module aligned'>"+
			  "<h2>Materiais:</h2>"+
			  "<div id ='total' class='inline-related'><h3><a href='#addItem' name='addItem' class='addlink' onclick='addItemMaterial()'>Adicionar</a> <span style='padding-left:340px'>Valor Total:<span style='padding-left:15px' id='valor_total'></span></span></h3></div>"+
			  "</fieldset>");
	container.appendTo($("div#Itens"));
	addItemMaterial();
};

removeItemMaterial = function(div_id){
	if (divItensNumeroItensNovo()>1) {
		$("div#Itens > fieldset > div#"+div_id).remove();
		atualizarValorTotalNovo();
	}
};

limparItensNovo = function() {
    $("div#Itens").empty();
};

numeroUltimoItem = function(){
	if (divItensNumeroItensNovo()>0) {
		return parseInt( $("div#Itens > fieldset > div.form-row:last").attr("ordem") );
	}
	return 0	
};

numeroUltimoItemPeca = function(numeroItem){
	if (divItensNumeroItensPecasNovo(numeroItem)>0) {
		return parseInt( $("div#ItensPecas_"+numeroItem+" > fieldset > table > tbody > tr.form-row:last").attr("ordem") );
	}
	return 0	
};

addItemMaterial = function() {
	$("div#Itens").attr("style", "visibility: visible");
	var numeroItem = numeroUltimoItem() + 1;
	var tipoMaterial = $("#tipoMaterial").attr("value");
	if (tipoMaterial == 'consumo') { //Materiais de Consumo
		var item = $("<div class='form-row' id='item_"+numeroItem+"'>"+
			  "<label>Material:</label>"+
			  "<input type='text' id='material_"+numeroItem+"' name='itens' value='' />"+
			  "<div>"+
			    "<label>Quantidade:</label>"+
			    "<input name='quantidades' id='qtd_"+numeroItem+"' type='text' maxlength='6' size='5'/>"+
			    "<label class='inline'>Valor Unitário (R$):</label>"+
			    "<input name='precos' id='preco_"+numeroItem+"' maxlength='12' type='text' size='10'/>"+
			    "<label class='inline'>Total (R$):</label>"+
			    "<input name='totais' id='total_"+numeroItem+"' maxlength='12' type='text' readonly='readonly' size='10'/>"+
			    "<label class='inline'><a href='#item_"+numeroItem+"' class='deletelink' onclick='removeItemMaterial(\"item_"+numeroItem+"\")'>Remover</a></label>"+
			  "</div>"+
			"</div>");
		$("div#Itens > fieldset > div#total").before(item);
		$("#item_"+numeroItem).attr("ordem",numeroItem); //setando a ordem
		$("#qtd_"+numeroItem).attr("onkeyup", "atualizarValorTotalNovo()"); //setando o onkeyup
		$("#qtd_"+numeroItem).attr("onkeypress", "mascara(this,somenteNumeros)"); //setando o onkeyup
		$("#preco_"+numeroItem).attr("onkeyup", "atualizarValorTotalNovo()"); //setando o onkeyup
		$("#preco_"+numeroItem).attr("onkeypress", "mascara(this,mascara_dinheiro)"); //setando o onkeyup
		$("#material_"+numeroItem).autocomplete("/buscar_materialconsumo/", {"minChars": 3}); //setando o autocomplete
	}
	else if(tipoMaterial == 'permanente') { //Materiais Permanente
		var item = $("<div class='form-row' id='item_"+numeroItem+"'>"+
			  "<label>ED:</label>"+
			  "<input type='text' id='ed_"+numeroItem+"' name='itens' value='' />"+
			  "<div>"+
			    "<label>Descrição:</label>"+
			    "<textarea rows='2' cols='64' name='descricoes'></textarea>"+
			    "<label class='inline'><a href='#item_"+numeroItem+"' class='deletelink' onclick='removeItemMaterial(\"item_"+numeroItem+"\")'>Remover</a></label>"+
			  "</div>"+
			  "<div>"+
			    "<label>Quantidade:</label>"+
			    "<input name='quantidades' id='qtd_"+numeroItem+"' type='text' maxlength='6' size='5'/>"+
			    "<label class='inline'>Valor Unitário (R$):</label>"+
			    "<input name='precos' id='preco_"+numeroItem+"' maxlength='12' type='text' size='10'/>"+
			    "<label class='inline'>Total (R$):</label>"+
			    "<input name='totais' id='total_"+numeroItem+"' maxlength='12' type='text' readonly='readonly' size='10'/>"+
			  "</div>"+
			"</div>");
		$("div#Itens > fieldset > div#total").before(item);
		$("#item_"+numeroItem).attr("ordem", numeroItem); //setando a ordem
		$("#qtd_"+numeroItem).attr("onkeyup", "atualizarValorTotalNovo()"); //setando o onkeyup
		$("#qtd_"+numeroItem).attr("onkeypress", "mascara(this,somenteNumeros)"); //setando o onkeypress
		$("#preco_"+numeroItem).attr("onkeyup", "atualizarValorTotalNovo()"); //setando o onkeyup
		$("#preco_"+numeroItem).attr("onkeypress", "mascara(this,mascara_dinheiro)"); //setando o onkeypress
		$("#ed_"+numeroItem).autocomplete("/buscar_categoriamaterialpermanente/"); //setando o autocomplete
	}
};

entradaAddItem = function() {
    if ($("#tipoMaterial").attr("value") == null) {
        alert("O tipo de Material deve ser escolhido");
        return;
    }
    $("div#itens").attr("style", "visibility: visible");
    var numeroItem = divItensNumeroItens();
	var tipoMaterial = $("#tipoMaterial").attr("value");
	var table = $("<table id='table_item_"+numeroItem+"' width='100%'></table>");
	if (divItensNumeroItens() > 0) { //adicionando o separador
		$("<tr><td colspan='10'><hr /></td></tr>").appendTo(table);
	}
	table.appendTo($("div#itens"));
	if (tipoMaterial == 'permanente') { //Material Permanente
        var trItem = $("<tr><td width='60px' align='right'>ED:</td>"+
		"<td><input type='text' class='input_text' id='item_"+numeroItem+"' name='itens' value=''/></td>"+
		"<td>Qtd: <input type='text' class='input_text' name='quantidades' id='qtd_"+numeroItem+"' size='5' maxlength='5' /></td>"+
		"<td>R$: <input type='text' class='input_text' name='precos' id='preco_"+numeroItem+"' size='11' maxlength='12' onkeypress='mascara(this,mascara_dinheiro)'/></td>"+
        "<td align='right' style='padding-right: 5px'><span style='font-weight: bold' id='valor_item_"+numeroItem+"'></span></td>"+"<span onclick='retirarItem()'>&nbsp;&nbsp;");
        trItem.appendTo(table);
        var trObs = $("<tr><td align='right'>Descrição:</td><td colspan = '5'><textarea class='input_text' rows='1' cols='90' name='descricoes'></textarea></td></tr>");
        trObs.appendTo(table);
        $("#qtd_"+numeroItem).attr("onkeyup", "atualizarValorTotal()"); //setando o onkeyup
        $("#qtd_"+numeroItem).attr("onkeypress", "mascara(this,somenteNumeros)"); //setando o onkeyup
        $("#preco_"+numeroItem).attr("onkeyup", "atualizarValorTotal()"); //setando o onkeyup
        $("#item_"+numeroItem).autocomplete("/buscar_categoriamaterialpermanente/"); //setando o autocomplete
	} else if (tipoMaterial == 'consumo') { //Material Consumo
        var trItem = $("<tr><td width='60px' align='right'>Material:</td>"+
		"<td><input type='text' class='input_text' id='item_"+numeroItem+"' name='itens' value=''/></td>"+
		"<td>Qtd: <input type='text' class='input_text' name='quantidades' id='qtd_"+numeroItem+"' size='5' maxlength='5' onkeypress='mascara(this,somenteNumeros)'/></td>"+
		"<td>R$: <input type='text' class='input_text' name='precos' id='preco_"+numeroItem+"' size='11' maxlength='12' onkeypress='mascara(this,mascara_dinheiro)'/></td>"+
        "<td align='right' style='padding-right: 5px'><span style='font-weight: bold' id='valor_item_"+numeroItem+"'></span></td>"+"<span onclick='retirarItem()'>&nbsp;&nbsp;");
        trItem.appendTo(table);
        $("#qtd_"+numeroItem).attr("onkeyup", "atualizarValorTotal()"); //setando o onkeyup
        $("#preco_"+numeroItem).attr("onkeyup", "atualizarValorTotal()"); //setando o onkeyup
        $("#item_"+numeroItem).autocomplete("/buscar_materialconsumo/", {"minChars": 3}); //setando o autocomplete
    }
};


/* ==========
   ALMOXARIFADO: Requisição
============= */

almox_req_add_item = function(url_autocomplete) {
    var numeroItem = divItensNumeroItens();
    var table = $("<table id='table_item_"+numeroItem+"'></table>");
    if (divItensNumeroItens() > 0) { //adicionando o separador
	$("<tr><td colspan='10'><hr /></td></tr>").appendTo(table);
    }
    table.appendTo($("div#itens"));
    var trItem = $("<tr><td>Material:</td>"+
	    	   "<td><input type='text' class='input_text' id='item_"+numeroItem+"' name='itens' value=''/>"+
	 	   "<td>Qtd:</td><td><input type='text' class='input_text' name='quantidades' size='5' maxlength='5' onkeypress='mascara(this,somenteNumeros)'/></td></tr>");
    trItem.appendTo(table);
    $("#item_"+numeroItem).autocomplete(url_autocomplete, {"minChars": 3}); //setando o autocomplete	
};


/* ==========
   PATRIMÔNIO: Movimento Baixa
============= */

patrimBaixaAddItem = function() {
	var numeroItem = divItensNumeroItens();
	var table = $("<table id='table_item_"+numeroItem+"' width='100%'></table>");
	if (divItensNumeroItens() > 0) { //adicionando o separador
		$("<tr><td colspan='10'><hr /></td></tr>").appendTo(table);
	}
	table.appendTo($("div#itens"));
	var trItem = $("<tr><td width='60px'>Inventário:</td>"+
		"<td><input type='text' class='input_text' id='item_"+numeroItem+"' name='itens' value=''/></td></tr>");
	trItem.appendTo(table);
	$("#item_"+numeroItem).autocomplete("/buscar_inventario_ativo/"); //setando o autocomplete
};


/* ==========
   PATRIMÔNIO: Requisição
============= */

patrimReqAddItem = function() {
	var numeroItem = divItensNumeroItens();
	var table = $("<table id='table_item_"+numeroItem+"' width='100%'></table>");
	if (divItensNumeroItens() > 0) { //adicionando o separador
		$("<tr><td colspan='10'><hr /></td></tr>").appendTo(table);
	}
	table.appendTo($("div#itens"));
	//linha que contém o item
	var trItem = $("<tr><td width='60px'>Inventário:</td>"+
		"<td><input type='text' class='input_text' id='item_"+numeroItem+"' name='itens' value=''/></td></tr>");
	trItem.appendTo(table);
	$("#item_"+numeroItem).autocomplete("/buscar_inventario_ativo_usuario/"+$("#solicitante_hidden").val()+"/"); //setando o autocomplete
};


/* ==========
   Funções Auxiliares na Adição e Remoção de Itens
============= */

retirarItem = function() {
	if (divItensNumeroItens()>1) {
		$("div#itens > table").eq(divItensNumeroItens()-1).remove();
	}
};

divItensNumeroItens = function() { //retorna o número de itens do #div_itens
	return $("div#itens > table").length;
};

divItensNumeroItensNovo = function() { //retorna o número de itens do #div_Itens
	return $("div#Itens > fieldset > div.form-row").length;
};

divItensNumeroItensPecasNovo = function(numeroItem) { //retorna o número de itens do #div_Itens
	return $("div#ItensPecas_"+numeroItem+" > fieldset > table > tbody > tr.form-row").length;
};

function somar_valores(args) {
    /*
    Obrigatório: valor(name).
    Opcionais: qtd(name), alvos_parciais(lista de objetos), alvo_final(objeto).
    */
    var valor_total = 0.00;
    var existe_item_incompleto = false;
    valores = $("input[name="+args.valor+"]");
    if (args.qtd != null) {
        qtds = $("input[name="+args.qtd+"]");
    } else {
        qtds = null;
    }
    for (var i=0; i<valores.length; i++) {
        valor = valores.eq(i).attr("value");
        if (qtds != null) {
            qtd = qtds.eq(i).attr("value");
        } else {
            qtd = 1;
        }
        if (valor == null || (qtds != null && qtd == null)) {
            if (args.alvos_parciais != null) {
                args.alvos_parciais.eq(i).html("0,00");
            }
            //existe_item_incompleto = true; //com o comentario, o alvo_final sempre vai ser preenchido (mesmo havendo itens incompletos).
        } else {
            valor_parcial = (parseFloat(mask_numbers(valor))/100) * parseFloat(qtd);
            if (args.alvos_parciais != null) {
                args.alvos_parciais.eq(i).html(mask_cash(valor_parcial.toFixed(2))+"");
            }
            valor_total += valor_parcial;
        }
    }
    valor_final = mask_cash(valor_total.toFixed(2))+"";
    if (!existe_item_incompleto) {
        if (args.alvo_final != null) {
            args.alvo_final.attr("value", valor_final);
            args.alvo_final.html(valor_final);
        }
    }
    return valor_final;
};

function montar_itens() {
    $("div#itens table").remove();
	html = "<table id='table_item_0'><tr><td>Material:</td><td><input type='text' id='item_0' name='itens' class='input_text' /></td><td>Qtd:</td><td><input type='text' name='quantidades' class='input_text' size='5' maxlength='5' onkeypress='mascara(this, somenteNumeros)' /></td></tr></table>"
	$("div#itens").append(html)
	createAutoComplete("item_0", "/buscar_material_consumo_estoque_uo/"+$("[name=uo_id]").attr("value")+"/");
    };


/* ==========
   Frota: Itens de serviço de manutenção
============= */
removeItemServico = function(div_id){
	if (divItensNumeroItensNovo()>1) {
		$("div#Itens > fieldset > div#"+div_id).remove();
		atualizarValorTotalNovo();
	}
};

removeItemPeca = function(numeroItem,div_id){
	if (divItensNumeroItensPecasNovo(numeroItem)>1) {
		$("div#ItensPecas_"+numeroItem+" > fieldset > table > tbody > tr#"+div_id).remove();
		atualizarValorTotalPeca();
	}
};

addItemServico = function() {
	$("div#Itens").attr("style", "visibility: visible");
	var numeroItem = numeroUltimoItem() + 1;
	var item = $("<div class='form-row' id='item_"+numeroItem+"'>"+
		  "<label>Serviço:</label>"+
		  "<input type='text' id='servico_"+numeroItem+"' name='servico_itens_"+numeroItem+"' value='' />"+
		  "<label class='inline'>Valor da Mão de Obra (R$):</label>"+
		  "<input name='servico_precos_"+numeroItem+"' id='preco_"+numeroItem+"' maxlength='12' type='text' size='10'/>"+
	     "<label class='inline'><a href='#item_"+numeroItem+"' class='deletelink' onclick='removeItemServico(\"item_"+numeroItem+"\")'>Remover Serviço</a></label>"+
	     "<div id='ItensPecas_"+numeroItem+"'></div>"+
		"<hr style='color: #5B80B2; background-color: #5B80B2; height: 3px;'/></div>");
	$("div#Itens > fieldset > div#total").before(item);
	$("#item_"+numeroItem).attr("ordem",numeroItem); //setando a ordem
	$("#preco_"+numeroItem).attr("onkeyup", "atualizarValorTotalManutencao()"); //setando o onkeyup
	$("#preco_"+numeroItem).attr("onkeypress", "mascara(this,mascara_dinheiro)"); //setando o onkeyup
	$("#servico_"+numeroItem).autocomplete("/buscar_tiposervico/", {"minChars": 3}); //setando o autocomplete
	var container = $("<fieldset class='module aligned'>"+
			  "<h2>Peças:</h2>"+
			  "<table id='Tabela_Pecas_"+numeroItem+"'><tr><th>Peça</th><th>Quantidade</th><th>Valor Unitário (R$)</th><th>Total (R$)</th><th>&nbsp;</th></tr></table>"+
			  "<div id ='totalpecas' class='inline-related'><h3><a href='#addItemPeca' name='addItemPeca' class='addlink' onclick='addItemPeca("+numeroItem+")'>Adicionar Peça</a> <span style='padding-left:440px'>Valor Total das Peças:<span style='padding-left:15px' id='valor_total_peca_"+numeroItem+"'></span></span></h3></div>"+
			  "</fieldset>");
	container.appendTo($("div#ItensPecas_"+numeroItem));
	addItemPeca(numeroItem);
};

addItemPeca = function(numeroItem) {
	$("div#Itens").attr("style", "visibility: visible");
	var numeroItemPeca = numeroUltimoItemPeca(numeroItem) + 1;
	var itempeca = $("<tr class='form-row' id='item_peca_"+numeroItem+"_"+numeroItemPeca+"'>"+
		  "<td><input type='text' id='peca_"+numeroItem+"_"+numeroItemPeca+"' name='peca_itens_"+numeroItem+"' value='' /></td>"+
		  "<td><input name='peca_quantidades_"+numeroItem+"' id='qtd_peca_"+numeroItem+"_"+numeroItemPeca+"' type='text' maxlength='6' size='5'/></td>"+
	     "<td><input name='peca_precos_"+numeroItem+"' id='preco_peca_"+numeroItem+"_"+numeroItemPeca+"' maxlength='12' type='text' size='10'/></td>"+
		  "<td><input name='peca_totais_"+numeroItem+"' id='total_peca_"+numeroItem+"_"+numeroItemPeca+"' maxlength='12' type='text' readonly='readonly' size='10'/></td>"+
		  "<td><label class='inline'><a href='#item_peca_"+numeroItem+"_"+numeroItemPeca+"' class='deletelink' onclick='removeItemPeca("+numeroItem+",\"item_peca_"+numeroItem+"_"+numeroItemPeca+"\")'>Remover Peça</a></label></td>"+
		"</tr>");
	$("table#Tabela_Pecas_"+numeroItem).append(itempeca);
	$("#item_peca_"+numeroItem+"_"+numeroItemPeca).attr("ordem",numeroItemPeca); //setando a ordem
	$("#preco_peca_"+numeroItem+"_"+numeroItemPeca).attr("onkeyup", "atualizarValorTotalPeca("+numeroItem+")"); //setando o onkeyup
	$("#preco_peca_"+numeroItem+"_"+numeroItemPeca).attr("onkeypress", "mascara(this,mascara_dinheiro)"); //setando o onkeyup
	$("#peca_"+numeroItem+"_"+numeroItemPeca).autocomplete("/buscar_pecareposicao/", {"minChars": 3}); //setando o autocomplete
};
