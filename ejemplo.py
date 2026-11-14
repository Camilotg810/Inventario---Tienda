"""Ejemplo de uso de productos_por_pedir con los datos de la tabla del README.

Ejecutar desde la raíz del proyecto (ver README, sección Ejecución).
"""

from inventario.reposicion import Producto, productos_por_pedir

productos = [
    Producto(codigo="A1", nombre="Arroz 500 g", stock=8, stock_minimo=10),
    Producto(codigo="B2", nombre="Aceite 1 L", stock=1, stock_minimo=20),
    Producto(codigo="C3", nombre="Azúcar 1 kg", stock=5, stock_minimo=10),
    Producto(codigo="D4", nombre="Sal 500 g", stock=50, stock_minimo=10),
]

print("Productos por pedir (del más urgente al menos):")
for p in productos_por_pedir(productos):
    print(
        f"- {p.codigo} {p.nombre}: stock {p.stock}/{p.stock_minimo}, "
        f"faltan {p.faltante}"
    )
