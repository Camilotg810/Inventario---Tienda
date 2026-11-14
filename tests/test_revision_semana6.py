"""Pruebas nuevas de la revisión de la semana 6 (las de la semana 5 no se tocan)."""

import pytest

from inventario.reposicion import Producto, productos_por_pedir


def producto(codigo, nombre, stock=0, minimo=5):
    return Producto(codigo=codigo, nombre=nombre, stock=stock, stock_minimo=minimo)


# --- H-01: el orden por nombre debe ser alfabético de verdad ---

def test_desempate_por_nombre_no_distingue_mayusculas():
    zeta = producto("A1", "Zeta")
    alfa = producto("B2", "alfa")

    assert productos_por_pedir([zeta, alfa]) == [alfa, zeta]


def test_desempate_por_nombre_ignora_tildes():
    zeta = producto("A1", "Zeta")
    arbol = producto("B2", "Árbol")
    azucar = producto("C3", "Azúcar")

    assert productos_por_pedir([zeta, azucar, arbol]) == [arbol, azucar, zeta]


# --- H-02: datos que no son enteros se rechazan en vez de ignorarse ---

@pytest.mark.parametrize(
    "stock_invalido",
    [float("nan"), 2.7, True, "5", None],
    ids=["nan", "decimal", "bool", "texto", "none"],
)
def test_stock_que_no_es_entero_lanza_type_error(stock_invalido):
    invalido = producto("A1", "Arroz", stock=stock_invalido)

    with pytest.raises(TypeError, match="A1"):
        productos_por_pedir([invalido])


def test_stock_minimo_que_no_es_entero_lanza_type_error():
    invalido = producto("B2", "Aceite", stock=1, minimo=10.5)

    with pytest.raises(TypeError, match="B2"):
        productos_por_pedir([invalido])
