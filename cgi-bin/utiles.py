from ast import literal_eval
# -*- coding: utf-8 -*-

def buscarEnArchivo(nombreDelArchivo, fcComparacion, elementoBuscado):
    """
    Utiliza fcComparacion para buscar elementoBuscado en el archivo nombreDelArchivo

    Trata a todas las lineas del archivo como si fueran diccionario, por lo cual
    el archivo debe tener el formato correcto, por ejemplo:

    alumnos.txt:
        {'edad': '23', 'apellido': 'Morales', 'pClave': '1234', 'nombre': 'Leonardo', 'nroLegajo': '5421', 'sexo': 'Masculino'}
        {'edad': '25', 'apellido': 'Perez', 'pClave': '1234', 'nroLegajo': '5432', 'sexo': 'Femenino', 'nombre': 'Maria'}
        ...
        {'edad': '24', 'apellido': 'Dominguez', 'pClave': '1234', 'nroLegajo': '4587', 'sexo': 'Masculino', 'nombre': 'Emmanuel'}

    sessiones.txt:

        {<<cockieId>>: {'Edad': '23', 'apellido': 'Morales', 'pClave': '1234', 'nombre': 'Leonardo', 'nroLegajo': '5421', 'sexo': 'Masculino'}}

    La fcComparacion debe comparar unalineadelarchivoconvertidaendiccionario con el elementoBuscado.
    En caso de +exito retorna el objeto encontrado y el numero de linea donde fue encontrado.
    En caso de -exito retorna None,None    

    """

    archi=open(nombreDelArchivo,'r')
    lineas = archi.readlines()
    archi.close()
    for pos,l  in enumerate(lineas):
        try:
            alumno_i = literal_eval(l[:-1]) #le sacamos el \n
        except SyntaxError:
            return None, None
        #alumno_i = literal_eval(l) #le sacamos el \n
        guardarEnArchivo("log.txt", "Buscando...%s%s"%(type(alumno_i), alumno_i))
        if fcComparacion(alumno_i,elementoBuscado):
            return alumno_i, pos
    return None, None

def guardarEnArchivo(nombreDelArchivo, dato):
    '''
        Guarda el dato en el archivo nombreDelArchivo
    '''
    arch=open(nombreDelArchivo,'a')
    arch.write(str(dato) + '\n')
    arch.close()