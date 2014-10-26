#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, fcntl, Cookie
from ej4 import parsear, limpiar
from utiles import guardarEnArchivo

SESSIONFILE = "sesionesTempV2.txt"

def main():
    template = '<li class="list-group-item item"><div class="col-xs-12 col-sm-1"><div class="estado"></div></div> <div class="col-xs-12 col-sm-9 nombre" > <span class="name">%s</span><br/> </div> <div class="clearfix"></div> </li>'
    sesiones = open(SESSIONFILE,"r")
    if not sesiones:
        print "<p>Error abriendo el archivo<br></p>\n"

    fd = sesiones.fileno()
    try:
        fcntl.flock(fd, fcntl.LOCK_EX|fcntl.LOCK_NB) #Bloqueamos el archivo
    except IOError:
        print "<p> Error en flock()</p>\n"
    
    #cookie['line_number'] = len(lineas)
    #print cookie
    print "Content-type: text/plain\n\n"
    print ""
    from ast import literal_eval
    for l in sesiones.readlines():
        sesion = literal_eval(l)
        usuario = sesion.values()[0]
        print "%s" % (template % usuario['nombre'])

    fcntl.flock(fd, fcntl.LOCK_UN) #Desbloqueamos el archivo
    sesiones.close()

if __name__ == '__main__':
    main()