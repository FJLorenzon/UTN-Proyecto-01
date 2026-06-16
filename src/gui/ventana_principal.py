'''
Created on 16 jun 2026

@author: ati05
'''

# Archivo: ventanas.py
import customtkinter as ctk

class MiAppPantallaCompleta(ctk.CTk):
    def __init__(self, titulo_ventana="Ventana main"):
        super().__init__()
        self.title(titulo_ventana)

        # Obtener el tamaño de la pantalla real
        ancho_max = self.winfo_screenwidth()
        alto_max = self.winfo_screenheight()

        # Calcular el tamaño del 70% (Para cuando se minimice/restaure)
        ancho_restaurado = int(ancho_max * 0.70)
        alto_restaurado = int(alto_max * 0.70)
        
        # Establecemos el posicionamiento
        posx = 0
        posy = 0
        
        # Establecer el límite mínimo (para que el usuario no la rompa estirándola)
        self.minsize(ancho_restaurado, alto_restaurado)
        
        # Asignamos como geometría base el tamaño del 70%
        self.geometry(f"{ancho_restaurado}x{alto_restaurado}+{posx}+{posy}")
        
        # Minimizar
        try:
            self.state('zoomed') # Intenta modo Windows
        except Exception:
            self.attributes('-zoomed', True) # Si falla modo Linux 

        self.label.pack(expand=True)