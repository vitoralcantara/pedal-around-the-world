
/*
Faz o bind de eventos para os campos que devem ser mascarados.
*/

$(document).ready(function(){
    $("form#processo_form input#id_numero").keypress(function(){
        mascara(this, mascara_processo);
    });
});
