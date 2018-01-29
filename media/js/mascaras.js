/*
Creditos: http://elcio.com.br/ajax/mascara/
*/

var v_obj = null
var v_fun = null

function mascara(o,f){
    v_obj=o
    v_fun=f
    setTimeout("execmascara()",1)
}

function execmascara(){
    v_obj.value=v_fun(v_obj.value)
}

function leech(v){
    v=v.replace(/o/gi,"0")
    v=v.replace(/i/gi,"1")
    v=v.replace(/z/gi,"2")
    v=v.replace(/e/gi,"3")
    v=v.replace(/a/gi,"4")
    v=v.replace(/s/gi,"5")
    v=v.replace(/t/gi,"7")
    return v
}

function somenteNumeros(v){
    return v.replace(/\D/g,"")
}

function somenteNumerosPontoVirgula(v){ // by adorilson
    return v.replace(/[^0123456789;]/g,"")
}

function mascara_telefone(v){
    v=v.replace(/\D/g,"")                 //Remove tudo o que não é dígito
    v=v.replace(/^(\d\d)(\d)/g,"($1) $2") //Coloca parênteses em volta dos dois primeiros dígitos
    v=v.replace(/(\d{4})(\d)/,"$1-$2")    //Coloca hífen entre o quarto e o quinto dígitos
    return v
}

function mask_phone_br(v){
    v=v.replace(/\D/g,"")                 //Remove tudo o que não é dígito
    v=v.replace(/^(\d\d)(\d)/g,"($1) $2") //Coloca parênteses em volta dos dois primeiros dígitos
    v=v.replace(/(\d{4})(\d)/,"$1-$2")    //Coloca hífen entre o quarto e o quinto dígitos
    return v
}

function mascara_data(v){
    v=v.replace(/\D/g,"")                    //Remove tudo o que não é dígito
    v=v.replace(/(\d{2})(\d)/,"$1/$2")       //Coloca um ponto entre o terceiro e o quarto dígitos
    v=v.replace(/(\d{2})(\d)/,"$1/$2")       //Coloca um ponto entre o terceiro e o quarto dígitos
    return v
}

function mask_date_BR(v){
    v=v.replace(/\D/g,"")                    //Remove tudo o que não é dígito
    v=v.replace(/(\d{2})(\d)/,"$1/$2")       //Coloca um ponto entre o terceiro e o quarto dígitos
    v=v.replace(/(\d{2})(\d)/,"$1/$2")       //Coloca um ponto entre o terceiro e o quarto dígitos
    return v
}

function mascara_cpf(v){
    v=v.replace(/\D/g,"")                    //Remove tudo o que não é dígito
    v=v.replace(/(\d{3})(\d)/,"$1.$2")       //Coloca um ponto entre o terceiro e o quarto dígitos
    v=v.replace(/(\d{3})(\d)/,"$1.$2")       //Coloca um ponto entre o terceiro e o quarto dígitos
                                             //de novo (para o segundo bloco de números)
    v=v.replace(/(\d{3})(\d{1,2})$/,"$1-$2") //Coloca um hífen entre o terceiro e o quarto dígitos
    return v
}

function mask_cpf(v){
    v=v.replace(/\D/g,"")                    //Remove tudo o que não é dígito
    v=v.replace(/(\d{3})(\d)/,"$1.$2")       //Coloca um ponto entre o terceiro e o quarto dígitos
    v=v.replace(/(\d{3})(\d)/,"$1.$2")       //Coloca um ponto entre o terceiro e o quarto dígitos
                                             //de novo (para o segundo bloco de números)
    v=v.replace(/(\d{3})(\d{1,2})$/,"$1-$2") //Coloca um hífen entre o terceiro e o quarto dígitos
    return v
}

function mascara_cep(v){
    v=v.replace(/D/g,"")                //Remove tudo o que não é dígito
    v=v.replace(/^(\d{5})(\d)/,"$1-$2") //Esse é tão fácil que não merece explicações
    return v
}

function mask_cep(v){
    v=v.replace(/D/g,"")                //Remove tudo o que não é dígito
    v=v.replace(/^(\d{5})(\d)/,"$1-$2") //Esse é tão fácil que não merece explicações
    return v
}

function mascara_cnpj(v){
    v=v.replace(/\D/g,"")                           //Remove tudo o que não é dígito
    v=v.replace(/^(\d{2})(\d)/,"$1.$2")             //Coloca ponto entre o segundo e o terceiro dígitos
    v=v.replace(/^(\d{2})\.(\d{3})(\d)/,"$1.$2.$3") //Coloca ponto entre o quinto e o sexto dígitos
    v=v.replace(/\.(\d{3})(\d)/,".$1/$2")           //Coloca uma barra entre o oitavo e o nono dígitos
    v=v.replace(/(\d{4})(\d)/,"$1-$2")              //Coloca um hífen depois do bloco de quatro dígitos
    return v
}

function mask_cnpj(v){
    v=v.replace(/\D/g,"")                           //Remove tudo o que não é dígito
    v=v.replace(/^(\d{2})(\d)/,"$1.$2")             //Coloca ponto entre o segundo e o terceiro dígitos
    v=v.replace(/^(\d{2})\.(\d{3})(\d)/,"$1.$2.$3") //Coloca ponto entre o quinto e o sexto dígitos
    v=v.replace(/\.(\d{3})(\d)/,".$1/$2")           //Coloca uma barra entre o oitavo e o nono dígitos
    v=v.replace(/(\d{4})(\d)/,"$1-$2")              //Coloca um hífen depois do bloco de quatro dígitos
    return v
}

function mask_time(v){
    v=v.replace(/\D/g,"")                    //Remove tudo o que não é dígito
    v=v.replace(/(\d{2})(\d)/,"$1:$2")       //Coloca um ponto entre o terceiro e o quarto dígitos
    v=v.replace(/(\d{2})(\d)/,"$1:$2")       //Coloca um ponto entre o terceiro e o quarto dígitos
    return v
}

function mascara_romanos(v){
    v=v.toUpperCase()             //Maiúsculas
    v=v.replace(/[^IVXLCDM]/g,"") //Remove tudo o que não for I, V, X, L, C, D ou M
    //Essa é complicada! Copiei daqui: http://www.diveintopython.org/refactoring/refactoring.html
    while(v.replace(/^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$/,"")!="")
        v=v.replace(/.$/,"")
    return v
}

function mascara_site(v){
    //Esse sem comentarios para que você entenda sozinho ;-)
    v=v.replace(/^http:\/\/?/,"")
    dominio=v
    caminho=""
    if(v.indexOf("/")>-1)
        dominio=v.split("/")[0]
        caminho=v.replace(/[^\/]*/,"")
    dominio=dominio.replace(/[^\w\.\+-:@]/g,"")
    caminho=caminho.replace(/[^\w\d\+-@:\?&=%\(\)\.]/g,"")
    caminho=caminho.replace(/([\?&])=/,"$1")
    if(caminho!="")dominio=dominio.replace(/\.+$/,"")
    v="http://"+dominio+caminho
    return v
}

function mascara_processo(v){ //Tulio
    v=v.replace(/\D/g,"")
    v=v.replace(/^(\d{5})(\d)/g,"$1.$2")
    v=v.replace(/(\d{6})(\d)/,"$1/$2")
    v=v.replace(/\/(\d{4})(\d)/,"/$1-$2")
    if (v.length > 20)
        v = v.substr(0, 20);
    return v
}

function mascara_empenho(v){ //Andressa
    v=v.replace(/\D/g,"")
    v=v.replace(/^(\d{4})(\d)/g,"$1NE$2")
    return v
}

function mascara_dinheiro(v){ //Tulio
    textoNumerico = v.replace(/\D/g,"");
    textoNumerico = textoNumerico.replace(/^0/,"")
    textoFormatado = "";
    if (textoNumerico.length == 1) {
        return "0,0"+textoNumerico;
    } else
    if (textoNumerico.length == 2) {
        return "0,"+textoNumerico;
    } else {
    for (i=0; i<textoNumerico.length; i++) {
        if (i == textoNumerico.length - 2) {
            textoFormatado += ",";
        }
        if ((i!= 0 && textoNumerico.length-i >= 5) && ((textoNumerico.length-i+1) % 3 == 0)) {
            textoFormatado += ".";
        }
        textoFormatado += textoNumerico.charAt(i);
    }
    return textoFormatado;
    }
}


