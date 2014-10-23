#!/usr/bin/python
# -*- coding: utf-8 -*-

from urlparse import urlparse, parse_qs
import os
import json
import Cookie
from ej4 import limpiar, parsear
NOMBRE_ARCH = "alumnos.txt"


def main():
    #1) Recuperamos los datos del qs:
    qs = parsear(os.getenv("QUERY_STRING"))
    #2) Obtenemos un diccionario con los valores del qs
    alumno = limpiar(qs)
    #3) Recuperar la cookie para saber la linea a actualizar:
    cookie_string = os.environ.get('HTTP_COOKIE')

    if not cookie_string:
        #Esto en teoria nunca pasa por como se invoca el script
        pass

    else:
        # Creamos una cookie
        cookie = Cookie.SimpleCookie()
        # load() parses the cookie string
        cookie.load(cookie_string)
        # Obtenemos el numero de linea en el cual se encuentra el alumno
        nro_linea = int(cookie['line_number'].value)

        #Llamar a actualizar_linea con el nro de linea y el nuevo contenido:
        actualizar_linea(nro_linea, alumno)
        # Cargamos la cookie con los valores necesarios para mostrar el mensaje de exito.
        cookie['messages'] = 'true'
        cookie['type_msg'] = 'ok'
        salida(nro_linea, alumno, cookie)


def actualizar_linea(nro_linea, alumno):
    from tempfile import mkstemp
    from shutil import move
    from os import remove, close

    #Create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path,'w')
    old_file = open(NOMBRE_ARCH, 'r')
    lines = old_file.readlines()
    for i, line in enumerate(lines):
        if i == nro_linea:
            new_file.write(str(alumno)+'\n')
        else:
            new_file.write(line)
    new_file.close()
    close(fh)
    old_file.close()
    #Remove original file
    remove(NOMBRE_ARCH)
    #Move new file
    move(abs_path, NOMBRE_ARCH)

def salida(nro_linea, alumno, cookie):
    print cookie
    print "Content-type:text/html\r\n\r\n"
    print ""
    print "<meta http-equiv=\"refresh\" content=\"5;url=../html/base.html\" />" #muestra el mensaje durante 5 segundos y redirige
    print open('/var/www/html/base.html').read()

if __name__ == '__main__':
    main()