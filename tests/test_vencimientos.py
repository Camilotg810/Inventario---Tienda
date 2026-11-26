"""Pruebas de HU-04 (FarmaStock): reporte de lotes que vencen en los próximos días.

Escritas antes de la implementación, a partir de los dos escenarios Gherkin del
documento de requisitos de la semana 3 y de los casos límite.
"""

from datetime import date, datetime

import pytest

from inventario.vencimientos import Lote, LoteProximo, lotes_por_vencer

HOY = date(2026, 10, 24)


def lote(codigo, vence, unidades=10, producto="Vitamina C"):
    return Lote(producto=producto, codigo_lote=codigo, unidades=unidades, vence=vence)


# --- Escenario 1: reporte de vencimientos próximos (HU-04) ---

def test_lista_solo_los_lotes_que_vencen_en_el_rango_ordenados_por_fecha():
    en_17_dias = lote("L-102", date(2026, 11, 10), 10, "Vitamina C")
    en_42_dias = lote("L-210", date(2026, 12, 5), 25, "Ibuprofeno 400mg")
    en_6_dias = lote("L-087", date(2026, 10, 30), 8, "Loratadina 10mg")
    muy_lejano = lote("L-300", date(2027, 3, 1), 40, "Amoxicilina 500mg")
    ya_vencido = lote("L-001", date(2026, 10, 1), 5, "Jarabe")

    resultado = lotes_por_vencer(
        [en_17_dias, muy_lejano, en_42_dias, ya_vencido, en_6_dias], HOY, 60
    )

    assert [r.codigo_lote for r in resultado] == ["L-087", "L-102", "L-210"]


def test_cada_fila_muestra_producto_lote_unidades_fecha_y_dias_restantes():
    resultado = lotes_por_vencer(
        [lote("L-102", date(2026, 11, 10), 10, "Vitamina C")], HOY, 60
    )

    assert resultado == [
        LoteProximo(
            producto="Vitamina C",
            codigo_lote="L-102",
            unidades=10,
            vence=date(2026, 11, 10),
            dias_restantes=17,
        )
    ]


# --- Casos límite ---

def test_el_ultimo_dia_del_rango_se_incluye_y_el_siguiente_no():
    dentro = lote("L-60", date(2026, 12, 23))   # 60 días exactos
    fuera = lote("L-61", date(2026, 12, 24))    # 61 días

    resultado = lotes_por_vencer([dentro, fuera], HOY, 60)

    assert [r.codigo_lote for r in resultado] == ["L-60"]


def test_un_lote_que_vence_hoy_se_incluye_con_cero_dias():
    resultado = lotes_por_vencer([lote("L-00", HOY)], HOY, 60)

    assert [r.dias_restantes for r in resultado] == [0]


def test_un_lote_vencido_ayer_no_se_incluye():
    assert lotes_por_vencer([lote("L-AY", date(2026, 10, 23))], HOY, 60) == []


def test_el_rango_por_defecto_es_60_dias():
    dentro = lote("L-60", date(2026, 12, 23))
    fuera = lote("L-61", date(2026, 12, 24))

    assert lotes_por_vencer([dentro, fuera], HOY) == lotes_por_vencer(
        [dentro, fuera], HOY, 60
    )


def test_otro_rango_filtra_con_ese_rango():
    cerca = lote("L-C", date(2026, 11, 3))   # 10 días
    lejos = lote("L-L", date(2026, 12, 1))   # 38 días

    assert [r.codigo_lote for r in lotes_por_vencer([cerca, lejos], HOY, 30)] == ["L-C"]


def test_con_la_misma_fecha_ordena_por_codigo_de_lote():
    b = lote("L-B", date(2026, 11, 10))
    a = lote("L-A", date(2026, 11, 10))

    assert [r.codigo_lote for r in lotes_por_vencer([b, a], HOY, 60)] == ["L-A", "L-B"]


def test_lista_vacia_devuelve_lista_vacia():
    assert lotes_por_vencer([], HOY, 60) == []


def test_si_ningun_lote_esta_en_el_rango_devuelve_lista_vacia():
    assert lotes_por_vencer([lote("L-X", date(2027, 6, 1))], HOY, 60) == []


def test_no_modifica_la_lista_de_entrada():
    original = [lote("L-B", date(2026, 11, 10)), lote("L-A", date(2026, 10, 30))]
    copia = list(original)

    lotes_por_vencer(original, HOY, 60)

    assert original == copia


# --- Escenario 2 (error): rango de días no válido ---

@pytest.mark.parametrize(
    "dias",
    [-15, 0, 2.5, "60", True, None],
    ids=["negativo", "cero", "decimal", "texto", "bool", "none"],
)
def test_dias_que_no_es_entero_mayor_a_cero_lanza_value_error(dias):
    with pytest.raises(ValueError, match="entero mayor a 0"):
        lotes_por_vencer([lote("L-102", date(2026, 11, 10))], HOY, dias)


def test_el_mensaje_de_dias_invalido_es_el_del_requisito():
    with pytest.raises(ValueError) as error:
        lotes_por_vencer([], HOY, -15)

    assert str(error.value) == "El rango de días debe ser un número entero mayor a 0"


# --- Datos de lote inválidos: se rechazan, no se ignoran ---

def test_unidades_negativas_lanzan_value_error_con_el_codigo_del_lote():
    with pytest.raises(ValueError, match="L-NEG"):
        lotes_por_vencer([lote("L-NEG", date(2026, 11, 10), unidades=-1)], HOY, 60)


@pytest.mark.parametrize("unidades", [2.5, "10", None, True])
def test_unidades_que_no_son_enteras_lanzan_type_error_con_el_codigo(unidades):
    with pytest.raises(TypeError, match="L-TIPO"):
        invalido = lote("L-TIPO", date(2026, 11, 10), unidades=unidades)
        lotes_por_vencer([invalido], HOY, 60)


@pytest.mark.parametrize(
    "vence", ["2026-11-10", None, datetime(2026, 11, 10, 8, 0)],
    ids=["texto", "none", "datetime"],
)
def test_vence_que_no_es_una_fecha_lanza_type_error_con_el_codigo(vence):
    with pytest.raises(TypeError, match="L-FECHA"):
        lotes_por_vencer([lote("L-FECHA", vence)], HOY, 60)


def test_un_lote_invalido_se_rechaza_aunque_este_fuera_del_rango():
    lejano_invalido = lote("L-MAL", date(2030, 1, 1), unidades=-5)

    with pytest.raises(ValueError, match="L-MAL"):
        lotes_por_vencer([lejano_invalido], HOY, 60)
