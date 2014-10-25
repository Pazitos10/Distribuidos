#!/usr/bin/python
# -*- coding: utf-8 -*-


import os, fcntl
from ej4 import parsear, limpiar

CHATFNAME = "chat.txt"
MAXLINE = 500

def main():

    print "Content-type: text/plain\n\n"
    print ""

    #print "<html><head></head><body>"
    
    query_string = os.getenv('QUERY_STRING')
    chatfile = open(CHATFNAME,"a+")
    if not chatfile:
        print "<p>Error abriendo el archivo<br></p>\n"

    fd = chatfile.fileno()
    try:
        fcntl.flock(fd, fcntl.LOCK_EX|fcntl.LOCK_NB) #Bloqueamos el archivo
    except IOError:
        print "<p> Error en flock()</p>\n"
    
    #for l in chatfile.readlines():
    #    print l

    news = limpiar(parsear(query_string)) #Lo nuevo es lo parseado de query_string
    news = news['newtxt'] #obtenemos el valor de adentro del diccionario
    chatfile.write(news+'\n')
    #print "<p>%s</p>" % (news)
    fcntl.flock(fd, fcntl.LOCK_UN) #Desbloqueamos el archivo
    chatfile.close()
    #print "</body></html>"

if __name__ == '__main__':
    main()


