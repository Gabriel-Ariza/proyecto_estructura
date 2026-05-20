from utils.manejo_json import cargar_datos
from utils.entradas import validar_entrada, limpiar
from utils.fechas_conversiones import parsear_fecha



def ordenar_burbuja_monto(ventas, ascendente=True):
    #Ordena las ventas por el campo total_venta usando Burbuja
    n = len(ventas)
    pasos = 0
    intercambios = 0
    
    dirección = "Ascendente" if ascendente else "Descendente"
    print(f"\n[INFO] Iniciando Ordenamiento Burbuja por 'Monto Total' en dirección: {dirección}")
    
    for i in range(n):
        for j in range(0, n - i - 1):
            pasos += 1
            condicion = (ventas[j]["total_venta"] > ventas[j + 1]["total_venta"]) if ascendente else (ventas[j]["total_venta"] < ventas[j + 1]["total_venta"])
            
            if condicion:
                aux = ventas[j]
                ventas[j] = ventas[j + 1]
                ventas[j + 1] = aux
                intercambios += 1
                
    print(f"[MÉTRICAS] Pasos/Comparaciones: {pasos} | Intercambios reales: {intercambios}")
    return ventas




def ordenar_insercion_fecha(ventas, cronologico=True):
    #Ordena las ventas por el campo fecha usando Inserción pura.
    pasos = 0
    intercambios = 0
    n = len(ventas)
    
    dirección = "Cronológico (Antiguo a Reciente)" if cronologico else "Inverso (Reciente a Antiguo)"
    print(f"\n[INFO] Iniciando Ordenamiento por Inserción por 'Fecha' en dirección: {dirección}")
    
    for i in range(1, n):
        clave = ventas[i]
        fecha_clave = parsear_fecha(clave["fecha"])
        j = i - 1
        
        while j >= 0:
            pasos += 1
            fecha_j = parsear_fecha(ventas[j]["fecha"])
            
            condicion = (fecha_j > fecha_clave) if cronologico else (fecha_j < fecha_clave)
            
            if condicion:
                ventas[j + 1] = ventas[j]
                intercambios += 1
                j -= 1
            else:
                break
        ventas[j + 1] = clave
        
    print(f"[MÉTRICAS] Pasos/Comparaciones: {pasos} | Desplazamientos/Intercambios: {intercambios}")
    return ventas


def ordenar_seleccion_producto(ventas, ascendente=True):
    #Ordena las ventas alfabéticamente por el nombre del primer producto comprado usando Selección.
    pasos = 0
    intercambios = 0
    n = len(ventas)
    
    dirección = "A-Z (Alfabético)" if ascendente else "Z-A (Inverso)"
    print(f"\n[INFO] Iniciando Ordenamiento por Selección por 'Nombre de Producto' en dirección: {dirección}")
    
    for i in range(n):
        indice_extremo = i
        for j in range(i + 1, n):
            pasos += 1
            
            prod_j = ventas[j]["items"][0]["nombre"].lower() if ventas[j]["items"] else ""
            prod_extremo = ventas[indice_extremo]["items"][0]["nombre"].lower() if ventas[indice_extremo]["items"] else ""
            
            condicion = (prod_j < prod_extremo) if ascendente else (prod_j > prod_extremo)
            if condicion:
                indice_extremo = j
                
        if indice_extremo != i:
            aux = ventas[i]
            ventas[i] = ventas[indice_extremo]
            ventas[indice_extremo] = aux
            intercambios += 1
            
    print(f"[MÉTRICAS] Pasos/Comparaciones: {pasos} | Intercambios reales: {intercambios}")
    return ventas





def mostrar_resultado_ordenado(ventas_ordenadas):
    #Muestra una mini-tabla formateada con los resultados del ordenamiento actual.
    print("\n" + "-"*90)
    print(f"{'ID Factura':<12} | {'Fecha':<16} | {'Primer Producto':<35} | {'Total Venta':>15}")
    print("-"*90)
    for v in ventas_ordenadas:
        primer_prod = v["items"][0]["nombre"] if v["items"] else "Sin ítems"
        if len(primer_prod) > 32:
            primer_prod = primer_prod[:29] + "..."
        print(f"{v['id_factura']:<12} | {v['fecha']:<16} | {primer_prod:<35} | ${v['total_venta']:>14,.2f}")
    print("-"*90 + "\n")





def ejecutar_ordenamiento_monto():
    #Controlador que maneja la sub-interfaz, carga la data y ejecuta Burbuja.
    data = cargar_datos()
    if not data["ventas"]:
        print("\n[INFO] No hay registros de ventas para poder realizar ordenamientos.")
        return
    
    print("\n--- CONFIGURACIÓN DE DIRECCIÓN ---")
    print("[1] Orden Ascendente (Menor a Mayor)")
    print("[2] Orden Descendente (Mayor a Menor)")
    dir_opt = validar_entrada("Seleccione la dirección: ", tipo=int, min_val=1, max_val=2)
    asc = (dir_opt == 1)
    
    ventas_copia = list(data["ventas"])
    limpiar()
    res = ordenar_burbuja_monto(ventas_copia, ascendente=asc)
    mostrar_resultado_ordenado(res)





def ejecutar_ordenamiento_fecha():
    #Controlador que maneja la sub-interfaz, carga la data y ejecuta Inserción.
    data = cargar_datos()
    if not data["ventas"]:
        print("\n[INFO] No hay registros de ventas para poder realizar ordenamientos.")
        return
        
    print("\n--- CONFIGURACIÓN DE DIRECCIÓN ---")
    print("[1] Cronológico (Más antiguo primero)")
    print("[2] Inverso (Más reciente primero)")
    dir_opt = validar_entrada("Seleccione la dirección: ", tipo=int, min_val=1, max_val=2)
    cron = (dir_opt == 1)
    
    ventas_copia = list(data["ventas"])
    limpiar()
    res = ordenar_insercion_fecha(ventas_copia, cronologico=cron)
    mostrar_resultado_ordenado(res)





def ejecutar_ordenamiento_producto():
    #Controlador que maneja la sub-interfaz, carga la data y ejecuta Selección.
    data = cargar_datos()
    if not data["ventas"]:
        print("\n[INFO] No hay registros de ventas para poder realizar ordenamientos.")
        return
        
    print("\n--- CONFIGURACIÓN DE DIRECCIÓN ---")
    print("[1] Alfabético (A a la Z)")
    print("[2] Alfabético Inverso (Z a la A)")
    dir_opt = validar_entrada("Seleccione la dirección: ", tipo=int, min_val=1, max_val=2)
    asc = (dir_opt == 1)
    
    ventas_copia = list(data["ventas"])
    limpiar()
    res = ordenar_seleccion_producto(ventas_copia, ascendente=asc)
    mostrar_resultado_ordenado(res)