import pytest

from inventario.reposicion import Producto, productos_por_pedir


def producto(codigo, stock, minimo, nombre=None):
    return Producto(
        codigo=codigo,
        nombre=nombre or f"Producto {codigo}",
        stock=stock,
        stock_minimo=minimo,
    )


# --- Casos normales ---

def test_incluye_solo_productos_con_stock_bajo_el_minimo():
    bajo = producto("A1", stock=2, minimo=10)
    suficiente = producto("B2", stock=50, minimo=10)

    resultado = productos_por_pedir([bajo, suficiente])

    assert resultado == [bajo]


def test_ordena_por_mayor_faltante_primero():
    poco_faltante = producto("A1", stock=8, minimo=10)    # falta 2
    mucho_faltante = producto("B2", stock=1, minimo=20)   # falta 19
    medio_faltante = producto("C3", stock=5, minimo=10)   # falta 5

    resultado = productos_por_pedir([poco_faltante, mucho_faltante, medio_faltante])

    assert resultado == [mucho_faltante, medio_faltante, poco_faltante]


def test_con_igual_faltante_ordena_por_nombre():
    zeta = producto("A1", stock=0, minimo=5, nombre="Zeta")
    alfa = producto("B2", stock=0, minimo=5, nombre="Alfa")

    resultado = productos_por_pedir([zeta, alfa])

    assert resultado == [alfa, zeta]


# --- Casos límite ---

def test_stock_igual_al_minimo_se_considera_por_pedir():
    en_el_umbral = producto("A1", stock=10, minimo=10)

    assert productos_por_pedir([en_el_umbral]) == [en_el_umbral]


def test_lista_vacia_devuelve_lista_vacia():
    assert productos_por_pedir([]) == []


def test_producto_agotado_con_stock_cero_se_incluye():
    agotado = producto("A1", stock=0, minimo=3)

    assert productos_por_pedir([agotado]) == [agotado]


def test_si_todos_tienen_stock_suficiente_devuelve_lista_vacia():
    productos = [
        producto("A1", stock=11, minimo=10),
        producto("B2", stock=100, minimo=5),
    ]

    assert productos_por_pedir(productos) == []


def test_no_modifica_la_lista_de_entrada():
    original = [producto("A1", stock=1, minimo=10), producto("B2", stock=50, minimo=10)]
    copia = list(original)

    productos_por_pedir(original)

    assert original == copia


# --- Casos de error ---

def test_stock_negativo_lanza_value_error():
    invalido = producto("A1", stock=-1, minimo=10)

    with pytest.raises(ValueError, match="A1"):
        productos_por_pedir([invalido])


def test_stock_minimo_negativo_lanza_value_error():
    invalido = producto("B2", stock=5, minimo=-3)

    with pytest.raises(ValueError, match="B2"):
        productos_por_pedir([invalido])
