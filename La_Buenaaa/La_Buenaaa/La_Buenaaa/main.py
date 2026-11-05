from voz import hablar, escuchar
from agente import (
    generar_arquitectura,
    ensenar_componente,
    validar_arquitectura,
    corregir_arquitectura,
    integrar_arquitectura,
    normalizar_componentes
)
from modelo_ia import preguntar_ia
from orquestador import ejecutar_agente
from base_datos import (
    crear_tablas,
    guardar_conversacion,
    consultar_historial
)


def procesar_solicitud(solicitud, por_voz=False):
    resultado = ejecutar_agente(solicitud)

    if not isinstance(resultado, dict):
        mensaje = "Error: el agente no devolvió un diccionario."
        print(mensaje)
        if por_voz:
            hablar(mensaje)
        return

    if resultado.get("requiere_componentes", False):
        respuesta = resultado.get(
            "respuesta",
            "Indica los componentes necesarios."
        )
        print("\nAgente:", respuesta)

        if por_voz:
            hablar(respuesta)
            hablar("Por favor, dime los componentes separados por comas.")
            entrada_componentes = escuchar()
        else:
            entrada_componentes = input(
                "\nComponentes separados por comas: "
            ).strip()

        if not entrada_componentes:
            mensaje = "Debes introducir los componentes."
            print(mensaje)
            if por_voz:
                hablar(mensaje)
            return

        resultado = ejecutar_agente(
            solicitud,
            entrada_componentes
        )

        if not isinstance(resultado, dict):
            mensaje = "Error: respuesta no válida del agente."
            print(mensaje)
            if por_voz:
                hablar(mensaje)
            return

    respuesta = resultado.get(
        "respuesta",
        "El agente no generó una respuesta."
    )

    print("\nPROCESO DEL AGENTE")
    print("==================")
    print("Herramienta:", resultado.get("herramienta", "No especificada"))
    print("Origen:", resultado.get("origen", "No especificado"))
    print("\nAgente:")
    print(respuesta)

    if por_voz:
        hablar(respuesta)

    # Guardar automáticamente la conversación y respuesta en SQLite
    guardar_conversacion(
        solicitud=solicitud,
        respuesta=respuesta,
        herramienta=resultado.get("herramienta"),
        origen=resultado.get("origen")
    )


def agente_automatico():
    print("\nAGENTE AUTOMÁTICO")
    print("Escribe 'salir' para terminar.")

    while True:
        solicitud = input("\nTú: ").strip()

        if solicitud.lower() == "salir":
            print("\nConversación finalizada. chaito perro.")
            break

        if not solicitud:
            print("\n que qieres saber.")
            continue

        procesar_solicitud(solicitud)


def agente_por_voz():
    print("\nAGENTE AUTOMÁTICO POR VOZ")
    print("Di 'salir' para terminar.")

    hablar(
        "Hola perro. Soy tu Agente de ciberseguridad. "
        "Estoy listo para escucharte que quieres saber."
    )

    while True:
        solicitud = escuchar()

        if not solicitud:
            continue

        if solicitud.lower().strip() == "salir":
            hablar("vemos perro . chaito besos.")
            break

        procesar_solicitud(solicitud, por_voz=True)


def main():
    while True:
        print("\nAGENTE ARQUITECTO DIGITAL")
        print("=========================")
        print("1. Enseñar")
        print("2. Generar")
        print("3. Validar")
        print("4. Corregir")
        print("5. Integrar")
        print("6. Consultar IA")
        print("7. Agente automático")
        print("8. Agente automático por VOZ")
        print("9. Consultar historial")
        print("10. Salir")

        opcion = input(
            "\nSelecciona una opción del 1 al 10: "
        ).strip()

        try:
            if opcion == "1":
                componente = input(
                    "\nEscribe el componente: "
                ).strip().lower()

                if componente:
                    print(ensenar_componente(componente))
                else:
                    print("Debes escribir un componente.")

            elif opcion == "2":
                nombre = input(
                    "\nEscribe el nombre del proyecto: "
                ).strip()

                if nombre:
                    print(generar_arquitectura(nombre))
                else:
                    print("Debes escribir el nombre del proyecto.")

            elif opcion == "3":
                entrada = input(
                    "\nEscribe los componentes separados por comas: "
                ).strip()

                componentes = normalizar_componentes(entrada)
                print(validar_arquitectura(componentes))

            elif opcion == "4":
                entrada = input(
                    "\nEscribe los componentes separados por comas: "
                ).strip()

                componentes = normalizar_componentes(entrada)
                print(corregir_arquitectura(componentes))

            elif opcion == "5":
                nombre = input(
                    "\nEscribe el nombre del proyecto: "
                ).strip()

                if nombre:
                    print(integrar_arquitectura(nombre))
                else:
                    print("Debes escribir el nombre del proyecto.")

            elif opcion == "6":
                pregunta = input(
                    "\nEscribe la pregunta que deseas realizar: "
                ).strip()

                if pregunta:
                    print(preguntar_ia(pregunta))
                else:
                    print("Debes escribir una pregunta.")

            elif opcion == "7":
                agente_automatico()

            elif opcion == "8":
                agente_por_voz()

            elif opcion == "9":
                historial = consultar_historial()
                print("\nHISTORIAL DEL AGENTE")
                print("===================")
                for registro in historial:
                    print("\nID:", registro[0])
                    print("Solicitud:", registro[1])
                    print("Respuesta:", registro[2])
                    print("Fecha:", registro[3])

            elif opcion == "10":
                print(
                    "\nSaliendo del Agente Arquitecto Digital. "
                    "¡Hasta pronto!"
                )
                break

            else:
                print(
                    "\nOpción no válida. Selecciona una opción del 1 al 10."
                )

        except ImportError as error:
            print(f"\nError al importar un módulo: {error}")

        except Exception as error:
            print(f"\nSe produjo un error: {error}")


if __name__ == "__main__":
    crear_tablas()
    main()
    
    