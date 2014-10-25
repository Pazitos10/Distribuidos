#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
otro.py --> refrescar.py
'''

import os, fcntl, Cookie
from ej4 import parsear, limpiar
from ej5b import eliminarCookies
from utiles import guardarEnArchivo


def main():
    #Recuperar la cookie para saber la linea a actualizar:
    query_string = os.getenv('QUERY_STRING')
    cookie_en_parametros = limpiar(parsear(query_string)) #Lo nuevo es lo parseado de query_string
    sessionHash = cookie_en_parametros['sessionHash'] #obtenemos el valor de adentro del diccionario
    
    eliminarCookies("sesionesTemp.txt",sessionHash)
    print "Content-type: text/html\n\n"
    print ""
    print "<meta http-equiv=\"refresh\" content=\"0;url=../html/login.html\" />" 
    
if __name__ == '__main__':
    main()


