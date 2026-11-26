"""Vencimientos de FarmaStock: qué lotes vencen pronto (HU-04)."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Lote:
    producto: str
    codigo_lote: str
    unidades: int
    vence: date


@dataclass(frozen=True)
class LoteProximo:
    producto: str
    codigo_lote: str
    unidades: int
    vence: date
    dias_restantes: int


def lotes_por_vencer(lotes: list[Lote], hoy: date, dias: int = 60) -> list[LoteProximo]:
    raise NotImplementedError
