import pygame
from Funciones import limpiarTerminal, esperarTecla, mezclador

mezclador() # Reproducimos la canción

while (True):
    limpiarTerminal()
    print("""
/*--------------------.
| REPRODUCTOR MÚSICAL |          
`--------------------*/

>> Elije una de las opaciones
          
1.- Pausar canción
2.- Continuar canción
3.- Detener canción
4.- Subir volumen
5.- Bajar volumen
6.- Salir del reproductor
""")
    
    opcion = input("Opción: ").strip()

    match (opcion):
        case '1':
            pygame.mixer.music.pause()
            print("Pausado")

            # Esperamos una tecla
            print("\n>> Presiona una tecla para continuar...")
            tecla = esperarTecla()

        case '2':
            pygame.mixer.music.unpause()
            print("Continuando")

            # Esperamos una tecla
            print("\n>> Presiona una tecla para continuar...")
            tecla = esperarTecla()
        
        case '3':
            pygame.mixer.music.stop()
            print("Detenido")

            # Esperamos una tecla
            print("\n>> Presiona una tecla para continuar...")
            tecla = esperarTecla()
        
        case '4':
            volume = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(min(1.0, volume + 0.1))
            print(f"Volumen: {pygame.mixer.music.get_volume():.1f}")

            # Esperamos una tecla
            print("\n>> Presiona una tecla para continuar...")
            tecla = esperarTecla()
        
        case '5':
            volume = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(max(0.0, volume - 0.1))
            print(f"Volumen: {pygame.mixer.music.get_volume():.1f}")

            # Esperamos una tecla
            print("\n>> Presiona una tecla para continuar...")
            tecla = esperarTecla()

        case '6':
            pygame.mixer.music.stop()

            print("Saliendo del reproductor...")
            break

        case _:
            print("\n>> La opción no es válida")

            # Esperamos una tecla
            print("\n>> Presiona una tecla para continuar...")
            tecla = esperarTecla()