# MODULO 2: VALIDACION Y ANALISIS DE CONTRASENAS
# ============================================================================

def analizar_fuerza_contrasena(contrasena):
    """Analiza la fuerza de una contrasena y retorna clasificacion"""
    puntos = 0
    problemas = []
    
    # Longitud
    if len(contrasena) >= 12:
        puntos += 2
    elif len(contrasena) >= 8:
        puntos += 1
    else:
        problemas.append("Muy corta (minimo 8 caracteres)")
    
    # Mayusculas
    if any(c.isupper() for c in contrasena):
        puntos += 1
    else:
        problemas.append("Sin mayusculas")
    
    # Minusculas
    if any(c.islower() for c in contrasena):
        puntos += 1
    else:
        problemas.append("Sin minusculas")
    
    # Numeros
    if any(c.isdigit() for c in contrasena):
        puntos += 1
    else:
        problemas.append("Sin numeros")
    
    # Simbolos
    simbolos = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if any(c in simbolos for c in contrasena):
        puntos += 2
    else:
        problemas.append("Sin simbolos especiales")
    
    # Patrones prohibidos
    patrones_malos = ["123", "password", "qwerty", "abc", "111", "000"]
    contrasena_lower = contrasena.lower()
    for patron in patrones_malos:
        if patron in contrasena_lower:
            puntos -= 2
            problemas.append(f"Contiene patron prohibido: {patron}")
            break
    
    # Clasificacion
    if puntos >= 7:
        clasificacion = "Muy fuerte"
    elif puntos >= 5:
        clasificacion = "Fuerte"
    elif puntos >= 3:
        clasificacion = "Media"
    else:
        clasificacion = "Debil"
    
    return clasificacion, puntos, problemas