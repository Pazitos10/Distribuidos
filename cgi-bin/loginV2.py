#!/usr/bin/python

def coincide(usuario1, usuario2):
    #guardarEnArchivo("log.txt", "Comparando...\n%s vs \n%s"%(usuario1, usuario2))
    return usuario1["nombre"] == usuario2["nombre"] and usuario1["palabraClave"] == usuario2["palabraClave"]

def crear_y_guardarSession(alumno):
    '''
        Retorna el hash md5 en base a los datos del alumno y un timestamp
        Escribe los datos referentes a la sesion en un archivo
    '''
    import md5
    from utiles import guardarEnArchivo
    from time import time
    str_alumno = str(alumno) #convertimos alumno (diccionario) en String
    str_timestamp = str(time()) #obtenemos timestamp 
    sessionHash = md5.new(str_alumno+str_timestamp).hexdigest() #creamos el md5 en base al String str_alumno
    sessionInfo = {str(sessionHash) : alumno }
    guardarEnArchivo("sesionesTempV2.txt", sessionInfo)
    return sessionHash

# Import modules for CGI handling 
import cgi, cgitb 
cgitb.enable()
form = cgi.FieldStorage() 

#from login import main_login
from utiles import buscarEnArchivo
# Create instance of FieldStorage 

# Get data from fields
nombre = form.getvalue('nombre')
password  = form.getvalue('palabraClave')
#import Cookie
#cookie = Cookie.SimpleCookie()
#cookie['line_number'] = 0
#print cookie
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
usuario = {"nombre": nombre, "palabraClave": password}
usuarioValido, nroLinea = buscarEnArchivo("usuarios.txt", coincide, usuario)
if usuarioValido != None:
    #Guardarlo en sesiones:
    print "<meta http-equiv=\"Set-Cookie\" content=\"leido=0; path=/; expires=null\" >"
    print "<meta http-equiv=\"Set-Cookie\" content=\"sessionHash = %s; path=/; expires=null\" >" % crear_y_guardarSession(usuarioValido)
    #print "<meta http-equiv=\"Refresh\" content=\"0;  url=../html/chat.html\"/>"
    print "<meta http-equiv=\"Refresh\" content=\"0;  url=../html/chatV2.html\"/>"
else:
    print "<meta http-equiv=\"Refresh\" content=\"0;  url=../html/loginV2.html\"/>"
print "</body>"
print "</html>"
#main_login({'nombre':nombre, 'palabraClave': password})

