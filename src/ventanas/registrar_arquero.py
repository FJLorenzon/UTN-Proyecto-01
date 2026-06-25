'''
Created on 24 jun 2026

@author: ati05
'''

# -*- coding: utf-8 -*-
import customtkinter as ctk
from db import registrar_arquero

class RegistrarArqueroWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registrar Nuevo Arquero")
        self.geometry("400x520")
        self.resizable(False, False)
        self.configure(fg_color="#0d1117")
        self.transient(parent)
        
        # Solución de visibilidad segura para Linux
        self.wait_visibility()  # Espera a que el sistema operativo la dibuje
        self.grab_set()         # Ahora sí bloquea la ventana de atrás de forma segura
        # ───────────────────────────────────────────────────────────────

        ctk.CTkLabel(self, text="📝 REGISTRO DE ARQUERO", font=ctk.CTkFont(size=16, weight="bold"), text_color="#e6edf3").pack(pady=20)

        # Campos de texto
        self.txt_nombre = self._crear_campo("Nombre Completo:")
        self.txt_nacionalidad = self._crear_campo("Nacionalidad:")
        self.txt_nacimiento = self._crear_campo("Fecha Nacimiento (AAAA-MM-DD):")
        self.txt_seleccion = self._crear_campo("Selección Nacional:")
        self.txt_club = self._crear_campo("Club Actual:")

        # Botón Guardar
        btn_guardar = ctk.CTkButton(self, text="Guardar Arquero", fg_color="#161b22", hover_color="#238636", text_color="#e6edf3", border_width=1, border_color="#30363d", command=self._guardar)
        btn_guardar.pack(pady=30, padx=40, fill="x")

    def _crear_campo(self, label_text):
        ctk.CTkLabel(self, text=label_text, text_color="#8b949e", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=40, pady=(10, 2))
        entry = ctk.CTkEntry(self, fg_color="#161b22", border_color="#30363d", text_color="#e6edf3")
        entry.pack(fill="x", padx=40)
        return entry

    def _guardar(self):
        nombre = self.txt_nombre.get()
        nacionalidad = self.txt_nacionalidad.get()
        nacimiento = self.txt_nacimiento.get()
        seleccion = self.txt_seleccion.get()
        club = self.txt_club.get()

        if nombre and nacionalidad:
            registrar_arquero(nombre, nacionalidad, nacimiento, None, None, seleccion, club)
            self.destroy()