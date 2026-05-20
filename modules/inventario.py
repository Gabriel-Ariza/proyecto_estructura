from utils.manejo_json import cargar_datos, guardar_datos
from utils.entradas import validar_entrada, limpiar



def listar_productos():
    data = cargar_datos()
        
    if not data["inventario"]:
        print("\n[INFO] No hay productos registrados en el inventario.")
        return

    print("\n" + "="*70)
    print("MÓDULO: LISTADO DE PRODUCTOS EN INVENTARIO".center(70))
    print("="*70)
    print(f"{'ID':<6} | {'Nombre del Producto':<35} | {'Precio Unit.':>14} | {'Stock':<6}")
    print("-"*70)
    
    for id_p, info in data["inventario"].items():        
        print(f"{id_p:<6} | {info['nombre']:<35} | ${info['precio']:>13,.2f} | {info['stock']:<6} | ")
    print("-"*70 + "\n")





def validar_nombre_producto_unico(data):
    while True:
        nombre = validar_entrada("Nombre del producto: ")
        
        existe = False
        for info in data["inventario"].values():
            if info["nombre"].lower() == nombre.lower():
                existe = True
                break
        
        if existe:
            print(f"\n[ERROR] Ya existe un producto registrado con el nombre '{nombre}'. Intente con otro.")
            print("-" * 50)
        else:
            return nombre

def agregar_producto():
    print("\n--- Registrar Nuevo Producto ---")
    data = cargar_datos()

    nombre = validar_nombre_producto_unico(data)

    # 2. Autogenerar ID manualmente
    ids_existentes = list(data["inventario"].keys())
    nuevo_id = 201
    if ids_existentes:
        mayor_id = 0
        for id_str in ids_existentes:
            id_int = int(id_str)
            if id_int > mayor_id:
                mayor_id = id_int
        nuevo_id = mayor_id + 1

    precio = validar_entrada("Precio unitario: ", tipo=float, min_val=0.0)
    stock = validar_entrada("Stock inicial: ", tipo=int, min_val=0)

    data["inventario"][str(nuevo_id)] = {
        "nombre": nombre,
        "precio": precio,
        "stock": stock,
    }
    
    guardar_datos(data)
    print(f"\n✓ Producto '{nombre}' añadido con éxito. ID Asignado: {nuevo_id}")





def modificar_producto():
    print("\n--- Modificar Datos de Producto ---")
    data = cargar_datos()
    
    if not data["inventario"]:
        print("\n[INFO] No hay productos registrados para modificar.")
        return
        
    id_p = validar_entrada("Ingrese el ID del producto a modificar: ", tipo=int)
    str_id_p = str(id_p)
    
    if str_id_p not in data["inventario"]:
        print(f"\n[ERROR] No se encontró el producto con ID {id_p}")
        return
        
    p = data["inventario"][str_id_p]
    print(f"\nEditando: {p['nombre']}")
    print("[Presione ENTER para mantener el valor actual]")
    print("-" * 45)

    nuevo_nombre = validar_entrada(f"Nuevo nombre ({p['nombre']}): ", tipo=str, default=p['nombre'])
    nuevo_precio = validar_entrada(f"Nuevo precio ({p['precio']}): ", tipo=float, min_val=0.0, default=p['precio'])
    nuevo_stock = validar_entrada(f"Nuevo stock ({p['stock']}): ", tipo=int, min_val=0, default=p['stock'])

    data["inventario"][str_id_p].update({
        "nombre": nuevo_nombre, 
        "precio": nuevo_precio, 
        "stock": nuevo_stock
    })
    
    guardar_datos(data)
    print("\nProducto actualizado con éxito.")





def eliminar_producto():
    print("\n--- Eliminar Producto de Inventario ---")
    data = cargar_datos()
    
    if not data["inventario"]:
        print("\n[INFO] No hay productos para eliminar.")
        return
        
    id_p = validar_entrada("Ingrese el ID del producto a eliminar: ", tipo=int)
    str_id_p = str(id_p)
    
    if str_id_p in data["inventario"]:
        nombre_prod = data["inventario"][str_id_p]["nombre"]
        
        # Validacion si el producto esta asociado a alguna venta
        for venta in data["ventas"]:
            for item in venta["items"]:
                if item["id_producto"] == id_p:
                    print(f"\n[ERROR] No se puede eliminar '{nombre_prod}': Ya se encuentra asociado a la factura #{venta['id_factura']}.")
                    return
                    
        confirmacion = validar_entrada(f"¿Está seguro de eliminar de forma permanente '{nombre_prod}'? (si/no): ").lower()
        if confirmacion == "si":
            del data["inventario"][str_id_p]
            guardar_datos(data)
            print(f"\n✓ El producto '{nombre_prod}' ha sido removido del sistema.")
        else:
            print("\nOperación cancelada.")
    else:
        print("\n[ERROR] ID de producto no encontrado.")





def listar_vendedores(data=None):
    if data is None:
        data = cargar_datos()
        
    if not data["vendedores"]:
        print("\n[INFO] No hay vendedores registrados en el sistema.")
        return

    print("\n" + "="*50)
    print("MÓDULO: LISTADO DE VENDEDORES".center(50))
    print("="*50)
    print(f"{'ID':<6} | {'Nombre Completo del Vendedor'}")
    print("-"*50)
    for id_v, nombre in data["vendedores"].items():
        print(f"{id_v:<6} | {nombre}")
    print("-"*50 + "\n")




def agregar_vendedor():
    print("\n--- Registrar Nuevo Vendedor ---")
    data = cargar_datos()
    
    ids_existentes = list(data["vendedores"].keys())
    nuevo_id = 1
    if ids_existentes:
        mayor_id = 0
        for id_str in ids_existentes:
            id_int = int(id_str)
            if id_int > mayor_id:
                mayor_id = id_int
        nuevo_id = mayor_id + 1

    nombre = validar_entrada("Nombre completo del vendedor: ")
    
    data["vendedores"][str(nuevo_id)] = nombre
    guardar_datos(data)
    print(f"\nVendedor '{nombre}' registrado con éxito. ID Asignado: {nuevo_id}")




def modificar_vendedor():
    print("\n--- Modificar Nombre de Vendedor ---")
    data = cargar_datos()
    
    if not data["vendedores"]:
        print("\n[INFO] No hay vendedores registrados.")
        return
        
    id_v = validar_entrada("Ingrese el ID del vendedor a modificar: ", tipo=int)
    str_id_v = str(id_v)
    
    if str_id_v in data["vendedores"]:
        nombre_antiguo = data["vendedores"][str_id_v]
        nuevo_nombre = validar_entrada(f"Nuevo nombre para '{nombre_antiguo}': ")
        
        data["vendedores"][str_id_v] = nuevo_nombre
        
        for venta in data["ventas"]:
            if venta["id_vendedor"] == id_v:
                venta["vendedor"] = nuevo_nombre
                
        guardar_datos(data)
        print("Datos del vendedor actualizados de manera integral.")
    else:
        print("\n[ERROR] ID de vendedor no encontrado.")





def eliminar_vendedor():
    print("\n--- Eliminar Registro de Vendedor ---")
    data = cargar_datos()
    
    if not data["vendedores"]:
        print("\n[INFO] No hay vendedores registrados.")
        return
        
    id_v = validar_entrada("Ingrese el ID del vendedor a dar de baja: ", tipo=int)
    str_id_v = str(id_v)
    
    if str_id_v in data["vendedores"]:
        nombre_vendedor = data["vendedores"][str_id_v]
                        
        # 2. Validación de que no tenga facturas asociadas en ventas
        for venta in data["ventas"]:
            if venta["id_vendedor"] == id_v:
                print(f"\n[ERROR] No se puede eliminar a '{nombre_vendedor}': Tiene facturas de venta asociadas en el histórico.")
                return
                
        confirmacion = validar_entrada(f"¿Confirma la eliminación del vendedor '{nombre_vendedor}'? (si/no): ").lower()
        if confirmacion == "si":
            del data["vendedores"][str_id_v]
            guardar_datos(data)
            print(f"\n✓ El vendedor '{nombre_vendedor}' ha sido removido del repositorio corporativo.")
        else:
            print("\nOperación cancelada.")
    else:
        print("\n[ERROR] ID de vendedor no encontrado.")