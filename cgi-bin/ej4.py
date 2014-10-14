#!/usr/bin/python
# -*- coding: utf-8 -*-

from urlparse import urlparse, parse_qs
import cgi
import os
import json
form = cgi.FieldStorage()
NOMBRE_ARCH = "alumnos.txt"


def convert2JSON(parametros): #parametros es una cadena que representa a un diccionario
    json_string = parametros.replace("'", "\"")
    return json_string

def convert2Dict(json_string):
    return json.loads(json_string)

def main():
    parametros = parsear(os.getenv("QUERY_STRING"))
    limpiar(parametros)
    guardar(parametros)
    salida(parametros)

def buscar(alumno):
    archi=open(NOMBRE_ARCH,'r')
    lineas = archi.readlines()
    archi.close()
    for pos,l  in enumerate(lineas):
        alumno_i = convert2Dict(l[:-1]) #le sacamos el \n
        if coincide(alumno_i,alumno):
            return alumno_i, pos
    return None, None

def guardar(alumno):
    archi=open(NOMBRE_ARCH,'a')
    archi.write(str(alumno)+'\n')
    archi.close()

def parsear(query):
    return parse_qs(query)


def limpiar(parametros):
    for k,v in parametros.iteritems():
        parametros[k] = parametros[k][0]

def salida(parametros):
    print "Content-type:text/html\r\n\r\n"
    print ""
    print "<html>"
    print "<head>"
    print "<title>Mostrando datos</title>"
    print "</head>"
    print "<body>"
    print "<form>"
    print "<p>Mostrando datos</p>"
    print "<h1>Se guardo con exito: %s</h1>" % (parametros)
    print "</form>"
    print "</body>"
    print "</html>"

if __name__ == '__main__':
    main()