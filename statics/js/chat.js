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
    var theArea = document.getElementById(divID);
    var reqObj = getReqObj();

    var url="../cgi-bin/cgiChatServer.py?newtxt=" + escape("<p>" + theText.value + "</p>");
    reqObj.open("GET", url, false);
    reqObj.send(null); 
    theArea.innerHTML = unescape(reqObj.responseText);
    theArea.scrollTop = theArea.scrollHeight;
    theText.value = "";
    return false;
}
//---------------------------------------------------------------
window.onload=function()
{
    document.forms[0][0].focus();
} 

$(document).ready(function(){
    setInterval("refreshChat()",1000);
});

function refreshChat () {
    var theArea = document.getElementById('targetDiv');
    var reqObj = getReqObj();
    
    var url="../cgi-bin/otro.py";
    reqObj.open("GET", url,false);
    reqObj.send(null); 
    theArea.innerHTML = unescape(reqObj.responseText);
    theArea.scrollTop = theArea.scrollHeight;
    return false;

}