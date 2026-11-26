"""Ingreso de mercancía de FarmaStock: registrar lotes y consultar el stock (HU-02)."""

from datetime import date, datetime

from inventario.vencimientos import Lote

MENSAJE_LOTE_CADUCADO = "No se pueden ingresar lotes con fecha de vencimiento caducada"


def registrar_ingreso(
    lotes: list[Lote],
    producto: str,
    codigo_lote: str,
    unidades: int,
    vence: date,
    hoy: date,
) -> list[Lote]:
    """Devuelve una lista nueva con el lote agregado, ordenada por vencimiento."""
    if not isinstance(producto, str) or not producto.strip():
        raise ValueError("El producto no puede estar vacío")
    if not isinstance(codigo_lote, str) or not codigo_lote.strip():
        raise ValueError("El código de lote no puede estar vacío")
    if isinstance(unidades, bool) or not isinstance(unidades, int):
        raise TypeError(f"Las unidades deben ser un entero, se recibió {unidades!r}")
    if unidades <= 0:
        raise ValueError(f"Las unidades deben ser mayores a 0 (se recibió {unidades})")
    if not isinstance(vence, date) or isinstance(vence, datetime):
        raise TypeError(
            f"La fecha de vencimiento debe ser un date, se recibió {vence!r}"
        )
    if vence < hoy:
        raise ValueError(MENSAJE_LOTE_CADUCADO)
    for existente in lotes:
        if existente.producto == producto and existente.codigo_lote == codigo_lote:
            raise ValueError(f"El lote {codigo_lote} de {producto} ya está registrado")

    nuevo = Lote(producto, codigo_lote, unidades, vence)
    return sorted([*lotes, nuevo], key=lambda x: (x.vence, x.codigo_lote))


def stock_total(lotes: list[Lote], producto: str) -> int:
    """Suma las unidades de todos los lotes del producto (0 si no tiene lotes)."""
    total = 0
    for existente in lotes:
        if existente.producto == producto:
            total += existente.unidades
    return total
