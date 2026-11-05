import sqlite3

def inicializar_base_de_datos():
    """Crea la base de datos y la tabla de proyectos si no existen."""
    conexion = sqlite3.connect("arquitectura_agente.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_proyecto TEXT NOT NULL,
            componentes TEXT,
            estado TEXT,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conexion.commit()
    conexion.close()


def guardar_proyecto_db(nombre_proyecto, componentes_str=""):
    """Guarda un proyecto en la base de datos."""
    conexion = sqlite3.connect("arquitectura_agente.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO proyectos (nombre_proyecto, componentes, estado) VALUES (?, ?, ?);",
        (nombre_proyecto, componentes_str, "Creado")
    )
    conexion.commit()
    conexion.close()


def consultar_historial_db():
    """Recupera los proyectos guardados."""
    conexion = sqlite3.connect("arquitectura_agente.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre_proyecto, componentes, fecha FROM proyectos;")
    resultados = cursor.fetchall()
    conexion.close()
    return resultados
