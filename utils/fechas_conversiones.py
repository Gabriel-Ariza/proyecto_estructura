from datetime import datetime



def ordenar_lista_ascendente(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j] > lista[j + 1]:
                # Intercambio
                aux = lista[j]
                lista[j] = lista[j + 1]
                lista[j + 1] = aux
    return lista



def parsear_fecha(cadena_fecha):
    try:
        return datetime.strptime(cadena_fecha, "%d/%m/%Y:%H:%M")
    except ValueError:
        try:
            return datetime.strptime(cadena_fecha, "%Y-%m-%d")
        except ValueError:
            return datetime.min
        



def formatear_dinero(valor):
    try:
        valor = int(float(valor))
        
        texto = "{:,}".format(valor)
        
        texto_final = texto.replace(",", ".")
        
        if valor >= 1000000:
            lista_partes = texto_final.split(".")
            millones = lista_partes[0]
            resto = ".".join(lista_partes[1:])
            texto_final = f"{millones}'{resto}"
            
        return f"${texto_final}"
    
    except (ValueError, TypeError):
        return "$0"