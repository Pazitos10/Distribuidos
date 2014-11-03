#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
otro.py --> refrescar.py
'''

import os, fcntl, Cookie
from ej4 import parsear, limpiar
from utiles import guardarEnArchivo, buscarEnArchivo
from datetime import datetime
from ast import literal_eval



CHATFNAME = "chatV2.txt"
INFOCHATNAME= "infoChatV2.txt"


def main():
    #Recuperar la cookie para saber la linea a actualizar:
    query_string = os.getenv('QUERY_STRING')
    #cookie_en_parametros = limpiar(parsear(query_string)) #Lo nuevo es lo parseado de query_string
    #leido = int(cookie_en_parametros['leido']) #obtenemos el valor de adentro del diccionario

    cookie_string = os.environ.get('HTTP_COOKIE')
    if cookie_string:
        cookie = Cookie.SimpleCookie()
        cookie.load(cookie_string)
        leido = int(cookie['leido'].value)
    else:
        leido = 0
    
    nro_linea = leido
    chatfile = open(CHATFNAME,"r")
    infochat = open(INFOCHATNAME,"r")
    infochat_lines = infochat.readlines()
    infochat.close()

    if not chatfile:
        print "<p>Error abriendo el archivo<br></p>\n"
    fd = chatfile.fileno()
    try:
        fcntl.flock(fd, fcntl.LOCK_EX|fcntl.LOCK_NB) #Bloqueamos el archivo
    except IOError:
        print "<p> Error en flock()</p>\n"
    
    lineas = chatfile.readlines()

    print "Set-Cookie: leido=%s ; path=/; expires=null" % len(lineas)
    print "Content-type: text/plain\n\n"
    print ""
    #print "<meta http-equiv=\"Set-Cookie\" content=\"leido=%s; path=/; expires=false\" >" % len(lineas) #obsoleto
    for l in lineas[nro_linea:]:
        print armarLinea(l, lineas.index(l), infochat_lines) 

    fcntl.flock(fd, fcntl.LOCK_UN) #Desbloqueamos el archivo
    chatfile.close()




def armarLinea(texto, pos, infochat_lines):
    datos = buscarInfo(infochat_lines, pos) # obtengo una lista de la forma [user, timeStamp]
    user = datos[0]
    timeStamp = datos[1]
    return '<li class="left clearfix"> \
                <span class="chat-img pull-left"> \
                    <img src="http://placehold.it/50/55C1E7/fff&text=%s" alt="User Avatar" class="img-circle" /> \
                </span> \
                <div class="chat-body clearfix">\
                    <div class="header"><strong class="primary-font">%s</strong>\
                        <small class="pull-right text-muted"><span class="glyphicon glyphicon-time"></span> %s </small>\
                    </div>\
                    <p>%s</p>\
                </div>\
            </li>' % (user[0],user, timeStamp, texto)

def buscarInfo(infochat_lines, pos):
    for l in infochat_lines:
        d = literal_eval(l)
        if d.has_key(pos):
            return d[pos]




if __name__ == '__main__':
    main()


