import os
from datetime import date
from utils.manejo_json import cargar_datos



def ordenar_burbuja_conteo(lista_conteo):
    n = len(lista_conteo)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista_conteo[j][1] < lista_conteo[j + 1][1]:
                aux = lista_conteo[j]
                lista_conteo[j] = lista_conteo[j + 1]
                lista_conteo[j + 1] = aux
    return lista_conteo


def reporte_ventas_del_dia():
    data = cargar_datos()
    hoy = date.today().isoformat()

    ventas_hoy = [v for v in data.get('ventas', []) if v.get('fecha', '').startswith(hoy) or hoy in v.get('fecha', '')]
    
    if not ventas_hoy:
        print(f"\n[INFO] No hay ventas registradas el día de hoy ({hoy}).")
        return

    total_dia = 0.0
    lineas = [f"Ventas del día ({hoy}):", "-" * 50]
    
    for venta in ventas_hoy:
        id_factura = venta.get('id_factura', 'N/A')
        for item in venta.get('items', []):
            subtotal = item.get('subtotal', 0)
            total_dia += subtotal
            lineas.append(f"Factura: {id_factura} | Producto: {item.get('id_producto')} | Cantidad: {item.get('cantidad')} | Subtotal: ${subtotal:,.2f}")

    lineas.append("-" * 50)
    lineas.append(f"Total del día: ${total_dia:,.2f}")
    
    print("\n" + "\n".join(lineas))

    ruta = os.path.join(os.getcwd(), 'reportes', f"ventas_del_dia_{hoy}.txt")
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write("\n".join(lineas))
    print(f"✓ Reporte exportado a: {ruta}")





def reporte_mas_vendidos():
    data = cargar_datos()
    if not data.get('ventas'):
        print("\n[INFO] No hay ventas registradas para generar el reporte.")
        return
        
    contador = {}
    for venta in data.get('ventas', []):
        for item in venta.get('items', []):
            pid = str(item.get('id_producto'))
            cantidad = item.get('cantidad', 0)
            contador[pid] = contador.get(pid, 0) + cantidad

    lista_conteo = [[pid, cant] for pid, cant in contador.items()]
    ordenados = ordenar_burbuja_conteo(lista_conteo)

    lineas = ["Productos más vendidos:", "-" * 50]
    for pid, cantidad in ordenados:
        nombre = data.get('inventario', {}).get(pid, {}).get('nombre', 'Producto desconocido')
        lineas.append(f"ID {pid:<5} | {nombre:<30} | Vendidos: {cantidad}")

    print("\n" + "\n".join(lineas))

    hoy = date.today().isoformat()
    ruta = os.path.join(os.getcwd(), 'reportes', f"mas_vendidos_{hoy}.txt")
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write("\n".join(lineas))
    print(f"✓ Reporte exportado a: {ruta}")





def reporte_baja_existencia(por_defecto=5):
    data = cargar_datos()
    bajos = [(pid, p) for pid, p in data.get('inventario', {}).items() if p.get('stock', 0) <= por_defecto]
    
    if not bajos:
        print(f"\n[INFO] No hay productos con stock menor o igual a {por_defecto}.")
        return
        
    lineas = [f"Productos con baja existencia (<= {por_defecto}):", "-" * 50]
    for pid, p in bajos:
        lineas.append(f"ID {pid:<5} | {p['nombre']:<30} | Stock: {p['stock']}")

    print("\n" + "\n".join(lineas))

    hoy = date.today().isoformat()
    ruta = os.path.join(os.getcwd(), 'reportes', f"baja_existencia_{hoy}.txt")
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write("\n".join(lineas))
    print(f"✓ Reporte exportado a: {ruta}")