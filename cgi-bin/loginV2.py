#!/usr/bin/python
import Cookie
from utiles import buscarEnArchivo
import os
from utiles import guardarEnArchivo

def coincide(usuario1, usuario2):
    '''Compara usuarios en formato diccionario como los que se encuentran en usuarios.txt '''
    #guardarEnArchivo("log.txt", "Comparando...\n%s vs \n%s"%(usuario1, usuario2))
    return usuario1["nombre"] == usuario2["nombre"] and usuario1["palabraClave"] == usuario2["palabraClave"]

def coincideHash(hashInfo, un_hash):
    '''
    hashInfo es una linea del archivo se sesionesTemp
    hashInfo.keys() devuelve una lista con una sola clave, la sessionHash
    '''
    return un_hash in hashInfo.keys()

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

#Verificamos si el usuario esta o no logueado...
#Obtenemos la cookie del entorno
cookie_string = os.environ.get('HTTP_COOKIE')
cookie = Cookie.SimpleCookie()
hashDeCookieValido = None
el_session_hash = ''
try:
    #transformamos el string de la cookie en un objeto cookie
    cookie.load(cookie_string)
    el_session_hash = cookie['sessionHash'].value
    #Verificamos si la cookie que se trajo es valida:
    hashDeCookieValido, offset = buscarEnArchivo('sesionesTempV2.txt', coincideHash, el_session_hash)
    #Errores al cargar la cookie:
except AttributeError, e:
    #el_session_hash = ''
    pass
except KeyError, e:
    #el_session_hash = ''
    pass

guardarEnArchivo("log.txt", "Session Hash >>> %s"%(el_session_hash))

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
usuarioValido = None
if hashDeCookieValido:
    #Esta logueado!
    #hashDeCookieValido tiene un diccionario con la informacion de la session
    print "<meta http-equiv=\"Set-Cookie\" content=\"sessionHash = %s; path=/; expires=null\" >" % el_session_hash
    print "<meta http-equiv=\"Set-Cookie\" content=\"leido=0; path=/; expires=null\" >"
    print "<meta http-equiv=\"Refresh\" content=\"0;  url=../html/chatV2.html\"/>"

else:
    #hashDeCookieValido es None, o sea que el usuario no venia logeado
    #Entonces tomamos los datos del formulario para buscarlo en usuarios.txt
    #primero importamos los modulos para el manejo de cgi
    import cgi, cgitb 
    cgitb.enable()
    form = cgi.FieldStorage() 

    #obtenemos los datos del formulario de login (el nombre y el apellido)
    nombre = form.getvalue('nombre')
    password  = form.getvalue('palabraClave')
    #con estos datos armamos un diccionario, formato con el cual fue guardado en el archivo usuarios.txt
    usuario = {"nombre": nombre, "palabraClave": password}
    #buscamos el usuario en usuarios.txt, si existe, devuelve diccionario usuario-lineaDelArchivoDondeLoEncontro, sino devuelve None-None
    usuarioValido, nroLinea = buscarEnArchivo("usuarios.txt", coincide, usuario) #nroLinea no se usa en este caso
    if usuarioValido:
        #Resulto un usuario valido, lo guardamos en sesiones:
        print "<meta http-equiv=\"Set-Cookie\" content=\"sessionHash = %s; path=/; expires=null\" >" % crear_y_guardarSession(usuarioValido)
        print "<meta http-equiv=\"Set-Cookie\" content=\"leido=0; path=/; expires=null\" >" #para que nos de todo el chat
        print "<meta http-equiv=\"Refresh\" content=\"0;  url=../html/chatV2.html\"/>"
    else:
        #ingreso argumentos no validos:
        print "<meta http-equiv=\"Refresh\" content=\"0;  url=../html/loginV2.html\"/>"
print "</body>"
print "</html>"
