import time
import logging
from google import genai
from google.genai import errors

logger = logging.getLogger(__name__)

cliente = genai.Client()


def preguntar_ia(mensaje: str, contexto: str = "") -> str | None:
    contenido_completo = mensaje
    if contexto:
        contenido_completo = f"Contexto de referencia:\n{contexto}\n\nConsulta:\n{mensaje}"

    for intento in range(3):
        try:
            respuesta = cliente.models.generate_content(
                model="gemini-3.5-flash-lite",  # O "gemini-3.5-flash" según soporte
                contents=contenido_completo
            )
            
            # Validar si la respuesta tiene texto válido
            if respuesta and hasattr(respuesta, 'text') and respuesta.text:
                return respuesta.text
            else:
                logger.warning("La respuesta de Gemini vino vacía.")
                return "La IA no generó texto para esta consulta."

        except errors.ServerError as e:
            if e.code not in (500, 502, 503, 504):
                raise

            logger.warning(
                "Error temporal de Gemini (%s). Intento %s de 3.",
                e.code,
                intento + 1
            )

            if intento < 2:
                time.sleep(2 ** (intento + 1))

        except Exception as e:
            # Imprime el error real en los logs para identificar el problema exacto
            logger.exception(f"Error detallado al consultar Gemini: {e}")
            return f"Error de conexión con la IA: {str(e)}"

    return None