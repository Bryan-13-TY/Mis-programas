"""
Calcualdora de subneteo VLSM.

Este archivo contiene las funciones para generar las subredes mediante el subneteo VLSM.

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

NoBitsHost = [-1, 0, 2, 6, 14, 30, 62, 126, 254, 510, 
              1022, 2046, 4094, 8190, 16382, 32766, 65534, 131070, 262142, 524286, 1048574,
              2097150, 4194302, 8388606, 16777214, 33554430, 67108862, 134217726, 268435454, 536870910, 1073741822] # El índice representa el valor de n

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

def CalcularNoHosts(NoHostSubred: list[int], NoBitsHost: list[int]) -> tuple[list[int], list[int]]:
    """
    Calcula el número de host.

    Parameters
    ----------
    NoHostSubred : list[int]
        Número de host para subred.
    NoBitsHost : list[int]
        Número de bits de host.

    Returns
    -------
    tuple
        (Direcciones requeridas, Potencia)

        - **Direcciones requeridas** (list[int]): Direcciones requeridas.
        - **Potencia** (list[int]): Potencia.
    """
    DirReq = []
    Pot = []

    for HostSubred in range(0, len(NoHostSubred)):
        for BitHost in range(0, len(NoBitsHost)):
            if (NoBitsHost[BitHost] >= NoHostSubred[HostSubred]):
                DirReq.append(NoBitsHost[BitHost])
                Pot.append(BitHost)
                break
    
    return DirReq, Pot

def CalcularIPsRed(Network: str, NewNetmaskBits: list[int]) -> list[str]:
    """
    Calcula las IPs de red.

    Parameters
    ----------
    Network : str
        Network de la red.
    NewNetmaskBits : list[int]
        Nueva máscara de red.
    
    Returns
    -------
    list[str]
        IPs de la red.
    """
    IPBase = int(Network, 2)
    IPs = []

    for Mascara in NewNetmaskBits:
        IPActual= IPBase
        IPBinaria = f'{IPActual}:032b'
        IPs.append(IPBinaria)

        Tamano = 2**(32 - Mascara)
        IPBase += Tamano
    return IPs

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

def CalcularSubredes(NoSubredes: int, NoHostSubred: list[int], DirReq: list[int], Pot: list[int], Netmask: int, Network: str) -> None:
    """
    Calculas las subredes.

    Parameters
    ----------
    NoSubredes : int
        Número de subredes.
    NoHostSubred : list[int]
        Número de hosts de subred.
    DirReq : list[int]
        Direcciones requeridas.
    Pot : list[int]
        Potencia.
    Netmask : int
        Máscara de red.
    Network : str
        Network.
    """
    NewNetmaskBitsL = []
    ListaDecimal = []
    ListaBinaria = [] 

    for Subred in range(0, NoSubredes):
        NewNetmaskBits = Netmask + ((32 - Netmask) - Pot[Subred]) # Calcular los bits de la máscara para cada subred
        NewNetmaskBitsL.append(NewNetmaskBits)

    for Subred in range(0, NoSubredes):
        
        NewNetmask, NewNetmaskBinario = CalcularMascaraRed(NewNetmaskBitsL[Subred])
        IPsRed = CalcularIPsRed(Network, NewNetmaskBitsL)
        IPSubred, IPSubredBinario = FuncionAux(format(int((IPsRed[Subred])[0:len(IPsRed[Subred]) - 5]), '032b'), ListaDecimal, ListaBinaria)
        PrimerHost, PrimerHostBinario = CalcularHostMin(IPSubredBinario.split("."), NewNetmaskBitsL[Subred])
        UltimoHost, UltimoHostBinario = CalcularHostMax(IPSubredBinario.split("."), NewNetmaskBitsL[Subred])
        Broadcast, BroadcastBinario = CalcularBroadcast(IPSubredBinario.split("."), NewNetmaskBitsL[Subred])

        print(f"\n{BRIGHT_RED}>> Subred {Subred + 1}: {NoHostSubred[Subred]} solicitados{RESET}")
        print(f"Número de hosts: {BRIGHT_MAGENTA}{DirReq[Subred]}{RESET}")
        print(f"IP de subred: {BRIGHT_BLUE}{IPSubred}/{NewNetmaskBitsL[Subred]}{RESET} {BRIGHT_YELLOW}{IPSubredBinario}{RESET}")
        print(f"Máscara de subred: {BRIGHT_BLUE}{NewNetmask}{RESET} {BRIGHT_YELLOW}{NewNetmaskBinario}{RESET}")
        ListaDecimal = []
        ListaBinaria = [] 
        print(f"Primer host: {BRIGHT_BLUE}{PrimerHost}{RESET} {BRIGHT_YELLOW}{PrimerHostBinario}{RESET}")
        print(f"Último host: {BRIGHT_BLUE}{UltimoHost}{RESET} {BRIGHT_YELLOW}{UltimoHostBinario}{RESET}")
        print(f"Broadcast: {BRIGHT_BLUE}{Broadcast}{RESET} {BRIGHT_YELLOW}{BroadcastBinario}{RESET}")

print("""
/*-----------------.
| CALCULADORA VLSM |
`-----------------*/""")

Direccion = input("\n1.- Ingresa una dirección IP: ")
if (ValidarDireccion(Direccion)):
    print(f"{BRIGHT_GREEN}>> La dirección IP {Direccion} es válida{RESET}")

    MascaraRed = int(input("\n2.- Ingresa la máscara de red (1 <= Netmask <= 32): "))
    if (MascaraRed >= 1 and MascaraRed <= 32):
        print(f"{BRIGHT_GREEN}>> La máscara de red {MascaraRed} es válida{RESET}")

        NoSubredes = int(input("\n3.- Ingresa el número de subredes (1 <= # <= 100): "))
        if (NoSubredes >= 1 and NoSubredes <= 100):
            print(f"{BRIGHT_GREEN}>> # de subredes dentro de rango{RESET}")
            
            Tope = 2**(32 - MascaraRed) - 2

            print(f"\n4.- Ingresa el número de hosts para las {NoSubredes} subredes\n")
            print(f"{BRIGHT_BLUE}>> {Tope} hosts disponibles para direccionar{RESET}")

            NoHostSubred = []
            NoHosts = 0
            for Subred in range(0, NoSubredes):
                NoHosts = int(input(f"Número de hosts para la subred {Subred + 1} (1 <= # <= {Tope}): ")) # Tope = 2, NoHosts = 2

                if (NoHosts >= 1 and NoHosts <= Tope):
                    NoHostSubred.append(NoHosts)
                else:
                    NoHostSubred.append(NoHosts)
                    print(f"{BRIGHT_RED}>> La subred {Subred + 1} no puede direccionar {NoHosts} hosts{RESET}")
                    break

                Tope = Tope - NoHosts
                print(f"{BRIGHT_BLUE}>> {Tope} hosts disponibles para direccionar{RESET}")
            
            if (2**(32 - MascaraRed) < sum(NoHostSubred)):
                print(f"\n{BRIGHT_RED}>> No se pueden direccionar {sum(NoHostSubred)} hosts con una máscara de {MascaraRed} bits{RESET}")
            else: 
                DirReq, Pot = CalcularNoHosts(sorted(NoHostSubred, reverse = True), NoBitsHost)
                DireccionBinario = ConvertirBinario(Direccion.split("."))
                Network, NetworkBinario = CalcularNetwork(DireccionBinario.split("."), MascaraRed)
                Netmask, NetmaskBinario = CalcularMascaraRed(MascaraRed)
                Broadcast, BroadcastBinario = CalcularBroadcast(DireccionBinario.split("."), MascaraRed)

                print(f"\nNúmero total de hosts solicitados: {sum(NoHostSubred)}")
                print(f"Número de direcciones requeridas: {sum(DirReq)}")
                print(f"Número total de hosts disponibles: {2**(32 - MascaraRed) - 2}")
                print(f"Número total de hosts usados: {Tope}")
                print(f"\nDirección IP: {BRIGHT_BLUE}{Direccion}{RESET} {BRIGHT_YELLOW}{DireccionBinario}{RESET}")
                print(f"Dirección de red: {BRIGHT_BLUE}{Network + "/"}{MascaraRed}{RESET} {BRIGHT_YELLOW}{NetworkBinario}{RESET}")
                print(f"Máscara de red: {BRIGHT_BLUE}{Netmask} = {MascaraRed}{RESET} {BRIGHT_YELLOW}{NetmaskBinario}{RESET}")
                print(f"Dirección de Broadcast: {BRIGHT_BLUE}{Broadcast}{RESET} {BRIGHT_YELLOW}{BroadcastBinario}{RESET}")

                CalcularSubredes(NoSubredes, sorted(NoHostSubred, reverse = True), DirReq, Pot, MascaraRed, ''.join(NetworkBinario.split(".")))
        else:
            print(f"{BRIGHT_RED}>> # de subredes fuera de rango{RESET}")
    else:
        print(f"{BRIGHT_RED}>> La máscara de red {MascaraRed} no es válida{RESET}")
else:
    print(f"{BRIGHT_RED}>> La dirección IP {Direccion} no es válida{RESET}")