"""
Calcualdora de subneteo IP.

Este archivo contiene las funciones para generar las subredes mediante el subneteo IP.

Autor: García Escamilla Bryan Alexis
Fecha 17/08/2025
"""

import re # Necesaria para usar expresiones regulares

BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
RESET = "\033[0m"

def FuncionAux(Cadena: str, Lista1: list[str], Lista2: list[str]) -> tuple[str, str]:
    """
    Construye una dirección a formato binario y decimal (separados en octetos).

    Parameters
    ----------
    Cadena : str
        Cadena binaria a convertir (sin puntos entre octetos).
    Lista1 : list[str]
        Lista vacía para la dirección en formato decimal.
    Lista2 : list[str]
        Lista vacía para la dirección en formato binario.

    Returns
    -------
    tuple
        (Dirección decimal, Dirección binaria)

        - **Dirección decimal** (str): dirección en formato decimal.
        - **Dirección binaria** (str): dirección en formato binario.
    """
    for Octeto in range(0, 32, 8):
        Lista2.append(Cadena[Octeto:Octeto + 8])
        Lista1.append(str(int(Cadena[Octeto:Octeto + 8], 2)))
    
    return '.'.join(Lista1), '.'.join(Lista2)

def ValidarDireccion(Direccion: str) -> re.Match | None:
    """
    Verifica el formato de una dirección IP.

    Parameters
    ----------
    Direccion : str
        Dirección IP a validar.

    Returns
    -------
    re.Match | none
        re.Match si el formato es válido, None en caso contrario.
    """
    Expresion_Regular = r"^((25[0-5]|2[0-4]\d|1\d\d|[0-9]?\d)\.){3}" \
                        r"(25[0-5]|2[0-4]\d|1\d\d|[0-9]?\d)$"
    
    return re.fullmatch(Expresion_Regular, Direccion)

def ConvertirBinario(Octetos: list[str]) -> str:
    """
    Convierte una dirección en formato decimal, separado por octetos al formato binario.

    Parameters
    ----------
    Octetos : list[str]
        Dirección en formato decimal, separado por octetos.

    Returns
    -------
    str
        Dirección en formato binario, separado por octetos.
    """
    DireccionBinario = []
    for Octeto in range(0,len(Octetos)):
        DireccionBinario.append(format(int(Octetos[Octeto]), '08b')) # Usamos format() para convertir el Octeto a formato binario de 8 bits
    
    return '.'.join(DireccionBinario)

def CalcularMascaraRed(MascaraRed: int) -> tuple[str, str]:
    """
    Calcula la máscara de red de una dirección IP.

    Parameters
    ----------
    MascaraRed : int
        Máscara de red.
    
    Returns
    -------
    tuple
        (Máscara decimal, Máscara binaria)

        - **Máscara decimal** (str): máscara de red en formato decimal.
        - **Máscara binaria** (str): máscara de red en formato binario.
    """
    CadenaBinaria = '1' * MascaraRed + '0' * (32 - MascaraRed)
    Netmask = []
    NetmaskBinario = []

    return FuncionAux(CadenaBinaria, Netmask, NetmaskBinario)

def CalcularWilcard(Netmask: list[str]) -> tuple[str, str]:
    """
    Calcular el wildcard de una dirección IP.

    Parameters
    ----------
    Netmask : list[str]
        Máscara de red en binario, separada por octetos.

    Returns
    -------
    tuple
        (Wildcard, Wildcard binario)

        - **Wildcard** (str): Wildcard en decimal, separado por octetos.
        - **Wildcard binario** (str): Wildcard en formato binario, separado por octetos.
    """
    Wildcard = []
    
    for Octeto in range(0, len(Netmask)):
        Wildcard.append(str(255 - int(Netmask[Octeto])))

    return '.'.join(Wildcard), ConvertirBinario(Wildcard)

def CalcularNetwork(DireccionBinario: list[str], Netmask: int) -> tuple[str, str]:
    """
    Calcula el network de una dirección IP.

    Parameters
    ----------
    DireccionBinario : lits[str]
        Dirección IP en binario, separada por octetos.
    Netmask : int
        Máscara de red.
    
    Returns
    -------
    tuple
        (Network decimal, Network binaria)

        - **Network decimal** (str): el network en formato decimal.
        - **Network binaria** (str): el nwtwork en formato binario.
    """
    CadenaBinaria = ''.join(DireccionBinario)[0:Netmask] + '0' * (32 - Netmask)
    Network = []
    NetworkBinario = []

    return FuncionAux(CadenaBinaria, Network, NetworkBinario)

def CalcularHostMin(DireccionBinario: list[str], Netmask: int) -> tuple[str, str]:
    """
    Calcula el host mínimo de una dirección IP.

    Parameters
    ----------
    DireccionBinario : list[str]
        Dirección IP en binario, separada por octetos.
    Netmask : int
        Máscara de red.
    
    Returns
    -------
    tuple
        (Host min decimal, Host min binaria)

        - **Host min decimal** (str): host mínimo en formato decimal.
        - **Host min binaria** (str): host mínimo en formato binario.
    """
    CadenaBinaria = ''.join(DireccionBinario)[0:Netmask] + '0' * (31 - Netmask) + '1'
    HostMin = []
    HostMinBinario = []

    return FuncionAux(CadenaBinaria, HostMin, HostMinBinario)

def CalcularHostMax(DireccionBinario: list[str], Netmask: int) -> tuple[str, str]:
    """
    Calcula el host máximo de una dirección IP.

    Parameters
    ----------
    DireccionBinario : list[str]
        Dirección IP en binario, separada por octetos.
    Netmask : int
        Máscara de red.
    
    Returns
    -------
    tuple
        (Host max decimal, Host max binaria)

        - **Host max decimal** (str): host máximo en formato decimal.
        - **Host max binaria** (str): host máximo en formato binario.
    """
    CadenaBinaria = ''.join(DireccionBinario)[0:Netmask] + '1' * (31 - Netmask) + '0'
    HostMax = []
    HostMaxBinario = []

    return FuncionAux(CadenaBinaria, HostMax, HostMaxBinario)

def CalcularBroadcast(DireccionBinario: list[str], Netmask: int) -> tuple[str, str]:
    """
    Calcula el broadcast de una dirección IP.

    Parameters
    ----------
    DireccionBinario : list[str]
        Dirección IP en binario, separada por octetos.
    Netmask : int
        Máscara de red. 

    Returns
    -------
    tuple
        (Broadcast decimal, Broadcast binaria)

        - **Broadcast decimal** (str): dirección de broadcast en formato decimal.
        - **Broadcast binaria** (str): dirección de broadcast en formato binario.
    """
    CadenaBinaria = ''.join(DireccionBinario)[0:Netmask] + '1' * (32 - Netmask)
    Broadcast = []
    BroadcastBinario = []

    return FuncionAux(CadenaBinaria, Broadcast, BroadcastBinario)

def CalcularClase(Octeto: str) -> str:
    """
    Determina la clase de la dirección IP.

    Esta función toma el primer octeto de la dirección IP y determina en que rango se encuentra.

    Parameters
    ----------
    Octeto : str
        Primer octeto de la dirección IP.

    Returns
    -------
    str
        Clase de la dirección IP.
    """
    if (int(Octeto) >= 1 and int(Octeto) <= 126):
        return 'A'
    elif (int(Octeto) >= 128 and int(Octeto) <= 191):
        return 'B'
    elif (int(Octeto) >= 192 and int(Octeto) <= 223):
        return 'C'
    elif (int(Octeto) >= 224 and int(Octeto) <= 239):
        return 'D'
    elif (int(Octeto) >= 240 and int(Octeto) <= 255):
        return 'E'

def CalcularSubredes(NoSubredes: int, Netmask: int, Netmask2: int, Clase: str, Network: list[str]) -> None:
    """
    Calcula las subredes.

    Parameters
    ----------
    NoSubredes : int
        Número de subredes a crear.
    Netmask : int
        Máscara de red.
    Netmask2 : int
        Máscara de red a transicionar.
    Clase : str
        Clase de la dirección IP.
    Network : list[str]
        Network en binario (sin puntos entre octetos).
    """
    NetworkAux = ''.join(Network)[0:Netmask]
    Bits = Netmask2 - Netmask
    FillNetwork = '0' * (32 - (len(NetworkAux) + Bits))
    FillHostMin = '0' * (31 - (len(NetworkAux) + Bits)) + '1'
    FillHostMax = '1' * (31 - (len(NetworkAux) + Bits)) + '0'
    FillBroadcast = '1' * (32 - (len(NetworkAux) + Bits))

    ListaDecimal = []
    ListaBinaria = []

    for Subred in range(0, NoSubredes):
        if (Subred == 100):
            break
        else:
            print(f"\n{BRIGHT_GREEN}>> Subred {Subred + 1}{RESET}")

            CadenaBinariaNetwork = NetworkAux + format(Subred, f'0{Bits}b') + FillNetwork
            CadenaDecimal, CadenaBinaria = FuncionAux(CadenaBinariaNetwork, ListaDecimal, ListaBinaria) 
            print(f"Network: {BRIGHT_BLUE}{CadenaDecimal + "/" + str(Netmask2)}{RESET} {BRIGHT_YELLOW}{CadenaBinaria}{RESET}")
            
            ListaDecimal = []
            ListaBinaria = []
            
            CadenaBinariaHostMin = NetworkAux + format(Subred, f'0{Bits}b') + FillHostMin
            CadenaDecimal, CadenaBinaria = FuncionAux(CadenaBinariaHostMin, ListaDecimal, ListaBinaria)
            print(f"HostMin: {BRIGHT_BLUE}{CadenaDecimal}{RESET} {BRIGHT_YELLOW}{CadenaBinaria}{RESET}")
            
            ListaDecimal = []
            ListaBinaria = []
            
            CadenaBinariaHostMax = NetworkAux + format(Subred, f'0{Bits}b') + FillHostMax
            CadenaDecimal, CadenaBinaria = FuncionAux(CadenaBinariaHostMax, ListaDecimal, ListaBinaria)
            print(f"HostMax: {BRIGHT_BLUE}{CadenaDecimal}{RESET} {BRIGHT_YELLOW}{CadenaBinaria}{RESET}")
            
            ListaDecimal = []
            ListaBinaria = []
            
            CadenaBinariaBroadcast = NetworkAux + format(Subred, f'0{Bits}b') + FillBroadcast
            CadenaDecimal, CadenaBinaria = FuncionAux(CadenaBinariaBroadcast, ListaDecimal, ListaBinaria)
            print(f"Broadcast: {BRIGHT_BLUE}{CadenaDecimal}{RESET} {BRIGHT_YELLOW}{CadenaBinaria}{RESET}")
            
            ListaDecimal = []
            ListaBinaria = []
            print(f"Hosts/Net: {BRIGHT_MAGENTA}{2**(32 - Netmask2) - 2}{RESET} Clase {BRIGHT_RED}{Clase}{RESET}")
    
    print(f"\nSubredes: {NoSubredes}")
    print(f"Hosts: {NoSubredes * (2**(32 - Netmask2) - 2)}")

print("""
/*---------------.
| CALCULADORA IP |      
`---------------*/""")

Direccion = input("\n1.- Ingresa una dirección IP: ")
if (ValidarDireccion(Direccion)):
    print(f"{BRIGHT_GREEN}>> La Dirección IP {Direccion} es válida{RESET}")
    
    MascaraRed = int(input("\n2.- Ingresa la máscara de red (1 <= Netmask <= 32): "))
    if (MascaraRed >= 1 and MascaraRed <= 32):
        print(f"{BRIGHT_GREEN}>> La máscara de red {MascaraRed} es válida{RESET}")

        MascaraRed2 = int(input("\n3.- Ingresa la máscara de red a convertir (1 <= Netmask <= 32, 0 para omitir): "))
        if (MascaraRed2 >= 1 and MascaraRed2 <= 32):
            print(f"{BRIGHT_GREEN}>> La segunda máscara de red {MascaraRed2} es válida{RESET}")
        elif (MascaraRed2 == 0):
            print(f"{BRIGHT_BLUE}>> Segunda máscara de red omitida{RESET}")
        else:
            print(f"{BRIGHT_RED}>> La segunda máscara de red {MascaraRed2} no es válida{RESET}")
            MascaraRed2 = -1

        DireccionBinario = ConvertirBinario(Direccion.split("."))
        Netmask, NetmaskBinario = CalcularMascaraRed(MascaraRed)
        Wildcard, WildcardBinario = CalcularWilcard(Netmask.split("."))
        Network, NetworkBinario = CalcularNetwork(DireccionBinario.split("."), MascaraRed)
        HostMin, HostMinBinario = CalcularHostMin(DireccionBinario.split("."), MascaraRed)
        HostMax, HostMaxBinario = CalcularHostMax(DireccionBinario.split("."), MascaraRed)
        Broadcast, BroadcastBinario = CalcularBroadcast(DireccionBinario.split("."), MascaraRed)
        Clase = CalcularClase(Direccion.split(".")[0])

        print(f"\nDirección: {BRIGHT_BLUE}{Direccion}{RESET} {BRIGHT_YELLOW}{DireccionBinario}{RESET}")
        print(f"Máscara de red: {BRIGHT_BLUE}{Netmask} = {MascaraRed}{RESET} {BRIGHT_YELLOW}{NetmaskBinario}{RESET}")
        print(f"Wildcard: {BRIGHT_BLUE}{Wildcard}{RESET} {BRIGHT_YELLOW}{WildcardBinario}{RESET}")
        print(f"\nNetwork: {BRIGHT_BLUE}{Network + "/" + str(MascaraRed)}{RESET} {BRIGHT_YELLOW}{NetworkBinario}{RESET}")
        print(f"HostMin: {BRIGHT_BLUE}{HostMin}{RESET} {BRIGHT_YELLOW}{HostMinBinario}{RESET}")
        print(f"HostMax: {BRIGHT_BLUE}{HostMax}{RESET} {BRIGHT_YELLOW}{HostMaxBinario}{RESET}")
        print(f"Broadcast: {BRIGHT_BLUE}{Broadcast}{RESET} {BRIGHT_YELLOW}{BroadcastBinario}{RESET}")
        print(f"Hosts/Net: {BRIGHT_MAGENTA}{2**(32 - MascaraRed) - 2}{RESET} Clase: {BRIGHT_RED}{Clase}{RESET}")

        if (MascaraRed2 == MascaraRed or MascaraRed2 > 32 or MascaraRed2 < 1):
            print(f"\n{BRIGHT_RED}>> No se pueden generar subredes{RESET}")
        elif (MascaraRed2 != 0 or MascaraRed2 != MascaraRed):
            if (MascaraRed2 < MascaraRed):
                print("\nSuperred")

                Netmask2, NetmaskBinario2 = CalcularMascaraRed(MascaraRed2)
                Wildcard2, WildcardBinario2 = CalcularWilcard(Netmask2.split("."))
                Network2, NetworkBinario2 = CalcularNetwork(DireccionBinario.split("."), MascaraRed2)
                HostMin2, HostMinBinario2 = CalcularHostMin(DireccionBinario.split("."), MascaraRed2)
                HostMax2, HostMaxBinario2 = CalcularHostMax(DireccionBinario.split("."), MascaraRed2)
                Broadcast2, BroadcastBinario2 = CalcularBroadcast(DireccionBinario.split("."), MascaraRed2)
                Clase = CalcularClase(Direccion.split(".")[0])

                print(f"\nMáscara de red: {BRIGHT_BLUE}{Netmask2} = {MascaraRed2}{RESET} {BRIGHT_YELLOW}{NetmaskBinario2}{RESET}")
                print(f"Wildcard: {BRIGHT_BLUE}{Wildcard2}{RESET} {BRIGHT_YELLOW}{WildcardBinario2}{RESET}")
                print(f"Network: {BRIGHT_BLUE}{Network2 + "/" + str(MascaraRed2)}{RESET} {BRIGHT_YELLOW}{NetworkBinario2}{RESET}")
                print(f"HostMin: {BRIGHT_BLUE}{HostMin2}{RESET} {BRIGHT_YELLOW}{HostMinBinario2}{RESET}")
                print(f"HostMax: {BRIGHT_BLUE}{HostMax2}{RESET} {BRIGHT_YELLOW}{HostMaxBinario2}{RESET}")
                print(f"Broadcast: {BRIGHT_BLUE}{Broadcast2}{RESET} {BRIGHT_YELLOW}{BroadcastBinario2}{RESET}")
                print(f"Hosts/Net: {BRIGHT_MAGENTA}{2**(32 - MascaraRed2) - 2}{RESET} Clase: {BRIGHT_RED}{Clase}{RESET}")
            else:
                print(f"\n{BRIGHT_GREEN}Subredes después de la transición de /{MascaraRed} a /{MascaraRed2}{RESET}")

                Netmask3, NetmaskBinario3 = CalcularMascaraRed(MascaraRed2)
                Wildcard3, WildcardBinario3 = CalcularWilcard(Netmask3.split("."))

                print(f"\nMáscara de red: {BRIGHT_BLUE}{Netmask3} = {MascaraRed2}{RESET} {BRIGHT_YELLOW}{NetmaskBinario3}{RESET}")
                print(f"Wildcard: {BRIGHT_BLUE}{Wildcard3}{RESET} {BRIGHT_YELLOW}{WildcardBinario3}{RESET}")

                CalcularSubredes(2**(MascaraRed2 - MascaraRed), MascaraRed, MascaraRed2, Clase, NetworkBinario.split("."))
        else:
            print(f"\n{BRIGHT_RED}>> No se pueden generar subredes{RESET}")
    else:
        print(f"{BRIGHT_RED}>> La máscara de red {MascaraRed} no es válida{RESET}")
else:
    print(f"{BRIGHT_RED}>> La Dirección IP {Direccion} no es válida{RESET}")