from func.validaciones import validar_opcion


def menu():
    ciclo = True
    while ciclo:
        print("="*50)
        print("TECHSTORE ANALYTICS v1.0 - sistema de ventas")
        print("="*50,"\n")
        print("    [1] Gestion de registros")
        print("    [2] Analisis estadistico")
        print("    [3] Ordenamiento de ventas")
        print("    [4] Busqueda de registros")
        print("    [5] Demostracion de recursividad")
        print("    [6] Generacion de reportes")
        print("    [7] Salir")
        print("\n","="*48)
        print("Registros cargados: 12   -   Ventas totales: 4'500.000")
        print("="*48)
        opcion = validar_opcion((input('\nIngrese Una opción --->  ')))
"""         switch = {
                1: ,
                2: ,
                3: ,
                4: ,
                5: ,
                6: ,
                }
        switch[opcion]() """
menu()