import os


def validar_entrada(mensaje, tipo=str, **kwargs):

    # Solo hasta que de un dato correcto retorna
    while True:
        try:
            valor_de_entrada = input(mensaje).strip()
            
            # Validamos si es null, y si se ha definido un valor por defecto en los kwargs, lo retornamos
            if not valor_de_entrada or valor_de_entrada.isspace():
                if 'default' in kwargs:
                    return kwargs['default']
                print("\n [ERROR] No has ingresado ningún dato... \n")
                continue

            # Convertimos el valor del input al solicitado
            dato_convertido = tipo(valor_de_entrada)
            
            # Si se ha definido un valor mínimo en los kwargs, lo validamos
            if 'min_val' in kwargs and dato_convertido < kwargs['min_val']:
                min_v = kwargs['min_val']
                print(f"\n [ERROR] El número {dato_convertido} está fuera del valor mínimo permitido. \n")
                continue

            # Si se ha definido un valor máximo en los kwargs, lo validamos
            if 'max_val' in kwargs and dato_convertido > kwargs['max_val']:
                max_v = kwargs['max_val']
                print(f"\n [ERROR] El número {dato_convertido} está fuera del valor máximo permitido. \n")
                continue

            # Si se pide un rango en el que debe estar el número, validamos ambos extremos
            if 'min_val' in kwargs and 'max_val' in kwargs:
                min_v = kwargs['min_val']
                max_v = kwargs['max_val']
                if not (min_v <= dato_convertido <= max_v):
                    print(f"\n [ERROR] El número {dato_convertido} está fuera del rango permitido! ({min_v}-{max_v}). \n")
                    continue
                
            return dato_convertido

        except (ValueError, TypeError):
            if tipo == int or tipo == float:
                print(f"\n [ERROR] '{valor_de_entrada}' no es un número válido. No se permiten caracteres ni letras... \n")
            else:
                print(f"\n [ERROR] Error: Se esperaba un dato de tipo {tipo.__name__}. Intente de nuevo. \n")



def limpiar():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')