import re
import speech_recognition as sr
import pyttsx3

NOMBRE_AGENTE = "La Buena"

def hablar(texto):
    """Convierte texto en voz de forma directa, limpia y segura."""
    if not texto:
        return

    print(f"\n[{NOMBRE_AGENTE.upper()} HABLANDO]:\n{texto}")
    
    # 1. Limpiar completamente el texto de formatos Markdown, asteriscos y códigos
    texto_limpio = str(texto)
    texto_limpio = re.sub(r'```[\s\S]*?```', '', texto_limpio)  # Bloques de código
    texto_limpio = re.sub(r'[*_`#~-]', '', texto_limpio)         # Símbolos markdown
    texto_limpio = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', texto_limpio) # Enlaces
    texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()    # Espacios múltiples
    
    if not texto_limpio:
        return

    # 2. Inicializar, reproducir y cerrar el motor de forma aislada para evitar bloqueos
    try:
        motor = pyttsx3.init()
        motor.setProperty("rate", 165)
        motor.setProperty("volume", 1.0)
        
        motor.say(texto_limpio)
        motor.runAndWait()
        motor.stop()
    except Exception as e:
        print(f"Error al reproducir el audio con pyttsx3: {e}")

def escuchar():
    """Escucha el micrófono y convierte voz en texto."""
    reconocedor = sr.Recognizer()

    try:
        with sr.Microphone() as fuente:
            print(f"\n🎤 [{NOMBRE_AGENTE.upper()} ESCUCHANDO]: Habla ahora...")
            reconocedor.adjust_for_ambient_noise(fuente, duration=0.5)
            
            audio = reconocedor.listen(
                fuente,
                timeout=6,
                phrase_time_limit=15
            )

        texto = reconocedor.recognize_google(audio, language="es-CO")
        print("\nTÚ DIJISTE:", texto)
        
        # Detectar comando de parada
        if texto.lower().strip() in ["para", "detente", "alto", "silencio"]:
            print(f"\n[{NOMBRE_AGENTE.upper()}: Orden de parada recibida]")
            return "para"

        return texto

    except sr.WaitTimeoutError:
        print("No se detectó ninguna voz.")
    except sr.UnknownValueError:
        print("No pude entender lo que dijiste.")
    except sr.RequestError:
        print("Error de conexión con el reconocimiento de voz.")
    except OSError as error:
        print("Error con el micrófono:", error)

    return None