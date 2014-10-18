var nombreReg = /^[A-Za-z]+$/;
var numeroReg =  /^[0-9]+$/;
var inputMessage = ['<span class="help-block" id="msg0"> Por favor, ingrese un nombre válido </span>',
                    '<span class="help-block" id="msg1"> Por favor, ingrese un apellido válido </span>',
                    '<span class="help-block" id="msg2"> Por favor, ingrese un nro. de legajo válido </span>',
                    '<span class="help-block" id="msg3"> Por favor, ingrese una edad válida </span>',
                    '<span class="help-block" id="msg4"> Por favor, ingrese una palabra clave válida </span>'
                    ];
var camposValidos = [true,true,true,true,true];


function validateForm(e){
    e.preventDefault();

    var nombre = $('#nombre').val();
    var apellido = $('#apellido').val();
    var legajo = $('#nroLegajo').val();
    var edad = $('#edad').val();
    var pClave = $('#pClave').val();

    limpiarErrores();
    validarNya(nombre, apellido);
    if (($('#edad').length > 0) && ($('#nroLegajo').length > 0))
        validarNumeros(legajo, edad);
    validarPclave(pClave);
    var hayError = mostrarErrores();
    if(!hayError){
        $("#form_alta").submit();
    }
    
}   


function validarNya (nombre,apellido) {
    
    if(nombreReg.test(nombre)){
        if(nombre.length > 70 ){
            $('#nombre').after(inputMessage[0]);
            camposValidos[0] = false;
        }
    }
    else{
        $('#nombre').after(inputMessage[0]);
        camposValidos[0] = false;
    }

    if(nombreReg.test(apellido)){
        if(apellido.length > 70){
            $('#apellido').after(inputMessage[1]);
            camposValidos[1] = false;
        }
    }
    else{
        $('#apellido').after(inputMessage[1]);
        camposValidos[1] = false;
    }

}

function validarNumeros (legajo,edad ) {
    if(numeroReg.test(legajo)){
        if(legajo.length > 4 ){
            $('#nroLegajo').after(inputMessage[2]);
            camposValidos[2] = false;
        } 
    }
    else{
        $('#nroLegajo').after(inputMessage[2]);   
        camposValidos[2] = false;
    }

    if(numeroReg.test(edad)){
        if(edad.length < 1 || edad.length > 2 || Number(edad) < 0){
            $('#edad').after(inputMessage[3]);
            camposValidos[3] = false;
        }
    }
    else{
        $('#edad').after(inputMessage[3]);   
        camposValidos[3] = false;
    }
}

function validarPclave (pClave) {
    if(pClave == ""){
        $('#pClave').after(inputMessage[4]);
        camposValidos[4] = false;
    }
}


function mostrarErrores () {
    var hayError = false;
    for (var i = 0; i < camposValidos.length; i++) {
        if (!camposValidos[i]) {
            $('#msg'+i).show();
            $(".entrada"+i).addClass("has-error");
            hayError = true;
        }
        else{
            $('#msg'+i).hide();
            $(".entrada"+i).removeClass("has-error");            
        }
    }
    return hayError;
}

function limpiarErrores () {
    for (var i = 0; i < camposValidos.length; i++) {
        $('#msg'+i).hide();
        $(".entrada"+i).removeClass("has-error");
        camposValidos[i] = true;
    };
}
