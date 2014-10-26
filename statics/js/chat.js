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
    //var theArea = document.getElementById(divID);
    var reqObj = getReqObj();

    var url="../cgi-bin/cgiChatServer.py?newtxt=" + escape("<p>" + theText.value + "</p>");
    reqObj.open("GET", url, false);
    reqObj.send(null); 
    //theArea.innerHTML = unescape(reqObj.responseText);
    //theArea.scrollTop = theArea.scrollHeight;
    theText.value = "";
    return false;
}
//---------------------------------------------------------------
function cleanCookie()
{
    $.cookie('leido', 0);
    
}

window.onload=function()
{
    //cleanCookie();
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
    var theArea = document.getElementById('targetDiv');
    var reqObj = getReqObj();
    var elTextoDelChat;
    var leido = $.cookie('leido');
    
    var url="../cgi-bin/otro.py?leido="+leido;
    reqObj.open("GET", url,false);
    reqObj.send(null);
    elTextoDelChat = unescape(reqObj.responseText);
    if (elTextoDelChat != "") {

        theArea.innerHTML += elTextoDelChat;
        theArea.scrollTop = theArea.scrollHeight;
        
    } 
    return false;

}
function refreshUsuarios () {
    var areaUsuarios = document.getElementById('contact-list');
    var reqObj = getReqObj();
    var elTextoQueTieneALosUsuarios;

    //var url="../cgi-bin/refreshContactList.py?sessionHash="+sessionHash;
    var url="../cgi-bin/refreshContactList.py";
    reqObj.open("GET", url,false);
    reqObj.send(null);
    elTextoQueTieneALosUsuarios = unescape(reqObj.responseText);
    areaUsuarios.innerHTML = elTextoQueTieneALosUsuarios;
    areaUsuarios.scrollTop = areaUsuarios.scrollHeight;
    return false;

}



function logout () {
    var sessionHash = $.cookie('sessionHash');
    window.location.href = "../cgi-bin/logout.py?sessionHash="+sessionHash;
    
}