"""Reposición de inventario: qué productos hay que pedir (HU-03)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Producto:
    codigo: str
    nombre: str
    stock: int
    stock_minimo: int


def productos_por_pedir(productos: list[Producto]) -> list[Producto]:
    raise NotImplementedError("Pendiente de implementar")
