from utils.entradas import validar_entrada, limpiar
import modules.inventario as inv
import modules.ventas as vtas
import modules.estadisticas as est
import modules.algoritmos as ordenamiento
import modules.busquedas as busqueda
import modules.recursividad as recursividad
import modules.reportes as rept
from utils.manejo_json import cargar_datos
from utils.fechas_conversiones import formatear_dinero



def menu_inventario():
    while True:
        print("\n" + "="*66)
        print("MÓDULO: INVENTARIO Y VENDEDORES".center(66))
        print("="*66 + "\n")
        print("    [1] Listar productos")
        print("    [2] Agregar un producto al inventario")
        print("    [3] Modificar un producto")
        print("    [4] Eliminar producto")
        print("    [5] Listar vendedores")
        print("    [6] Agregar un nuevo vendedor")
        print("    [7] Modificar vendedor")
        print("    [8] Eliminar un vendedor")
        print("    [9] Regresar al Menú Principal")
        print("\n" + "="*66)
        
        opt = validar_entrada("\nSeleccione una opción ---> ", tipo=int, min_val=1, max_val=9)
        limpiar()
        
        if opt == 1:
            inv.listar_productos()
        elif opt == 2:
            inv.agregar_producto()
        elif opt == 3:
            inv.modificar_producto()
        elif opt == 4:
            inv.eliminar_producto()
        elif opt == 5:
            inv.listar_vendedores()
        elif opt == 6:
            inv.agregar_vendedor()
        elif opt == 7:
            inv.modificar_vendedor()
        elif opt == 8:
            inv.eliminar_vendedor()
        elif opt == 9:
            break



def menu_registros():
    while True:
        print("\n" + "="*66)
        print("MÓDULO 1: GESTIÓN DE REGISTROS".center(66))
        print("="*66 + "\n")
        print("\t[1] Ingresar nueva venta")
        print("\t[2] Mostrar registros")
        print("\t[3] Modificar una venta")
        print("\t[4] Eliminar registro")
        print("\t[5] Regresar al Menú Principal")
        print("\n" + "="*66)
        
        opt = validar_entrada('\nIngrese una opción ---> ', tipo=int, min_val=1, max_val=5)
        
        if opt == 1:
            vtas.ingresar_venta()
        elif opt == 2:
            vtas.mostrar_registros()
        elif opt == 3:
            vtas.modificar_registro()
        elif opt == 4:
            vtas.eliminar_registro()
        else:
            break



def menu_estadistico():
    while True:
        print("\n" + "="*66)
        print("MÓDULO 2: ESTADÍSTICAS TECHSTORE".center(66))
        print("="*66 + "\n")
        print("\t[1] Total Acumulado del Periodo")
        print("\t[2] Promedio de Ventas")
        print("\t[3] Venta Máxima y Mínima")
        print("\t[4] Calcular la Mediana del Conjunto de Ventas")
        print("\t[5] Top 3 de Productos Más Vendidos")
        print("\t[6] Ventas por Vendedor")
        print("\t[7] Regresar al Menú Principal")
        print("\n" + "="*66)
        
        opt = validar_entrada('\nIngrese una opción ---> ', tipo=int, min_val=1, max_val=7)
        
        if opt == 1:
            est.calcular_total_acumulado()
        elif opt == 2:
            est.calcular_promedio_ventas()
        elif opt == 3:
            est.calcular_maxima_minima()
        elif opt == 4:
            est.calcular_mediana_ventas()
        elif opt == 5:
            est.calcular_top_productos()
        elif opt == 6:
            est.calcular_ventas_por_vendedor()
        else:
            break


def menu_ordenamiento():
    while True:
        print("\n" + "="*66)
        print("MÓDULO 3: ALGORITMOS DE ORDENAMIENTO".center(66))
        print("="*66 + "\n")
        print("\t[1] Ordenar por Monto Total [Ascendente - Descendente]")
        print("\t[2] Ordenar por Fecha [Cronológico - Inverso]")
        print("\t[3] Ordenar por Nombre de Producto [A-Z  /  Z-A]")
        print("\t[4] Regresar al Menú Principal")
        print("\n" + "="*66)
        
        opt = validar_entrada('\nIngrese una opción ---> ', tipo=int, min_val=1, max_val=4)
        limpiar()
        
        if opt == 1:
            ordenamiento.ejecutar_ordenamiento_monto()
        elif opt == 2:
            ordenamiento.ejecutar_ordenamiento_fecha()
        elif opt == 3:
            ordenamiento.ejecutar_ordenamiento_producto()
        elif opt == 4:
            break



def menu_busqueda():
    while True:
        print("\n" + "="*66)
        print("MÓDULO 4: MÓDULOS DE BÚSQUEDA".center(66))
        print("="*66 + "\n")
        print("\t[1] Búsqueda por ID (Producto - Vendedor - Factura)")
        print("\t[2] Búsqueda Binaria por Monto Total (Factura)")
        print("\t[3] Regresar al Menú Principal")
        print("\n" + "="*66)
        
        opt = validar_entrada('\nIngrese una opción ---> ', tipo=int, min_val=1, max_val=3)
        
        if opt == 1:
            busqueda.controlador_busqueda_id()
        elif opt == 2:
            busqueda.controlador_busqueda_montoFactura()
        elif opt == 3:
            break



def menu_recursividad():
    while True:
        print("\n" + "="*66)
        print("MÓDULO 5: RECURSIVIDAD EXPLÍCITA".center(66))
        print("="*66 + "\n")
        print("\t[1] Calcular Suma Total de Ventas (Recursivo)")
        print("\t[2] Contar Ventas sobre un Umbral Económico")
        print("\t[3] Búsqueda por ID con Retroceso (Backtracking)")
        print("\t[4] Cálculo de Factorial para Fórmula Estadística")
        print("\t[5] Regresar al Menú Principal")
        print("\n" + "="*66)
        
        opt = validar_entrada('\nIngrese una opción ---> ', tipo=int, min_val=1, max_val=5)
        
        if opt == 1:
            recursividad.controlador_sumar_ventas()
        elif opt == 2:
            recursividad.controlador_contar_umbral()
        elif opt == 3:
            recursividad.controlador_backtracking()
        elif opt == 4:
            recursividad.factorial_didactico()
        else:
            break



def menu_reportes():
    while True:
        print("\n" + "="*66)
        print("MÓDULO 6: EXPORTACIÓN DE REPORTES".center(66))
        print("="*66 + "\n")
        print("\t[1] Reporte de Ventas del Día")
        print("\t[2] Reporte de Productos Más Vendidos")
        print("\t[3] Reporte de Alerta de Baja Existencia")
        print("\t[4] Regresar al Menú Principal")
        print("\n" + "="*66)
        
        opt = validar_entrada('\nIngrese una opción ---> ', tipo=int, min_val=1, max_val=3)
        
        if opt == 1:
            rept.reporte_ventas_del_dia()
        elif opt == 2:
            rept.reporte_mas_vendidos()
        elif opt == 3:
            limite = validar_entrada("Defina el tope límite de existencias a buscar (ENTER para 5): ", tipo=int, default=5, min_val=0)
            print(f"\n[*] Buscando artículos con stock crítico igual o menor a {limite}...")
            rept.reporte_baja_existencia(por_defecto=limite)
        else:
            break


def menu():
    while True:
        data = cargar_datos()
        total_regs, dinero_total = vtas.obtener_kpis_menu(data)
        info_banner = f"Registros cargados: {total_regs}   -   Ventas totales: {formatear_dinero(dinero_total)}"
        
        print("\n" + "="*66)
        print("TECHSTORE ANALYTICS v1.0 - SISTEMA DE VENTAS".center(66))
        print("="*66 + "\n")
        print("\t[1] Gestión de Inventario y Vendedores")
        print("\t[2] Gestión de Ventas")
        print("\t[3] Análisis Estadístico (KPIs)")
        print("\t[4] Algoritmos de Ordenamiento")
        print("\t[5] Módulos de Búsqueda")
        print("\t[6] Recursividad")
        print("\t[7] Módulo de Reportes")
        print("\t[8] Salir del Sistema")
        print("\n" + "="*66)
        print(info_banner.center(66))
        print("="*66)
        
        opcion = validar_entrada('\nIngrese una opción ---> ', tipo=int, min_val=0, max_val=8)
        limpiar()
        if opcion == 0:
            print("\n\n\t✓ Saliendo del programa...")
            print("\t✓ Gracias por usar TECHSTORE ANALYTICS v1.0\n")
            break
        else:
            switch = {
                1: menu_inventario,
                2: menu_registros,
                3: menu_estadistico,
                4: menu_ordenamiento,
                5: menu_busqueda,
                6: menu_recursividad,
                7: menu_reportes,
            }
            switch[opcion]()
menu()