# Bitácora de uso de IA

Proyecto: Inventario Tienda
Estudiante: Juan Camilo Trujillo Garrido
Funcionalidad: HU-03 Ver los productos por pedir
Asistente usado: Claude (chat). El código inicial, las pruebas y el refactor fueron generados por el asistente a partir de mis indicaciones; yo los revisé, los ejecuté y decidí qué conservar.

## Entradas

### Entrada 1

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** "No alcancé a hacer la historia de usuario de la semana 3, créala tú y genérame todo." El asistente propuso HU-03: ver los productos cuyo stock llegó al mínimo, ordenados por urgencia.
- **Decisión:** Aceptada
- **Por qué:** Es pequeña (una función principal), tiene prioridad Must en un inventario y trae de forma natural casos límite (stock igual al umbral, lista vacía, agotado) y un escenario de error (cantidades negativas), como pide la tarea. Lo declaré en el README porque la historia no viene de mi documento de la semana 3.
- **Verificación:** Contrasté la historia con los requisitos del enunciado (una función, casos límite, un error en el criterio de aceptación).
- **Commit relacionado:** b0506f8 Pruebas de productos por pedir (en rojo)

### Entrada 2

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** El asistente propuso 10 pruebas antes del código: 3 normales (filtrar, ordenar por faltante, desempate por nombre), 5 de límite (stock igual al mínimo, lista vacía, agotado, todos suficientes, no modificar la lista de entrada) y 2 de error (stock negativo y mínimo negativo).
- **Decisión:** Aceptada
- **Por qué:** Cubren el mínimo exigido (2 normales, 2 límite, 1 error) y además fijan decisiones del contrato que no son obvias: el orden y que `stock == stock_minimo` sí se pide.
- **Verificación:** Ejecuté `pytest` con un stub que lanza `NotImplementedError`: fallaron las 10, que es lo esperado para el commit en rojo.
- **Commit relacionado:** b0506f8 Pruebas de productos por pedir (en rojo)

### Entrada 3

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Primera implementación de `productos_por_pedir`: un bucle con las validaciones dentro, `append` a una lista y un `sort` con una lambda que repetía la resta `stock_minimo - stock`.
- **Decisión:** Aceptada con cambios
- **Por qué:** Cumplía el contrato y pasó todo, pero la regla `stock <= stock_minimo` y el cálculo del faltante estaban sin nombre y mezclados con la validación. En la fase de refactor los separé en `Producto.faltante`, `Producto.requiere_pedido`, `_validar` y `_orden_de_urgencia`.
- **Verificación:** `pytest` dio 10 de 10 antes y después del refactor, sin tocar ningún archivo de `tests/` (`git diff` de `tests/` vacío entre commits).
- **Commit relacionado:** 47b8831 Implementa productos_por_pedir (pruebas en verde) y 7ee27b3 Refactor

### Entrada 4

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Se consideró validar también dentro de la función que no haya dos productos con el mismo `codigo`.
- **Decisión:** Rechazada
- **Por qué:** No está en el criterio de aceptación de HU-03 y mezcla dos responsabilidades (reponer y registrar productos). Quedó escrito como supuesto en el contrato: la unicidad se valida al registrar.
- **Verificación:** Revisé que el criterio de aceptación y el contrato del README no la exigen; las 10 pruebas cubren lo que sí se promete.
- **Commit relacionado:** b0506f8 (el supuesto está en el README)

### Entrada 5

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Comprobar que las pruebas detectan errores reales cambiando el código a propósito (prueba de mutación manual): `<=` por `<`, orden invertido, quitar la validación del mínimo y quitar el desempate por nombre.
- **Decisión:** Aceptada
- **Por qué:** Que todo pase en verde no demuestra que las pruebas sirvan; necesitaba ver que fallan cuando la regla se rompe.
- **Verificación:** Cada cambio hizo fallar exactamente una prueba distinta (umbral, orden, error de mínimo negativo, desempate). Al restaurar el archivo volvieron las 10 en verde y `git status` quedó limpio. La primera vez una mutación dio un resultado raro por el caché de bytecode (`__pycache__`); lo repetí limpiándolo.
- **Commit relacionado:** ninguno (se probó y se descartó; el código entregado no cambió)

### Entrada 6

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Se consideró convertir con `int(...)` los valores de stock que lleguen como texto o decimales para ser más "tolerante".
- **Decisión:** Rechazada
- **Por qué:** El contrato dice que `stock` y `stock_minimo` son enteros. Convertir en silencio podría ocultar datos mal capturados (por ejemplo `2.7` truncado a `2`) y habría que definir más reglas que la historia no pide.
- **Verificación:** Revisé el contrato; la dataclass `Producto` declara `int` y las pruebas de error cubren los negativos.
- **Commit relacionado:** 47b8831 Implementa productos_por_pedir (pruebas en verde)

### Entrada 7

- **Fecha:** 2026-11-14
- **Prompt o sugerencia:** Segunda revisión de `reposicion.py` y de los tests con tres criterios (corrección y pruebas, diseño y legibilidad, seguridad con los cinco puntos), tabla de hallazgos con línea y severidad, y separando problemas seguros de sospechas. El asistente devolvió 4 problemas seguros (orden por nombre, validación incompleta, falta de docstrings, validación duplicada) y 4 sospechas (`<=` contra `<`, `sorted` que modifica la entrada, `faltante` negativo, códigos repetidos).
- **Decisión:** Aceptada con cambios
- **Por qué:** Acepté los 4 problemas seguros porque cada uno se podía reproducir. Descarté las 4 sospechas como falsos positivos después de comprobarlas (ver verificación). No copié la tabla tal cual: cada fila se clasificó en `revision_seguridad.md`, sección 3.
- **Verificación:** Ejecuté la función con entradas que reproducen cada hallazgo. El orden devolvió `Azúcar, Zeta, alfa, arroz, Árbol` y un stock `NaN` desapareció de la lista sin error: ambos reales. Las sospechas no se confirmaron: `<=` es lo que pide el contrato y lo cubre una prueba, `sorted` no modifica la entrada (`original == copia` dio `True`), `faltante` solo se calcula sobre productos con `stock <= stock_minimo`, y los códigos repetidos son un supuesto documentado en la entrada 4. Además, `ruff` y la lista de revisión encontraron cosas que la IA no señaló (líneas largas, `pytest>=8.0` sin versión fijada, falta de `.env.example`).
- **Commit relacionado:** ninguno por sí sola; los hallazgos reales quedaron en H-01 a H-07 de `revision_seguridad.md`.

### Entrada 8

- **Fecha:** 2026-11-14
- **Prompt o sugerencia:** Corregir H-01: el desempate por nombre debía ser alfabético de verdad. El asistente propuso una clave de orden `_clave_nombre` que pasa el nombre a minúsculas con `casefold()` y le quita las tildes con `unicodedata`.
- **Decisión:** Aceptada con cambios
- **Por qué:** Cambié la idea de usar solo `casefold()`: la tienda tiene nombres en español como `Árbol` y `Azúcar`, y sin quitar las tildes seguirían quedando al final. Dejé la `ñ` fuera a propósito (se ordena como `n`) y la anoté como pendiente, porque el orden correcto depende de la configuración regional.
- **Verificación:** Escribí primero 2 pruebas nuevas y las vi fallar en rojo. Tras el cambio, las 12 pasan (10 anteriores + 2 nuevas). No toqué la lógica de ninguna prueba de la semana 5.
- **Commit relacionado:** 4ab1ab3 Fix H-01

### Entrada 9

- **Fecha:** 2026-11-14
- **Prompt o sugerencia:** Corregir H-02: rechazar `stock` y `stock_minimo` que no sean enteros. El asistente propuso lanzar `TypeError` con el código del producto para decimales, `NaN`, `bool`, texto y `None`.
- **Decisión:** Aceptada
- **Por qué:** Un stock `NaN` hacía desaparecer un producto de la lista de pedidos sin ningún aviso, y eso es peor que un error visible. Es coherente con la entrada 6: no convertir en silencio los datos mal capturados, sino rechazarlos. Usé `TypeError` y no `ValueError` porque el problema es el tipo, no el valor. Excluí `bool` porque en Python `True` es un entero.
- **Verificación:** 6 pruebas nuevas (5 valores inválidos de `stock` y 1 de `stock_minimo`), en rojo antes del arreglo y en verde después: 18 de 18. El README y el docstring de `productos_por_pedir` ya mencionan el `TypeError`, y los mensajes incluyen el código del producto.
- **Commit relacionado:** 4847cf9 Fix H-02

### Entrada 10

- **Fecha:** 2026-11-14
- **Prompt o sugerencia:** Refactor de la validación duplicada (H-07) y borradores de los docstrings de `Producto`, `requiere_pedido` y `productos_por_pedir` (H-06).
- **Decisión:** Aceptada
- **Por qué:** `_validar` repetía el mismo bloque para `stock` y para `stock_minimo`; una sola función auxiliar deja la regla en un lugar. Los docstrings eran lo que pedía la tarea: qué hace, qué recibe, qué devuelve y qué errores lanza.
- **Verificación:** Hice el refactor en un commit aparte con las 12 pruebas en verde antes y después. Comparé cada frase del docstring con el código: el orden lo fija `_orden_de_urgencia`, el no modificar la entrada lo cubre `test_no_modifica_la_lista_de_entrada`, y los dos errores con el código del producto los cubren las pruebas de error. En los tests, las 2 líneas largas se reformatearon sin cambiar la lógica: el árbol sintáctico (`ast`) del archivo es idéntico antes y después.
- **Commit relacionado:** 4dee476 Refactor R-01, 8ac0da6 Docs y de8df82 Style

### Entrada 11

- **Fecha:** 2026-11-14
- **Prompt o sugerencia:** Las correcciones, el README y el informe se hicieron con el asistente ejecutando comandos (pruebas, ruff, pip-audit, git) sobre una copia del repositorio, en la rama `revision-semana-6` y no en `main`.
- **Decisión:** Aceptada
- **Por qué:** La tarea pide que el trabajo delegado a un agente vaya en una rama propia, con instrucciones delimitadas y con el diff revisado antes de integrar. Los commits son pequeños (uno por hallazgo) para poder revisarlos de a uno.
- **Verificación:** Revisé el diff con `git diff main..revision-semana-6` antes de integrarlo con `git merge revision-semana-6` (avance rápido, sin conflictos). se agregaron componentes nuevo al proyecto y no se registra ninguna novedad, 18p passed, Después de integrar, volví a ejecutar `pytest`, `ruff check .` y `pip-audit -r requirements.txt` y probé el README en una carpeta limpia.
- **Commit relacionado:** rama `revision-semana-6` (de 4387ff1 a 601f5b8 y los commits de informe y bitácora)

### Entrada 12

- **Fecha:** 2026-11-14
- **Prompt o sugerencia:** Resolver el orden de la `ñ` con `locale.strxfrm` o con la librería `babel`, para que `Ñame` quede después de `Nuez`.
- **Decisión:** Rechazada
- **Por qué:** Con `locale` el resultado depende de la configuración regional de cada equipo y las pruebas dejarían de ser reproducibles; `babel` sería una dependencia nueva para un desempate de bajo impacto. Lo dejé como pendiente con un plan.
- **Verificación:** Comprobé que hoy la `ñ` se ordena como `n` (`Ñame` antes que `Nuez`) y que solo afecta el desempate entre productos con el mismo faltante. Quedó documentado en el README (supuestos) y en `revision_seguridad.md`, sección 4.
- **Commit relacionado:** Vi que los tests de la semana 5 solo cambiaron en el formato de dos líneas largas y que la lógica nueva está en reposicion.py y en tests/test_revision_semana6.py.

## Resumen

| Decisión | Cantidad |
|---|---|
| Aceptadas | 6 |
| Aceptadas con cambios | 3 |
| Rechazadas | 3 |

## Errores que atraparon las pruebas

El código generado pasó las 10 pruebas en la primera ejecución, así que las pruebas no detectaron un error real en la implementación inicial. Para saber si de todas formas protegían el comportamiento, rompí el código a propósito de cuatro formas; cada cambio lo atrapó una prueba distinta. Por ejemplo, cambiar `<=` por `<` hizo fallar `test_stock_igual_al_minimo_se_considera_por_pedir`, y quitar la validación del mínimo hizo fallar `test_stock_minimo_negativo_lanza_value_error`. Al restaurar el código volvió todo a verde.

### Semana 6

Las pruebas de la semana 5 no detectaron dos errores reales del código, porque no probaban esos casos: el orden por nombre con mayúsculas y tildes (H-01) y los datos que no son enteros, como `NaN` (H-02). Los encontró la revisión: escribí pruebas nuevas, las vi fallar en rojo y luego las puse en verde con el arreglo. Las 10 pruebas originales no cambiaron de lógica.

## Reflexión final (5 a 8 líneas)

El asistente me ayudó más al proponer casos límite que yo no habría escrito primero, como el stock igual al mínimo, la lista vacía y no modificar la lista de entrada. Escribir las pruebas antes me obligó a decidir el orden y el umbral desde el contrato, no al revés. Mis pruebas no atraparon un error real porque el código pasó a la primera, pero la prueba de mutación mostró que sí detectan reglas rotas. Aprendí que "todo en verde" no basta y que un caché de bytecode puede dar resultados engañosos. Para la próxima funcionalidad haría yo mismo los primeros casos de prueba antes de pedirle ideas al asistente y pediría la implementación en pasos pequeños, para entender cada línea antes de aceptarla.
