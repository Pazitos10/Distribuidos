function cargarAlta(){
    $( ".formulario" ).load( "pruebaAlta.html" ); //altaAlumno.html
}


function cargarModif () {
    if ($.cookie('sesion') === undefined || $.cookie('sesion') === null) //cookie no existe
        $( ".formulario" ).load( "pruebaModif.html" );  //form de busqueda
    else{
        $( ".formulario" ).load( "pruebaModifCD2.html" ); //ex alta2.html con los datos del usuario
    }
}
        

function cargarResultados () {
    $( ".formulario" ).load( "resultadosCargados.html" );
}

function cargarFormConsultas () {
    $( ".formulario" ).load( "pruebaConsultas.html" );  //form de consultas - seleccion de filtro y valor
}

function borrarCookie () {
    var sesion = $.cookie('sesion');
    var hay_busqueda = $.cookie('hay_busqueda');
    var cookieAEliminar = "None";
    var result = true;
    var result_2 = true;
    if (sesion !== undefined) {
        cookiesAEliminar = sesion
        result = $.removeCookie('sesion', { path: '/' });
    };
    if (hay_busqueda !== undefined) {
        result_2 = $.removeCookie('hay_busqueda', { path: '/' });
    };
    if (result && result_2) {
        alert('Cookies eliminadas');
    }
    else{
        alert('Error al eliminar cookies');
    }
    $.cookie('eliminar',cookiesAEliminar, {path: '/'});
}