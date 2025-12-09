# MODULO 4: BUSQUEDA RECURSIVA
# ============================================================================

def buscar_recursivo(lista, termino, indice=0, resultados=None):
    """Busca en una lista de forma recursiva"""
    if resultados is None:
        resultados = []
    
    if indice >= len(lista):
        return resultados
    
    elemento = lista[indice]
    termino_lower = termino.lower()
    
    # Buscar en servicio y usuario
    if (termino_lower in elemento['servicio'].lower() or 
        termino_lower in elemento['usuario'].lower()):
        resultados.append(elemento)
    
    return buscar_recursivo(lista, termino, indice + 1, resultados)