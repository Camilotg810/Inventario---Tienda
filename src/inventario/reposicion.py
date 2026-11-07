"""Reposición de inventario: qué productos hay que pedir (HU-03)."""

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


def _validar(producto: Producto) -> None:
    """Lanza ValueError si el producto tiene cantidades negativas."""
    if producto.stock < 0:
        raise ValueError(
            f"Producto {producto.codigo}: el stock no puede ser negativo ({producto.stock})"
        )
    if producto.stock_minimo < 0:
        raise ValueError(
            f"Producto {producto.codigo}: el stock minimo no puede ser negativo "
            f"({producto.stock_minimo})"
        )


def _orden_de_urgencia(producto: Producto) -> tuple[int, str]:
    """Clave de orden: mayor faltante primero y, a igual faltante, por nombre."""
    return (-producto.faltante, producto.nombre)


def productos_por_pedir(productos: list[Producto]) -> list[Producto]:
    for producto in productos:
        _validar(producto)

    por_pedir = [p for p in productos if p.requiere_pedido]
    return sorted(por_pedir, key=_orden_de_urgencia)
