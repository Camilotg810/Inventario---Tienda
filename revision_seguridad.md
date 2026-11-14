# Informe de revisión de código y seguridad

Proyecto: Inventario Tienda (HU-03 Ver los productos por pedir)
Estudiante: Juan Camilo Trujillo Garrido
Fecha: 2026-11-14
Commit revisado: d93df8e (antes de las correcciones)

## 1. Herramientas y criterios

- **Linter:** ruff 0.17.5 con las reglas E, F, B, S. Configuración en `pyproject.toml`. Resultado inicial: 11 avisos (3 E501 y 8 S101). Resultado final: sin avisos.
- **Auditoría de dependencias:** pip-audit 2.10.1 — resultado: sin vulnerabilidades, antes y después de fijar las versiones.
- **Lista de revisión:** la de la semana 6 (corrección y pruebas, diseño y legibilidad, seguridad).
- **Revisión con IA:** Claude (chat) con el prompt de revisión de la semana (ver sección 3).
- **Pruebas:** 10 de la semana 5 (sin modificar su lógica) + 8 nuevas = 18 en verde.

### Puntos de seguridad revisados

| Punto | ¿Aplica? | Resultado |
|---|---|---|
| Inyección (consultas con parámetros) | No: el proyecto no tiene base de datos, consultas SQL, comandos del sistema ni `eval`/`exec`. Solo recibe objetos `Producto` en memoria. | Sin hallazgos (ruff con reglas S tampoco reporta nada) |
| Secretos (código, historial, .gitignore, .env.example) | Sí | Sin claves en el código ni en `git log -p --all` (búsqueda de password, secret, api_key, token, llaves privadas: 0 coincidencias). `.env` ya estaba en `.gitignore`. Faltaba `.env.example` → H-04 |
| Contraseñas (scrypt, bcrypt o argon2 con sal) | No: el proyecto no tiene usuarios, login ni guarda contraseñas. | Sin hallazgos |
| Control de acceso (rol verificado y prueba de abuso) | No: no hay roles ni operaciones restringidas; `productos_por_pedir` es una función de solo lectura. Por eso no hay prueba de abuso. La entrada inválida sí se prueba (H-02). | Sin hallazgos. Pendiente para cuando exista registro de productos (ver sección 4) |
| Dependencias (existen, necesarias, versión fijada, pip-audit) | Sí | `pytest` existe y es necesaria; no tenía versión fijada → H-03. pip-audit sin vulnerabilidades |

## 2. Tabla de hallazgos

Archivo y línea se refieren al commit revisado (d93df8e).

| Id | Archivo y línea | Problema | Categoría (OWASP o tipo) | Severidad | Corrección | Commit |
|---|---|---|---|---|---|---|
| H-01 | src/inventario/reposicion.py:38 | El desempate por nombre compara texto tal cual: las mayúsculas van antes que las minúsculas y las tildes al final. Con `Zeta, alfa, Árbol, Azúcar, arroz` devuelve `Azúcar, Zeta, alfa, arroz, Árbol`. | Error de lógica | Media | Clave de orden sin mayúsculas ni tildes (`_clave_nombre`) y 2 pruebas nuevas | 4ab1ab3 |
| H-02 | src/inventario/reposicion.py:23-33 (`_validar`) | Solo se rechazan negativos. `stock=NaN` se acepta y el producto desaparece de la lista sin error; `2.7` y `True` también pasan; texto y `None` fallan con un `TypeError` sin código del producto. | Validación de entrada (CWE-20) | Media | `_exigir_entero_no_negativo`: `TypeError` con el código del producto si no es entero (bool incluido) y 6 pruebas nuevas | 4847cf9 |
| H-03 | requirements.txt:1 | `pytest>=8.0` sin versión fijada: instalaciones distintas según el día, sin reproducibilidad. | A06 Componentes vulnerables o desactualizados | Baja (solo herramienta de pruebas) | `pytest==9.2.0`, `ruff==0.17.5`, `pip-audit==2.10.1`; pip-audit sin hallazgos | df65802 |
| H-04 | raíz del repositorio / .gitignore | No existía `.env.example` y `.gitignore` solo cubría `.env`, no `.env.*`. | Gestión de secretos (buena práctica) | Baja | `.env.example` (hoy sin variables) y `.gitignore` con `.env.*` y `!.env.example` | d1f375c |
| H-05 | src/inventario/reposicion.py:27; tests/test_reposicion.py:7 y :59 | Líneas de más de 88 caracteres (E501). | Estilo | Baja | En `src`, al refactorizar (R-01). En tests, solo formato: el AST del archivo es idéntico antes y después | 4dee476 y de8df82 |
| H-06 | src/inventario/reposicion.py:7, :19, :41 | Sin docstring `Producto`, `requiere_pedido` ni `productos_por_pedir` (la función principal). | Mantenibilidad | Baja | Docstrings con qué hace, qué recibe, qué devuelve y qué errores lanza | 8ac0da6 |
| H-07 | src/inventario/reposicion.py:25-33 | Dos bloques casi idénticos para validar `stock` y `stock_minimo` (duplicación). | Mantenibilidad | Baja | Función auxiliar `_exigir_no_negativo`, luego ampliada en H-02. Pruebas sin cambios (12 de 12 antes y después) | 4dee476 |
| H-08 | README.md:4; bitacora_ia.md:4 | El README tenía `[nombre y apellido]` y el nombre en la bitácora estaba sin commit. | Documentación | Baja | Nombre en la bitácora commiteado; README reescrito con las ocho secciones | 48d2e3d y 601f5b8 |

**Severidad:** alta (permite acceder o cambiar datos sin permiso, o expone secretos), media (error probable o riesgo con condiciones), baja (estilo o mantenibilidad). No hay hallazgos de severidad alta.

### Avisos del linter no corregidos

| Regla | Archivo y línea | Por qué se mantiene |
|---|---|---|
| S101 (8 avisos) | tests/test_reposicion.py:18, 28, 37, 45, 49, 55, 61, 70 | `assert` es la forma normal de comprobar en pytest. Solo se ignora para `tests/**` en `pyproject.toml`; en `src` la regla sigue activa. |

## 3. Revisión con IA

**Prompt usado:** pedí a Claude revisar `reposicion.py` y los tests con tres criterios (corrección y pruebas, diseño y legibilidad, seguridad con los cinco puntos), una tabla de hallazgos con archivo, línea y severidad, y la indicación de separar problemas seguros de sospechas. Entrada 7 de `bitacora_ia.md`.

| Hallazgo de la IA | ¿Real o falso positivo? | Cómo lo verifiqué |
|---|---|---|
| Seguro: el orden por nombre distingue mayúsculas y tildes (línea 38) | Real → H-01 | Ejecuté la función con 5 nombres y salió un orden no alfabético; escribí la prueba, falló en rojo y pasó tras el arreglo |
| Seguro: `_validar` deja pasar NaN, decimales y `True` (líneas 23-33) | Real → H-02 | Ejecuté `Producto("X","n",float("nan"),5)`: devolvió lista vacía sin error. 6 pruebas rojas antes del arreglo |
| Seguro: faltan docstrings en la función principal | Real → H-06 | Revisé el archivo: `productos_por_pedir`, `Producto` y `requiere_pedido` no tenían |
| Seguro: validación duplicada en `_validar` | Real → H-07 | Lectura del código; refactor con las pruebas en verde antes y después |
| Sospecha: `<=` debería ser `<` en `requiere_pedido` | Falso positivo | El contrato dice que `stock == stock_minimo` sí se pide y lo cubre `test_stock_igual_al_minimo_se_considera_por_pedir`; la prueba de mutación de la semana 5 (entrada 5) ya lo comprobó |
| Sospecha: `sorted` modifica la lista de entrada | Falso positivo | `sorted` crea una lista nueva; ejecuté la función y `original == copia` dio `True`. Lo cubre `test_no_modifica_la_lista_de_entrada` |
| Sospecha: `faltante` puede ser negativo y romper el orden | Falso positivo | Solo se ordenan los productos ya filtrados por `requiere_pedido`, que cumplen `stock <= stock_minimo`, así que su faltante es 0 o mayor |
| Sospecha: no se validan códigos repetidos | Falso positivo (decisión documentada) | La unicidad es un supuesto del contrato y se valida al registrar (entrada 4 de la bitácora). Con códigos repetidos la función devuelve ambos productos, como se espera. Queda como pendiente para el registro |

**Lo que la IA no encontró:** la revisión de la IA se centró en `reposicion.py` y no señaló los problemas que encontré con otras herramientas: las líneas largas (H-05, con ruff), `pytest>=8.0` sin versión fijada (H-03, con la lista de revisión), la ausencia de `.env.example` (H-04, con la lista de revisión) y el nombre sin commit y el marcador `Juan Camilo Trujillo` en el README (H-08, con `git status` y al leer el README). Todos son de baja severidad: la IA se fijó en la lógica del código y no en el entorno del repositorio.

## 4. Pendientes

| Pendiente | Por qué no se corrigió todavía | Plan |
|---|---|---|
| La `ñ` se ordena como `n` (por ejemplo `Ñame` antes que `Nuez`) | El orden correcto en español depende de la configuración regional; con `locale` el resultado cambia según el equipo y se rompería la reproducibilidad de las pruebas. El impacto es bajo (solo afecta el desempate). | Cuando se defina el idioma de despliegue, usar una comparación regional (`locale.strxfrm` o `babel`) y agregar su prueba |
| Unicidad del `codigo` de producto | No pertenece a HU-03 (decisión de la semana 5, entrada 4). | Validarla en la capa de registro del siguiente incremento, con una prueba de códigos duplicados |
| Inyección, contraseñas y control de acceso no se pudieron revisar | Hoy no aplican: no hay base de datos, usuarios ni roles. | Al agregar registro, usuarios o roles: consultas con parámetros, contraseñas con scrypt, bcrypt o argon2, y una prueba de abuso por cada operación restringida |

**Claves expuestas:** Ninguna.
