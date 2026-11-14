# Inventario Tienda

## 1. Qué es

Sistema pequeño de control de inventario para una tienda de barrio, proyecto final del seminario.

Por ahora implementa una historia de usuario:

**HU-03 (prioridad Must): ver los productos por pedir.** Como encargado de la tienda, quiero ver la lista de productos cuyo stock llegó al mínimo, ordenada por urgencia, para saber qué debo pedirle hoy al proveedor.

La función `productos_por_pedir` recibe una lista de productos y devuelve los que tienen `stock <= stock_minimo`, primero los que más faltan. El contrato completo está en el [anexo](#anexo-contrato-de-hu-03).

> Esta historia se redactó con ayuda de un asistente de IA porque la historia de la semana 3 no se alcanzó a completar. Se declara aquí para que sea transparente.

## 2. Requisitos

- Python 3.10 o superior (lo exige la versión fijada de `pytest`).
- `git` para clonar el repositorio (o descomprimir el `.zip` de la entrega).
- Conexión a internet solo para instalar las herramientas de `requirements.txt`.

El código del proyecto usa únicamente la librería estándar de Python. Las dependencias de `requirements.txt` son herramientas de desarrollo: `pytest` (pruebas), `ruff` (linter) y `pip-audit` (auditoría de dependencias).

## 3. Instalación

Entra a la carpeta `inventario-tienda` del proyecto y crea un entorno virtual:

```bash
python -m venv .venv
```

Actívalo:

```bash
# Linux o macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (cmd)
.venv\Scripts\activate.bat
```

Instala las herramientas:

```bash
pip install -r requirements.txt
```

El proyecto no usa claves ni variables de entorno. Existe un `.env.example` como plantilla para cuando se agregue alguna; `.env` está en `.gitignore` y no debe subirse al repositorio.

## 4. Ejecución

El proyecto es una librería sin interfaz todavía. Para verla funcionar, `ejemplo.py` ejecuta `productos_por_pedir` con cuatro productos. Hay que indicar dónde está el paquete (`src`) antes de ejecutarlo:

```bash
# Linux o macOS
PYTHONPATH=src python ejemplo.py

# Windows (PowerShell)
$env:PYTHONPATH="src"; python ejemplo.py

# Windows (cmd)
set PYTHONPATH=src && python ejemplo.py
```

Salida esperada:

```
Productos por pedir (del más urgente al menos):
- B2 Aceite 1 L: stock 1/20, faltan 19
- C3 Azúcar 1 kg: stock 5/10, faltan 5
- A1 Arroz 500 g: stock 8/10, faltan 2
```

Para usar la función en otro código:

```python
from inventario.reposicion import Producto, productos_por_pedir

lista = productos_por_pedir([Producto("A1", "Arroz 500 g", stock=2, stock_minimo=10)])
```

## 5. Pruebas

```bash
pytest
```

Hay 18 pruebas: 10 de la semana 5 y 8 de la revisión de la semana 6 (`tests/test_revision_semana6.py`). Otras comprobaciones de calidad y seguridad:

```bash
ruff check .                    # linter con reglas E, F, B y S (seguridad); configurado en pyproject.toml
pip-audit -r requirements.txt   # vulnerabilidades conocidas en las dependencias
```

El informe de la revisión está en [revision_seguridad.md](revision_seguridad.md).

## 6. Estructura

```
src/inventario/reposicion.py       # implementación (Producto, productos_por_pedir)
tests/test_reposicion.py           # pruebas de la semana 5
tests/test_revision_semana6.py     # pruebas nuevas de la revisión de la semana 6
ejemplo.py                         # ejemplo ejecutable
pyproject.toml                     # configuración de ruff
pytest.ini                         # configuración de pytest
requirements.txt                   # herramientas de desarrollo con versión fijada
.env.example                       # plantilla de variables de entorno (hoy vacía)
revision_seguridad.md              # informe de revisión de código y seguridad
bitacora_ia.md                     # bitácora de uso de IA
```

## 7. Uso de IA

Se usó Claude (chat) como asistente en dos etapas:

- **Semana 5:** propuso la historia de usuario, las 10 pruebas, la primera implementación y el refactor. Cada propuesta se revisó, se ejecutó y se decidió si aceptarla, cambiarla o rechazarla.
- **Semana 6:** hizo una segunda revisión del código, ayudó a corregir los hallazgos y a redactar los docstrings y este README. Cada hallazgo se verificó ejecutando el código antes de incluirlo en el informe, y los docstrings se compararon con lo que hace el código.

El detalle de cada decisión, con su verificación y su commit, está en [bitacora_ia.md](bitacora_ia.md).

## 8. Autor y licencia

Autor: Juan Camilo Trujillo Garrido.

Proyecto académico del seminario. No se ha definido una licencia de código abierto.

## Anexo: contrato de HU-03

**Criterios de aceptación**

- *Escenario normal:* dado un conjunto de productos, cuando consulto los productos por pedir, entonces veo solo los que tienen `stock <= stock_minimo`, con el que más le falta primero.
- *Escenario de error:* dado un producto con stock o stock mínimo inválido, cuando consulto los productos por pedir, entonces el sistema rechaza la operación con un error que indica el código del producto.

```python
def productos_por_pedir(productos: list[Producto]) -> list[Producto]
```

```python
@dataclass(frozen=True)
class Producto:
    codigo: str        # identificador único, por ejemplo "A1"
    nombre: str        # nombre legible, por ejemplo "Arroz 500 g"
    stock: int         # unidades disponibles (entero >= 0)
    stock_minimo: int  # umbral de reposición (entero >= 0)
```

**Qué recibe:** una lista de `Producto` (puede estar vacía).

**Qué devuelve:** una lista nueva con los productos donde `stock <= stock_minimo`, ordenada así:
1. Mayor faltante primero (`faltante = stock_minimo - stock`).
2. Si el faltante es igual, por `nombre` en orden alfabético, sin distinguir mayúsculas ni tildes.

**Errores** (el mensaje siempre incluye el `codigo` del producto):
- `ValueError` si `stock < 0` o `stock_minimo < 0`.
- `TypeError` si `stock` o `stock_minimo` no es un entero (decimales, `NaN`, texto, `None` y `bool` se rechazan).

Todos los productos se validan antes de filtrar, así que un dato inválido nunca se ignora en silencio.

**Supuestos**
- Los códigos de producto no se repiten (la unicidad se valida en la capa de registro, no aquí).
- La función no modifica la lista que recibe.
- La `ñ` se ordena como `n` (ver pendientes en `revision_seguridad.md`).

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
| `A1: 2.7/10` | `TypeError` que menciona `A1` |
