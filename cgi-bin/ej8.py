#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Tiene que:
-Leer un archivo con cadenas que representan diccionarios del tipo:
    {'apellido': 'Morales',
     'edad': '21',
     'nombre': 'Leonardo',
     'nroLegajo': '5421',
     'pClave': '1234',
     'sexo': 'Masculino'
    }

-Por cada linea, generar el string del tipo:
    <tr>
        <td>1</td>
        <td>Bruno</td>
        <td>Pazos</td>
        <td>Masculino</td>
        <td>21</td>
        <td>5454</td>
    </tr>

Entonces:
<tr><td>{nombre}</td><td>{apellido}</td><td>{sexo}</td><td>{edad}</td><td>{nroLegajo}</td></tr>

'''
import ast, os
from ej4 import limpiar, parsear

def crearTablaHtml(fc_evaluar, atributo):
    result = []
    arch = open("/var/www/cgi-bin/alumnos.txt", 'r')
    lineas = arch.readlines()
    arch.close()
    for linea in lineas:
        lineaAux = linea[:-1]
        d = ast.literal_eval(lineaAux)
        if fc_evaluar(d[atributo]):
        #if funcionEdad("")[0](d[atributo]):
            result.append("<tr><td>{nombre}</td><td>{apellido}</td><td>{sexo}</td><td>{edad}</td><td>{nroLegajo}</td></tr>".format(**d))

    tablaHtml = "".join(result)
    #print "RESULTADO: %s\nTIPO: %s" %(tabla, type(tabla))
    return tablaHtml


def mayorQue(valorComparacionFijo, valorVariable):
    '''
        True si valor es mayor que otroValorComparacion
    '''
    #print 'Comparando %d vs %d\n'%(valorVariable, valorComparacionFijo)
    return int(valorVariable) > valorComparacionFijo

def CreaClausura (conQueValorFijo):
    '''
        Concepto: funciones parcialmente evaluadas.
        Hay una funcion generica mayorQue (ver mas arriba)
        esta fc retorna una clausura que usa la fc mayorQue para comparar con conQueValorFijo
        y dejar variable la edad.

    '''
    def mayorQueUnValor (edad): return mayorQue(conQueValorFijo, edad)
    return mayorQueUnValor

def valorEnRango(vmin, vmax, valor):
    '''
        castea porque valor puede ser string. Esto es para no obligar a la funcion main a castear el atributo del diccionario
        que le esta enviando a fc_evaluar, y que quede lo suficientemente generico.
    '''
    return int(valor) >= vmin and int(valor) <= vmax

def clausuraValorEnRangos(valorMin, valorMax):
    '''
        ver docstring de fc CreaClausura.
        Utiliza valorEnRango y devuelve una funcion que nos dice si un valor (este valor es un valor del diccionario en la funcion main)
        esta dentro del rango.
        La gracia, variar los valores max y min al permitir invocar esta funcion (funcion parcialmente evaluada) 
        y devolver una funcion que recibe un valor que todavia no sabemos cual es. 
    '''
    def valorEnRangoParcialmenteEvaluada(valor): return valorEnRango(valorMin, valorMax, valor)
    return valorEnRangoParcialmenteEvaluada

def prueba():
    '''
        1) Crear una funcion de filtro para los diccionarios en el archivo de texto alumnos.txt.
            Para esto se crean fuciones de comparacion y despues funciones que crean clausuras. Esto es 
            para poder obtener valores de un query string y enviarlo a la uncion que crea clausuras y asi evitar
            por un lado duplicacion de codigo y exceso de sentencias condicionales.
        2) ejecutar main con la funcion de validacion/filtro del alumno y el atributo del diccionario que se esta comparando. 
    '''
    print "\n\nMAYORES DE 40:"
    func = CreaClausura(40)
    main(func, 'edad')
    
    #Ahora prueba valor en rango:
    print "\n\nEDAD EN RANGO (24 - 46):"
    func = clausuraValorEnRangos(24, 46)
    main(func, 'edad')

    #probamos con funcion lambda para listar todos:
    print "\n\nTODOS:"
    main(lambda v: True, 'edad')

    #probamos con funcion lambda para listar todos:
    print "\n\nLEGAJO EN RANGO 1000 - 3000:"
    func = clausuraValorEnRangos(1000, 3000)
    main(func, 'nroLegajo')

def siempreTrue(valor):
    return True

def consultaEdad(query):
    '''
    '''
    #Determinar si es por valor o por rango:
    #edad-1 se utiiliza para hacer la clausura.
    if query.has_key('edad-2'):#es por rango
        fcParcialmenteEval = clausuraValorEnRangos(int(query['edad-1']), int(query['edad-2']))        
    else: 
        fcParcialmenteEval = clausuraValorEnRangos(int(query['edad-1']), int(query['edad-1']))        
    return fcParcialmenteEval, 'edad'

def cadenasIguales(cadena, otraCadena): return cadena == otraCadena

def consultaNombre(query):
    def nombreIgualA(nombre): return cadenasIguales(query['nombre'], nombre)
    return nombreIgualA, 'nombre'

def consultaApellido(query):
    def apellidoIgualA(apellido): return cadenasIguales(query['apellido'], apellido)
    return apellidoIgualA, 'apellido'
   
def consultaSexo(query):
    def sexoIgualA(sexo): return cadenasIguales(query['sexo'], sexo)
    return sexoIgualA, 'sexo'
 
def consultaLegajo(query):
    if query.has_key('nroLegajo-2'):#es por rango
        fcParcialmenteEval = clausuraValorEnRangos(int(query['nroLegajo-1']), int(query['nroLegajo-2']))        
    else: 
        fcParcialmenteEval = clausuraValorEnRangos(int(query['nroLegajo-1']), int(query['nroLegajo-1']))        
    return fcParcialmenteEval, 'nroLegajo'

def listarTodos(query):
    return siempreTrue, 'nombre' #nombre es solo ilustrativo, no se usa, pero tiene que llevar algo que exista

def determinarConsulta(query):
    '''
        Retorna, en base al query, la funcion necesaria y el atributo.
    '''
    options =  {'Edad' : consultaEdad,
                'Nombre': consultaNombre,
                'Apellido': consultaApellido,
                'Sexo': consultaSexo,
                'NroLegajo': consultaLegajo,
                '*':listarTodos
                }
    return options[query['search-attr']](query)

def main():
    import Cookie
    #1) Recuperamos los datos del qs:
    qs = parsear(os.getenv("QUERY_STRING"))
    #2) Obtenemos un diccionario con los valores del qs
    query = limpiar(qs)

    cookie = Cookie.SimpleCookie()
    print "Content-type:text/html\r\n\r\n"
    print ""
    func_evaluadora, atributo = determinarConsulta(query)
    archivo_resultados = open("/var/www/html/resultadosCargados.html","w")
    resultados = crearTablaHtml(func_evaluadora, atributo)
    archivo_resultados.write((open("/var/www/html/resultados.html").read()) % (resultados))
    archivo_resultados.close()
    #print open("/var/www/html/resultadosCargados.html").read()
    
    print "<meta http-equiv=\"Set-Cookie\" content=\"hay_busqueda=true; path=/; expires=null\" >"
    print "<meta http-equiv=\"refresh\" content=\"0;url=../html/base.html\" >" #muestra el mensaje durante 5 segundos y redirige
    

if __name__ == '__main__':
    main()
