# MODULO 6: GESTION DE ARCHIVOS
# ============================================================================

import os
import datetime
from Modulo_1 import (cifrado_cesar, descifrado_cesar)
def guardar_contrasenas(registros, archivo="contrasenas.txt"):
    """Guarda los registros en archivo de texto"""
    try:
        with open(archivo, 'w', encoding='utf-8') as f:
            for registro in registros:
                linea = f"{registro['servicio']}|{registro['usuario']}|"
                linea += f"{registro['contrasena']}|{registro['metodo_cifrado']}|"
                linea += f"{registro['fecha']}\n"
                f.write(linea)
        return True
    except Exception as e:
        print(f"Error al guardar: {e}")
        return False

def cargar_contrasenas(archivo="contrasenas.txt"):
    """Carga los registros desde archivo de texto"""
    registros = []
    if not os.path.exists(archivo):
        return registros
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    partes = linea.split('|')
                    if len(partes) == 5:
                        registros.append({
                            'servicio': partes[0],
                            'usuario': partes[1],
                            'contrasena': partes[2],
                            'metodo_cifrado': partes[3],
                            'fecha': partes[4]
                        })
    except Exception as e:
        print(f"Error al cargar: {e}")
    
    return registros

def registrar_log(mensaje, archivo="audit_log.txt"):
    """Registra una accion en el log de auditoria"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(archivo, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {mensaje}\n")
    except Exception as e:
        print(f"Error al registrar log: {e}")

def guardar_contrasena_maestra(contrasena, archivo="maestra.txt"):
    """Guarda la contrasena maestra cifrada"""
    cifrada = cifrado_cesar(contrasena, 7)
    try:
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(cifrada)
        return True
    except:
        return False

def cargar_contrasena_maestra(archivo="maestra.txt"):
    """Carga y descifra la contrasena maestra"""
    if not os.path.exists(archivo):
        return None
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            cifrada = f.read().strip()
            return descifrado_cesar(cifrada, 7)
    except:
        return None