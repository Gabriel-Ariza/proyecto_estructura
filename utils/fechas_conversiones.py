
def formato_pesos(valor):

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