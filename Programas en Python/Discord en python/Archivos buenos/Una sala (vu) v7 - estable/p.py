print("""
 /\\_/\\  
( o.o ) 
 > ^ <
""")
print("""
 / \\__
(    @\\___
 /         O
/   (_____/
/_____/   U
""")
print("""
  **     **
 *****  *****
**************
 ************
  **********
    ******
      **
""")
print("""
    ^
   /^\\
  /___\\
  |= |=
  |.-.|
  |'-'|
  |   |
 /|_|_|\\ 
   / \\
  /___\\
""")
print("""
 (\\_/)
 ( •_•)
 / >🍪
""")
print("""
 ,_,  
(O,O) 
(   ) 
 " "
""")
print("""
           __
          / _)
   .-^^^-/ /
__/       /
<__.|_|-|_|
""")

cadena = "@usuario /sticker dog"
partes = cadena.split(" ", 1)

print(f"{partes}")

if (partes[1].startswith("/sticker")):
    print("Se imprime el sticker")

usuarios = {"general": {"Bryan": ("1.1.1.1", 5007), "Carlos": ("2.2.2.2", 5007)}}


print(f"{list(usuarios['general'].keys())}")

cadena1 = "h"

if (cadena1):
    print("Cadena no vacia")