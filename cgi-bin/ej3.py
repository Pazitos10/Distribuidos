#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb 

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
query_string = form.qs_on_post

print "Content-type:text/html\r\n\r\n"
print
print open('/var/www/Distribuidos/html/alta.html').read()