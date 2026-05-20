import json
from pathlib import Path

ruta_archivo = Path(__file__).resolve().parent.parent / 'data.json'
# accede a la raiz del proyecto y luego a la data


data_inicial = {
    "inventario": {
        201: {"nombre": "Teclado Mecánico RGB", "precio": 189900.0, "stock": 15},
        202: {"nombre": "Mouse Gamer Pro", "precio": 85000.0, "stock": 40},
        203: {"nombre": "Nintendo Switch", "precio": 1500000.0, "stock": 10},
        204: {"nombre": "Auriculares Inalámbricos", "precio": 299900.0, "stock": 25},
        205: {"nombre": "Silla Gamer Ergonómica", "precio": 499900.0, "stock": 5}
    },
    "vendedores": {
        1: "Carlos Ruiz",
        2: "Laura Torres",
        3: "Benito Campos"
    },
    "ventas": [
        {"id_factura": 1,"fecha": "19/05/2026:14:30","id_vendedor": 1,"cliente": "Juan Pérez",
            "items": [
                {"id_producto": 201,"nombre": "Teclado Mecánico RGB","cantidad": 2,"precio_unitario": 189900.0,"subtotal": 379800.0},
                {"id_producto": 202,"nombre": "Mouse Gamer Pro","cantidad": 1,"precio_unitario": 85000.0,"subtotal": 85000.0}
            ],
            "total_venta": 464800.0
        },
        {"id_factura": 2,"fecha": "20/05/2026:10:15","id_vendedor": 2,"cliente": "María Gómez",
            "items": [
                {"id_producto": 203,"nombre": "Nintendo Switch","cantidad": 1,"precio_unitario": 1500000.0,"subtotal": 1500000.0}
            ],
            "total_venta": 1500000.0
        },
        {"id_factura": 3,"fecha": "21/05/2026:16:45","id_vendedor": 3,"cliente": "Pedro Martínez",
            "items": [
                {"id_producto": 204,"nombre": "Auriculares Inalámbricos","cantidad": 1,"precio_unitario": 299900.0,"subtotal": 299900.0},
                {"id_producto": 205,"nombre": "Silla Gamer Ergonómica","cantidad": 1,"precio_unitario": 499900.0,"subtotal": 499900.0}
            ],
            "total_venta": 799800.0
        }
    ]
}



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