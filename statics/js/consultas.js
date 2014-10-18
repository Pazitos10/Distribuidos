function verificaCampos (e) {
//El objetivo de esta funcion es determinar el tipo de filtro a aplicar
//Cada una de las funciones llamadas, modificara el css del formulario de manera correspondiente

    e.preventDefault();
    var valorSelect = $('#search-attr').val();

    switch(valorSelect) {
        case "*":
            filtrarTodo();
            break;
        case "Edad":
            filtrarNum('edad');
            break;
        case "NroLegajo":   
            filtrarNum('nroLegajo');
            break;
        case "Nombre":
            filtraNYA('nombre');
            break;
        case "Apellido":
            filtraNYA('apellido');
            break;
        default: //filtra por sexo
            filtrarPorSexo();
    }

}


//Settings Css 
function filtrarTodo () { 
    resetValorBusqueda();
    $('#entrada-normal').hide();
    $('#entrada-numeros').hide();
    $('#checkbox').hide();
    $('#select-filtro').attr("class","form-group col-md-6");
    $('#boton').attr("class","form-group col-md-6");
    $('#boton').removeAttr("style");
}

function filtraNYA (valorSelect) { 
    resetValorBusqueda();
    $('#entrada-normal').show();
    $('#entrada-numeros').hide();
    $('#checkbox').hide();
    $('#campo-valor').show();
    $('#campo-valor').attr("class","form-group col-md-4");
    $('#select-filtro').attr("class","form-group col-md-4");
    $('#boton').attr("class","form-group col-md-4");
    $('#boton').attr("style","margin-top:25px");
    $('#valor-busqueda').attr('name',valorSelect);
    
}

function filtrarPorSexo(){
    $('#entrada-normal').show();
    $('#entrada-numeros').hide();
    $('#checkbox').hide();
    $('#campo-valor').show();
    $('#campo-valor').attr("class","form-group col-md-4");
    $('#select-filtro').attr("class","form-group col-md-4");
    $('#boton').attr("class","form-group col-md-4"); 
    $('#boton').attr("style","margin-top:25px");
    $('#valor-busqueda').replaceWith('<select id="valor-busqueda" name="sexo" class="form-control">' +
                                        '<option value="Masculino">Masculino</option>' + 
                                        '<option value="Femenino">Femenino</option>' + 
                                    '</select>');
}

function filtrarNum(valor){
    resetValorBusqueda();
    $('#entrada-normal').hide();
    $('#entrada-numeros').show();
    $('#chk-rango').removeAttr('disabled');
    $('#checkbox').show();
    $('#campo-valor').attr("class","form-group col-md-4");
    $('#select-filtro').attr("class","form-group col-md-4");
     $('#checkbox').attr("style","margin-left:55px");
    $('#boton').attr("class","form-group col-md-4"); 
    $('#boton').attr("style","margin-top:25px");
    $('#valor-busqueda-1').attr('name',valor+'-1');
    $('#valor-busqueda-2').attr('name',valor+'-2');
    verificaRango();
}

function verificaRango(){
//Verifica si se ha habilitado la opcion de buscar por rango y habilita el 2do input

    if ($('#chk-rango').prop('checked')){
        $('#valor-busqueda-2').removeAttr('disabled');
    }
    else{
        $('#valor-busqueda-2').attr('disabled','true');   
    }
}

function resetValorBusqueda () {
//Reemplaza el div de entrada doble (para ingreso por rangos), por uno simple 
    $('#valor-busqueda').replaceWith('<input class="form-control" id="valor-busqueda" type="text">');
}


function validarConsulta (e) {
    e.preventDefault();

    var nombreReg = /^[A-Za-z]+$/;
    var numeroReg =  /^[0-9]+$/;
    var mensaje = '<span class="help-block" id="msg"> Por favor, ingrese un valor válido </span>';
    var hayError;
    var valorSelect = $('#search-attr').val();

    quitarMensajesError();

    switch(valorSelect) {
        case "Edad":
            hayError = validarEdad(numeroReg,mensaje);
            break;
        case "NroLegajo":   
            hayError = validarNroLegajo(numeroReg,mensaje);
            break;
        case "Nombre":
            hayError = validarTexto(nombreReg,$(':input[name="nombre"]').val(),'nombre',mensaje);
            break;
        case "Apellido":
            hayError = validarTexto(nombreReg,$(':input[name="apellido"]').val(),'apellido',mensaje);
            break;
    }


    // if (!hayError){
    //     $('#form-consulta').submit();
    // }
    $('#form-consulta').submit();

}


function quitarMensajesError () {
    $('.entrada1').removeClass('has-error');
    $('.entrada2').removeClass('has-error');
    $('.entrada3').removeClass('has-error');
    $('#msg').hide();
}



function validarTexto (expresion,valorInput,nombreId,mensaje) {
    if(expresion.test(valorInput)){
        if(valorInput.length > 70 ){
            $('.entrada1').addClass('has-error');
            $(':input[name="'+nombreId+'"]' ).after(mensaje);
            return true;
        }
    }
    else{
        $('.entrada1').addClass('has-error');
        $(':input[name="'+nombreId+'"]').after(mensaje);
        return true;
    }
    return false;
}

function validarNroLegajo (expresion,mensaje) {
    var nroLegajo_1 = $(':input[name="nroLegajo-1"]').val();
    var legajos = [nroLegajo_1];

    var esPorRango = $('#chk-rango').prop('checked');
    if (esPorRango){
        var nroLegajo_2 = $(':input[name="nroLegajo-2"]').val();
        legajos.push(nroLegajo_2);
    }

    for (var i = 1; i < (legajos.length + 1); i++) {
        if(expresion.test(legajos[1])){
            if(legajos[1].length > 4 ){
                $('.entrada'+i).addClass('has-error');
                $(':input[name="nroLegajo-'+i+'"]').after(mensaje);
                return true;
            } 
        }
        else{
            $('.entrada'+i).addClass('has-error');
            $(':input[name="nroLegajo-'+i+'"]').after(mensaje);
            return true;
        }
    }

    return false;

}

function validarEdad (expresion,mensaje) {
    var edad_1 = $(':input[name="edad-1"]').val();
    var edades = [edad_1];

    var esPorRango = $('#chk-rango').prop('checked');
    if (esPorRango){
        var edad_2 = $(':input[name="edad-2"]').val();
        edades.push(edad_2);
    }

    for (var i = 1; i < (edades.length +1); i++) {
        if(expresion.test(edades[i])){
            if(edades[i].length < 1 || edades[i].length > 2 || Number(edades[i]) < 0){
                $(':input[name="edad-'+i+'"]').after(mensaje);
                $('.entrada'+i).addClass('has-error');
                return true;
            }
        }
        else{
            $(':input[name="edad-'+i+'"]').after(mensaje);
            $('.entrada'+i).addClass('has-error');
            return true;
        }
    }
    return false;
}
