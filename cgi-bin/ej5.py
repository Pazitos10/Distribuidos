#!/usr/bin/python
# -*- coding: utf-8 -*-

from urlparse import urlparse, parse_qs
import os
import json
NOMBRE_ARCH = "alumnos.txt"


def convert2JSON(parametros): #parametros es una cadena que representa a un diccionario
    json_string = parametros.replace("'", "\"")
    return json_string

def convert2Dict(json_string):
    json_string = json_string.replace("'","\"")
    return json.loads(json_string)

def main():
    alumno = parsear(os.getenv("QUERY_STRING"))
    limpiar(alumno)
    alumno, pos = buscar(alumno)
    #guardar(parametros)
    salida(alumno)

def buscar(alumno):
    archi=open(NOMBRE_ARCH,'r')
    lineas = archi.readlines()
    archi.close()
    for pos,l  in enumerate(lineas):
        alumno_i = convert2Dict(l[:-1]) #le sacamos el \n
        if coincide(alumno_i,alumno):
            return alumno_i, pos
    return None, None

def coincide(alumno_1, alumno_2):
    return alumno_1["nombre"] == alumno_2["nombre"] and alumno_1["apellido"] == alumno_2["apellido"] and alumno_1["pClave"] == alumno_2["pClave"]

def guardar(alumno):
    archi=open(NOMBRE_ARCH,'a')
    archi.write(str(alumno))
    archi.close()

def parsear(query):
    return parse_qs(query)


def limpiar(parametros):
    for k,v in parametros.iteritems():
        parametros[k] = parametros[k][0]


def salida(alumno):
    print "Content-type:text/html\r\n\r\n"
    print
    #print (open('/var/www/Distribuidos/html/alta2.html').read()).format(**alumno)
    if alumno["sexo"] == "Masculino":
        print (open('/var/www/Distribuidos/html/alta2.html').read()) % (alumno["nombre"],alumno["apellido"],alumno["nroLegajo"],"selected","",alumno["edad"],alumno["pClave"])
    else:
        print (open('/var/www/Distribuidos/html/alta2.html').read()) % (alumno["nombre"],alumno["apellido"],alumno["nroLegajo"],"","selected",alumno["edad"],alumno["pClave"])




if __name__ == '__main__':
    main()