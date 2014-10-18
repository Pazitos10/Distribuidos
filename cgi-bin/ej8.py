#!/usr/bin/python
# -*- coding: utf-8 -*-




def main():
    alumnos = open("/var/www/cgi-bin/alumnos.txt").read()


if __name__ == '__main__':
    main()

print "Content-type:text/html\r\n\r\n"
print ""
print (open("/var/www/html/mama.html").read()) % ("<tr><td>2</td><td>Leonardo</td><td>Morales</td><td>Masculino</td><td>22</td><td>5455</td></tr>")