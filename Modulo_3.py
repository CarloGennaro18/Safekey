# MODULO 3: GENERADOR DE CONTRASENAS
# ============================================================================
import random
def generar_contrasena(longitud=12, mayusculas=True, numeros=True, simbolos=True):
    """Genera una contrasena aleatoria segura"""
    caracteres = list("abcdefghijklmnopqrstuvwxyz")
    
    if mayusculas:
        caracteres.extend(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    
    if numeros:
        caracteres.extend(list("0123456789"))
    
    if simbolos:
        caracteres.extend(list("!@#$%^&*()_+-=[]{}|;:,.<>?"))
    
    if len(caracteres) == 0:
        caracteres = list("abcdefghijklmnopqrstuvwxyz")
    
    contrasena = ""
    for i in range(longitud):
        contrasena += random.choice(caracteres)
    
    return contrasena