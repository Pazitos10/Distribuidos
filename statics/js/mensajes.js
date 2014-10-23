var msg = [ '<div class="alert alert-success mensaje mensaje_ok"><span class="glyphicon glyphicon-ok"> \
                </span> <strong>Éxito!</strong> \
                <hr class="message-inner-separator"> \
                <p>¡La operación se ha realizado correctamente!.</p> \
             </div>',
            '<div class="alert alert-danger mensaje mensaje_error"> \
                <span class="glyphicon glyphicon-hand-right"></span> \
                <strong>Ha ocurrido un error</strong> \
                <hr class="message-inner-separator"> \
                <p>Realice los cambios necesarios y vuelva a intentarlo.</p> \
            </div>'];


function verificarMensajes () {
    limpiarMensajes();
    var hay_mensajes = $.cookie('messages');
    var type_msg = $.cookie('type_msg');
    var hay_busqueda = $.cookie('hay_busqueda');
    var hay_modificacion = $.cookie('hay_modificacion');


    if(Boolean(hay_mensajes)){
        if(type_msg === "ok")
            $('.mensajes').after(msg[0]);
        else
            $('.mensajes').after(msg[1]);
    }

    if (Boolean(hay_busqueda) !== false ) {
        cargarResultados();
        $.removeCookie("hay_busqueda",{expires:null, path:"/"});
    };

    if (Boolean(hay_modificacion) !== false ) {
        cargarModif();
        $.removeCookie("hay_modificacion",{expires:null, path:"/"});
    };
}



function limpiarMensajes () {
    $('.mensaje_ok').hide();
    $('.mensaje_error').hide();
}

