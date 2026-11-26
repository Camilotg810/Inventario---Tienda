# FarmaStock

## 1. Qué es

FarmaStock es el proyecto final del seminario: un sistema de gestión de inventario y ventas para farmacias comunitarias pequeñas. Controla los medicamentos por lote y fecha de vencimiento, las ventas en efectivo y a crédito (fiado) y el cierre de caja. Sus requisitos están en el documento de requisitos de la semana 3, con 9 historias de usuario. Las necesidades de ese documento están **por validar con un cliente** (preguntas pendientes P-01 a P-04 del documento de la semana 3, y P-05 y P-06 en el Anexo A).

Este repositorio contiene el módulo de inventario, que es la parte implementada hasta ahora:

| Funcionalidad | Origen | Código |
|---|---|---|
| **HU-04** Reporte de lotes que vencen en los próximos 60 días | Documento de requisitos de la semana 3 (necesidad N-01) | `src/inventario/vencimientos.py` |
| **HU-R1** Reposición: productos por pedir | Propuesta con ayuda de IA en la semana 5; no está entre las 9 historias del documento | `src/inventario/reposicion.py` |

Las otras 8 historias (HU-01, HU-02, HU-03, HU-05, HU-06, HU-07, HU-08 y HU-09) **no están implementadas**.

> Nota sobre la numeración: en la semana 5 la reposición se llamó HU-03. Aquí se llama HU-R1 porque la HU-03 del documento de requisitos es la venta fiada. La bitácora y el informe de seguridad conservan el nombre original, porque así se escribieron.

## 2. Requisitos

- Python 3.10 o superior (lo exige la versión fijada de `pytest`).
- `git` para clonar el repositorio (o descomprimir el `.zip` de la entrega).
- Conexión a internet solo para instalar las herramientas de `requirements.txt`.

El código usa únicamente la librería estándar de Python. Las dependencias de `requirements.txt` son herramientas de desarrollo: `pytest` (pruebas), `ruff` (linter) y `pip-audit` (auditoría de dependencias).

## 3. Instalación

Entra a la carpeta del proyecto y crea un entorno virtual:

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

El proyecto es una librería sin interfaz todavía. `ejemplo.py` ejecuta las dos funciones con datos de ejemplo. Hay que indicar dónde está el paquete (`src`):

```bash
# Linux o macOS
PYTHONPATH=src python ejemplo.py

# Windows (PowerShell)
$env:PYTHONPATH="src"; python ejemplo.py

# Windows (cmd)
set PYTHONPATH=src && python ejemplo.py
```

Salida esperada (la fecha de hoy está fijada en el ejemplo, 24/10/2026, para que la salida no cambie):

```
Lotes que vencen en los próximos 60 días (el más pronto primero):
- Loratadina 10mg, lote L-087: 8 unidades, vence 30/10/2026 (faltan 6 días)
- Vitamina C, lote L-102: 10 unidades, vence 10/11/2026 (faltan 17 días)
- Ibuprofeno 400mg, lote L-210: 25 unidades, vence 05/12/2026 (faltan 42 días)

Productos por pedir (del más urgente al menos):
- B2 Aceite 1 L: stock 1/20, faltan 19
- C3 Azúcar 1 kg: stock 5/10, faltan 5
- A1 Arroz 500 g: stock 8/10, faltan 2
```

Para usar las funciones en otro código:

```python
from datetime import date
from inventario.vencimientos import Lote, lotes_por_vencer

filas = lotes_por_vencer([Lote("Vitamina C", "L-102", 10, date(2026, 11, 10))], date.today(), 60)
```

## 5. Pruebas y pipeline

```bash
pytest
```

Hay 45 pruebas: 10 de la semana 5, 8 de la revisión de la semana 6 y 27 de HU-04. Otras comprobaciones de calidad y seguridad:

```bash
ruff check .                    # linter con reglas E, F, B y S (seguridad); configurado en pyproject.toml
pip-audit -r requirements.txt   # vulnerabilidades conocidas en las dependencias
```

**Pipeline.** El archivo `.github/workflows/ci.yml` ejecuta esos tres pasos (ruff, pytest y pip-audit) en GitHub Actions con Python 3.12 y 3.14, en cada push y en cada pull request. La última ejecución se ve en la pestaña **Actions** del repositorio.

El informe de la revisión de código y seguridad está en [revision_seguridad.md](revision_seguridad.md).

## 6. Estructura

```
src/inventario/vencimientos.py     # HU-04: lotes por vencer
src/inventario/reposicion.py       # HU-R1: productos por pedir
tests/test_vencimientos.py         # pruebas de HU-04
tests/test_reposicion.py           # pruebas de la semana 5
tests/test_revision_semana6.py     # pruebas de la revisión de la semana 6
ejemplo.py                         # ejemplo ejecutable
.github/workflows/ci.yml           # pipeline de integración continua
pyproject.toml                     # configuración de ruff
pytest.ini                         # configuración de pytest
requirements.txt                   # herramientas de desarrollo con versión fijada
.env.example                       # plantilla de variables de entorno (hoy vacía)
revision_seguridad.md              # informe de revisión de código y seguridad
bitacora_ia.md                     # bitácora de uso de IA
```

## 7. Uso de IA

Se usó Claude como asistente en tres etapas:

- **Semana 5:** propuso la historia de reposición, las 10 pruebas, la primera implementación y el refactor.
- **Semana 6:** hizo una segunda revisión del código y ayudó con las correcciones, los docstrings y el informe de seguridad. Cada hallazgo se verificó ejecutando el código.
- **Etapa final:** escribió las pruebas y la implementación de HU-04 (pruebas primero), el pipeline y esta documentación, en la rama `final-farmastock`. Las pruebas se comprobaron con una prueba de mutación manual y los pasos del pipeline en una carpeta limpia.

Cada decisión, con su verificación y su commit, está en [bitacora_ia.md](bitacora_ia.md) (entradas 1 a 12 de las semanas 5 y 6, y 13 a 17 de la etapa final).

## 8. Autor y licencia

Autor: Juan Camilo Trujillo Garrido.

Proyecto académico del seminario. No se ha definido una licencia de código abierto.

## Anexo A. Contrato de HU-04 (lotes por vencer)

```python
def lotes_por_vencer(lotes: list[Lote], hoy: date, dias: int = 60) -> list[LoteProximo]
```

```python
@dataclass(frozen=True)
class Lote:
    producto: str      # por ejemplo "Vitamina C"
    codigo_lote: str   # por ejemplo "L-102"
    unidades: int      # entero >= 0
    vence: date        # un date, no un datetime
```

**Criterios de aceptación** (del documento de requisitos de la semana 3)

- *Escenario 1:* dado que hay lotes con vencimiento dentro de los próximos días (por ejemplo el lote L-102 de «Vitamina C», 10 unidades, vence el 10/11/2026), cuando se consulta el reporte a 60 días, entonces la lista sale ordenada por fecha de vencimiento y muestra producto, lote, unidades y días restantes.
- *Escenario 2 (error):* dado que el rango de días es `-15`, cuando se consulta, entonces se rechaza con el mensaje «El rango de días debe ser un número entero mayor a 0».

**Reglas**

- Entra un lote si le quedan entre 0 y `dias` días, ambos extremos incluidos. Los lotes ya vencidos no entran.
- Orden: por fecha de vencimiento y, a igual fecha, por código de lote.
- `dias` debe ser un entero mayor a 0; `bool`, decimales, texto y `None` se rechazan con `ValueError`.
- Si las `unidades` de un lote son negativas se lanza `ValueError`; si no son enteras, o `vence` no es un `date`, se lanza `TypeError`. Los mensajes incluyen el código del lote y se validan todos los lotes antes de filtrar.
- No modifica la lista que recibe. `hoy` se recibe como parámetro para poder probar con fechas fijas.

**Preguntas pendientes para el cliente** (se siguen de P-01 a P-04 del documento de la semana 3)

| Id | Pregunta | Qué hace el código hoy |
|---|---|---|
| P-05 | ¿El reporte debe mostrar también los lotes que ya vencieron? | No los muestra |
| P-06 | ¿Deben aparecer los lotes con 0 unidades? | Sí los muestra |

## Anexo B. Contrato de HU-R1 (productos por pedir)

```python
def productos_por_pedir(productos: list[Producto]) -> list[Producto]
```

- Devuelve los productos con `stock <= stock_minimo`, ordenados por mayor faltante (`stock_minimo - stock`) y, a igual faltante, por nombre alfabético sin distinguir mayúsculas ni tildes.
- Lanza `ValueError` si `stock` o `stock_minimo` son negativos y `TypeError` si no son enteros (`bool`, decimales, `NaN`, texto y `None` se rechazan). El mensaje incluye el código del producto.
- Los códigos de producto no se repiten (supuesto: se validaría al registrar productos). La `ñ` se ordena como `n` (pendiente en `revision_seguridad.md`).
- Casos límite: `stock == stock_minimo` sí se pide; lista vacía devuelve lista vacía; un producto agotado se incluye.
