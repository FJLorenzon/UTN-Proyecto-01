'''
Created on 12 jun 2026

@author: ati05
'''

import customtkinter as ctk
import gui.ventana_principal as app

if __name__ == "__main__":
    
    app = app.MiAppPantallaCompleta('lala')
    
    '''
    etiqueta2 = ctk.CTkLabel(master=app, text='Hola ventana', font=('Arial', 16))
    etiqueta2.pack(padx=10, pady=10, anchor='center', side= 'top')
    '''
    app.mainloop()