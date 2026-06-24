'''
Created on 12 jun 2026

@author: ati05
'''

# -*- coding: utf-8 -*-
"""
main.py - Menú principal de la aplicación Análisis de Arqueros
Proyecto UTN - 2026
"""

import customtkinter as ctk
from ventanas.registrar_arquero import RegistrarArqueroWindow
from ventanas.cargar_partido import CargarPartidoWindow
from ventanas.ver_estadisticas import VerEstadisticasWindow
from ventanas.graficos import GraficosWindow

# ── Tema global ──────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# ── Paleta personalizada ─────────────────────────────────────────────────────
COLOR_BG        = "#0d1117"   # fondo principal  (noche de estadio)
COLOR_PANEL     = "#161b22"   # panel / tarjeta
COLOR_ACENTO    = "#39d353"   # verde eléctrico  (césped iluminado)
COLOR_ACENTO2   = "#1a7f37"   # verde oscuro
COLOR_TEXTO     = "#e6edf3"   # blanco suave
COLOR_SUBTEXTO  = "#8b949e"   # gris medio
COLOR_BORDE     = "#30363d"   # borde sutil
COLOR_HOVER     = "#238636"   # hover de botón


class MenuPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Análisis de Arqueros · UTN")
        self.geometry("520x640")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG)

        self._panel()

    # ── Construcción de la interfaz ──────────────────────────────────────────
    def _panel(self):
        # ── Encabezado ───────────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color=COLOR_PANEL,
                              corner_radius=0, height=160)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="🥅",
            font=ctk.CTkFont(size=48),
            text_color=COLOR_ACENTO
        ).pack(pady=(28, 4))

        ctk.CTkLabel(
            header,
            text="ANÁLISIS DE ARQUEROS",
            font=ctk.CTkFont(family="Helvetica", size=20, weight="bold"),
            text_color=COLOR_TEXTO
        ).pack()

        ctk.CTkLabel(
            header,
            text="Estadísticas · Partidos · Gráficos",
            font=ctk.CTkFont(size=12),
            text_color=COLOR_SUBTEXTO
        ).pack(pady=(2, 0))

        # ── Separador decorativo ─────────────────────────────────────────────
        sep = ctk.CTkFrame(self, height=3, fg_color=COLOR_ACENTO,
                           corner_radius=0)
        sep.pack(fill="x")

        # ── Área de botones ──────────────────────────────────────────────────
        contenedor = ctk.CTkFrame(self, fg_color=COLOR_BG)
        contenedor.pack(expand=True, fill="both", padx=60, pady=40)

        opciones = [
            ("➕  Registrar arquero",          self._abrir_registrar_arquero),
            ("📋  Cargar estadísticas de partido", self._abrir_cargar_partido),
            ("📊  Ver estadísticas por arquero",   self._abrir_ver_estadisticas),
            ("📈  Gráficos de evolución",          self._abrir_graficos),
        ]

        for texto, comando in opciones:
            btn = ctk.CTkButton(
                contenedor,
                text=texto,
                command=comando,
                height=52,
                corner_radius=10,
                fg_color=COLOR_PANEL,
                hover_color=COLOR_HOVER,
                text_color=COLOR_TEXTO,
                font=ctk.CTkFont(size=14),
                border_width=1,
                border_color=COLOR_BORDE,
                anchor="w"
            )
            btn.pack(fill="x", pady=8)

        # ── Footer ───────────────────────────────────────────────────────────
        ctk.CTkLabel(
            self,
            text="UTN · Proyecto Universitario 2026",
            font=ctk.CTkFont(size=11),
            text_color=COLOR_SUBTEXTO
        ).pack(pady=(0, 16))

    # ── Abrir ventanas ───────────────────────────────────────────────────────
    def _abrir_registrar_arquero(self):
        RegistrarArqueroWindow(self)

    def _abrir_cargar_partido(self):
        CargarPartidoWindow(self)

    def _abrir_ver_estadisticas(self):
        VerEstadisticasWindow(self)

    def _abrir_graficos(self):
        GraficosWindow(self)


# ── Punto de entrada ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    from db import crear_tablas
    crear_tablas()          # garantiza que la BD esté lista al arrancar
    app = MenuPrincipal()
    app.mainloop()