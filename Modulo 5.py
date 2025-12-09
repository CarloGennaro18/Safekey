# MODULO 5: VALIDACION RECURSIVA DE INTEGRIDAD
# ============================================================================

def validar_entrada_recursiva(entrada, campos_requeridos, indice=0):
    """Valida recursivamente que una entrada tenga todos los campos"""
    if indice >= len(campos_requeridos):
        return True, []
    
    campo = campos_requeridos[indice]
    errores = []
    
    if campo not in entrada or not entrada[campo]:
        errores.append(f"Campo faltante o vacio: {campo}")
    
    es_valido, errores_restantes = validar_entrada_recursiva(
        entrada, campos_requeridos, indice + 1
    )
    
    return len(errores) == 0 and es_valido, errores + errores_restantes

def revisar_integridad_recursiva(registros, indice=0, errores_encontrados=None):
    """Revisa recursivamente la integridad de todos los registros"""
    if errores_encontrados is None:
        errores_encontrados = []
    
    if indice >= len(registros):
        return errores_encontrados
    
    registro = registros[indice]
    campos_requeridos = ['servicio', 'usuario', 'contrasena', 'metodo_cifrado', 'fecha']
    
    es_valido, errores = validar_entrada_recursiva(registro, campos_requeridos)
    
    if not es_valido:
        errores_encontrados.append({
            'indice': indice,
            'servicio': registro.get('servicio', 'DESCONOCIDO'),
            'errores': errores
        })
    
    return revisar_integridad_recursiva(registros, indice + 1, errores_encontrados)
