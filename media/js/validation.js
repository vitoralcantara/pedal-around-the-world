
show_invalid = function(response) {
    $("div#msg_father").html(response.message);
    $(":input").removeClass("invalid");
    if (!response.field_in_list) {
        $("[name="+response.field_name+"]").addClass("invalid");
    } else {
        $("[name="+response.field_name+"]:enabled:eq("+response.field_index+")").addClass("invalid");
    }
    window.scroll(0, 0);
}

validate_submit = function(form, validation_url, after_validate, args) {
    $.ajax({
        type: "POST",
        url: validation_url,
        data: form.formSerialize(),
        dataType: "json",
        success: function(response) {
            if (!response.valid) {
                show_invalid(response);
            } else {
                after_validate(args);
            }
        }
    }); 
}

same_page_submit = function(options) {
    /*
    options:
     form: required; JQueryObject.
     container: required; JQueryObject.
     button: optional; DOMObject.
    */
    if (options.button != null && $("span.loading").length == 0) {
        $(options.button).after($("<span class='loading'>Carregando...</span>"));
    } else {
        $("span.loading").show();
    }
    $.ajax({type: "POST",
            url: options.form.attr("action"),
            data: options.form.formSerialize(),
            dataType: "text/html",
            success: function(response){
                $("span.loading").hide();
                options.container.html(response);
            }
    });
}

default_submit = function(options) {
    /*
    options:
     form: required; JQueryObject.
     container: required; JQueryObject.
     button: optional; DOMObject.
    */
    options.form.submit();
}

ajax_submit = function(options) {
    /*
    options:
     form_id: optional; String. [default: first form]
     validation_url: optional; String. [with or without validation]
     container_id: optional; String. [default or same page submit]
     button: optional; DOMObject. [default: span.loading will be placed after this]
    */
    if (options.form_id != null) {
        form = $("form#"+form_id);
    } else {
        form = $("form:first");
    }
    if (options.container_id == null) { // default_submit
        submit_function = default_submit;
    } else { // same_page_submit
        submit_function = same_page_submit;
    }
    submit_function_args = {'form': form, 'button': options.button,
                            'container': $("div#"+options.container_id)}
    if (options.validation_url != null) { // with validation
        validate_submit(form, options.validation_url, submit_function, 
                        submit_function_args);
    } else { // without validation
        submit_function(submit_function_args);
    }
};

