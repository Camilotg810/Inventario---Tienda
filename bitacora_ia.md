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

## Resumen

| Decisión | Cantidad |
|---|---|
| Aceptadas | 3 |
| Aceptadas con cambios | 1 |
| Rechazadas | 2 |

## Errores que atraparon las pruebas

El código generado pasó las 10 pruebas en la primera ejecución, así que las pruebas no detectaron un error real en la implementación inicial. Para saber si de todas formas protegían el comportamiento, rompí el código a propósito de cuatro formas; cada cambio lo atrapó una prueba distinta. Por ejemplo, cambiar `<=` por `<` hizo fallar `test_stock_igual_al_minimo_se_considera_por_pedir`, y quitar la validación del mínimo hizo fallar `test_stock_minimo_negativo_lanza_value_error`. Al restaurar el código volvió todo a verde.

## Reflexión final (5 a 8 líneas)

El asistente me ayudó más al proponer casos límite que yo no habría escrito primero, como el stock igual al mínimo, la lista vacía y no modificar la lista de entrada. Escribir las pruebas antes me obligó a decidir el orden y el umbral desde el contrato, no al revés. Mis pruebas no atraparon un error real porque el código pasó a la primera, pero la prueba de mutación mostró que sí detectan reglas rotas. Aprendí que "todo en verde" no basta y que un caché de bytecode puede dar resultados engañosos. Para la próxima funcionalidad haría yo mismo los primeros casos de prueba antes de pedirle ideas al asistente y pediría la implementación en pasos pequeños, para entender cada línea antes de aceptarla.
