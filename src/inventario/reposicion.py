"""Reposición de inventario: qué productos hay que pedir (HU-03)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Producto:
    codigo: str
    nombre: str
    stock: int
    stock_minimo: int


def productos_por_pedir(productos: list[Producto]) -> list[Producto]:
    por_pedir = []
    for p in productos:
        if p.stock < 0:
            raise ValueError(f"Producto {p.codigo}: el stock no puede ser negativo ({p.stock})")
        if p.stock_minimo < 0:
            raise ValueError(f"Producto {p.codigo}: el stock minimo no puede ser negativo ({p.stock_minimo})")
        if p.stock <= p.stock_minimo:
            por_pedir.append(p)

    por_pedir.sort(key=lambda p: (-(p.stock_minimo - p.stock), p.nombre))
    return por_pedir
