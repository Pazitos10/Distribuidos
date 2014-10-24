#!/usr/bin/python
# -*- coding: utf-8 -*-


import os, fcntl
from ej4 import parsear, limpiar

CHATFNAME = "chat.txt"
MAXLINE = 500

def main():

    print "Content-type: text/plain\n\n"
    print ""

    chatfile = open(CHATFNAME,"r")
    if not chatfile:
        print "<p>Error abriendo el archivo<br></p>\n"

    fd = chatfile.fileno()
    try:
        fcntl.flock(fd, fcntl.LOCK_EX|fcntl.LOCK_NB) #Bloqueamos el archivo
    except IOError:
        print "<p> Error en flock()</p>\n"
    
    for l in chatfile.readlines():
        print "<p>%s</p>" % (l)

    fcntl.flock(fd, fcntl.LOCK_UN) #Desbloqueamos el archivo
    chatfile.close()

if __name__ == '__main__':
    main()


