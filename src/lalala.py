'''
Created on 12 jun 2026

@author: ati05
'''

from logica.func_global import sumar, raiz_cuadrada, potencia  


a = int(input('Ingresar valor base: '))
b = int(input('Ingresar valor exponente: '))
        
        
resultado= potencia(a, b)
        
print(f'El número {a} elevado {b} es: {resultado}')