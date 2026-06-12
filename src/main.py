'''
Created on 12 jun 2026

@author: ati05
'''

import customtkinter as ctk

app = ctk.CTk()
app.geometry('500x500')
app.title('Etiquetas')

etiqueta2 = ctk.CTkLabel(master=app, text='Hola ventana', font=('Arial', 16))
etiqueta2.pack(padx =1000, pady=10, ancho='C', side= 'top')