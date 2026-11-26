"""Pruebas de HU-02 (FarmaStock): ingreso de mercancía por lote y fecha.

Escritas antes de la implementación, a partir de los dos escenarios del documento
de requisitos de la semana 3 (registro exitoso y lote caducado) y de los casos límite.
"""

from datetime import date, datetime, timedelta

import pytest

from inventario.ingreso_lotes import (
    MENSAJE_LOTE_CADUCADO,
    registrar_ingreso,
    stock_total,
)
from inventario.vencimientos import Lote

HOY = date(2026, 10, 24)


def lote(codigo, vence, unidades=10, producto="Vitamina C"):
    return Lote(producto=producto, codigo_lote=codigo, unidades=unidades, vence=vence)


def ingresar(lotes, producto="Ibuprofeno 400mg", codigo="L-8821", unidades=50,
             vence=date(2027, 12, 15)):
    return registrar_ingreso(lotes, producto, codigo, unidades, vence, HOY)


# --- Escenario 1: registro exitoso de un lote con fecha válida ---

def test_ingreso_valido_agrega_el_lote_y_actualiza_el_stock_del_producto():
    resultado = ingresar([])

    assert resultado == [lote("L-8821", date(2027, 12, 15), 50, "Ibuprofeno 400mg")]
    assert stock_total(resultado, "Ibuprofeno 400mg") == 50


def test_ingreso_suma_al_stock_que_el_producto_ya_tenia():
    existentes = [lote("L-100", date(2027, 6, 1), 30, "Ibuprofeno 400mg")]

    resultado = ingresar(existentes)

    assert stock_total(resultado, "Ibuprofeno 400mg") == 80
    assert len(resultado) == 2


def test_los_lotes_quedan_ordenados_por_vencimiento_para_rotacion_fifo():
    tarde = lote("L-300", date(2028, 1, 1), 5, "Ibuprofeno 400mg")
    temprano = lote("L-050", date(2027, 1, 1), 5, "Ibuprofeno 400mg")

    resultado = ingresar([tarde, temprano])  # entra L-8821 con vence 2027-12-15

    assert [x.codigo_lote for x in resultado] == ["L-050", "L-8821", "L-300"]


def test_no_modifica_la_lista_original():
    original = [lote("L-100", date(2027, 6, 1), 30, "Ibuprofeno 400mg")]
    copia = list(original)

    ingresar(original)

    assert original == copia


# --- Casos límite ---

def test_un_lote_que_vence_hoy_se_acepta():
    resultado = ingresar([], vence=HOY)

    assert stock_total(resultado, "Ibuprofeno 400mg") == 50


def test_un_lote_que_vencio_ayer_se_rechaza():
    with pytest.raises(ValueError):
        ingresar([], vence=HOY - timedelta(days=1))


def test_una_unidad_es_la_cantidad_minima_valida():
    resultado = ingresar([], unidades=1)

    assert stock_total(resultado, "Ibuprofeno 400mg") == 1


def test_stock_de_un_producto_sin_lotes_es_cero():
    assert stock_total([], "Ibuprofeno 400mg") == 0


def test_el_stock_no_mezcla_lotes_de_otros_productos():
    lotes = [
        lote("L-1", date(2027, 1, 1), 7, "Ibuprofeno 400mg"),
        lote("L-2", date(2027, 1, 1), 99, "Loratadina 10mg"),
    ]

    assert stock_total(lotes, "Ibuprofeno 400mg") == 7


def test_el_mismo_codigo_de_lote_en_otro_producto_se_acepta():
    existentes = [lote("L-8821", date(2027, 1, 1), 10, "Loratadina 10mg")]

    resultado = ingresar(existentes)

    assert len(resultado) == 2


# --- Escenario 2 (error): lote con fecha de vencimiento caducada ---

def test_lote_caducado_se_rechaza_con_el_mensaje_del_criterio_de_aceptacion():
    existentes = [lote("L-100", date(2027, 6, 1), 30, "Loratadina 10mg")]

    with pytest.raises(ValueError) as error:
        registrar_ingreso(
            existentes, "Loratadina 10mg", "L-777", 20, date(2025, 1, 10), HOY
        )

    assert str(error.value) == (
        "No se pueden ingresar lotes con fecha de vencimiento caducada"
    )
    assert str(error.value) == MENSAJE_LOTE_CADUCADO
    assert stock_total(existentes, "Loratadina 10mg") == 30


# --- Otros errores de datos ---

@pytest.mark.parametrize("unidades", [0, -5])
def test_unidades_cero_o_negativas_se_rechazan(unidades):
    with pytest.raises(ValueError, match="unidades"):
        ingresar([], unidades=unidades)


@pytest.mark.parametrize("unidades", [2.5, "50", True, None])
def test_unidades_que_no_son_un_entero_lanzan_typeerror(unidades):
    with pytest.raises(TypeError, match="unidades"):
        ingresar([], unidades=unidades)


def test_codigo_de_lote_repetido_para_el_mismo_producto_se_rechaza():
    existentes = [lote("L-8821", date(2027, 1, 1), 10, "Ibuprofeno 400mg")]

    with pytest.raises(ValueError, match="L-8821"):
        ingresar(existentes)


@pytest.mark.parametrize("producto,codigo", [("", "L-1"), ("   ", "L-1"),
                                             ("Ibuprofeno", ""), ("Ibuprofeno", "  ")])
def test_producto_o_codigo_vacios_se_rechazan(producto, codigo):
    with pytest.raises(ValueError):
        ingresar([], producto=producto, codigo=codigo)


@pytest.mark.parametrize("vence", [datetime(2027, 12, 15, 10, 30), "2027-12-15", None])
def test_fecha_de_vencimiento_debe_ser_un_date(vence):
    with pytest.raises(TypeError, match="fecha"):
        ingresar([], vence=vence)
