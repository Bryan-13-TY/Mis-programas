import random

peticion = """GET /axel/aplicaciones/sockets/java HTTP/1.1
Host: 148.204.58.221
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: es-419,es;q=0.9,en;q=0.8,la;q=0.7
"""

tokens = peticion.split("\n")
print(tokens[0])
tokens1 = tokens[0].split(" ")
print(tokens1)
tokens2 = tokens1[1]
print(tokens2)

if not tokens2[-1].endswith("/"):
    print(f"Se reedirige a {tokens2 + '/'}")
else:
    print("Ruta coorrecta")


cadena = "123456789"
print(cadena[1:])
print(cadena[1::])
print(cadena[:-1])
print(cadena[::-1])
print(cadena[:1])
print(cadena[::1])
print(cadena[1::len(cadena)])

lista = [i**2 for i in range(100) if i % 2 == 0]
print(lista)