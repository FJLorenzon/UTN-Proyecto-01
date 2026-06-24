'''
Created on 24 jun 2026

@author: ati05
'''
# -*- coding: utf-8 -*-
"""
ventanas/ver_estadisticas.py
Muestra las estadísticas acumuladas y el historial de partidos de un arquero.
"""

import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import db

COLOR_BG       = "#0d1117"
COLOR_PANEL    = "#161b22"
COLOR_PANEL2   = "#1c2128"
COLOR_ACENTO   = "#39d353"
COLOR_TEXTO    = "#e6edf3"
COLOR_SUBTEXTO = "#8b949e"
COLOR_BORDE    = "#30363d"
COLOR_HOVER    = "#238636"


def _porc(num, den):
    """Devuelve un porcentaje formateado o '—' si no aplica."""
    if den and den > 0:
        return f"{num / den * 100:.1f}%"
    return "—"


class VerEstadisticasWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Estadísticas del arquero")
        self.geometry("600x700")
        self.resizable(True, True)
        self.configure(fg_color=COLOR_BG)
        self.grab_set()
        self.focus()

        self._arqueros = db.obtener_arqueros()
        self._map_nombres = {
            f"{nombre}  ({sel or '—'})": id_
            for id_, nombre, sel in self._arqueros
        }

        self._build_ui()

    def _build_ui(self):
        # ── Encabezado + selector ────────────────────────────────────────────
        top = ctk.CTkFrame(self, fg_color=COLOR_PANEL, corner_radius=0)
        top.pack(fill="x")

        ctk.CTkLabel(
            top,
            text="Estadísticas del arquero",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLOR_TEXTO
        ).pack(pady=(20, 8))

        sel_row = ctk.CTkFrame(top, fg_color=COLOR_PANEL)
        sel_row.pack(padx=30, fill="x", pady=(0, 16))

        opciones = list(self._map_nombres.keys()) if self._map_nombres \
                   else ["(sin arqueros registrados)"]

        self.combo = ctk.CTkComboBox(
            sel_row,
            values=opciones,
            height=36,
            fg_color=COLOR_BG,
            border_color=COLOR_BORDE,
            text_color=COLOR_TEXTO,
            button_color=COLOR_ACENTO,
            dropdown_fg_color=COLOR_PANEL,
            corner_radius=8,
            command=self._cargar
        )
        self.combo.pack(side="left", expand=True, fill="x", padx=(0, 10))

        ctk.CTkButton(
            sel_row,
            text="Ver",
            command=lambda: self._cargar(self.combo.get()),
            width=80,
            height=36,
            corner_radius=8,
            fg_color=COLOR_ACENTO,
            hover_color=COLOR_HOVER,
            text_color="#0d1117",
            font=ctk.CTkFont(weight="bold")
        ).pack(side="left")

        sep = ctk.CTkFrame(self, height=2, fg_color=COLOR_ACENTO, corner_radius=0)
        sep.pack(fill="x")

        # ── Área de contenido scrollable ─────────────────────────────────────
        self.scroll = ctk.CTkScrollableFrame(
            self, fg_color=COLOR_BG, corner_radius=0)
        self.scroll.pack(expand=True, fill="both", padx=0, pady=0)

        self._placeholder()

    # ── Placeholder inicial ──────────────────────────────────────────────────
    def _placeholder(self):
        self._limpiar()
        ctk.CTkLabel(
            self.scroll,
            text="Seleccioná un arquero para ver sus estadísticas",
            font=ctk.CTkFont(size=13),
            text_color=COLOR_SUBTEXTO
        ).pack(pady=60)

    def _limpiar(self):
        for w in self.scroll.winfo_children():
            w.destroy()

    # ── Carga y renderizado ──────────────────────────────────────────────────
    def _cargar(self, seleccion):
        arquero_id = self._map_nombres.get(seleccion)
        if not arquero_id:
            return

        totales  = db.obtener_estadisticas_totales(arquero_id)
        partidos = self._obtener_partidos(arquero_id)

        self._limpiar()
        self._render_totales(totales)
        self._render_partidos(partidos)

    def _obtener_partidos(self, arquero_id):
        con = sqlite3.connect(db.DATABASE_NAME)
        cur = con.cursor()
        cur.execute("""
            SELECT partido, resultado, minutos_jugados,
                   goles_recibidos, remates_recibidos, centros_cortados,
                   pases_totales, pases_ok, penales_encontra, penales_atajados
            FROM partidos_arquero
            WHERE arquero_id = ?
            ORDER BY id DESC
        """, (arquero_id,))
        rows = cur.fetchall()
        con.close()
        return rows

    # ── Tarjetas de totales ──────────────────────────────────────────────────
    def _render_totales(self, totales):
        remates, goles, centros, pases_tot, pases_ok, pen_ataj, n_partidos = totales

        remates    = remates    or 0
        goles      = goles      or 0
        centros    = centros    or 0
        pases_tot  = pases_tot  or 0
        pases_ok   = pases_ok   or 0
        pen_ataj   = pen_ataj   or 0

        ctk.CTkLabel(
            self.scroll,
            text="RESUMEN GLOBAL",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLOR_ACENTO
        ).pack(anchor="w", padx=24, pady=(20, 8))

        grid = ctk.CTkFrame(self.scroll, fg_color=COLOR_BG)
        grid.pack(fill="x", padx=24)

        metricas = [
            ("Partidos",        str(n_partidos or 0)),
            ("Goles recibidos", str(goles)),
            ("% Paradas",       _porc(remates - goles, remates)),
            ("Centros cortados", str(centros)),
            ("% Pases ok",      _porc(pases_ok, pases_tot)),
            ("Penales atajados", str(pen_ataj)),
        ]

        for i, (label, valor) in enumerate(metricas):
            col = i % 3
            row = i // 3
            card = ctk.CTkFrame(grid, fg_color=COLOR_PANEL, corner_radius=10)
            card.grid(row=row, column=col, padx=6, pady=6, sticky="ew")
            ctk.CTkLabel(
                card, text=valor,
                font=ctk.CTkFont(size=22, weight="bold"),
                text_color=COLOR_ACENTO
            ).pack(pady=(12, 2))
            ctk.CTkLabel(
                card, text=label,
                font=ctk.CTkFont(size=11),
                text_color=COLOR_SUBTEXTO
            ).pack(pady=(0, 10))

        grid.columnconfigure((0, 1, 2), weight=1)

    # ── Historial de partidos ────────────────────────────────────────────────
    def _render_partidos(self, partidos):
        ctk.CTkLabel(
            self.scroll,
            text="HISTORIAL DE PARTIDOS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLOR_ACENTO
        ).pack(anchor="w", padx=24, pady=(24, 8))

        if not partidos:
            ctk.CTkLabel(
                self.scroll,
                text="No hay partidos cargados para este arquero.",
                font=ctk.CTkFont(size=12),
                text_color=COLOR_SUBTEXTO
            ).pack(anchor="w", padx=24)
            return

        for p in partidos:
            (partido, resultado, minutos, goles, remates,
             centros, pases_tot, pases_ok,
             pen_contra, pen_ataj) = p

            card = ctk.CTkFrame(
                self.scroll, fg_color=COLOR_PANEL, corner_radius=10)
            card.pack(fill="x", padx=24, pady=5)

            # Cabecera de la tarjeta
            cab = ctk.CTkFrame(card, fg_color=COLOR_PANEL, corner_radius=0)
            cab.pack(fill="x", padx=14, pady=(12, 4))

            ctk.CTkLabel(
                cab, text=partido,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=COLOR_TEXTO
            ).pack(side="left")

            ctk.CTkLabel(
                cab, text=resultado,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=COLOR_ACENTO
            ).pack(side="right")

            # Detalle en dos columnas
            det = ctk.CTkFrame(card, fg_color=COLOR_PANEL)
            det.pack(fill="x", padx=14, pady=(4, 12))

            items = [
                ("⏱ Minutos",         str(minutos)),
                ("🥅 Goles recibidos", str(goles)),
                ("🧤 Remates",         str(remates)),
                ("✂️ Centros cortados", str(centros)),
                ("🎯 Pases ok",        f"{pases_ok}/{pases_tot} ({_porc(pases_ok, pases_tot)})"),
                ("🟡 Penales atajados", f"{pen_ataj}/{pen_contra}"),
            ]

            for j, (k, v) in enumerate(items):
                col = j % 2
                row = j // 2
                ctk.CTkLabel(
                    det,
                    text=f"{k}:  {v}",
                    font=ctk.CTkFont(size=12),
                    text_color=COLOR_SUBTEXTO
                ).grid(row=row, column=col, sticky="w", padx=10, pady=2)

            det.columnconfigure((0, 1), weight=1)