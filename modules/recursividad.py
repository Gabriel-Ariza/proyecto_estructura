from utils.entradas import validar_entrada, limpiar
from utils.manejo_json import cargar_datos



def sumar_ventas_recursivo(lista_ventas, idx):

    # si el indice supera el tamaño de la lista es porque no se encontro
    if idx >= len(lista_ventas):
        return 0.0
        
    # Sumamos el monto actual con lo que devuelvan las funciones de adelante
    return lista_ventas[idx].get("total_venta", 0.0) + sumar_ventas_recursivo(lista_ventas, idx + 1)




def contar_ventas_umbral_recursivo(lista_ventas, idx, umbral):
    
    # Cuenta cuántas facturas superan un valor monetario específico sin usar ciclos.
    if idx >= len(lista_ventas):
        return 0
        
    # Evaluamos la condición de la factura en la posición actual de la recursion
    if lista_ventas[idx].get("total_venta", 0.0) > umbral:
        acumulador = 1
    else:
        acumulador = 0
        
    # Sumamos nuestro acumulador (1 o 0) al resultado de las siguientes posiciones
    return acumulador + contar_ventas_umbral_recursivo(lista_ventas, idx + 1, umbral)





def buscar_en_lista_recursiva(lista, idx, criterio_str, tipo_est):
    # Función tipo bucle para buscar un ID en una lista de elementos (vendedores, productos o facturas).

    if idx >= len(lista):
        return None
        
    # Extraemos un ID según el tipo de elemento que le pasemos
    if tipo_est == "factura":
        id_actual = lista[idx].get("id_factura")
    else:
        id_actual = lista[idx][0] # Para ítems de vendedores o inventario
        
    # Comparamos el ID actual con el criterio de búsqueda
    if str(id_actual) == criterio_str:
        return lista[idx]
        
    return buscar_en_lista_recursiva(lista, idx + 1, criterio_str, tipo_est)



def buscar_id_backtracking(data, criterio_id):

    # algoritmo de busqueda con backtracking para encontrar un ID en las colecciones.
    criterio_str = str(criterio_id).strip()
    ruta_exploracion = []
    
    # --- ruta 1: Intentar buscar en Vendedores ---
    ruta_exploracion.append("Colección Vendedores")
    # Convertimos el diccionario de vendedores a una lista de tuplas para facilitar la búsqueda
    lista_v = list(data.get("vendedores", {}).items())
    res_v = buscar_en_lista_recursiva(lista_v, 0, criterio_str, "vendedor")
    
    if res_v:
        ruta_exploracion.append("Vendedor encontrado con exito")
        return True, ruta_exploracion
        

    # APLICACIÓN DEL RETROCESO (BACKTRACKING):
    # El camino de Vendedores falló, devolvió None. El algoritmo retrocede y toma otra ruta
    ruta_exploracion.append("Fallo en la ruta de Vendedores (Retrocediendo...)")
    
    # --- ruta 2: Intentar buscar en Inventario ---
    ruta_exploracion.append("Colección Inventario")
    lista_p = list(data.get("inventario", {}).items())
    res_p = buscar_en_lista_recursiva(lista_p, 0, criterio_str, "producto")
    
    if res_p:
        ruta_exploracion.append("Producto encontrado con exito")
        return True, ruta_exploracion
        
    # Segundo Retroceso en caso de fallo continuo
    ruta_exploracion.append("Fallo en la ruta de Inventario (Retrocediendo...)")
    
    # --- RUTA 3: Intentar buscar en Ventas ---
    ruta_exploracion.append("Colección Ventas")
    lista_fac = data.get("ventas", [])
    res_fac = buscar_en_lista_recursiva(lista_fac, 0, criterio_str, "factura")
    
    if res_fac:
        ruta_exploracion.append("Factura encontrada con exito")
        return True, ruta_exploracion
        
    # Si llegó aquí, todas las rutas del árbol de decisión fallaron por completo
    ruta_exploracion.append("FALLÓ (ID no existente en todo el sistema)")
    return False, ruta_exploracion





def factorial_didactico(numero):
    # en matemática el factorial de 0 o 1 es siempre 1
    if numero == 0 or numero == 1:
        return 1
        
    # Multiplicamos el número actual por el factorial de su antecesor (n - 1)
    return numero * factorial_didactico(numero - 1)