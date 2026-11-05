from agente import (
    decidir_herramienta,
    detectar_componente,
)

# Importamos las funciones actualizadas de motor_dominios
from motor_dominios import (
    ensenar,
    generar_arquitectura,
    validar_arquitectura,
    corregir_arquitectura,
    integrar_arquitectura,
    consulta_libre
)

from modelo_ia import preguntar_ia

from memoria_agente import (
    guardar_interaccion,
    construir_contexto,
    detectar_proyecto
)

from estado_proyecto import (
    actualizar_estado_desde_solicitud,
    construir_resumen_proyecto
)


def construir_contexto_completo():
    """Une el estado estructurado del proyecto con el historial reciente."""
    resumen_proyecto = construir_resumen_proyecto()
    contexto_conversacion = construir_contexto()

    contexto_completo = (
        resumen_proyecto
        + "\n\nHISTORIAL RECIENTE\n"
        + "=================\n"
        + contexto_conversacion
    )

    return contexto_completo


def crear_resultado(
    solicitud,
    herramienta,
    origen,
    respuesta,
    requiere_componentes=False
):
    """Crea el resultado estándar y guarda la interacción en memoria."""
    # Extraer el texto limpio si la respuesta viene dentro de un diccionario (como los devueltos por motor_dominios)
    texto_a_guardar = respuesta
    if isinstance(respuesta, dict):
        texto_a_guardar = respuesta.get("respuesta", str(respuesta))

    guardar_interaccion(
        solicitud,
        texto_a_guardar
    )

    return {
        "herramienta": herramienta,
        "origen": origen,
        "requiere_componentes": requiere_componentes,
        "respuesta": respuesta
    }


def ejecutar_agente(
    solicitud,
    entrada_componentes=None,
    dominio="ciberseguridad"
):
    """Coordina la solicitud utilizando los dominios locales o Gemini."""
    if solicitud.strip() == "":
        return {
            "herramienta": "ninguna",
            "origen": "python",
            "requiere_componentes": False,
            "respuesta": "Debes escribir una solicitud."
        }

    detectar_proyecto(solicitud)
    actualizar_estado_desde_solicitud(solicitud)

    herramienta = decidir_herramienta(solicitud)

    if herramienta == "ensenar":
        # Usamos la función 'ensenar' del motor_dominios que busca en los JSON
        resultado_dominio = ensenar(
            dominio=dominio,
            concepto=solicitud,
            permitir_ia=True
        )

        return crear_resultado(
            solicitud=solicitud,
            herramienta="ensenar",
            origen=resultado_dominio.get("origen", "base local"),
            respuesta=resultado_dominio.get("respuesta")
        )

    elif herramienta == "generar":
        resultado_dominio = generar_arquitectura(
            dominio=dominio,
            nombre_proyecto=solicitud
        )

        return crear_resultado(
            solicitud=solicitud,
            herramienta="generar",
            origen="base local",
            respuesta=resultado_dominio.get("respuesta")
        )

    elif herramienta == "validar":
        if (
            entrada_componentes is None
            or entrada_componentes.strip() == ""
        ):
            return {
                "herramienta": "validar",
                "origen": "python",
                "requiere_componentes": True,
                "respuesta": (
                    "Para validar necesito conocer "
                    "los componentes actuales del proyecto."
                )
            }

        resultado_dominio = validar_arquitectura(
            dominio=dominio,
            elementos_presentes=entrada_componentes
        )

        return crear_resultado(
            solicitud=solicitud,
            herramienta="validar",
            origen="base local",
            respuesta=resultado_dominio.get("respuesta")
        )

    elif herramienta == "corregir":
        if (
            entrada_componentes is None
            or entrada_componentes.strip() == ""
        ):
            return {
                "herramienta": "corregir",
                "origen": "python",
                "requiere_componentes": True,
                "respuesta": (
                    "Para corregir necesito conocer "
                    "los componentes actuales del proyecto."
                )
            }

        resultado_dominio = corregir_arquitectura(
            dominio=dominio,
            elementos_presentes=entrada_componentes
        )

        return crear_resultado(
            solicitud=solicitud,
            herramienta="corregir",
            origen="base local",
            respuesta=resultado_dominio.get("respuesta")
        )

    elif herramienta == "integrar":
        resultado_dominio = integrar_arquitectura(
            dominio=dominio,
            nombre_proyecto=solicitud
        )

        return crear_resultado(
            solicitud=solicitud,
            herramienta="integrar",
            origen="base local",
            respuesta=resultado_dominio.get("respuesta")
        )

    else:
        # Si no coincide con ninguna herramienta estricta, usamos consulta libre sobre el dominio o IA
        resultado_dominio = consulta_libre(
            dominio=dominio,
            pregunta=solicitud,
            permitir_ia=True
        )

        return crear_resultado(
            solicitud=solicitud,
            herramienta="ia",
            origen=resultado_dominio.get("origen", "gemini"),
            respuesta=resultado_dominio.get("respuesta")
        )