# Informe de revisión de código y seguridad

Proyecto: FarmaStock (módulo de inventario: HU-02, HU-04 y HU-R1)
Estudiante: Juan Camilo Trujillo Garrido
Fecha: 2026-11-14 (ronda 1) y 2026-11-27 (ronda 2)
Commits revisados: ronda 1, d93df8e, solo `reposicion.py` (HU-R1, que en la semana 5 se llamó HU-03); ronda 2, b570a5e, todo el código actual, incluidas HU-02 (semana 5) y HU-04, antes de las correcciones H-09 a H-12.

## 1. Herramientas y criterios

- **Linter:** ruff 0.17.5 con las reglas E, F, B, S. Configuración en `pyproject.toml`. Ronda 1: 11 avisos (3 E501 y 8 S101), final sin avisos. Ronda 2: sin avisos antes y después.
- **Auditoría de dependencias:** pip-audit 2.10.1 — resultado: sin vulnerabilidades, antes y después de fijar las versiones (ronda 1) y de nuevo el 2026-11-27 (ronda 2).
- **Lista de revisión:** la de la semana 6 (corrección y pruebas, diseño y legibilidad, seguridad).
- **Revisión con IA:** Claude (chat) con el prompt de revisión de la semana, en las dos rondas (ver sección 3). Limitación: el mismo asistente que ayudó a escribir el código lo revisó, así que puede compartir sus puntos ciegos.
- **Pruebas:** 83 en verde: 10 de la propuesta de reposición (sin modificar su lógica), 8 de la ronda 1, 27 de HU-04, 25 de HU-02 y 13 nuevas de la ronda 2.

### Puntos de seguridad revisados

| Punto | ¿Aplica? | Resultado |
|---|---|---|
| Inyección (consultas con parámetros) | No: el proyecto no tiene base de datos, consultas SQL, comandos del sistema ni `eval`/`exec`. Solo recibe objetos `Producto` y `Lote` en memoria. | Sin hallazgos (ruff con reglas S tampoco reporta nada) |
| Secretos (código, historial, .gitignore, .env.example) | Sí | Sin claves en el código ni en `git log -p --all` (búsqueda de password, secret, api_key, token, llaves privadas, repetida en la ronda 2: 4 coincidencias, todas la palabra «secretos» en el texto de este informe y de un mensaje de commit, ninguna clave). `.env` ya estaba en `.gitignore`. Faltaba `.env.example` → H-04 |
| Contraseñas (scrypt, bcrypt o argon2 con sal) | No: el proyecto no tiene usuarios, login ni guarda contraseñas. | Sin hallazgos |
| Control de acceso (rol verificado y prueba de abuso) | Todavía no se puede revisar: no hay usuarios ni capa de acceso en este módulo. HU-02 es una operación solo del Administrador, pero `registrar_ingreso` es una función en memoria que no conoce roles; el diseño de la semana 4 pone la comprobación de rol en la API (`POST /api/lotes` responde 403 a un cajero). Por eso no hay prueba de abuso todavía. | Sin hallazgo corregible ahora; **pendiente importante** (sección 4) |
| Dependencias (existen, necesarias, versión fijada, pip-audit) | Sí | `pytest`, `ruff` y `pip-audit` existen, se usan y tienen versión fijada (H-03). pip-audit sin vulnerabilidades. Las acciones de GitHub Actions están fijadas por etiqueta (`@v4`, `@v5`), no por commit: pendiente |

## 2. Tabla de hallazgos

Ronda 1 (H-01 a H-08): archivo y línea del commit d93df8e. Ronda 2 (H-09 a H-12): archivo y línea del commit b570a5e.

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
| H-09 | src/inventario/ingreso_lotes.py:37 (`_ya_esta_registrado`) y :74 (`stock_total`) | El producto se compara con `==`: `Ibuprofeno 400mg` e `ibuprofeno 400mg ` eran dos productos. Reproducido: el segundo ingreso con el mismo código `L-1` se aceptó (2 lotes) y `stock_total` dio 10 con un nombre y 0 con el otro. | Error de lógica / integridad de datos | Media | `_clave_producto` (sin mayúsculas ni espacios de más) en la unicidad y en el stock; el texto guardado no cambia; 5 pruebas nuevas | 69f2253 |
| H-10 | src/inventario/ingreso_lotes.py:33 y src/inventario/vencimientos.py:103 | `hoy` no se valida: con `None`, un `datetime` o un texto falla con `'<' not supported between instances of 'datetime.date' and 'NoneType'`, un mensaje que no dice qué dato está mal. | Validación de entrada (CWE-20) | Baja (falla con error, no en silencio) | `TypeError` «La fecha de hoy debe ser un date» en ambas funciones; 8 pruebas nuevas | fa3b87f |
| H-11 | src/inventario/reposicion.py:40; vencimientos.py:39, :46, :54; ingreso_lotes.py:18, :29 | La comprobación «entero pero no bool» estaba escrita 4 veces y «date pero no datetime» 3, en tres módulos (duplicación). | Mantenibilidad | Baja | `es_entero` y `es_fecha` en `inventario/validaciones.py`; pruebas sin cambios (83 de 83 antes y después, `tests/` sin diferencias) | 2aa5151 |
| H-12 | src/inventario/reposicion.py:1 | El docstring del módulo decía HU-03, que en el documento de requisitos es la venta fiada (la reposición es HU-R1). | Documentación | Baja | Docstring con HU-R1 y la nota del nombre antiguo | 5f2da72 |

**Severidad:** alta (permite acceder o cambiar datos sin permiso, o expone secretos), media (error probable o riesgo con condiciones), baja (estilo o mantenibilidad). No hay hallazgos de severidad alta.

### Avisos del linter no corregidos

| Regla | Archivo y línea | Por qué se mantiene |
|---|---|---|
| S101 (8 avisos) | tests/test_reposicion.py:18, 28, 37, 45, 49, 55, 61, 70 | `assert` es la forma normal de comprobar en pytest. Solo se ignora para `tests/**` en `pyproject.toml`; en `src` la regla sigue activa. |

## 3. Revisión con IA

### Ronda 2 (2026-11-27, todo el código de FarmaStock)

**Prompt usado:** el de la semana: revisar `ingreso_lotes.py`, `vencimientos.py`, `reposicion.py` y sus pruebas con tres criterios (corrección y pruebas, diseño y legibilidad, seguridad con los cinco puntos), una tabla con archivo, línea y severidad, y la separación de problemas seguros y sospechas. Entrada 23 de `bitacora_ia.md`.

| Hallazgo de la IA | ¿Real o falso positivo? | Cómo lo verifiqué |
|---|---|---|
| Seguro: el mismo producto con otra capitalización o espacios cuenta como otro producto (`ingreso_lotes.py` líneas 37 y 74) | Real → H-09 | Ejecuté dos ingresos del lote `L-1` con `Ibuprofeno 400mg` e `ibuprofeno 400mg `: se aceptaron los dos y el stock dio 10 y 0 según el nombre |
| Seguro: `hoy` no se valida y el error no dice qué dato falla (`ingreso_lotes.py:33`, `vencimientos.py:103`) | Real → H-10 | Ejecuté ambas funciones con `None`, un `datetime` y un texto: `TypeError` con mensaje de operadores, sin mencionar `hoy` |
| Seguro: validación de tipos duplicada entre los tres módulos | Real → H-11 | Busqué `isinstance` en `src/`: 4 veces «entero no bool» y 3 «date no datetime» |
| Sospecha: `vence < hoy` debería ser `<=` | Falso positivo | El contrato y P-07 dicen que un lote que vence hoy se acepta; lo cubre `test_un_lote_que_vence_hoy_se_acepta` |
| Sospecha: `registrar_ingreso` modifica la lista recibida | Falso positivo | Usa `sorted([*lotes, nuevo])`, que crea una lista nueva; lo cubre `test_no_modifica_la_lista_original` |
| Sospecha: `_orden_de_vencimiento` está duplicado en `ingreso_lotes.py` y `vencimientos.py` | Falso positivo | Reciben tipos distintos (`Lote` y `LoteProximo`) y cada uno pertenece a su módulo; unirlos obligaría a que un módulo dependa del otro por una línea |
| Sospecha: `unidades` no tiene tope superior (`10**18` se acepta) | Confirmada, pero sin regla en los requisitos | Lo ejecuté y se acepta; el documento no define un máximo, así que no lo decidí en el código: pendiente P-09 |
| Sospecha: `lotes` podría traer elementos que no son `Lote` | Falso positivo (decisión) | Es una función interna con tipos declarados; los datos se validarán en el borde (la API de la semana 4). Con `[1]` falla con `AttributeError`, no en silencio |

**Lo que la IA no encontró:** (1) que HU-02 es una operación solo del Administrador y que nada en el código lo comprueba: no es un fallo hoy, pero es el punto de control de acceso más importante del proyecto y debe tener prueba de abuso en la API; (2) las acciones de GitHub Actions fijadas por etiqueta y no por commit; (3) el identificador viejo HU-03 en el docstring de `reposicion.py` (H-12), que encontré al buscar texto con `grep`; (4) que el informe seguía diciendo «Inventario Tienda» aunque el proyecto es FarmaStock.

### Ronda 1 (2026-11-14, `reposicion.py`)

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

**Lo que la IA no encontró:** la revisión de la IA se centró en `reposicion.py` y no señaló los problemas que encontré con otras herramientas: las líneas largas (H-05, con ruff), `pytest>=8.0` sin versión fijada (H-03, con la lista de revisión), la ausencia de `.env.example` (H-04, con la lista de revisión) y el nombre sin commit y el marcador `[nombre y apellido]` en el README (H-08, con `git status` y al leer el README). Todos son de baja severidad: la IA se fijó en la lógica del código y no en el entorno del repositorio.

## 4. Pendientes

| Pendiente | Por qué no se corrigió todavía | Plan |
|---|---|---|
| La `ñ` se ordena como `n` (por ejemplo `Ñame` antes que `Nuez`) | El orden correcto en español depende de la configuración regional; con `locale` el resultado cambia según el equipo y se rompería la reproducibilidad de las pruebas. El impacto es bajo (solo afecta el desempate). | Cuando se defina el idioma de despliegue, usar una comparación regional (`locale.strxfrm` o `babel`) y agregar su prueba |
| **Control de acceso de HU-02** (solo el Administrador ingresa lotes) | El módulo no tiene usuarios ni roles; la comprobación pertenece a la API. | Cuando exista `POST /api/lotes`, verificar el rol y agregar una prueba de abuso: un cajero recibe 403 y el lote no se crea. Lo mismo para el cierre de caja (HU-07) |
| Acciones de GitHub Actions fijadas por etiqueta (`checkout@v4`, `setup-python@v5`) | Fijarlas por commit exige consultar los hashes en GitHub, que desde este entorno no están disponibles; riesgo bajo porque el flujo solo tiene permiso de lectura. | Fijarlas por SHA con comentario de la versión y dejar que Dependabot las actualice |
| P-09: `unidades` sin tope máximo | El documento de requisitos no define un máximo por lote. | Preguntar al cliente cuál es un ingreso razonable y rechazar los mayores con prueba |
| Unicidad del `codigo` de producto | No pertenece a HU-03 (decisión de la semana 5, entrada 4). | Validarla en la capa de registro del siguiente incremento, con una prueba de códigos duplicados |
| Inyección y contraseñas no se pudieron revisar | Hoy no aplican: no hay base de datos ni usuarios. | Al agregar registro, usuarios o roles: consultas con parámetros, contraseñas con scrypt, bcrypt o argon2, y una prueba de abuso por cada operación restringida |

**Claves expuestas:** Ninguna.

**Nota sobre el estado del pipeline:** el flujo de GitHub Actions (`.github/workflows/ci.yml`) se probó solo en local; su primera ejecución real aparece en la pestaña Actions al subir el repositorio.
