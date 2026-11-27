"""Pruebas nuevas de la revisión de la semana 6 sobre HU-02 y HU-04 (FarmaStock).

Cada grupo corresponde a un hallazgo de `revision_seguridad.md`. Se escribieron
antes de corregir y fallaron en rojo con el código del commit revisado.
"""

from datetime import date, datetime

import pytest

from inventario.ingreso_lotes import registrar_ingreso, stock_total
from inventario.vencimientos import Lote, lotes_por_vencer

HOY = date(2026, 10, 24)


def lote(producto, codigo, unidades=10):
    return Lote(producto, codigo, unidades, date(2027, 1, 1))


# --- H-09: el mismo producto escrito con otras mayúsculas o espacios ---

@pytest.mark.parametrize("escrito", ["ibuprofeno 400mg", "  Ibuprofeno 400mg ",
                                     "IBUPROFENO   400MG"])
def test_el_stock_cuenta_el_producto_aunque_cambien_mayusculas_o_espacios(escrito):
    lotes = [lote("Ibuprofeno 400mg", "L-1", 10)]

    assert stock_total(lotes, escrito) == 10


def test_codigo_repetido_se_rechaza_aunque_el_producto_se_escriba_distinto():
    existentes = [lote("Ibuprofeno 400mg", "L-1")]

    with pytest.raises(ValueError, match="L-1"):
        registrar_ingreso(
            existentes, " ibuprofeno  400MG", "L-1", 5, date(2027, 6, 1), HOY
        )


def test_productos_distintos_siguen_separados():
    lotes = [lote("Ibuprofeno 400mg", "L-1", 10), lote("Ibuprofeno 600mg", "L-2", 7)]

    assert stock_total(lotes, "ibuprofeno 600mg") == 7


# --- H-10: `hoy` inválido debe dar un TypeError que lo diga ---

HOY_INVALIDOS = [datetime(2026, 10, 24, 9, 0), None, "2026-10-24", True]


@pytest.mark.parametrize("hoy", HOY_INVALIDOS)
def test_registrar_ingreso_rechaza_un_hoy_que_no_es_date(hoy):
    with pytest.raises(TypeError, match="hoy"):
        registrar_ingreso([], "Vitamina C", "L-1", 1, date(2027, 1, 1), hoy)


@pytest.mark.parametrize("hoy", HOY_INVALIDOS)
def test_lotes_por_vencer_rechaza_un_hoy_que_no_es_date(hoy):
    with pytest.raises(TypeError, match="hoy"):
        lotes_por_vencer([Lote("Vitamina C", "L-1", 1, date(2026, 11, 1))], hoy)
