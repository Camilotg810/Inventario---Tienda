"""Ejemplos de uso del módulo de inventario de FarmaStock.

Ejecutar desde la raíz del proyecto (ver README, sección Ejecución).
"""

from datetime import date

from inventario.reposicion import Producto, productos_por_pedir
from inventario.vencimientos import Lote, lotes_por_vencer

# --- HU-04: lotes que vencen en los próximos 60 días ---
# La fecha de hoy se fija para que la salida siempre sea la misma.
hoy = date(2026, 10, 24)
lotes = [
    Lote("Vitamina C", "L-102", 10, date(2026, 11, 10)),
    Lote("Ibuprofeno 400mg", "L-210", 25, date(2026, 12, 5)),
    Lote("Loratadina 10mg", "L-087", 8, date(2026, 10, 30)),
    Lote("Amoxicilina 500mg", "L-300", 40, date(2027, 3, 1)),
]

print("Lotes que vencen en los próximos 60 días (el más pronto primero):")
for fila in lotes_por_vencer(lotes, hoy, 60):
    print(
        f"- {fila.producto}, lote {fila.codigo_lote}: {fila.unidades} unidades, "
        f"vence {fila.vence:%d/%m/%Y} (faltan {fila.dias_restantes} días)"
    )

# --- Reposición: productos por pedir ---
productos = [
    Producto(codigo="A1", nombre="Arroz 500 g", stock=8, stock_minimo=10),
    Producto(codigo="B2", nombre="Aceite 1 L", stock=1, stock_minimo=20),
    Producto(codigo="C3", nombre="Azúcar 1 kg", stock=5, stock_minimo=10),
    Producto(codigo="D4", nombre="Sal 500 g", stock=50, stock_minimo=10),
]

print()
print("Productos por pedir (del más urgente al menos):")
for p in productos_por_pedir(productos):
    print(
        f"- {p.codigo} {p.nombre}: stock {p.stock}/{p.stock_minimo}, "
        f"faltan {p.faltante}"
    )
