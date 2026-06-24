'''
Created on 24 jun 2026

@author: ati05
'''
# -*- coding: utf-8 -*-
import sqlite3

DATABASE_NAME = "analisis_arqueros.db"

def conectar():
    """Establece la conexión con la base de datos SQLite."""
    return sqlite3.connect(DATABASE_NAME)

def crear_tablas():
    """Crea las tablas necesarias si no existen."""
    conexion = conectar()
    cursor = conexion.cursor()
    
    # 1. Tabla de Arqueros (Datos fijos)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS arqueros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            nacionalidad TEXT NOT NULL,
            nacimiento DATE,
            altura INTEGER,
            peso INTEGER,
            seleccion TEXT,
            club TEXT
        )
    """)
    
    # 2. Tabla de Partidos (Estadísticas por partido de cada arquero)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS partidos_arquero (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            arquero_id INTEGER NOT NULL,
            partido TEXT NOT NULL,
            resultado TEXT NOT NULL,
            minutos_jugados INTEGER NOT NULL,
            goles_recibidos INTEGER DEFAULT 0,
            remates_recibidos INTEGER DEFAULT 0,
            centros_cortados INTEGER DEFAULT 0,
            pases_totales INTEGER DEFAULT 0,
            pases_ok INTEGER DEFAULT 0,
            penales_encontra INTEGER DEFAULT 0,
            penales_atajados INTEGER DEFAULT 0,
            FOREIGN KEY (arquero_id) REFERENCES arqueros (id) ON DELETE CASCADE
        )
    """)
    
    conexion.commit()
    conexion.close()

def registrar_arquero(nombre, nacionalidad, nacimiento, altura, peso, seleccion, club):
    """Inserta un nuevo arquero en la base de datos."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO arqueros (nombre, nacionalidad, nacimiento, altura, peso, seleccion, club) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (nombre, nacionalidad, nacimiento, altura, peso, seleccion, club)
    )
    conexion.commit()
    conexion.close()

def registrar_partido(arquero_id, partido, resultado, minutos_jugados, goles, remates, centros, pases_totales, pases_ok, penales_encontra, penales_atajados):
    """Inserta las estadísticas de un partido para un arquero específico."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO partidos_arquero 
        (arquero_id, partido, resultado, minutos_jugados, goles_recibidos, remates_recibidos, centros_cortados, pases_totales, pases_ok, penales_encontra, penales_atajados)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (arquero_id, partido, resultado, minutos_jugados, goles, remates, centros, pases_totales, pases_ok, penales_encontra, penales_atajados))
    conexion.commit()
    conexion.close()

def obtener_arqueros():
    """Devuelve la lista de todos los arqueros registrados."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, seleccion FROM arqueros")
    lista = cursor.fetchall()
    conexion.close()
    return lista

def obtener_estadisticas_totales(arquero_id):
    """Suma y calcula las métricas globales acumuladas de un arquero."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT 
            SUM(remates_recibidos),
            SUM(goles_recibidos),
            SUM(centros_cortados),
            SUM(pases_totales),
            SUM(pases_ok),
            SUM(penales_atajados),
            COUNT(partidos_arquero.id)
        FROM partidos_arquero
        WHERE arquero_id = ?
    """, (arquero_id,))
    
    res = cursor.fetchone()
    conexion.close()
    return res

# Si ejecutamos este archivo directamente, inicializa las tablas para probar
if __name__ == "__main__":
    crear_tablas()
    print("¡Base de datos y tablas de arqueros inicializadas correctamente!")