from datetime import datetime
from utils.manejo_json import cargar_datos, guardar_datos
from utils.entradas import validar_entrada



def obtener_kpis_menu(data):
    total_ventas_cant = len(data.get("ventas", []))
    
    dinero_total = 0.0
    for venta in data.get("ventas", []):
        dinero_total += venta.get("total_venta", 0.0)
        
    return total_ventas_cant, dinero_total



def ingresar_venta():
    print("\n" + "="*70)
    print("         REGISTRO DE NUEVA VENTA".center(70))
    print("="*70 + "\n")
    
    data = cargar_datos()
    
    # Validar que existan productos y vendedores para poder vender
    if not data["inventario"]:
        print("[ERROR] No hay productos en el inventario. Registre productos primero.")
        return
    if not data["vendedores"]:
        print("[ERROR] No hay vendedores registrados. Registre vendedores primero.")
        return

    items_venta = []
    total_venta = 0
    
    nuevo_id = max([v["id_factura"] for v in data["ventas"]], default=0) + 1 if data["ventas"] else 1


    print("--- Vendedores Disponibles ---")
    for id_v, nombre_v in data["vendedores"].items():
        print(f" ID: {id_v} - Nombre: {nombre_v}")
    print("-" * 35)
    
    id_vendedor = validar_entrada("Ingrese el ID del vendedor que realiza la venta: ", tipo=int)
    if str(id_vendedor) not in data["vendedores"]:
        print("\n[ERROR] ID de vendedor no encontrado. Operación cancelada.")
        return
        
    nombre_vendedor = data["vendedores"][str(id_vendedor)]
    cliente = validar_entrada("Nombre del cliente: ", default="Consumidor Final")
    fecha = datetime.now().strftime("%d/%m/%Y:%H:%M")
    
    print("\n--- Lista de productos ---")
    
    while True:
        id_prod = validar_entrada("ID del producto (0 para terminar): ", tipo=int, min_val=0)
        if id_prod == 0:
            break
            
        str_id_prod = str(id_prod)
        if str_id_prod not in data["inventario"]:
            print("[ERROR] El ID de producto no existe en el inventario. Intente de nuevo.\n")
            continue
            
        producto_info = data["inventario"][str_id_prod]
        stock_disponible = producto_info["stock"]
        
        if stock_disponible <= 0:
            print(f"[ERROR] '{producto_info['nombre']}' no tiene stock disponible (Stock: 0).\n")
            continue
            
        cantidad = validar_entrada(f"Cantidad para '{producto_info['nombre']}' (Disponible: {stock_disponible}): ", tipo=int, min_val=1)
        
        if cantidad > stock_disponible:
            print(f"[ERROR] Stock insuficiente. Solo puede llevar hasta {stock_disponible} unidades.\n")
            continue
            
        # Descontar stock inmediatamente del inventario
        producto_info["stock"] -= cantidad
        
        precio_unitario = producto_info["precio"] if "precio" in producto_info else producto_info.get("precio", 0.0)
        subtotal = cantidad * precio_unitario
        total_venta += subtotal
        
        items_venta.append({
            "id_producto": id_prod,
            "nombre": producto_info["nombre"],
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "subtotal": subtotal
        })
        
        print(f" Añadido: {producto_info['nombre']} x{cantidad} = ${subtotal:,.2f}\n")
    
    if items_venta:
        nueva_venta = {
            "id_factura": nuevo_id,
            "fecha": fecha,
            "id_vendedor": id_vendedor,
            "vendedor": nombre_vendedor,
            "cliente": cliente,
            "items": items_venta,
            "total_venta": total_venta
        }
        data["ventas"].append(nueva_venta)
        guardar_datos(data)
        print("\n" + "Venta registrada con éxito.".center(50))
        print(f"ID Factura: {nuevo_id} | Total: ${total_venta:,.2f}\n")
    else:
        print("\nVenta cancelada (No se añadieron productos).")





def mostrar_registros():
    data = cargar_datos()
    
    if not data["ventas"]:
        print("\nNo hay registros de ventas.")
        return
    
    print("\n" + "="*125)
    print("LISTADO DE VENTAS REGISTRADAS".center(125))
    print("="*125)
    
    print(f"{'ID':<5} | {'Fecha':<16} | {'Vendedor':<15} | {'Cliente':<18} | {'Resumen Productos':<40} | {'Total':>12}")
    print("-"*125)
    
    for v in data["ventas"]:
        id_vendedor_v = str(v.get("id_vendedor", ""))
        nombre_vendedor = data["vendedores"].get(id_vendedor_v, v.get("vendedor", "Desconocido"))
        
        items_resumen = ", ".join([f"{item['nombre'][:12]} (x{item['cantidad']})" for item in v["items"]])
        if len(items_resumen) > 40:
            items_resumen = items_resumen[:37] + "..."
        
        print(f"{v['id_factura']:<5} | {v['fecha']:<16} | {nombre_vendedor:<15} | {v['cliente']:<18} | {items_resumen:<40} | ${v['total_venta']:>11,.2f}")
    
    print("-"*125 + "\n")


def modificar_registro():
    data = cargar_datos()
    
    if not data["ventas"]:
        print("\nNo hay registros para modificar.")
        return
    
    id_factura = validar_entrada("\nIngrese el ID de la factura a modificar: ", tipo=int, min_val=1)
    
    venta_encontrada = None
    indice = -1
    
    for i, v in enumerate(data["ventas"]):
        if v["id_factura"] == id_factura:
            venta_encontrada = v
            indice = i
            break
    
    if not venta_encontrada:
        print(f"\n[ERROR] No se encontró factura con ID {id_factura}")
        return
    
    print(f"\n--- Modificando Factura #{id_factura} ---")
    print("[1] Reasignar Vendedor por ID")
    print("[2] Modificar nombre del cliente")
    print("[3] Modificar fecha manualmente")
    print("[4] Cancelar")
    
    opcion = validar_entrada('\nSeleccione qué desea modificar: ', tipo=int, min_val=1, max_val=4)
    
    if opcion == 1:
        print("\n--- Vendedores Disponibles ---")
        for id_v, nombre_v in data["vendedores"].items():
            print(f" ID: {id_v} - Nombre: {nombre_v}")
        print("-"*35)
        
        nuevo_id_v = validar_entrada("Ingrese el nuevo ID del vendedor: ", tipo=int)
        if str(nuevo_id_v) in data["vendedores"]:
            data["ventas"][indice]["id_vendedor"] = nuevo_id_v
            data["ventas"][indice]["vendedor"] = data["vendedores"][str(nuevo_id_v)]
            print("✓ Vendedor actualizado con éxito.")
        else:
            print("[ERROR] ID de vendedor no válido. No se realizaron cambios.")
            return
            
    elif opcion == 2:
        nuevo_cliente = validar_entrada("Nuevo nombre de cliente: ")
        data["ventas"][indice]["cliente"] = nuevo_cliente
        print("✓ Cliente actualizado con éxito.")
        
    elif opcion == 3:
        nueva_fecha = validar_entrada("Nueva fecha (DD/MM/YYYY:HH:MM): ")
        data["ventas"][indice]["fecha"] = nueva_fecha
        print("✓ Fecha actualizada con éxito.")
    else:
        print("Modificación cancelada.")
        return
    
    guardar_datos(data)





def eliminar_registro():
    data = cargar_datos()
    
    if not data["ventas"]:
        print("\nNo hay registros para eliminar.")
        return
    
    id_factura = validar_entrada("\nIngrese el ID de la factura a eliminar: ", tipo=int, min_val=1)
    
    venta_encontrada = None
    indice = -1
    
    for i, v in enumerate(data["ventas"]):
        if v["id_factura"] == id_factura:
            venta_encontrada = v
            indice = i
            break
    
    if not venta_encontrada:
        print(f"\n[ERROR] No se encontró factura con ID {id_factura}")
        return
    
    print(f"\n--- Confirmación de Eliminación ---")
    print(f"ID Factura: {venta_encontrada['id_factura']}")
    print(f"Fecha:      {venta_encontrada['fecha']}")
    print(f"Cliente:    {venta_encontrada['cliente']}")
    print(f"Total:      ${venta_encontrada['total_venta']:,.2f}")
    
    confirmacion = validar_entrada("\n¿Confirma la eliminación? Esta acción devolverá los productos al stock (si/no): ").lower()
    
    if confirmacion == "si":
        for item in venta_encontrada["items"]:
            id_p_str = str(item["id_producto"])
            if id_p_str in data["inventario"]:
                data["inventario"][id_p_str]["stock"] += item["cantidad"]
        
        data["ventas"].pop(indice)
        guardar_datos(data)
        print(f"\n✓ Factura #{id_factura} eliminada correctamente y stock reabastecido.")
    else:
        print("\nEliminación cancelada.")