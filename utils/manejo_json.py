import json
from pathlib import Path

ruta_archivo = Path(__file__).resolve().parent.parent / 'data.json'
# accede a la raiz del proyecto y luego a la data

data_inicial = []


def cargar_datos():

    if not ruta_archivo.exists():
        guardar_datos(data_inicial)
        return data_inicial.copy()

    try:
        with ruta_archivo.open('r', encoding='utf-8') as f:
            data = json.load(f)
            if not data:
                guardar_datos(data_inicial)
                return data_inicial.copy()
            return data
    except (json.JSONDecodeError, ValueError):
        guardar_datos(data_inicial)
        return data_inicial.copy()


def guardar_datos(data):

    with ruta_archivo.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)