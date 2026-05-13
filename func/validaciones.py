

def es_opcion_valida(valor, min_val, max_val):

    try:
        numero = int(valor)
        if min_val <= numero <= max_val:
            return True, None
        else:
            return False, f"El número {numero} está fuera del rango de opciones permitidas! ({min_val}-{max_val})."
            
    except (ValueError, TypeError):
        if not valor or valor.isspace():
            return False, "No has ingresado ningún dato..."
        return False, f"'{valor}' no es un número válido. No se permiten caracteres ni letras..."



def validar_opcion(entrada_inicial, min_val=1, max_val=7):
    
    while True:
        es_valida, mensaje_error = es_opcion_valida(entrada_inicial, min_val, max_val)
        
        if es_valida:
            return int(entrada_inicial)
        
        print("\n", "[ERROR]  " + mensaje_error, "\n")
        
        valor_a_validar = input(f"Introduce una opción nuevamente ({min_val}-{max_val}) ---> ").strip()
        entrada_inicial = valor_a_validar