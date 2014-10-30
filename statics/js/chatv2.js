/*$(document).on('click', '.panel-heading span.icon_minim', function (e) {
    var $this = $(this);
    if (!$this.hasClass('panel-collapsed')) {
        $this.parents('.panel').find('.panel-body').slideUp();
        $this.addClass('panel-collapsed');
        $this.removeClass('glyphicon-minus').addClass('glyphicon-plus');
    } else {
        $this.parents('.panel').find('.panel-body').slideDown();
        $this.removeClass('panel-collapsed');
        $this.removeClass('glyphicon-plus').addClass('glyphicon-minus');
    }
});
$(document).on('focus', '.panel-footer input.chat_input', function (e) {
    var $this = $(this);
    if ($('#minim_chat_window').hasClass('panel-collapsed')) {
        $this.parents('.panel').find('.panel-body').slideDown();
        $('#minim_chat_window').removeClass('panel-collapsed');
        $('#minim_chat_window').removeClass('glyphicon-plus').addClass('glyphicon-minus');
    }
});
$(document).on('click', '#new_chat', function (e) {
    var size = $( ".chat-window:last-child" ).css("margin-left");
     size_total = parseInt(size) + 400;
    alert(size_total);
    var clone = $( "#chat_window_1" ).clone().appendTo( ".container" );
    clone.css("margin-left", size_total);
});
$(document).on('click', '.icon_close', function (e) {
    //$(this).parent().parent().parent().parent().remove();
    $( "#chat_window_1" ).remove();
});*/


function getReqObj() {
    var XMLHttpRequestObject; 
        if (window.XMLHttpRequest) { 
            XMLHttpRequestObject = new XMLHttpRequest(); 
        } else if (window.ActiveXObject) { 
            XMLHttpRequestObject = new ActiveXObject("Microsoft.XMLHTTP"); 
        }
        return XMLHttpRequestObject; 
}
//---------------------------------------------------------------
function submitHandler(txtID, divID) 
{
    var theText = document.getElementById(txtID);
    var reqObj = getReqObj();

    //sesionHash del usuario que emitio el mensaje
    var user =  $.cookie('sessionHash');
    //timeStamp del mensaje p. ej: 26-10-2014 12:36 o 26-10-2014 22:08  
    var timeStamp = moment().format('DD-MM-YYYY HH:mm:ss');
    // console.log(user+'  '+timeStamp);
    var url="../cgi-bin/cgiChatServerV2.py?newtxt=" + escape("<p>" + theText.value + "</p>")+'&user='+String(user)+'&timeStamp='+String(timeStamp);
    

    reqObj.open("GET", url , false);
    reqObj.send(null); 
    theText.value = "";
    return false;
}
//---------------------------------------------------------------

window.onload=function()
{
    document.forms[0][0].focus();
} 

$(window).unload(function() {
    //cleanCookie();
    console.log("Bye now!");
    $.cookie('leido', 0, {path:'/', expire:null});
});


$(document).ready(function(){
    $('#btn-cerrar-sesion').click(logout);
    setInterval("refreshChat()",1000);
    setInterval("refreshUsuarios()",2000);
});

function refreshChat () {
    var theArea = $('.chat');
    var reqObj = getReqObj();
    var elTextoDelChat;
    var leido = $.cookie('leido');
    
    //var url="../cgi-bin/refrescarV2.py?leido="+leido;
    var url="../cgi-bin/refrescarV2.py";

    reqObj.open("GET", url,false);
    reqObj.send(null);
    elTextoDelChat = unescape(reqObj.responseText);
    if (elTextoDelChat !== "") {

        theArea.append(elTextoDelChat);
        theArea.scrollTop = theArea.scrollHeight;
        
    } 
    return false;

}
function refreshUsuarios () {
    var areaUsuarios = document.getElementById('contact-list');
    var reqObj = getReqObj();
    var elTextoQueTieneALosUsuarios;

    var url="../cgi-bin/refreshContactListV2.py";
    reqObj.open("GET", url,false);
    reqObj.send(null);
    elTextoQueTieneALosUsuarios = unescape(reqObj.responseText);
    areaUsuarios.innerHTML = elTextoQueTieneALosUsuarios;
    areaUsuarios.scrollTop = areaUsuarios.scrollHeight;
    return false;

}



function logout () {
    var sessionHash = $.cookie('sessionHash');
    window.location.href = "../cgi-bin/logoutV2.py?sessionHash="+sessionHash;
    
}