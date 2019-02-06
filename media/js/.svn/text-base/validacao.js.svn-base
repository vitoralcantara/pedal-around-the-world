
/*
Este arquivo só será mantido enquando houver funções utilizando o "validate_and_submit".
O arquivo "validation.js" deve ser utilizado no lugar deste.
*/

validate_and_submit = function(validateUrl) {
    form = $("form");
    $.ajax({
        type: "POST",
        url: validateUrl,
        data: form.formSerialize(),
        dataType: "json",
        success: function(response) {
            if (!response.valid) {
                show_error(response);
            } else {
                form.submit();
            }
        }
    });
};

show_error = function(response) {
    $("ul.messagelist").remove();
    $("p.errornote").html(response.message);
    $("p.errornote").show();
    $(":input").removeClass("invalid");
    if (!response.field_in_list) {
        $("[name="+response.field_name+"]").addClass("invalid");
    } else {
        $("[name="+response.field_name+"]:enabled:eq("+response.field_index+")").addClass("invalid");
    }
    window.scroll(0, 0);
}

