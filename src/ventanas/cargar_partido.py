'''
Created on 24 jun 2026

@author: ati05
'''
# -*- coding: utf-8 -*-
import customtkinter as ctk
import platform
from db import obtener_arqueros, registrar_partido

class CargarPartidoWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Cargar Estadísticas de Partido")
        self.geometry("450x650")
        self.resizable(False, False)
        self.configure(fg_color="#0d1117")
        self.transient(parent)
        self.wait_visibility()  # Espera a que la ventana sea visible
        self.grab_set()         # Captura el foco modal de manera segura
        
        # ── Encabezado Principal ──────────────────────────────────────
        ctk.CTkLabel(
            self, 
            text="📋 ESTADÍSTICAS DEL PARTIDO", 
            font=ctk.CTkFont(size=16, weight="bold"), 
            text_color="#e6edf3"
        ).pack(pady=(15, 5))

        # Contenedor con Scroll para albergar todos los campos cómodamente
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, 
            fg_color="transparent", 
            scrollbar_button_color="#30363d",
            scrollbar_button_hover_color="#39d353"
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Habilitar scroll con ruedita en la base del frame
        self._vincular_ruedita(self.scroll_frame)

        # ── Cargar arqueros disponibles ───────────────────────────────
        self.lista_arqueros = obtener_arqueros()
        opciones_combo = [f"{arq[0]} - {arq[1]} ({arq[2]})" for arq in self.lista_arqueros]

        lbl_arq = ctk.CTkLabel(self.scroll_frame, text="Seleccionar Arquero:", text_color="#8b949e")
        lbl_arq.pack(anchor="w", padx=20)
        self._vincular_ruedita(lbl_arq)

        self.combo_arquero = ctk.CTkComboBox(self.scroll_frame, values=opciones_combo, fg_color="#161b22", border_color="#30363d", text_color="#e6edf3")
        self.combo_arquero.pack(fill="x", padx=20, pady=(2, 10))
        self._vincular_ruedita(self.combo_arquero)

        # ── Campos de texto / Opciones ───────────────────────────────
        self.txt_rival = self._crear_campo("Rival")
        
        # Resultado del partido usando un ComboBox para que sea limpio
        lbl_res = ctk.CTkLabel(self.scroll_frame, text="Resultado del Partido:", text_color="#8b949e", font=ctk.CTkFont(size=12))
        lbl_res.pack(anchor="w", padx=20, pady=(6, 2))
        self._vincular_ruedita(lbl_res)

        self.combo_resultado = ctk.CTkComboBox(self.scroll_frame, values=["Victoria", "Empate", "Derrota"], fg_color="#161b22", border_color="#30363d", text_color="#e6edf3")
        self.combo_resultado.pack(fill="x", padx=20, pady=(2, 10))
        self._vincular_ruedita(self.combo_resultado)

        self.txt_minutos = self._crear_campo("Minutos Jugados:", "90")
        self.txt_goles = self._crear_campo("Goles Recibidos:", "0")
        self.txt_remates = self._crear_campo("Remates al Arco Recibidos:", "0")
        self.txt_centros = self._crear_campo("Centros Cortados / Descolgados:", "0")
        
        # Sección de pases
        self.txt_pases_totales = self._crear_campo("Pases Totales Intentados:", "0")
        self.txt_pases_ok = self._crear_campo("Pases Correctos (Efectivos):", "0")
        
        # Sección de penales
        self.txt_penales_encontra = self._crear_campo("Penales en Contra (Sancionados):", "0")
        self.txt_penales_atajados = self._crear_campo("Penales Atajados:", "0")

        # ── Botón Guardar (Fuera del scroll para que quede fijo abajo) ──
        btn_guardar = ctk.CTkButton(
            self, 
            text="Registrar Partido", 
            fg_color="#161b22", 
            hover_color="#238636", 
            text_color="#e6edf3", 
            border_width=1, 
            border_color="#30363d", 
            command=self._guardar
        )
        btn_guardar.pack(pady=15, padx=40, fill="x")

    def _crear_campo(self, label_text, default=""):
        lbl = ctk.CTkLabel(self.scroll_frame, text=label_text, text_color="#8b949e", font=ctk.CTkFont(size=12))
        lbl.pack(anchor="w", padx=20, pady=(6, 2))
        self._vincular_ruedita(lbl)
        
        entry = ctk.CTkEntry(self.scroll_frame, fg_color="#161b22", border_color="#30363d", text_color="#e6edf3")
        entry.insert(0, default)
        entry.pack(fill="x", padx=20)
        self._vincular_ruedita(entry)
        return entry

    def _vincular_ruedita(self, widget):
        """ Enlaza de manera segura el evento de la ruedita del ratón al frame con scroll """
        sistema = platform.system()
        if sistema == "Linux":
            # Linux usa botones discretos para subir y bajar
            widget.bind("<Button-4>", lambda e: self.scroll_frame._parent_canvas.yview_scroll(-1, "units"))
            widget.bind("<Button-5>", lambda e: self.scroll_frame._parent_canvas.yview_scroll(1, "units"))
        else:
            # Windows y macOS usan la propiedad delta
            widget.bind("<MouseWheel>", lambda e: self.scroll_frame._parent_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    def _guardar(self):
        seleccionado = self.combo_arquero.get()
        if not seleccionado or not self.txt_rival.get():
            return
        
        arquero_id = int(seleccionado.split(" - ")[0])
        
        registrar_partido(
            arquero_id=arquero_id,
            partido=self.txt_rival.get(),
            resultado=self.combo_resultado.get(),
            minutos_jugados=int(self.txt_minutos.get() or 90),
            goles_recibidos=int(self.txt_goles.get() or 0),
            remates_recibidos=int(self.txt_remates.get() or 0),
            centros_cortados=int(self.txt_centros.get() or 0),
            pases_totales=int(self.txt_pases_totales.get() or 0),
            pases_ok=int(self.txt_pases_ok.get() or 0),
            penales_encontra=int(self.txt_penales_encontra.get() or 0),
            penales_atajados=int(self.txt_penales_atajados.get() or 0)
        )
        self.destroy()