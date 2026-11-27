"""Comprobaciones de tipo que comparten los módulos de FarmaStock."""

from datetime import date, datetime


def es_entero(valor: object) -> bool:
    """True si `valor` es un entero de verdad; un `bool` no cuenta (True no es 1)."""
    return isinstance(valor, int) and not isinstance(valor, bool)


def es_fecha(valor: object) -> bool:
    """True si `valor` es un `date`; un `datetime` no cuenta (trae hora)."""
    return isinstance(valor, date) and not isinstance(valor, datetime)
