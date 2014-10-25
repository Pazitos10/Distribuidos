#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
otro.py --> refrescar.py
'''

import os, fcntl, Cookie
from ej4 import parsear, limpiar
from utiles import guardarEnArchivo

CHATFNAME = "chat.txt"
MAXLINE = 500

def main():
    #Recuperar la cookie para saber la linea a actualizar:
    query_string = os.getenv('QUERY_STRING')
    cookie_en_parametros = limpiar(parsear(query_string)) #Lo nuevo es lo parseado de query_string
    leido = int(cookie_en_parametros['leido']) #obtenemos el valor de adentro del diccionario
    
    nro_linea = leido
    guardarEnArchivo("log.txt", "RECUPERANDO LINEA DE LA COOKIE: %d"%nro_linea)
    chatfile = open(CHATFNAME,"r")
    if not chatfile:
        print "<p>Error abriendo el archivo<br></p>\n"

    fd = chatfile.fileno()
    try:
        fcntl.flock(fd, fcntl.LOCK_EX|fcntl.LOCK_NB) #Bloqueamos el archivo
    except IOError:
        print "<p> Error en flock()</p>\n"
    
    lineas = chatfile.readlines()
    #cookie['line_number'] = len(lineas)
    #print cookie
    print "Content-type: text/plain\n\n"
    print ""
    print "<meta http-equiv=\"Set-Cookie\" content=\"leido=%s; path=/; expires=null\" >" %len(lineas)
    for l in lineas[nro_linea:]:
        print "<p>%s</p>" % (l)

    fcntl.flock(fd, fcntl.LOCK_UN) #Desbloqueamos el archivo
    chatfile.close()

if __name__ == '__main__':
    main()


