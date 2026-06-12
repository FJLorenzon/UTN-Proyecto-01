'''
Created on 12 jun 2026

@author: ati05
'''

import customtkinter as ctk

# Configuración del tema visual (puedes probar "blue", "green" o "dark-blue")
ctk.set_appearance_mode("System")  # Detecta si tu Linux usa modo oscuro o claro
ctk.set_default_color_theme("blue")

class MiAppModerna(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurar la ventana principal
        self.title("¡Entorno Eclipse Listo!")
        self.geometry("400x250")
        self.resizable(False, False)

        # Crear una etiqueta (Label)
        self.label = ctk.CTkLabel(
            self, 
            text="¡Eclipse y PyDev funcionando!", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label.pack(padx=20, pady=30)

        # Crear un botón
        self.boton = ctk.CTkButton(
            self, 
            text="Hacer clic aquí", 
            command=self.evento_click
        )
        self.boton.pack(padx=20, pady=10)
        
        # Un switch para cambiar el modo oscuro/claro manualmente
        self.switch = ctk.CTkSwitch(
            self, 
            text="Modo Oscuro", 
            command=self.cambiar_modo
        )
        self.switch.pack(padx=20, pady=20)
        if ctk.get_appearance_mode() == "Dark":
            self.switch.select()

    def evento_click(self):
        # Cambia el texto de la etiqueta al presionar el botón
        self.label.configure(text="¡Todo marcha a la perfección! 🚀")
        self.boton.configure(state="disabled", text="¡Listo!")

    def cambiar_modo(self):
        if self.switch.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

if __name__ == "__main__":
    app = MiAppModerna()
    app.mainloop()