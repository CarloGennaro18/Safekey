# Modulo 1: Cifrado y descifrado
# ============================================================================

def cifrado_cesar(texto, desplazamiento):
    """Cifra texto usando el metodo Cesar con desplazamiento"""
    resultado = ""
    for char in texto:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            resultado += chr((ord(char) - base + desplazamiento) % 26 + base)
        else:
            resultado += char
    return resultado

def descifrado_cesar(texto, desplazamiento):
    """Descifra texto cifrado con Cesar"""
    return cifrado_cesar(texto, -desplazamiento)

def invertir_texto_recursivo(texto, indice=0):
    """Invierte un texto usando recursividad"""
    if indice >= len(texto):
        return ""
    return invertir_texto_recursivo(texto, indice + 1) + texto[indice]

def cifrado_recursivo(texto, desplazamiento=3):
    """Cifra invirtiendo el texto recursivamente y aplicando desplazamiento"""
    texto_invertido = invertir_texto_recursivo(texto)
    return cifrado_cesar(texto_invertido, desplazamiento)

def descifrado_recursivo(texto, desplazamiento=3):
    """Descifra revirtiendo el proceso recursivo"""
    texto_descifrado = descifrado_cesar(texto, desplazamiento)
    return invertir_texto_recursivo(texto_descifrado)