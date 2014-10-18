#!/usr/bin/python
# -*- coding: utf-8 -*-

from urlparse import urlparse, parse_qs
import cgi,cgitb
import os
import json
import Cookie
#cgitb.enable()
form = cgi.FieldStorage()
NOMBRE_ARCH = "alumnos.txt"


def convert2JSON(parametros): #parametros es una cadena que representa a un diccionario
    json_string = parametros.replace("'", "\"")
    return json_string

def convert2Dict(json_string):
    return json.loads(json_string)

def main():
    parametros = parsear(os.getenv("QUERY_STRING"))
    alumno = limpiar(parametros)
    guardar(alumno)
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

def guardar(alumno):
    archi=open(NOMBRE_ARCH,'a')
    archi.write(str(alumno)+'\n')
    archi.close()

def parsear(query):
    '''
        Retorna un diccionario con los valores del query string.
        Los valores del diccionario son una lista.
    '''
    return parse_qs(query)


def limpiar(diccionario_qs):
    '''
        parse_qs devuelve un diccionario con la siguiente forma: 
        {'apellido': ['Oporto'], 'nombre': ['Alberto'], 'pClave': ['1234']}
        limpiar, devuelve un diccionario asi:
        {'apellido': 'Oporto', 'nombre': 'Alberto', 'pClave': '1234'}
    '''
    result = diccionario_qs.copy()
    for k,v in diccionario_qs.iteritems():
        result[k] = diccionario_qs[k][0]
    return result

def salida(parametros):
    cookie = Cookie.SimpleCookie()
    arch_salida = '/var/www/html/base.html'
    if parametros != None:
        #arch_salida = '/var/www/Distribuidos/html/ok.html'
        cookie['messages'] = 'true'
        cookie['type_msg'] = 'ok'
    else:
        #arch_salida = '/var/www/Distribuidos/html/error.html'
        cookie['messages'] = 'false'
        cookie['type_msg'] = 'error'

    print cookie
    print "Content-type:text/html\r\n\r\n"
    print ""
    print "<meta http-equiv=\"refresh\" content=\"5;url=../html/base.html\" />" #muestra el mensaje durante 5 segundos y redirige
    print open(arch_salida).read()


if __name__ == '__main__':
    main()