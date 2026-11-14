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
