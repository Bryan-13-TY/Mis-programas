texto_entrada = "@Edwyn /sticker dog"

if (texto_entrada.startswith("@")):
    partes = texto_entrada.split(" ", 1)

    if (len(partes) < 2):
        print("[Sistema] Formato: @usuario mensaje")

    if (partes[1] == "/audio"):
        print("Se graba audio")

        destinatario, contenido = partes
        destinatario = destinatario[1:]

        print(destinatario)
        print(contenido)
    elif (partes[1].startswith("/sticker")):
        partes2 = partes[1].split(" ")

        if (len(partes2) < 2):
            print("[Sistema] Formato: /sticker nombre_sticker")

        _, nombre_sticker = partes2

        print(f"Se muestra sticker {nombre_sticker}") 
        destinatario, contenido = partes
        destinatario = destinatario[1:]

        print(destinatario)
        print(contenido)
    else:
        destinatario, contenido = partes
        destinatario = destinatario[1:]

        print(destinatario)
        print(contenido)