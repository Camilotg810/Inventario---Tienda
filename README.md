# Inventario Tienda

Sistema pequeño de control de inventario para una tienda de barrio.
Proyecto final del seminario. Estudiante: [nombre y apellido]

## Funcionalidad de la semana 5

### Historia de usuario

**HU-03 (prioridad Must): Ver los productos por pedir.**
Como encargado de la tienda, quiero ver la lista de productos cuyo stock llegó al mínimo, ordenada por urgencia, para saber qué debo pedirle hoy al proveedor.

> Nota: esta historia se redactó con ayuda de un asistente de IA porque la historia de la semana 3 no se alcanzó a completar. Se declara aquí para que sea transparente.

**Criterio de aceptación**

- *Escenario normal:* dado un conjunto de productos, cuando consulto los productos por pedir, entonces veo solo los que tienen `stock <= stock_minimo`, con el que más le falta primero.
- *Escenario de error:* dado un producto con stock o stock mínimo negativo, cuando consulto los productos por pedir, entonces el sistema rechaza la operación con un error que indica el código del producto.

### Contrato de la función

```python
def productos_por_pedir(productos: list[Producto]) -> list[Producto]
```

```python
@dataclass(frozen=True)
class Producto:
    codigo: str        # identificador único, por ejemplo "A1"
    nombre: str        # nombre legible, por ejemplo "Arroz 500 g"
    stock: int         # unidades disponibles (>= 0)
    stock_minimo: int  # umbral de reposición (>= 0)
```

**Qué recibe:** una lista de `Producto` (puede estar vacía).

**Qué devuelve:** una lista nueva con los productos donde `stock <= stock_minimo`, ordenada así:
1. Mayor faltante primero (`faltante = stock_minimo - stock`).
2. Si el faltante es igual, por `nombre` en orden alfabético.

**Errores:** lanza `ValueError` si algún producto tiene `stock < 0` o `stock_minimo < 0`. El mensaje incluye el `codigo` del producto.

**Supuestos**
- Los códigos de producto no se repiten (la unicidad se valida en la capa de registro, no aquí).
- `stock` y `stock_minimo` son enteros.
- La función no modifica la lista que recibe.

**Casos límite**
- `stock == stock_minimo` **sí** se considera por pedir.
- Lista vacía devuelve lista vacía.
- Producto agotado (`stock == 0`) se incluye.
- Si todos tienen stock suficiente, devuelve lista vacía.

**Ejemplos**

| Entrada (código, stock, mínimo) | Salida (códigos en orden) |
|---|---|
| `A1: 2/10`, `B2: 50/10` | `[A1]` |
| `A1: 8/10`, `B2: 1/20`, `C3: 5/10` | `[B2, C3, A1]` (faltantes 19, 5, 2) |
| `A1: 10/10` | `[A1]` (en el umbral) |
| `[]` | `[]` |
| `A1: -1/10` | `ValueError` que menciona `A1` |

### Cómo ejecutar las pruebas

```bash
pip install -r requirements.txt
pytest
```

Solo se usa la librería estándar de Python para el código; `pytest` es únicamente para las pruebas.

### Estructura

```
src/inventario/reposicion.py   # implementación
tests/test_reposicion.py       # pruebas
bitacora_ia.md                 # bitácora de uso de IA
```
