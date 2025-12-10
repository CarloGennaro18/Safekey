# MODULO 7: INTERFAZ Y MENU PRINCIPAL
# ============================================================================
import os
import random
from datetime import datetime 

from Modulo_1 import (cifrado_cesar, descifrado_cesar, cifrado_recursivo, descifrado_recursivo)
from Modulo_2 import (analizar_fuerza_contrasena)
from Modulo_3 import (generar_contrasena)
from Modulo_4 import (buscar_recursivo)
from Modulo_5 import (revisar_integridad_recursiva)
from Modulo_6 import (guardar_contrasenas, cargar_contrasena_maestra, registrar_log, guardar_contrasena_maestra, cargar_contrasenas)

def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu_principal():
    """Muestra el menu principal del sistema"""
    print("\n" + "="*60)
    print("           SAFEKEY VAULT+ - GESTOR DE CONTRASENAS")
    print("="*60)
    print("1. Agregar nueva contrasena")
    print("2. Consultar contrasenas")
    print("3. Editar contrasena")
    print("4. Eliminar contrasena")
    print("5. Buscar contrasenas")
    print("6. Generar contrasena segura")
    print("7. Revisar integridad del sistema")
    print("8. Ver log de auditoria")
    print("9. Salir")
    print("="*60)

def verificar_contrasena_maestra():
    """Verifica la contrasena maestra con 3 intentos"""
    contrasena_guardada = cargar_contrasena_maestra()
    
    if contrasena_guardada is None:
        print("\n*** PRIMERA VEZ - CONFIGURAR CONTRASENA MAESTRA ***")
        while True:
            nueva = input("Ingrese contrasena maestra: ")
            if len(nueva) < 6:
                print("La contrasena debe tener al menos 6 caracteres.")
                continue
            confirmar = input("Confirme contrasena maestra: ")
            if nueva == confirmar:
                guardar_contrasena_maestra(nueva)
                registrar_log("Contrasena maestra configurada")
                print("Contrasena maestra guardada exitosamente!")
                return True
            else:
                print("Las contrasenas no coinciden. Intente nuevamente.")
    
    intentos = 3
    while intentos > 0:
        intento = input(f"\nIngrese contrasena maestra ({intentos} intentos): ")
        if intento == contrasena_guardada:
            registrar_log("Acceso exitoso al sistema")
            return True
        intentos -= 1
        if intentos > 0:
            print(f"Contrasena incorrecta. Intentos restantes: {intentos}")
    
    print("\n*** SISTEMA BLOQUEADO - DEMASIADOS INTENTOS FALLIDOS ***")
    registrar_log("Sistema bloqueado por intentos fallidos")
    return False

def agregar_contrasena(registros):
    """Agrega una nueva contrasena al sistema"""
    print("\n--- AGREGAR NUEVA CONTRASENA ---")
    
    servicio = input("Nombre del servicio (ej: Gmail): ")
    usuario = input("Usuario o correo: ")
    
    print("\nOpciones:")
    print("1. Ingresar contrasena manualmente")
    print("2. Generar contrasena segura")
    opcion = input("Seleccione opcion: ")
    
    if opcion == "2":
        contrasena = generar_contrasena_interactivo()
    else:
        contrasena = input("Contrasena: ")
    
    # Analizar fuerza
    clasificacion, puntos, problemas = analizar_fuerza_contrasena(contrasena)
    print(f"\nAnalisis de seguridad:")
    print(f"Clasificacion: {clasificacion} ({puntos} puntos)")
    if problemas:
        print("Problemas detectados:")
        for problema in problemas:
            print(f"  - {problema}")
    
    # Elegir metodo de cifrado
    print("\nMetodo de cifrado:")
    print("1. Cifrado Cesar")
    print("2. Cifrado Recursivo")
    metodo = input("Seleccione metodo (1 o 2): ")
    
    if metodo == "2":
        contrasena_cifrada = cifrado_recursivo(contrasena)
        metodo_nombre = "recursivo"
    else:
        contrasena_cifrada = cifrado_cesar(contrasena, 5)
        metodo_nombre = "cesar"
    
    # Crear registro
    nuevo_registro = {
        'servicio': servicio,
        'usuario': usuario,
        'contrasena': contrasena_cifrada,
        'metodo_cifrado': metodo_nombre,
        'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    registros.append(nuevo_registro)
    guardar_contrasenas(registros)
    registrar_log(f"Anadida contrasena para '{servicio}'")
    
    print(f"\nContrasena guardada exitosamente para {servicio}!")
    input("\nPresione Enter para continuar...")

def consultar_contrasenas(registros):
    """Consulta y muestra las contrasenas guardadas"""
    if len(registros) == 0:
        print("\nNo hay contrasenas guardadas.")
        input("\nPresione Enter para continuar...")
        return
    
    print("\n--- CONTRASENAS GUARDADAS ---")
    for i, registro in enumerate(registros, 1):
        print(f"\n{i}. Servicio: {registro['servicio']}")
        print(f"   Usuario: {registro['usuario']}")
        print(f"   Metodo: {registro['metodo_cifrado']}")
        print(f"   Fecha: {registro['fecha']}")
        print(f"   Contrasena: [CIFRADA]")
    
    print("\n0. Volver al menu")
    seleccion = input("\nSeleccione numero para ver contrasena (0 para volver): ")
    
    try:
        num = int(seleccion)
        if num == 0:
            return
        if 1 <= num <= len(registros):
            registro = registros[num - 1]
            
            # Descifrar
            if registro['metodo_cifrado'] == "recursivo":
                contrasena_real = descifrado_recursivo(registro['contrasena'])
            else:
                contrasena_real = descifrado_cesar(registro['contrasena'], 5)
            
            print(f"\nContrasena descifrada: {contrasena_real}")
            registrar_log(f"Consultada contrasena de '{registro['servicio']}'")
        else:
            print("Numero invalido.")
    except ValueError:
        print("Entrada invalida.")
    
    input("\nPresione Enter para continuar...")

def editar_contrasena(registros):
    """Edita una contrasena existente"""
    if len(registros) == 0:
        print("\nNo hay contrasenas para editar.")
        input("\nPresione Enter para continuar...")
        return
    
    print("\n--- EDITAR CONTRASENA ---")
    for i, registro in enumerate(registros, 1):
        print(f"{i}. {registro['servicio']} - {registro['usuario']}")
    
    try:
        num = int(input("\nSeleccione numero a editar: "))
        if 1 <= num <= len(registros):
            registro = registros[num - 1]
            
            print(f"\nEditando: {registro['servicio']}")
            print("Deje en blanco para mantener el valor actual")
            
            nuevo_servicio = input(f"Servicio [{registro['servicio']}]: ")
            nuevo_usuario = input(f"Usuario [{registro['usuario']}]: ")
            nueva_contrasena = input("Nueva contrasena (Enter para mantener): ")
            
            if nuevo_servicio:
                registro['servicio'] = nuevo_servicio
            if nuevo_usuario:
                registro['usuario'] = nuevo_usuario
            if nueva_contrasena:
                # Cifrar nueva contrasena
                if registro['metodo_cifrado'] == "recursivo":
                    registro['contrasena'] = cifrado_recursivo(nueva_contrasena)
                else:
                    registro['contrasena'] = cifrado_cesar(nueva_contrasena, 5)
            
            registro['fecha'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            guardar_contrasenas(registros)
            registrar_log(f"Editada contrasena de '{registro['servicio']}'")
            print("\nContrasena actualizada exitosamente!")
        else:
            print("Numero invalido.")
    except ValueError:
        print("Entrada invalida.")
    
    input("\nPresione Enter para continuar...")

def eliminar_contrasena(registros):
    """Elimina una contrasena del sistema"""
    if len(registros) == 0:
        print("\nNo hay contrasenas para eliminar.")
        input("\nPresione Enter para continuar...")
        return
    
    print("\n--- ELIMINAR CONTRASENA ---")
    for i, registro in enumerate(registros, 1):
        print(f"{i}. {registro['servicio']} - {registro['usuario']}")
    
    try:
        num = int(input("\nSeleccione numero a eliminar: "))
        if 1 <= num <= len(registros):
            registro = registros[num - 1]
            confirmar = input(f"Eliminar '{registro['servicio']}'? (s/n): ")
            if confirmar.lower() == 's':
                servicio_eliminado = registro['servicio']
                registros.pop(num - 1)
                guardar_contrasenas(registros)
                registrar_log(f"Eliminada contrasena de '{servicio_eliminado}'")
                print("\nContrasena eliminada exitosamente!")
            else:
                print("\nOperacion cancelada.")
        else:
            print("Numero invalido.")
    except ValueError:
        print("Entrada invalida.")
    
    input("\nPresione Enter para continuar...")

def buscar_contrasenas(registros):
    """Busca contrasenas usando busqueda recursiva"""
    if len(registros) == 0:
        print("\nNo hay contrasenas para buscar.")
        input("\nPresione Enter para continuar...")
        return
    
    print("\n--- BUSCAR CONTRASENAS ---")
    termino = input("Ingrese termino de busqueda: ")
    
    resultados = buscar_recursivo(registros, termino)
    
    if len(resultados) == 0:
        print(f"\nNo se encontraron resultados para '{termino}'")
    else:
        print(f"\nSe encontraron {len(resultados)} resultado(s):")
        for resultado in resultados:
            print(f"\n- Servicio: {resultado['servicio']}")
            print(f"  Usuario: {resultado['usuario']}")
            print(f"  Fecha: {resultado['fecha']}")
    
    registrar_log(f"Busqueda realizada: '{termino}'")
    input("\nPresione Enter para continuar...")

def generar_contrasena_interactivo():
    """Genera una contrasena de forma interactiva"""
    print("\n--- GENERADOR DE CONTRASENAS ---")
    
    try:
        longitud = int(input("Longitud (minimo 8): "))
        if longitud < 8:
            longitud = 8
    except ValueError:
        longitud = 12
    
    mayusculas = input("Incluir mayusculas? (s/n): ").lower() == 's'
    numeros = input("Incluir numeros? (s/n): ").lower() == 's'
    simbolos = input("Incluir simbolos? (s/n): ").lower() == 's'
    
    contrasena = generar_contrasena(longitud, mayusculas, numeros, simbolos)
    
    print(f"\nContrasena generada: {contrasena}")
    
    clasificacion, puntos, problemas = analizar_fuerza_contrasena(contrasena)
    print(f"Fuerza: {clasificacion} ({puntos} puntos)")
    
    registrar_log("Contrasena generada automaticamente")
    
    return contrasena

def revisar_integridad(registros):
    """Revisa la integridad del sistema recursivamente"""
    print("\n--- REVISION DE INTEGRIDAD ---")
    print("Analizando registros...")
    
    errores = revisar_integridad_recursiva(registros)
    
    if len(errores) == 0:
        print("\nTodos los registros estan correctos!")
        print(f"Total de registros verificados: {len(registros)}")
    else:
        print(f"\nSe encontraron {len(errores)} registro(s) con problemas:")
        for error in errores:
            print(f"\nRegistro #{error['indice'] + 1}: {error['servicio']}")
            for problema in error['errores']:
                print(f"  - {problema}")
    
    registrar_log(f"Revision de integridad: {len(errores)} errores encontrados")
    input("\nPresione Enter para continuar...")

def ver_log():
    """Muestra el log de auditoria"""
    print("\n--- LOG DE AUDITORIA ---")
    
    if not os.path.exists("audit_log.txt"):
        print("\nNo hay registros en el log.")
    else:
        try:
            with open("audit_log.txt", 'r', encoding='utf-8') as f:
                contenido = f.read()
                if contenido:
                    print(contenido)
                else:
                    print("\nEl log esta vacio.")
        except Exception as e:
            print(f"Error al leer log: {e}")
    
    input("\nPresione Enter para continuar...")

#  ==================== Funcion principal =============================

def main():
    """Funcion principal del programa"""
    limpiar_pantalla()
    print("\n" + "="*60)
    print("         BIENVENIDO A SAFEKEY VAULT+")
    print("="*60)
    
    # Verificar contrasena maestra
    if not verificar_contrasena_maestra():
        return
    
    # Cargar registros
    registros = cargar_contrasenas()
    
    while True:
        limpiar_pantalla()
        mostrar_menu_principal()
        
        opcion = input("\nSeleccione una opcion: ")
        
        if opcion == "1":
            agregar_contrasena(registros)
        elif opcion == "2":
            consultar_contrasenas(registros)
        elif opcion == "3":
            editar_contrasena(registros)
        elif opcion == "4":
            eliminar_contrasena(registros)
        elif opcion == "5":
            buscar_contrasenas(registros)
        elif opcion == "6":
            contrasena = generar_contrasena_interactivo()
            input("\nPresione Enter para continuar...")
        elif opcion == "7":
            revisar_integridad(registros)
        elif opcion == "8":
            ver_log()
        elif opcion == "9":
            print("\nGracias por usar SAFEKEY VAULT+!")
            registrar_log("Sistema cerrado")
            break
        else:
            print("\nOpcion invalida.")
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()