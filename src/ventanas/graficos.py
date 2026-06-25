'''
Created on 24 jun 2026

@author: ati05
'''

# -*- coding: utf-8 -*-
"""
ventanas/graficos.py
Gráficos de evolución partido a partido para un arquero,
usando matplotlib embebido dentro de customtkinter.
"""

import sqlite3
import customtkinter as ctk
import matplotlib
matplotlib.use("TkAgg")                          # backend compatible con Tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import db

COLOR_BG       = "#0d1117"
COLOR_PANEL    = "#161b22"
COLOR_ACENTO   = "#39d353"
COLOR_ACENTO2  = "#1a7f37"
COLOR_TEXTO    = "#e6edf3"
COLOR_SUBTEXTO = "#8b949e"
COLOR_BORDE    = "#30363d"
COLOR_HOVER    = "#238636"

# Paleta para el gráfico (oscuro, coherente con la app)
MPL_BG      = "#0d1117"
MPL_PANEL   = "#161b22"
MPL_TEXTO   = "#e6edf3"
MPL_GRID    = "#21262d"
MPL_VERDE   = "#39d353"
MPL_NARANJA = "#f0883e"
MPL_AZUL    = "#58a6ff"
MPL_ROJO    = "#f85149"


class GraficosWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Gráficos de evolución")
        self.geometry("860x680")
        self.resizable(True, True)
        self.configure(fg_color=COLOR_BG)
        self.transient(parent)
        
        # Solución de visibilidad segura para Linux
        self.wait_visibility()  # Espera a que el sistema operativo la dibuje
        self.grab_set()         # Ahora sí bloquea la ventana de atrás de forma segura
        # ───────────────────────────────────────────────────────────────
        self.focus()

        # Protocolo para cerrar la ventana limpiando la memoria de Matplotlib
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        self._arqueros = db.obtener_arqueros()
        self._map_nombres = {
            f"{nombre}  ({sel or '—'})": id_
            for id_, nombre, sel in self._arqueros
        }

        self._build_ui()

    # ── UI ───────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Barra superior de controles
        ctrl = ctk.CTkFrame(self, fg_color=COLOR_PANEL, corner_radius=0)
        ctrl.pack(fill="x")

        ctk.CTkLabel(
            ctrl,
            text="Gráficos de evolución",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLOR_TEXTO
        ).pack(side="left", padx=20, pady=16)

        # Selector de métrica
        self.combo_metrica = ctk.CTkComboBox(
            ctrl,
            values=[
                "Goles recibidos por partido",
                "Remates recibidos por partido",
                "% Eficiencia en pases",
                "Centros cortados por partido",
                "Penales atajados acumulados",
                "Vista general (4 métricas)",
            ],
            width=240,
            height=34,
            fg_color=COLOR_BG,
            border_color=COLOR_BORDE,
            text_color=COLOR_TEXTO,
            button_color=COLOR_ACENTO,
            dropdown_fg_color=COLOR_PANEL,
            corner_radius=8
        )
        self.combo_metrica.pack(side="right", padx=(4, 10), pady=12)

        opciones = list(self._map_nombres.keys()) if self._map_nombres \
                   else ["(sin arqueros)"]

        self.combo_arquero = ctk.CTkComboBox(
            ctrl,
            values=opciones,
            width=220,
            height=34,
            fg_color=COLOR_BG,
            border_color=COLOR_BORDE,
            text_color=COLOR_TEXTO,
            button_color=COLOR_ACENTO,
            dropdown_fg_color=COLOR_PANEL,
            corner_radius=8
        )
        self.combo_arquero.pack(side="right", padx=4, pady=12)

        ctk.CTkButton(
            ctrl,
            text="Graficar",
            command=self._graficar,
            width=90,
            height=34,
            corner_radius=8,
            fg_color=COLOR_ACENTO,
            hover_color=COLOR_HOVER,
            text_color="#0d1117",
            font=ctk.CTkFont(weight="bold")
        ).pack(side="right", padx=4, pady=12)

        sep = ctk.CTkFrame(self, height=2, fg_color=COLOR_ACENTO, corner_radius=0)
        sep.pack(fill="x")

        # Área del gráfico
        self.canvas_frame = ctk.CTkFrame(self, fg_color=COLOR_BG, corner_radius=0)
        self.canvas_frame.pack(expand=True, fill="both", padx=0, pady=0)

        # Mensaje inicial
        self.lbl_mensaje = ctk.CTkLabel(
            self.canvas_frame,
            text="Seleccioná un arquero y una métrica, luego pulsá Graficar.",
            font=ctk.CTkFont(size=13),
            text_color=COLOR_SUBTEXTO
        )
        self.lbl_mensaje.place(relx=0.5, rely=0.5, anchor="center")

        self._canvas_mpl = None

    # ── Datos ────────────────────────────────────────────────────────────────
    def _obtener_partidos(self, arquero_id):
        con = sqlite3.connect(db.DATABASE_NAME)
        cur = con.cursor()
        cur.execute("""
            SELECT partido, goles_recibidos, remates_recibidos,
                   goles_recibidos, centros_cortados, pases_totales,
                   pases_ok, penales_atajados
            FROM partidos_arquero
            WHERE arquero_id = ?
            ORDER BY id ASC
        """, (arquero_id,))
        rows = cur.fetchall()
        con.close()
        return rows

    # ── Graficado ────────────────────────────────────────────────────────────
    def _graficar(self):
        seleccion = self.combo_arquero.get()
        arquero_id = self._map_nombres.get(seleccion)
        if not arquero_id:
            return

        metrica = self.combo_metrica.get()
        datos   = self._obtener_partidos(arquero_id)

        # Limpiar canvas anterior por completo
        if self._canvas_mpl:
            self._canvas_mpl.get_tk_widget().destroy()
            self._canvas_mpl = None

        for w in self.canvas_frame.winfo_children():
            w.destroy()

        if not datos:
            ctk.CTkLabel(
                self.canvas_frame,
                text="Este arquero no tiene partidos cargados.",
                font=ctk.CTkFont(size=13),
                text_color=COLOR_SUBTEXTO
            ).place(relx=0.5, rely=0.5, anchor="center")
            return

        # Extraer vectores
        etiquetas  = [f"P{i+1}" for i in range(len(datos))]
        goles      = [d[1] for d in datos]
        remates    = [d[2] for d in datos]
        centros    = [d[3] for d in datos]
        pases_tot  = [d[4] for d in datos]
        pases_ok   = [d[5] for d in datos]
        pen_ataj   = [d[7] for d in datos]
        
        efic_pases = [round(ok / tot * 100, 1) if tot else 0
                      for ok, tot in zip(pases_ok, pases_tot)]
        pen_acum   = []
        acc = 0
        for pa in pen_ataj:
            acc += pa
            pen_acum.append(acc)

        if metrica == "Vista general (4 métricas)":
            fig, axes = plt.subplots(2, 2, figsize=(9, 5.5))
            fig.patch.set_facecolor(MPL_BG)
            fig.subplots_adjust(hspace=0.45, wspace=0.35)

            plots = [
                (axes[0, 0], goles,      "Goles recibidos",         MPL_ROJO),
                (axes[0, 1], remates,    "Remates recibidos",        MPL_NARANJA),
                (axes[1, 0], efic_pases, "% Eficiencia en pases",    MPL_AZUL),
                (axes[1, 1], centros,    "Centros cortados",         MPL_VERDE),
            ]

            for ax, y, titulo, color in plots:
                self._plot_linea(ax, etiquetas, y, titulo, color)

        else:
            fig, ax = plt.subplots(figsize=(9, 4.5))
            fig.patch.set_facecolor(MPL_BG)

            dispatch = {
                "Goles recibidos por partido":    (goles,      "Goles recibidos",       MPL_ROJO),
                "Remates recibidos por partido":  (remates,    "Remates recibidos",      MPL_NARANJA),
                "% Eficiencia en pases":          (efic_pases, "% Eficiencia en pases",  MPL_AZUL),
                "Centros cortados por partido":   (centros,    "Centros cortados",        MPL_VERDE),
                "Penales atajados acumulados":    (pen_acum,   "Penales atajados (acum)", MPL_VERDE),
            }

            y_data, titulo, color = dispatch.get(
                metrica, (goles, "Goles recibidos", MPL_ROJO))
            self._plot_linea(ax, etiquetas, y_data, titulo, color)

        # Incrustar en la ventana
        self._canvas_mpl = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self._canvas_mpl.draw()
        self._canvas_mpl.get_tk_widget().pack(expand=True, fill="both", padx=10, pady=10)
        plt.close(fig)

    # ── Helper de gráfico ────────────────────────────────────────────────────
    def _plot_linea(self, ax, etiquetas, y, titulo, color):
        ax.set_facecolor(MPL_PANEL)
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines[["left", "bottom"]].set_color(MPL_GRID)
        ax.tick_params(colors=MPL_TEXTO, labelsize=9)
        ax.xaxis.label.set_color(MPL_TEXTO)
        ax.yaxis.label.set_color(MPL_TEXTO)
        ax.title.set_color(MPL_TEXTO)
        ax.grid(axis="y", color=MPL_GRID, linewidth=0.8, linestyle="--")

        x = range(len(etiquetas))

        # Área bajo la curva
        ax.fill_between(x, y, alpha=0.15, color=color)

        # Línea y puntos
        ax.plot(x, y, color=color, linewidth=2, marker="o",
                markersize=6, markerfacecolor=color, zorder=3)

        ax.set_xticks(list(x))
        ax.set_xticklabels(etiquetas, fontsize=8)
        ax.set_title(titulo, fontsize=11, pad=8, fontweight="bold")

        # Anotaciones de valor sobre cada punto
        for xi, yi in zip(x, y):
            ax.annotate(
                str(yi),
                (xi, yi),
                textcoords="offset points",
                xytext=(0, 8),
                ha="center",
                fontsize=8,
                color=MPL_TEXTO
            )

    def _on_closing(self):
        # Liberar memoria explícita de pyplot antes de destruir el widget
        plt.close('all')
        self.destroy()