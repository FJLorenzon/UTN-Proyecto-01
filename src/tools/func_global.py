'''
Created on 4 jun 2026

@author: ati05

Archivo de funciones globales
'''

## FUNCION PARA MOSTRAR EL MENSAJE CON LAS OPCIONES QUE EL SISTEMA VA A UTILIZAR
def validar_inicio(inicio, fin, mensaje):
    # Verificamos que el dato ingresado por el usuario se un numero y este dentro del rango
    while True:
        # Validamos que lo que ingrese sea un numero
        try:
            # Soliciatamos el dato al usuario   
            valor_ingresado = int(input(mensaje))
            
            # Validamos que este dentro del rango
            if valor_ingresado < inicio or valor_ingresado > fin:
                print('\n ** La opción seleccionada no se encuentra en la lista ** \n')               
            else:
                return valor_ingresado
             
        except ValueError: 
            print('\n ** ¡Error! Debe ingresar un número válido ** \n')