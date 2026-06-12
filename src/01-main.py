'''
Created on 12 jun 2026

@author: ati05
'''

import customtkinter as ctk

app = ctk.CTk()
app.geometry('500x500')
app.title('Botones')


def pulsar():
    print('lala')
    
boton1 = ctk.CTkButton(master=app, text='Enviar1', command= pulsar)
boton1.grid(row=1, column=0, padx=10, pady= 10)

app.mainloop()