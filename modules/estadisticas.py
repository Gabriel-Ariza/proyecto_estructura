from utils.manejo_json import cargar_datos, guardar_datos
from utils.entradas import validar_entrada, limpiar
from utils.fechas_conversiones import formatear_dinero, ordenar_lista_ascendente



def calcular_total_acumulado():
    print("\n" + "="*50)
    print("      TOTAL ACUMULADO DEL PERIODO".center(50))
    print("="*50)
    data = cargar_datos()
    
    if not data["ventas"]:
        print("\n[INFO] No hay ventas registradas en el periodo.")
        return
    
    total = 0.0
    for venta in data["ventas"]:
        total += venta["total_venta"]
        
    print(f"\n El total bruto de ingresos es: {formatear_dinero(total)}")
    print(f" Cantidad de transacciones evaluadas: {len(data['ventas'])}")
    print("="*50)


def calcular_promedio_ventas():
    print("\n" + "="*50)
    print("           PROMEDIO DE VENTAS".center(50))
    print("="*50)
    data = cargar_datos()
    
    if not data["ventas"]:
        print("\n[INFO] No hay ventas registradas para promediar.")
        return
    
    total = 0.0
    cantidad_ventas = 0
    for venta in data["ventas"]:
        total += venta["total_venta"]
        cantidad_ventas += 1
        
    promedio = total / cantidad_ventas
    print(f"\n Ticket promedio por factura: {formatear_dinero(promedio)}")
    print("="*50)





def calcular_maxima_minima():
    print("\n" + "="*50)
    print("         VENTA MÁXIMA Y MÍNIMA".center(50))
    print("="*50)
    data = cargar_datos()
    
    if not data["ventas"]:
        print("\n[INFO] No hay registros para evaluar extremos.")
        return
    
    venta_max = data["ventas"][0]
    venta_min = data["ventas"][0]
    
    for venta in data["ventas"]:
        if venta["total_venta"] > venta_max["total_venta"]:
            venta_max = venta
        if venta["total_venta"] < venta_min["total_venta"]:
            venta_min = venta
            
    print(f"\nVENTA MÁXIMA (Factura #{venta_max['id_factura']}):")
    print(f"   Cliente: {venta_max['cliente']}")
    print(f"   Monto:   {formatear_dinero(venta_max['total_venta'])}")
    
    print(f"\nVENTA MÍNIMA (Factura #{venta_min['id_factura']}):")
    print(f"   Cliente: {venta_min['cliente']}")
    print(f"   Monto:   {formatear_dinero(venta_min['total_venta'])}")
    print("="*50)





def calcular_mediana_ventas():
    print("\n" + "="*50)
    print("         MEDIANA DEL CONJUNTO DE VENTAS".center(50))
    print("="*50)
    data = cargar_datos()
    
    if not data["ventas"]:
        print("\n[INFO] No hay datos de ventas para calcular la mediana.")
        return
    
    montos = []
    for venta in data["ventas"]:
        montos.append(venta["total_venta"])
        
    montos_ordenados = ordenar_lista_ascendente(montos)
    n = len(montos_ordenados)
    
    # Calcular la posición central de la mediana
    if n % 2 != 0:
        mediana = montos_ordenados[n // 2]
    else:
        mitad1 = montos_ordenados[(n // 2) - 1]
        mitad2 = montos_ordenados[n // 2]
        mediana = (mitad1 + mitad2) / 2.0
        
    print(f"\n La mediana estadística del conjunto es: {formatear_dinero(mediana)}")
    print(f" (El 50% de las ventas fueron mayores y el otro 50% menores a esta cifra)")
    print("="*50)





def calcular_top_productos():
    print("\n" + "="*50)
    print("         TOP 3 PRODUCTOS MÁS VENDIDOS".center(50))
    print("="*50)
    data = cargar_datos()
    
    if not data["ventas"]:
        print("\n[INFO] No hay histórico de ventas para consolidar productos.")
        return
        
    conteo_productos = {}
    for venta in data["ventas"]:
        for item in venta["items"]:
            nombre = item["nombre"]
            cant = item["cantidad"]
            if nombre in conteo_productos:
                conteo_productos[nombre] += cant
            else:
                conteo_productos[nombre] = cant
                
    lista_productos = list(conteo_productos.items())
    
    # burbuja ordenamiento de mayor a menor
    n = len(lista_productos)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista_productos[j][1] < lista_productos[j + 1][1]:
                aux = lista_productos[j]
                lista_productos[j] = lista_productos[j + 1]
                lista_productos[j + 1] = aux


    top_limite = 3 if n >= 3 else n
    print(f"\n Ranking de los artículos con mayor rotación en bodega:")
    for idx in range(top_limite):
        prod_nombre, prod_cant = lista_productos[idx]
        print(f"   [{idx + 1}] {prod_nombre:<30} -> {prod_cant} unidades vendidas.")
    print("="*50)




def calcular_ventas_por_vendedor():
    print("\n" + "="*60)
    print("         RENDIMIENTO DE VENTAS POR VENDEDOR".center(60))
    print("="*60)
    data = cargar_datos()
    
    if not data.get("ventas"):
        print("\n[INFO] No hay transacciones registradas en el sistema.")
        return
        
    metricas_vendedores = {}
    
    for venta in data["ventas"]:
        id_v_str = str(venta.get("id_vendedor", ""))
        monto = venta.get("total_venta", 0.0)
        
        if id_v_str not in metricas_vendedores:
            metricas_vendedores[id_v_str] = {"total": 0.0, "facturas": 0}
            
        metricas_vendedores[id_v_str]["total"] += monto
        metricas_vendedores[id_v_str]["facturas"] += 1
            
    print(f"\n{'Nombre Asesor':<22} | {'Facturas':<8} | {'Total Recaudado':<16} | {'Promedio':>11}")
    print("-"*65)
    
    for id_v, info in metricas_vendedores.items():
        nombre = data.get("vendedores", {}).get(id_v, f"Vendedor ID {id_v}")
        
        tot = info["total"]
        cant_facturas = info["facturas"]
        promedio_ind = tot / cant_facturas if cant_facturas > 0 else 0.0
        
        print(f"{nombre:<22} | {cant_facturas:<8} | {formatear_dinero(tot):<16} | {formatear_dinero(promedio_ind):>11}")
        
    print("="*60)