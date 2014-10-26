#!/usr/bin/python
# -*- coding: utf-8 -*-


import os, fcntl
from ej4 import parsear, limpiar
from utiles import guardarEnArchivo, buscarEnArchivo


CHATFNAME = "chatV2.txt"
INFOCHATNAME= "infoChatV2.txt"

def main():

    print "Content-type: text/plain\n\n"
    print ""

    query_string = os.getenv('QUERY_STRING')
    chatfile = open(CHATFNAME,"a+")
    infoChat = open(INFOCHATNAME,"a+")

    if not chatfile:
        print "<p>Error abriendo el archivo<br></p>\n"

    fd = chatfile.fileno()
    try:
        fcntl.flock(fd, fcntl.LOCK_EX|fcntl.LOCK_NB) #Bloqueamos el archivo
    except IOError:
        print "<p> Error en flock()</p>\n"
    
    
    new_lines = limpiar(parsear(query_string)) #Lo nuevo es lo parseado de query_string
    
    news = new_lines['newtxt'] #obtenemos el valor de adentro del diccionario
    timeStamp = str(new_lines['timeStamp'])

    chatfile.write(news+'\n')
    chatfile.close() # cerramos temporalmente

    
    chatfile = open(CHATFNAME,"r")
    chatfile_lines = chatfile.readlines()
    pos = chatfile_lines.index(news+'\n')

    user = nombreDeUsrConSesion(str(new_lines['user']))

    datosChat = {pos:[user, timeStamp]}
    infoChat.write(str(datosChat)+'\n')
    infoChat.close()
    

    fcntl.flock(fd, fcntl.LOCK_UN) #Desbloqueamos el archivo
    chatfile.close() #cerramos definitivamente


def coincide(sessionInfo1, hashKey):
    return sessionInfo1.keys()[0] == hashKey

def nombreDeUsrConSesion(sessionHash):
    #log = open('log.txt','a+')
    usr = buscarEnArchivo("sesionesTempV2.txt", coincide, sessionHash)
    #log.write(str(type(usr))+ ' ' + str(usr))
    #log.close()
    return usr[0].values()[0]['nombre']

if __name__ == '__main__':
    main()


