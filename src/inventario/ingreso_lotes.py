"""Ingreso de mercancía de FarmaStock: registrar lotes y consultar el stock (HU-02)."""

from datetime import date, datetime

from inventario.vencimientos import Lote

MENSAJE_LOTE_CADUCADO = "No se pueden ingresar lotes con fecha de vencimiento caducada"


def _exigir_texto(valor: str, nombre: str) -> None:
    """Lanza ValueError si `valor` no es un texto con contenido."""
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{nombre} no puede estar vacío")


def _exigir_unidades_validas(unidades: int) -> None:
    """Lanza TypeError si no es un entero (un bool no vale) y ValueError si es <= 0."""
    if isinstance(unidades, bool) or not isinstance(unidades, int):
        raise TypeError(f"Las unidades deben ser un entero, se recibió {unidades!r}")
    if unidades <= 0:
        raise ValueError(f"Las unidades deben ser mayores a 0 (se recibió {unidades})")


def _exigir_fecha_vigente(vence: date, hoy: date) -> None:
    """Lanza TypeError si no es un `date` y ValueError si ya está caducada.

    Un lote que vence hoy se acepta: la historia solo rechaza fechas anteriores.
    """
    if not isinstance(vence, date) or isinstance(vence, datetime):
        raise TypeError(
            f"La fecha de vencimiento debe ser un date, se recibió {vence!r}"
        )
    if vence < hoy:
        raise ValueError(MENSAJE_LOTE_CADUCADO)


def _clave_producto(nombre: str) -> str:
    """Nombre sin diferencias de mayúsculas ni de espacios, para comparar productos."""
    return " ".join(nombre.split()).casefold()


def _ya_esta_registrado(lotes: list[Lote], producto: str, codigo_lote: str) -> bool:
    """Un código de lote es único dentro de cada producto."""
    clave = _clave_producto(producto)
    return any(
        _clave_producto(lote.producto) == clave and lote.codigo_lote == codigo_lote
        for lote in lotes
    )


def _orden_de_vencimiento(lote: Lote) -> tuple[date, str]:
    """Primero el que vence antes; si empatan, por código de lote (rotación FIFO)."""
    return (lote.vence, lote.codigo_lote)


def registrar_ingreso(
    lotes: list[Lote],
    producto: str,
    codigo_lote: str,
    unidades: int,
    vence: date,
    hoy: date,
) -> list[Lote]:
    """Devuelve una lista nueva con el lote agregado, ordenada por vencimiento.

    No modifica `lotes`. Lanza TypeError o ValueError si los datos no valen,
    o si el lote ya está registrado para ese producto.
    """
    _exigir_texto(producto, "El producto")
    _exigir_texto(codigo_lote, "El código de lote")
    _exigir_unidades_validas(unidades)
    _exigir_fecha_vigente(vence, hoy)
    if _ya_esta_registrado(lotes, producto, codigo_lote):
        raise ValueError(f"El lote {codigo_lote} de {producto} ya está registrado")

    nuevo = Lote(producto, codigo_lote, unidades, vence)
    return sorted([*lotes, nuevo], key=_orden_de_vencimiento)


def stock_total(lotes: list[Lote], producto: str) -> int:
    """Suma las unidades de todos los lotes del producto (0 si no tiene lotes)."""
    clave = _clave_producto(producto)
    return sum(
        lote.unidades for lote in lotes if _clave_producto(lote.producto) == clave
    )
