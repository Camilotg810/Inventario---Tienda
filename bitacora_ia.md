# Bitácora de uso de IA

Proyecto: FarmaStock (las entradas 1 a 12 son del módulo de reposición que se propuso antes como HU-03 y hoy se llama HU-R1)
Estudiante: Juan Camilo Trujillo Garrido
Funcionalidad de la semana 5: HU-02 Ingreso de lotes (entradas 18 a 22); también HU-04 (entradas 13 a 17) y HU-R1
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
- **Verificación:** Revisé el diff con `git diff main..revision-semana-6` antes de integrarlo con `git merge revision-semana-6` (avance rápido, sin conflictos). Vi que los tests de la semana 5 solo cambiaron en el formato de dos líneas largas y que la lógica nueva está en `reposicion.py` y en `tests/test_revision_semana6.py`. Después de integrar, volví a ejecutar `pytest`, `ruff check .` y `pip-audit -r requirements.txt` y probé el README en una carpeta limpia.
- **Commit relacionado:** rama `revision-semana-6` (de 4387ff1 a 601f5b8 y los commits de informe y bitácora)

### Entrada 12

- **Fecha:** 2026-11-14
- **Prompt o sugerencia:** Resolver el orden de la `ñ` con `locale.strxfrm` o con la librería `babel`, para que `Ñame` quede después de `Nuez`.
- **Decisión:** Rechazada
- **Por qué:** Con `locale` el resultado depende de la configuración regional de cada equipo y las pruebas dejarían de ser reproducibles; `babel` sería una dependencia nueva para un desempate de bajo impacto. Lo dejé como pendiente con un plan.
- **Verificación:** Comprobé que hoy la `ñ` se ordena como `n` (`Ñame` antes que `Nuez`) y que solo afecta el desempate entre productos con el mismo faltante. Quedó documentado en el README (supuestos) y en `revision_seguridad.md`, sección 4.
- **Commit relacionado:** ninguno (pendiente documentado en el informe)

### Entrada 13

- **Fecha:** 2026-11-26
- **Prompt o sugerencia:** "Sigamos del proyecto que estamos, que es FarmaStock; no quiero que me des otros proyectos diferentes." El asistente propuso alinear el repositorio con FarmaStock implementando una historia real del documento de requisitos de la semana 3 (HU-04, vencimientos a 60 días) y ajustar el README.
- **Decisión:** Aceptada
- **Por qué:** El proyecto declarado es FarmaStock y el código de las semanas 5 y 6 no correspondía a ninguna de sus 9 historias. HU-04 es pequeña, no necesita base de datos y trae dos escenarios con datos concretos (uno de éxito y uno de error). No se creó ningún proyecto nuevo.
- **Verificación:** Comparé los datos de las pruebas con el escenario 1 del documento (lote L-102, Vitamina C, 10 unidades, vence el 10/11/2026) y con el mensaje del escenario 2 («El rango de días debe ser un número entero mayor a 0»). El README aclara que la reposición de la semana 5 no es una de las 9 historias y pasa a llamarse HU-R1 para no confundirla con la HU-03 (fiado).
- **Commit relacionado:** a4ebffa Implementa HU-04 y 287fe91 README de FarmaStock

### Entrada 14

- **Fecha:** 2026-11-26
- **Prompt o sugerencia:** Escribir las pruebas de HU-04 antes del código, a partir de los dos escenarios Gherkin y de los casos límite. El asistente propuso 27 pruebas: la lista ordenada con producto, lote, unidades y días restantes, los límites del rango (día 60 incluido, día 61 y vencidos excluidos, vence hoy), el rango por defecto, el desempate, la lista vacía, no modificar la entrada y los errores de `dias`, unidades y fecha.
- **Decisión:** Aceptada
- **Por qué:** Cada regla del contrato tiene su prueba, y los errores se rechazan en vez de ignorarse, como aprendí en H-02 de la semana 6.
- **Verificación:** Con un stub que lanza `NotImplementedError` fallaron las 27 nuevas y las 18 anteriores siguieron pasando. Tras implementar pasaron las 45. Hice una prueba de mutación manual de 6 cambios (`<=` por `<` en el rango, quitar `0 <=`, orden invertido, aceptar `dias = 0`, aceptar `bool`, no validar lotes) y cada cambio hizo fallar al menos una prueba; al restaurar volvieron las 45 en verde. No se tocó ningún archivo de las pruebas de las semanas 5 y 6.
- **Commit relacionado:** 98b7bfb Pruebas de HU-04 (en rojo) y a4ebffa Implementa HU-04 (en verde)

### Entrada 15

- **Fecha:** 2026-11-26
- **Prompt o sugerencia:** Al implementar, el asistente señaló dos puntos que el documento no define: si el reporte debe mostrar los lotes ya vencidos y si deben aparecer los lotes con 0 unidades. Una opción era decidirlos en el código (por ejemplo, ocultar los lotes agotados).
- **Decisión:** Rechazada
- **Por qué:** La historia no lo dice y la tarea de requisitos pide que lo que no tiene origen vaya a preguntas pendientes, no al código. Decidirlo sería inventar un requisito. Hoy el código no muestra los vencidos y sí muestra los de 0 unidades, y ambas cosas quedaron escritas como supuestos.
- **Verificación:** Revisé que el texto de HU-04 en el documento de la semana 3 no mencione ninguno de los dos casos. Quedaron como P-05 y P-06 en el Anexo A del README, con lo que hace el código hoy, y hay una prueba que fija cada comportamiento.
- **Commit relacionado:** a4ebffa Implementa HU-04 y 287fe91 README de FarmaStock

### Entrada 16

- **Fecha:** 2026-11-26
- **Prompt o sugerencia:** Crear un pipeline de integración continua que ejecute ruff, pytest y pip-audit. El asistente propuso un archivo de GitHub Actions (`.github/workflows/ci.yml`) que se ejecuta en cada push y pull request, con Python 3.12 y 3.14, con permisos de solo lectura.
- **Decisión:** Aceptada
- **Por qué:** Son las mismas tres comprobaciones que ya hacía a mano desde la semana 6, ahora automáticas. No agregué despliegue porque el proyecto todavía no tiene nada que desplegar.
- **Verificación:** Comprobé que el YAML es válido y repetí sus pasos en una carpeta limpia con un entorno nuevo (Python 3.12): ruff sin avisos, 45 pruebas en verde y pip-audit sin vulnerabilidades. Python 3.14 no se probó en esa simulación. La ejecución real en GitHub se ve en la pestaña Actions después de subir los cambios.
- **Commit relacionado:** d352916 CI: pipeline de GitHub Actions

### Entrada 17

- **Fecha:** 2026-11-26
- **Prompt o sugerencia:** Revisar mis cambios de la semana 6 antes de seguir. El asistente encontró tres errores de texto en mis ediciones: el informe de seguridad decía `Juan Camilo Trujillo` donde iba el marcador `[nombre y apellido]`, la Entrada 12 tenía mi observación del diff en el campo "Commit relacionado" y la verificación de la Entrada 11 era confusa.
- **Decisión:** Aceptada
- **Por qué:** Eran errores míos al editar, no del código. Dejaban afirmaciones falsas o confusas en el informe y en la bitácora.
- **Verificación:** Revisé el diff de cada cambio (3 inserciones y 3 eliminaciones en 2 archivos) y comprobé que mi observación sobre el diff de la Entrada 11 quedó en su lugar y que la Entrada 12 volvió a su texto original.
- **Commit relacionado:** bf80f8b Docs: corrige 3 errores de texto

### Semana 5 rehecha con FarmaStock (HU-02)

Esta funcionalidad reemplaza, para la entrega de la semana 5, a la historia de reposición del inventario de la tienda: HU-02 sí viene del documento de requisitos de FarmaStock. Se hizo el 2026-11-26, después de la fecha límite del 7 de noviembre. Las entradas 18 a 22 son de este trabajo.

### Entrada 18

- **Fecha:** 2026-11-26
- **Prompt o sugerencia:** "Haz la semana 5 con FarmaStock, no con el inventario de tienda." El asistente propuso HU-02 (ingreso de lotes por código y fecha de vencimiento) en vez de HU-04.
- **Decisión:** Aceptada
- **Por qué:** La tarea exige una historia Must y HU-04 es Should; HU-02 es Must, pequeña, tiene un escenario de error claro (lote caducado, con su mensaje) y reutiliza la clase `Lote` ya existente.
- **Verificación:** Comprobé la prioridad en la tabla MoSCoW del documento de la semana 3 y copié los dos escenarios sin cambiarlos.
- **Commit relacionado:** a482cfc Pruebas de HU-02 FarmaStock (en rojo)

### Entrada 19

- **Fecha:** 2026-11-26
- **Prompt o sugerencia:** El asistente escribió 25 casos de prueba (17 funciones, algunas parametrizadas) antes del código: 4 normales, 6 límite, el escenario de error del criterio y 14 de datos inválidos.
- **Decisión:** Aceptada con cambios
- **Por qué:** Cubren lo mínimo y fijan dos reglas que el documento no define: un lote que vence hoy se acepta y un código repetido en el mismo producto se rechaza. Las dejé como preguntas pendientes P-07 y P-08 en el README en vez de darlas por correctas. Cambié una línea de prueba que superaba el límite de ruff.
- **Verificación:** Con un módulo temporal que lanza `NotImplementedError` (no confirmado) fallaron los 25 casos; sin el módulo, falla la importación. Confirmé el commit solo con el archivo de pruebas.
- **Commit relacionado:** a482cfc

### Entrada 20

- **Fecha:** 2026-11-26
- **Prompt o sugerencia:** Primera implementación: `registrar_ingreso` con las cinco validaciones dentro de la función y un `sorted` con lambda; `stock_total` con un bucle.
- **Decisión:** Aceptada con cambios
- **Por qué:** Cumplía el contrato, pero mezclaba validación, regla de unicidad y orden en una sola función. En el refactor las separé en `_exigir_texto`, `_exigir_unidades_validas`, `_exigir_fecha_vigente`, `_ya_esta_registrado` y `_orden_de_vencimiento`.
- **Verificación:** Las 25 pruebas nuevas pasaron en el primer intento (70 en total), así que no atraparon un error real. Ruff encontró una línea de 90 caracteres, que partí. Hice una mutación manual de 9 cambios (por ejemplo `<` por `<=` en la fecha, o quitar la comprobación de `datetime`) y las pruebas atraparon los 9.
- **Commit relacionado:** 22340a5 Implementa HU-02 (pruebas en verde)

### Entrada 21

- **Fecha:** 2026-11-26
- **Prompt o sugerencia:** Rechazar un lote repetido sumando las unidades al lote existente, o rechazarlo con error.
- **Decisión:** Rechazada (la opción de sumar)
- **Por qué:** Sumar ocultaría un ingreso duplicado por error y el documento no lo pide. Elegí lanzar `ValueError` y lo dejé como pregunta pendiente P-08 para el cliente.
- **Verificación:** La prueba `test_codigo_de_lote_repetido_para_el_mismo_producto_se_rechaza` fija el comportamiento; una mutación que quita la comprobación la hizo fallar.
- **Commit relacionado:** 22340a5

### Entrada 22

- **Fecha:** 2026-11-26
- **Prompt o sugerencia:** Refactor con las pruebas en verde: dividir las validaciones, nombrar el orden (antes un lambda) y usar `any` y `sum`.
- **Decisión:** Aceptada
- **Por qué:** Cada paso de `registrar_ingreso` ahora se lee por su nombre y el comportamiento no cambia.
- **Verificación:** `pytest` dio 70 de 70 antes y después, `ruff check .` limpio y `git diff` de `tests/` vacío entre el commit verde y el refactor.
- **Commit relacionado:** 22817c9 Refactor HU-02

### Semana 6 con FarmaStock (revisión de HU-02, HU-04 y HU-R1)

Segunda ronda de la revisión de la semana 6, hecha el 2026-11-27 sobre todo el código actual. No usé un agente de código: las correcciones las hice yo con el asistente en el chat, una por commit, en la rama `semana6-revision-farmastock`. Entradas 23 a 26.

### Entrada 23

- **Fecha:** 2026-11-27
- **Prompt o sugerencia:** El prompt de revisión de la semana sobre `ingreso_lotes.py`, `vencimientos.py`, `reposicion.py` y sus pruebas. El asistente devolvió 3 hallazgos seguros y 5 sospechas.
- **Decisión:** Aceptada con cambios
- **Por qué:** Los 3 seguros eran reales (H-09, H-10, H-11); de las 5 sospechas, 3 eran falsos positivos, 1 se confirmó pero no tiene regla en los requisitos (sin tope de unidades, queda como P-09) y 1 era una decisión de diseño. No copié ninguna sin ejecutarla.
- **Verificación:** Ejecuté cada caso en Python (dos ingresos con el mismo código y el nombre escrito distinto, `hoy` con `None` y `datetime`, `unidades=10**18`, lista con un `1`) y busqué `isinstance` en `src/`. Lo que la IA no encontró (control de acceso de HU-02, acciones de CI fijadas por etiqueta, el docstring con HU-03) está en `revision_seguridad.md`.
- **Commit relacionado:** 21f5051 Pruebas de la revisión (en rojo)

### Entrada 24

- **Fecha:** 2026-11-27
- **Prompt o sugerencia:** Corregir H-09: comparar el producto sin mayúsculas ni espacios de más al buscar el stock y al revisar si el código de lote ya existe.
- **Decisión:** Aceptada
- **Por qué:** Un lote repetido pasaba solo por escribir el nombre distinto y el stock quedaba partido, lo que va contra el objetivo de HU-02 (controlar el inventario por lote). Elegí normalizar solo para comparar y no el texto guardado, para no alterar lo que el administrador escribió.
- **Verificación:** 5 pruebas nuevas fallaron en rojo antes y pasaron después (83 en total); `ruff check .` limpio; ninguna prueba existente se modificó.
- **Commit relacionado:** 69f2253 Fix H-09

### Entrada 25

- **Fecha:** 2026-11-27
- **Prompt o sugerencia:** Validar `hoy` en las dos funciones (H-10) y mover las comprobaciones repetidas de tipo a `validaciones.py` (H-11).
- **Decisión:** Aceptada
- **Por qué:** H-10 cambia un mensaje de error confuso por uno que nombra el dato, y H-11 quita una comprobación escrita 4 y 3 veces en tres módulos. El refactor no cambia el comportamiento.
- **Verificación:** Las 8 pruebas de `hoy` pasaron a verde; tras el refactor, 83 de 83 y `git diff` de `tests/` vacío entre los commits fa3b87f y 2aa5151.
- **Commit relacionado:** fa3b87f Fix H-10 y 2aa5151 Refactor H-11

### Entrada 26

- **Fecha:** 2026-11-27
- **Prompt o sugerencia:** Dos propuestas: poner un tope de 10.000 unidades por lote en `registrar_ingreso`, y unir los dos `_orden_de_vencimiento` en una sola función.
- **Decisión:** Rechazada
- **Por qué:** El tope sería una regla inventada: el documento de requisitos no define un máximo; la dejé como pregunta P-09 para el cliente. Unir las funciones obligaba a que un módulo dependa del otro por una línea, y cada una recibe un tipo distinto.
- **Verificación:** Comprobé en el documento de la semana 3 que HU-02 no menciona un máximo, y que los dos orden reciben `Lote` y `LoteProximo`.
- **Commit relacionado:** ninguno (no se cambió el código)

### Etapa final: informe y diapositivas (2026-11-27)

Entradas 27 y 28, del informe final (`docs/informe_final.md` y `.pdf`) y de las diapositivas (`docs/diapositivas.pdf`).

### Entrada 27

- **Fecha:** 2026-11-27
- **Prompt o sugerencia:** Redactar el informe final con la plantilla del módulo 7 y preparar 8 diapositivas, con evidencias reales enlazadas (archivos, commits, bitácora, pipeline).
- **Decisión:** Aceptada con cambios
- **Por qué:** El borrador cumple la estructura de la plantilla, pero corregí dos cosas: una frase decía «segunda revisión con IA» para un caso que fue de la primera ronda, y la tarea de la semana 7 no figura como entregada en Q10, así que el informe lo dice sin adornos. Las reflexiones son un borrador que debo revisar y ajustar a lo que de verdad pienso.
- **Verificación:** Comprobé cada hash de commit con `git log`, los 26 enlaces del informe contra los archivos del repositorio, el conteo de pruebas (83) con `pytest`, y la ejecución del pipeline abriendo la página de GitHub Actions: ejecución #1 en `main`, commit 0499433, verde en Python 3.12 y 3.14. Las dos salidas de la diapositiva 5 las generé ejecutando el código de los commits b570a5e y 69f2253.
- **Commit relacionado:** el que agrega `docs/informe_final.pdf` y `docs/diapositivas.pdf`

### Entrada 28

- **Fecha:** 2026-11-27
- **Prompt o sugerencia:** Redactar rápido el plan de pruebas, la guía de despliegue y el plan de operación para que la carpeta `docs/` quedara completa.
- **Decisión:** Rechazada
- **Por qué:** El proyecto no tiene servidor, base de datos ni interfaz, así que una guía de despliegue y un plan de operación serían texto sin nada real que describir, y un plan de pruebas escrito a última hora tampoco tendría evidencia. Prefiero listarlos como pendientes en el informe (sección 5).
- **Verificación:** Revisé el repositorio: solo hay funciones y pruebas, y el pipeline; lo dejé escrito en `docs/LEEME.md` y en el informe.
- **Commit relacionado:** ninguno (pendiente documentado)

## Resumen

| Decisión | Cantidad |
|---|---|
| Aceptadas | 14 |
| Aceptadas con cambios | 7 |
| Rechazadas | 7 |

## Errores que atraparon las pruebas

El código generado pasó las 10 pruebas en la primera ejecución, así que las pruebas no detectaron un error real en la implementación inicial. Para saber si de todas formas protegían el comportamiento, rompí el código a propósito de cuatro formas; cada cambio lo atrapó una prueba distinta. Por ejemplo, cambiar `<=` por `<` hizo fallar `test_stock_igual_al_minimo_se_considera_por_pedir`, y quitar la validación del mínimo hizo fallar `test_stock_minimo_negativo_lanza_value_error`. Al restaurar el código volvió todo a verde.

### Semana 6

Las pruebas de la semana 5 no detectaron dos errores reales del código, porque no probaban esos casos: el orden por nombre con mayúsculas y tildes (H-01) y los datos que no son enteros, como `NaN` (H-02). Los encontró la revisión: escribí pruebas nuevas, las vi fallar en rojo y luego las puse en verde con el arreglo. Las 10 pruebas originales no cambiaron de lógica.

### Semana 6 con FarmaStock

La revisión encontró dos errores reales que las 70 pruebas anteriores no cubrían: el mismo producto escrito con otras mayúsculas o espacios se contaba como otro (H-09) y un `hoy` inválido fallaba con un mensaje poco claro (H-10). Escribí las 13 pruebas nuevas, las vi fallar y luego las pasé a verde. La IA no vio lo más importante para la seguridad futura: que HU-02 es solo del Administrador y nada lo comprueba todavía; quedó como pendiente con su prueba de abuso planeada.

### Semana 5 con HU-02

Las 25 pruebas pasaron a la primera, así que no atraparon un error del código. La mutación manual de 9 cambios las atrapó todas. Lo útil fue que, al escribirlas, aparecieron dos reglas que el documento no define (lote que vence hoy y código repetido) y quedaron como preguntas pendientes P-07 y P-08.

### Etapa final

Las 27 pruebas de HU-04 se escribieron antes del código y fallaron todas con el stub, así que no hubo un error del código que ellas atraparan. Para saber si protegen el comportamiento hice una prueba de mutación manual de 6 cambios y las pruebas detectaron los 6. Además, la IA señaló dos reglas que el documento de requisitos no define (lotes vencidos y lotes con 0 unidades) y las dejé como preguntas pendientes en vez de decidirlas en el código.

## Reflexión final (5 a 8 líneas)

El asistente me ayudó más al proponer casos límite que yo no habría escrito primero, como el stock igual al mínimo, la lista vacía y no modificar la lista de entrada. Escribir las pruebas antes me obligó a decidir el orden y el umbral desde el contrato, no al revés. Mis pruebas no atraparon un error real porque el código pasó a la primera, pero la prueba de mutación mostró que sí detectan reglas rotas. Aprendí que "todo en verde" no basta y que un caché de bytecode puede dar resultados engañosos. Para la próxima funcionalidad haría yo mismo los primeros casos de prueba antes de pedirle ideas al asistente y pediría la implementación en pasos pequeños, para entender cada línea antes de aceptarla.
