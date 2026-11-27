"""Reposición: qué productos hay que pedir (HU-R1; en la semana 5 se llamó HU-03)."""

import unicodedata
from dataclasses import dataclass

from inventario.validaciones import es_entero


@dataclass(frozen=True)
class Producto:
    """Producto del inventario con su stock actual y su umbral de reposición.

    Atributos:
        codigo: identificador único del producto, por ejemplo "A1".
        nombre: nombre legible, por ejemplo "Arroz 500 g".
        stock: unidades disponibles (entero >= 0).
        stock_minimo: umbral de reposición (entero >= 0).
    """

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
        """True si el stock llegó al mínimo o quedó por debajo (stock <= mínimo)."""
        return self.stock <= self.stock_minimo


def _exigir_entero_no_negativo(codigo: str, descripcion: str, valor: int) -> None:
    """Valida un dato numérico del producto, indicando su código si falla.

    Lanza TypeError si `valor` no es un entero (un bool tampoco vale) y
    ValueError si es negativo.
    """
    if not es_entero(valor):
        raise TypeError(
            f"Producto {codigo}: {descripcion} debe ser un entero, "
            f"se recibió {valor!r}"
        )
    if valor < 0:
        raise ValueError(
            f"Producto {codigo}: {descripcion} no puede ser negativo ({valor})"
        )


def _validar(producto: Producto) -> None:
    """Lanza TypeError o ValueError si stock o stock mínimo no son válidos."""
    _exigir_entero_no_negativo(producto.codigo, "el stock", producto.stock)
    _exigir_entero_no_negativo(
        producto.codigo, "el stock mínimo", producto.stock_minimo
    )


def _clave_nombre(nombre: str) -> str:
    """Nombre sin tildes ni distinción de mayúsculas, para ordenar alfabéticamente."""
    descompuesto = unicodedata.normalize("NFD", nombre.casefold())
    return "".join(c for c in descompuesto if not unicodedata.combining(c))


def _orden_de_urgencia(producto: Producto) -> tuple[int, str]:
    """Clave de orden: mayor faltante primero y, a igual faltante, por nombre."""
    return (-producto.faltante, _clave_nombre(producto.nombre))


def productos_por_pedir(productos: list[Producto]) -> list[Producto]:
    """Devuelve los productos que hay que pedir al proveedor, del más urgente al menos.

    Un producto se pide cuando `stock <= stock_minimo`. El orden es: mayor
    faltante primero (`stock_minimo - stock`) y, a igual faltante, por nombre
    alfabético sin distinguir mayúsculas ni tildes.

    Recibe:
        productos: lista de `Producto`; puede estar vacía. No se modifica.

    Devuelve:
        Una lista nueva con los productos por pedir; vacía si ninguno lo requiere.

    Lanza:
        TypeError: si `stock` o `stock_minimo` de algún producto no es un entero.
        ValueError: si `stock` o `stock_minimo` de algún producto es negativo.
        Ambos mensajes incluyen el código del producto. Se validan todos los
        productos antes de filtrar, así que un dato inválido nunca se ignora.
    """
    for producto in productos:
        _validar(producto)

    por_pedir = [p for p in productos if p.requiere_pedido]
    return sorted(por_pedir, key=_orden_de_urgencia)
