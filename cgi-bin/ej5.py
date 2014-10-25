#!/usr/bin/python
# -*- coding: utf-8 -*-

from urlparse import urlparse, parse_qs
import os
import json
import Cookie
import time

NOMBRE_ARCH = "alumnos.txt"
SESSION_FILE = "session.txt"


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
    # Instantiate a SimpleCookie object
    cookie = Cookie.SimpleCookie()
    cookie['line_number'] = pos
    #guardar(parametros)
    salida(cookie, alumno)


def obtenerHash(alumno):
    '''
        Retorna el hash md5 en base a los datos del alumno y un timestamp
        Escribe los datos referentes a la sesion en un archivo
    '''
    import md5, json

    str_alumno = str(json.dumps(alumno)) #convertimos alumno (diccionario) en String
    str_timestamp = str(time.time()) #obtenemos timestamp 
    sessionHash = md5.new(str_alumno+str_timestamp).hexdigest() #creamos el md5 en base al String str_alumno
    arch=open(SESSION_FILE,'a')
    linea = {sessionHash : str_alumno}

    arch.write(str(linea) + '\n')
    arch.close()
    return sessionHash


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
    '''
        Elimina los \n de los atributos del diccionario
    '''
    for k,v in parametros.iteritems():
        parametros[k] = parametros[k][0]

def actualizarHtmlModif(alumno):
    archivo_destino = open("/var/www/html/pruebaModifCD2.html","w")
    
    if alumno["sexo"] == "Masculino":
        string_form = (alumno["nombre"],alumno["apellido"],alumno["nroLegajo"],"selected","",alumno["edad"],alumno["pClave"])
    else:
        string_form = (alumno["nombre"],alumno["apellido"],alumno["nroLegajo"],"","selected",alumno["edad"],alumno["pClave"])
    
    archivo_destino.write((open("/var/www/html/pruebaModifCD.html").read()) % (string_form))
    archivo_destino.close()


def salida(cookie, alumno):

    
    print cookie
    print "Content-type:text/html\r\n\r\n"
    print ""

    actualizarHtmlModif(alumno)

    print "<meta http-equiv=\"Set-Cookie\" content=\"hay_modificacion=true; path=/; expires=null\" >"
    print ("<meta http-equiv=\"Set-Cookie\" content=\"sesion=%s; path=/; expires=null\" >") % obtenerHash(alumno)
    print "<meta http-equiv=\"Refresh\" content=\"0;  url=../html/base.html\"/>"
  

    

if __name__ == '__main__':
    main()