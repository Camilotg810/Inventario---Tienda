"""Reposición de inventario: qué productos hay que pedir (HU-03)."""

import unicodedata
from dataclasses import dataclass


@dataclass(frozen=True)
class Producto:
    codigo: str
    nombre: str
    stock: int
    stock_minimo: int

    @property
    def faltante(self) -> int:
        """Unidades que faltan para llegar al stock mínimo (0 o menos si sobra)."""
        return self.stock_minimo - self.stock

    @property
    def requiere_pedido(self) -> bool:
        return self.stock <= self.stock_minimo


def _exigir_no_negativo(codigo: str, descripcion: str, valor: int) -> None:
    """Lanza ValueError si `valor` es negativo, indicando el código del producto."""
    if valor < 0:
        raise ValueError(
            f"Producto {codigo}: {descripcion} no puede ser negativo ({valor})"
        )


def _validar(producto: Producto) -> None:
    """Lanza ValueError si el producto tiene cantidades negativas."""
    _exigir_no_negativo(producto.codigo, "el stock", producto.stock)
    _exigir_no_negativo(producto.codigo, "el stock mínimo", producto.stock_minimo)


def _clave_nombre(nombre: str) -> str:
    """Nombre sin tildes ni distinción de mayúsculas, para ordenar alfabéticamente."""
    descompuesto = unicodedata.normalize("NFD", nombre.casefold())
    return "".join(c for c in descompuesto if not unicodedata.combining(c))


def _orden_de_urgencia(producto: Producto) -> tuple[int, str]:
    """Clave de orden: mayor faltante primero y, a igual faltante, por nombre."""
    return (-producto.faltante, _clave_nombre(producto.nombre))


def productos_por_pedir(productos: list[Producto]) -> list[Producto]:
    for producto in productos:
        _validar(producto)

    por_pedir = [p for p in productos if p.requiere_pedido]
    return sorted(por_pedir, key=_orden_de_urgencia)
