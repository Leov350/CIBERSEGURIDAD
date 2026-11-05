
import sqlite3

from datetime import datetime

# Nombre de la base de datos
DB_NAME = "agente_arquitecto.db"


def conectar():
    conexion = sqlite3.connect(DB_NAME)
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_tablas():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            solicitud TEXT NOT NULL,
            respuesta TEXT,
            herramienta TEXT,
            origen TEXT,
            fecha TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            arquitectura TEXT,
            fecha TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


def guardar_conversacion(
    solicitud,
    respuesta,
    herramienta=None,
    origen=None
):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO conversaciones
        (solicitud, respuesta, herramienta, origen, fecha)
        VALUES (?, ?, ?, ?, ?)
    """, (
        solicitud,
        respuesta,
        herramienta,
        origen,
        datetime.now().isoformat()
    ))

    conexion.commit()
    conexion.close()


def consultar_historial():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, solicitud, respuesta, fecha
        FROM conversaciones
        ORDER BY id DESC
    """)

    resultados = cursor.fetchall()
    conexion.close()

    return resultados
