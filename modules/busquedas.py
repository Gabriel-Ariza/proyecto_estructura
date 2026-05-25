from utils.entradas import validar_entrada, limpiar
from utils.manejo_json import cargar_datos



#? =========== 1.A busqueda lineal por id ==============================
#? =====================================================================

def busqueda_lineal_iterativa(data, criterio_id):
    criterio_str = str(criterio_id).strip()
    coincidencias = {"vendedor": None, "producto": None, "factura": None}
    comparaciones = 0

    # Buscar en vendedores
    for id_v, nombre in data.get("vendedores", {}).items():
        comparaciones += 1
        if str(id_v) == criterio_str:
            coincidencias["vendedor"] = (id_v, nombre)
            break

    # 2. Buscar en inventario
    for id_p, info in data.get("inventario", {}).items():
        comparaciones += 1
        if str(id_p) == criterio_str:
            coincidencias["producto"] = (id_p, info)
            break

    # 3. Buscar en Ventas
    for venta in data.get("ventas", []):
        comparaciones += 1
        if str(venta.get("id_factura")) == criterio_str:
            coincidencias["factura"] = venta
            break

    return coincidencias, comparaciones





#? =========== 1.B busqueda recursiva por id ============================
#? ======================================================================

def buscar_vendedor_recursivo(lista_vendedores, idx, criterio_str):
    # si el indice supera el tamaño de la lista es porque no se encontro
    if idx >= len(lista_vendedores):
        return None, 0

    comparaciones = 1
    
    # si la clave del ítem actual coincide con el criterio, retorna el resultado y las comparaciones realizadas
    if str(lista_vendedores[idx][0]) == criterio_str:
        return lista_vendedores[idx], comparaciones


    # avanza a la siguiente posición de la lista y acumula las comparaciones hacia atrás
    res, sub_comp = buscar_vendedor_recursivo(lista_vendedores, idx + 1, criterio_str)

    # se hace una pila de llamadas recursivas hasta llegar al final de la lista, y luego se van sumando las comparaciones
    # a medida que se retorna hacia atrás

    # Retorna el resultado hallado y acumula las comparaciones hacia atrás
    return res, comparaciones + sub_comp



def buscar_producto_recursivo(lista_productos, idx, criterio_str):
    # si el indice supera el tamaño de la lista es porque no se encontro
    if idx >= len(lista_productos):
        return None, 0
        
    comparaciones = 1
    
    # Como productos es una lista de tuplas (id, info), extrae el ID de la posición 0 de forma segura
    if str(lista_productos[idx][0]) == criterio_str:
        return lista_productos[idx], comparaciones
        
    # PASO RECURSIVO: Avanza a la siguiente posición de la lista
    res, sub_comp = buscar_producto_recursivo(lista_productos, idx + 1, criterio_str)
    return res, comparaciones + sub_comp



def buscar_venta_recursivo(lista_ventas, idx, criterio_str):
    # si el indice supera el tamaño de la lista es porque no se encontro
    if idx >= len(lista_ventas):
        return None, 0
        
    comparaciones = 1
    
    # Como ventas es una lista de diccionarios, extrae el ID de la llave "id_factura" de forma segura
    if str(lista_ventas[idx].get("id_factura")) == criterio_str:
        return lista_ventas[idx], comparaciones
        
    # Invocamos la función para analizar la factura de la siguiente posición
    res, sub_comp = buscar_venta_recursivo(lista_ventas, idx + 1, criterio_str)
    return res, comparaciones + sub_comp



def busqueda_lineal_recursiva(data, criterio_id):

    criterio_str = str(criterio_id).strip()
    coincidencias = {"vendedor": None, "producto": None, "factura": None}
    
    # Convertimos a listas indexables para usarlas por indice
    lista_vendedores = list(data.get("vendedores", {}).items())
    lista_productos = list(data.get("inventario", {}).items())
    lista_ventas = data.get("ventas", [])

    # llamamos cada recursion de forma independiente pasándole sus parámetros desde el índice 0
    vendedores, vendedores_comparaciones = buscar_vendedor_recursivo(lista_vendedores, 0, criterio_str)
    productos, productos_comparaciones = buscar_producto_recursivo(lista_productos, 0, criterio_str)
    ventas, ventas_comparaciones = buscar_venta_recursivo(lista_ventas, 0, criterio_str)

    # guardamos los resultados finales al diccionario de coincidencias
    coincidencias["vendedor"] = vendedores
    coincidencias["producto"] = productos
    coincidencias["factura"] = ventas
    
    # Sumamos todas las operaciones efectuadas en la memoria
    total_comparaciones = vendedores_comparaciones + productos_comparaciones + ventas_comparaciones

    return coincidencias, total_comparaciones





#? ========= 2.A busqueda binaria por monto total factura ===============
#? ======================================================================

def ordenar_ventas_por_monto(lista_ventas):
    # facturas de menor a mayor monto usando el método de burbuja
    ventas_ordenadas = list(lista_ventas)
    n = len(ventas_ordenadas)
    for i in range(n):
        for j in range(0, n - i - 1):
            if ventas_ordenadas[j].get("total_venta", 0.0) > ventas_ordenadas[j + 1].get("total_venta", 0.0):
                aux = ventas_ordenadas[j]
                ventas_ordenadas[j] = ventas_ordenadas[j + 1]
                ventas_ordenadas[j + 1] = aux
    return ventas_ordenadas



def busqueda_binaria_iterativa(lista_ventas_ordenada, monto_buscado):
    izq = 0
    der = len(lista_ventas_ordenada) - 1
    comparaciones = 0

    while izq <= der:
        centro = (izq + der) // 2
        monto_centro = lista_ventas_ordenada[centro].get("total_venta", 0.0)
        comparaciones += 1

        if monto_centro == monto_buscado:
            return lista_ventas_ordenada[centro], comparaciones
        elif monto_centro < monto_buscado:
            izq = centro + 1
        else:
            der = centro - 1

    return None, comparaciones


def busqueda_binaria_recursiva(lista_ventas_ordenada, monto_buscado, izq, der):
    if izq > der:
        return None, 0

    centro = (izq + der) // 2
    monto_centro = lista_ventas_ordenada[centro].get("total_venta", 0.0)
    comparaciones = 1

    if monto_centro == monto_buscado:
        return lista_ventas_ordenada[centro], comparaciones
    elif monto_centro < monto_buscado:
        res, sub_comp = busqueda_binaria_recursiva(lista_ventas_ordenada, monto_buscado, centro + 1, der)
        return res, comparaciones + sub_comp
    else:
        res, sub_comp = busqueda_binaria_recursiva(lista_ventas_ordenada, monto_buscado, izq, centro - 1)
        return res, comparaciones + sub_comp






#? ================= VISTA Y ENTREGA DE RESULTADOS ======================
#? ======================================================================

def mostrar_coincidencia_lineal(coincidencias):
    encontrado = False
    print("\n" + "-"*50)
    print("RESULTADOS DE LA BÚSQUEDA SIMULTÁNEA POR ID".center(50))
    print("-"*50)
    
    if coincidencias["vendedor"]:
        id_v, nombre = coincidencias["vendedor"]
        print(f"[VENDEDOR ENCONTRADO] -> ID: {id_v} | Nombre: {nombre}")
        encontrado = True
        
    if coincidencias["producto"]:
        id_p, info = coincidencias["producto"]
        print(f"[PRODUCTO ENCONTRADO] -> ID: {id_p} | Nombre: {info['nombre']} | Precio: ${info['precio']:,.2f} | Stock: {info['stock']}")
        encontrado = True
        
    if coincidencias["factura"]:
        fac = coincidencias["factura"]
        print(f"[FACTURA ENCONTRADA]  -> Factura N°: {fac['id_factura']} | Cliente: {fac['cliente']} | Total Facturado: ${fac['total_venta']:,.2f}")
        encontrado = True

    if not encontrado:
        print("No se encontró ningún registro con ese ID en toda la base de datos.")
    print("-"*50)



def controlador_busqueda_id():
    print("\n--- BÚSQUEDA GLOBAL SIMULTÁNEA POR ID ---")
    data = cargar_datos()
    
    id_buscado = validar_entrada("Ingrese el ID numérico a rastrear: ", tipo=int, min_val=1)
    
    print("\nSeleccione el algoritmo a utilizar:")
    print("[1] Ejecución Iterativa (Ciclos)")
    print("[2] Ejecución Recursiva (Pila de funciones)")
    paradigma = validar_entrada("Opción ---> ", tipo=int, min_val=1, max_val=2)
    
    if paradigma == 1:
        coincidencias, comparaciones = busqueda_lineal_iterativa(data, id_buscado)
        print(f"\n[MÉTODO] Algoritmo Lineal Iterativo ejecutado con éxito.")
    else:
        coincidencias, comparaciones = busqueda_lineal_recursiva(data, id_buscado)
        print(f"\n[MÉTODO] Algoritmo Lineal Recursivo ejecutado con éxito.")
        
    mostrar_coincidencia_lineal(coincidencias)
    print(f"comparaciones ejecutadas: {comparaciones}\n")





def controlador_busqueda_montoFactura():
    print("\n--- BÚSQUEDA BINARIA DE FACTURAS POR MONTO ---")
    data = cargar_datos()
    
    if not data.get("ventas"):
        print("\nNo existen ventas registradas en el sistema para realizar la búsqueda.")
        return
        
    monto_buscado = validar_entrada("Ingrese el valor exacto del monto total de la factura: ", tipo=float, min_val=0.0)
    
    print("\nSeleccione el algoritmo a utilizar:")
    print("[1] Ejecución Iterativa (Ciclos)")
    print("[2] Ejecución Recursiva (Pila de funciones)")
    paradigma = validar_entrada("Opción ---> ", tipo=int, min_val=1, max_val=2)
    
    # Pre-requisito de la búsqueda binaria: ordenar la lista por el campo clave
    # utilizamos el metodo de burbuja
    ventas_ordenadas = ordenar_ventas_por_monto(data["ventas"])
    
    if paradigma == 1:
        factura, comparaciones = busqueda_binaria_iterativa(ventas_ordenadas, monto_buscado)
        print(f"\n[MÉTODO] Algoritmo Binario Iterativo ejecutado con éxito.")
    else:
        factura, comparaciones = busqueda_binaria_recursiva(ventas_ordenadas, monto_buscado, 0, len(ventas_ordenadas) - 1)
        print(f"\n[MÉTODO] Algoritmo Binario Recursivo ejecutado con éxito.")
        
    print("\n\n" + "-"*50)
    if factura:
        print(f"[FACTURA HALLADA] Factura N°: {factura['id_factura']}")
        print(f"Cliente: {factura['cliente']}")
        print(f"Fecha de Registro: {factura['fecha']}")
        print(f"Monto Total Recaudado: ${factura['total_venta']:,.2f}")
    else:
        print(f"No se encontró ninguna factura con el monto exacto de ${monto_buscado:,.2f}")
    print("-"*50)
    print(f"comparaciones binarias ejecutadas: {comparaciones}\n")