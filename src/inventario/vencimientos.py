"""Vencimientos de FarmaStock: qué lotes vencen pronto (HU-04)."""

from dataclasses import dataclass
from datetime import date, datetime

MENSAJE_DIAS_INVALIDOS = "El rango de días debe ser un número entero mayor a 0"


@dataclass(frozen=True)
class Lote:
    """Lote de un medicamento con su fecha de vencimiento.

    Atributos:
        producto: nombre del medicamento, por ejemplo "Vitamina C".
        codigo_lote: identificador del lote, por ejemplo "L-102".
        unidades: unidades que quedan del lote (entero >= 0).
        vence: fecha de vencimiento (un `date`, no un `datetime`).
    """

    producto: str
    codigo_lote: str
    unidades: int
    vence: date


@dataclass(frozen=True)
class LoteProximo:
    """Fila del reporte: un lote que vence pronto y los días que le quedan."""

    producto: str
    codigo_lote: str
    unidades: int
    vence: date
    dias_restantes: int


def _validar_dias(dias: int) -> None:
    """Lanza ValueError si `dias` no es un entero mayor a 0 (un bool no vale)."""
    if isinstance(dias, bool) or not isinstance(dias, int) or dias <= 0:
        raise ValueError(MENSAJE_DIAS_INVALIDOS)


def _validar_hoy(hoy: date) -> None:
    """Lanza TypeError si `hoy` no es un `date` (un `datetime` tampoco vale)."""
    if not isinstance(hoy, date) or isinstance(hoy, datetime):
        raise TypeError(f"La fecha de hoy debe ser un date, se recibió {hoy!r}")


def _validar_lote(lote: Lote) -> None:
    """Lanza TypeError o ValueError, con el código del lote, si sus datos no valen."""
    codigo, unidades = lote.codigo_lote, lote.unidades
    if isinstance(unidades, bool) or not isinstance(unidades, int):
        raise TypeError(
            f"Lote {codigo}: las unidades deben ser un entero, se recibió {unidades!r}"
        )
    if unidades < 0:
        raise ValueError(
            f"Lote {codigo}: las unidades no pueden ser negativas ({unidades})"
        )
    if not isinstance(lote.vence, date) or isinstance(lote.vence, datetime):
        raise TypeError(
            f"Lote {codigo}: la fecha de vencimiento debe ser un date, "
            f"se recibió {lote.vence!r}"
        )


def _orden_de_vencimiento(fila: LoteProximo) -> tuple[date, str]:
    """Clave de orden: primero el que vence antes y, a igual fecha, por lote."""
    return (fila.vence, fila.codigo_lote)


def lotes_por_vencer(
    lotes: list[Lote], hoy: date, dias: int = 60
) -> list[LoteProximo]:
    """Devuelve los lotes que vencen pronto, el que vence antes primero.

    Un lote entra en el reporte si le quedan entre 0 y `dias` días (inclusive:
    el que vence hoy y el que vence justo en `hoy + dias` sí entran). Los lotes ya
    vencidos no entran. El orden es por fecha de vencimiento y, a igual fecha,
    por código de lote.

    Recibe:
        lotes: lista de `Lote`; puede estar vacía. No se modifica.
        hoy: fecha desde la que se cuentan los días (se recibe para poder probar).
        dias: tamaño del rango, entero mayor a 0. Por defecto 60.

    Devuelve:
        Una lista nueva de `LoteProximo` con producto, lote, unidades, fecha y
        días restantes; vacía si ningún lote cae en el rango.

    Lanza:
        ValueError: si `dias` no es un entero mayor a 0, o si un lote tiene
            unidades negativas (el mensaje incluye el código del lote).
        TypeError: si `hoy` no es un `date`, o si las unidades de un lote no son
            un entero o su fecha de vencimiento no es un `date` (en los lotes, el
            mensaje incluye el código del lote).
        Se validan todos los lotes antes de filtrar, así que un dato inválido nunca
        se ignora aunque el lote esté fuera del rango.
    """
    _validar_hoy(hoy)
    _validar_dias(dias)
    for lote in lotes:
        _validar_lote(lote)

    filas = [
        LoteProximo(
            producto=lote.producto,
            codigo_lote=lote.codigo_lote,
            unidades=lote.unidades,
            vence=lote.vence,
            dias_restantes=(lote.vence - hoy).days,
        )
        for lote in lotes
    ]
    en_rango = [fila for fila in filas if 0 <= fila.dias_restantes <= dias]
    return sorted(en_rango, key=_orden_de_vencimiento)
