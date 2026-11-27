# Informe final del proyecto integrador

Proyecto: FarmaStock, gestión de inventario y ventas para una farmacia de barrio
Estudiante: Juan Camilo Trujillo Garrido
Repositorio: https://github.com/Camilotg810/Inventario---Tienda
Fecha: 2026-11-27

## 1. Resumen

FarmaStock es un sistema para una farmacia comunitaria pequeña: controla el inventario por lote y fecha de vencimiento, las ventas en efectivo y a crédito (fiado) y el cierre de caja. Usé IA (Claude) en las seis fases del seminario: propuesta, requisitos, diseño, código, pruebas y operación (integración continua). Lo implementado es **parte del módulo de inventario**: HU-02 (ingreso de lotes, prioridad Must), HU-04 (vencimientos a 60 días) y una función de reposición (HU-R1), con 83 pruebas que pasan en el pipeline de GitHub Actions en Python 3.12 y 3.14. Las otras siete historias no están implementadas. El resultado principal de la verificación: la IA entregó código y pruebas que pasaban a la primera pero tenían errores reales (datos inválidos aceptados, productos duplicados por escribir el nombre distinto, requisitos sin origen), que encontré con revisión, ejecución de casos y pruebas de mutación. Hay además una corrección de fondo que declaro en la sección 2: los requisitos no vienen de una entrevista real.

## 2. Problema y usuario

**Quién y qué problema.** Una farmacia de barrio con un Cajero y un Administrador. Los problemas que recoge el [documento de requisitos](https://github.com/Camilotg810/Inventario---Tienda/blob/main/docs/02_requisitos_S3.pdf): medicamentos que se vencen sin que nadie lo note, ventas fiadas anotadas en una libreta, el cierre de caja manual y la dificultad de vender cuando se cae internet. Los usuarios son el Cajero (vende, cobra, registra abonos) y el Administrador (ingresa lotes, aprueba cupos de crédito, cierra la caja). La [propuesta del módulo 1](https://github.com/Camilotg810/Inventario---Tienda/blob/main/docs/01_propuesta_S2.pdf) resume la idea.

**Corrección importante.** El documento de requisitos de la semana 3 dice que los requisitos salieron de una entrevista con un cliente y de un permiso suyo. **Esa entrevista no se realizó como allí se describe.** Los requisitos los elaboré con apoyo de IA a partir de un escenario de farmacia comunitaria. Por eso no los presento como necesidades confirmadas: están **por validar con un cliente real**, y el README, el diseño y la bitácora lo dicen. No se cambió el documento de la semana 3 (está en `docs/` tal como se entregó); la corrección está aquí y en el [LEEME de docs](https://github.com/Camilotg810/Inventario---Tienda/blob/main/docs/LEEME.md).

## 3. La IA en el ciclo de vida

| Módulo y fase | Qué hice con IA | Herramienta | Evidencia | Cómo verifiqué |
|---|---|---|---|---|
| 1. Fundamentos | Banco de 10 prompts evaluados con ficha y propuesta del proyecto FarmaStock. Los rehice el 2026-11-26 para que la propuesta fuera de FarmaStock | Claude (chat) | [banco](https://github.com/Camilotg810/Inventario---Tienda/blob/main/docs/01_banco_prompts_S2.pdf), [propuesta](https://github.com/Camilotg810/Inventario---Tienda/blob/main/docs/01_propuesta_S2.pdf) | Cada prompt tiene su resultado y su calificación; corregí contradicciones del propio texto de las fichas |
| 2. Requisitos | Historias de usuario, escenarios Gherkin, necesidades, MoSCoW y requisitos no funcionales | Claude (chat) | [requisitos](https://github.com/Camilotg810/Inventario---Tienda/blob/main/docs/02_requisitos_S3.pdf), [bitácora de prompts](https://github.com/Camilotg810/Inventario---Tienda/blob/main/docs/02_bitacora_prompts_S3.pdf) | Trazabilidad de cada historia con su necesidad; en la revisión posterior encontré un actor inventado (caso 1) |
| 3. Diseño | Alternativas de arquitectura, matriz ponderada, diagramas C4, ADR-001, modelo de datos y API | Claude (chat) | [diseño](https://github.com/Camilotg810/Inventario---Tienda/blob/main/docs/03_diseno_S4.pdf) y [fuentes](https://github.com/Camilotg810/Inventario---Tienda/tree/main/docs/03_diseno_fuentes) | Totales de la matriz y sensibilidad calculados con un script; cada elemento de los diagramas contrastado con una historia (caso 2) |
| 4. Código | Funciones `registrar_ingreso`, `lotes_por_vencer`, `productos_por_pedir`, con contrato, pruebas primero y refactor | Claude (chat) | [ingreso_lotes.py](https://github.com/Camilotg810/Inventario---Tienda/blob/main/src/inventario/ingreso_lotes.py), [vencimientos.py](https://github.com/Camilotg810/Inventario---Tienda/blob/main/src/inventario/vencimientos.py), commits [a482cfc](https://github.com/Camilotg810/Inventario---Tienda/commit/a482cfc), [22340a5](https://github.com/Camilotg810/Inventario---Tienda/commit/22340a5), [22817c9](https://github.com/Camilotg810/Inventario---Tienda/commit/22817c9) | Pruebas escritas antes del código (rojo, verde, refactor), ruff con reglas E, F, B, S y lectura línea por línea |
| 5. Pruebas | 83 pruebas (casos normales, límite y error) y pruebas de mutación manuales | Claude (chat) | [tests/](https://github.com/Camilotg810/Inventario---Tienda/tree/main/tests), [bitácora, entradas 14, 20 y 24](https://github.com/Camilotg810/Inventario---Tienda/blob/main/bitacora_ia.md) | Mutación manual: 6 de 6 cambios detectados en HU-04 y 9 de 9 en HU-02; nuevas pruebas vistas en rojo antes de corregir (casos 3 y 4) |
| 6. Operación | Pipeline de integración continua y revisión de seguridad | Claude (chat) | [ci.yml](https://github.com/Camilotg810/Inventario---Tienda/blob/main/.github/workflows/ci.yml), [última ejecución](https://github.com/Camilotg810/Inventario---Tienda/actions/runs/46033127026), [revision_seguridad.md](https://github.com/Camilotg810/Inventario---Tienda/blob/main/revision_seguridad.md) | La ejecución #1 en `main` (commit 0499433) pasó en Python 3.12 y 3.14: ruff, pytest y pip-audit. No hay guía de despliegue ni plan de operación (ver sección 5) |

## 4. Verificación: lo que la IA hizo mal y cómo lo encontré

**Caso 1: un actor sin origen en los requisitos (fase: requisitos).**
- **Qué propuso la IA:** el documento de requisitos incluía una «Pasarela de Pagos QR» como sistema externo, sin ninguna historia ni necesidad que la pidiera.
- **Qué estaba mal:** un elemento sin origen en los requisitos. Si se hubiera dejado, el diseño habría construido una integración de pago que nadie pidió.
- **Cómo lo detecté:** al diseñar (semana 4) la regla era que cada elemento de los diagramas debe salir de una historia; hice la tabla de trazabilidad y la pasarela no tenía ninguna.
- **Qué hice:** la quité del contexto y de los contenedores, y lo expliqué en la sección «Qué corregí del borrador». Commit [37df515](https://github.com/Camilotg810/Inventario---Tienda/commit/37df515) (documento de diseño en `docs/`).

**Caso 2: un borrador de arquitectura con piezas y campos que sobraban (fase: diseño).**
- **Qué propuso la IA:** un diagrama de contenedores con una cola RabbitMQ y un modelo de datos con `saldo_adeudado` en CLIENTE y `cambio` en VENTA; sin entidad para el descuento de adulto mayor y sin un identificador para sincronizar ventas sin duplicarlas.
- **Qué estaba mal:** la cola no resuelve el modo sin conexión (ocurre en el navegador) y sube el costo; los dos campos son valores derivados que pueden quedar desincronizados; faltaban `GRUPO_CLIENTE` (HU-06) y `uuid_venta` (HU-09).
- **Cómo lo detecté:** contrastando cada contenedor y cada campo con las historias y los requisitos no funcionales, y con el atributo de costo de la matriz.
- **Qué hice:** eliminé la cola y los campos derivados, añadí `GRUPO_CLIENTE` y `uuid_venta`, y dejé el borrador junto al diagrama final. Commit [37df515](https://github.com/Camilotg810/Inventario---Tienda/commit/37df515).

**Caso 3: código que aceptaba datos inválidos en silencio (fase: código).**
- **Qué propuso la IA:** `productos_por_pedir` validaba solo los números negativos.
- **Qué estaba mal:** con `stock = NaN` el producto desaparecía de la lista sin error, y `2.7` o `True` también pasaban. Un dato mal capturado quedaba oculto.
- **Cómo lo detecté:** en la revisión con IA de la semana 6 (ronda 1); ejecuté `Producto("X", "n", float("nan"), 5)` y devolvió una lista vacía sin error. Escribí 6 pruebas, las vi fallar y luego las pasé a verde.
- **Qué hice:** `TypeError` con el código del producto si el valor no es un entero (un `bool` tampoco). Commit [4847cf9](https://github.com/Camilotg810/Inventario---Tienda/commit/4847cf9). Antes, en el commit [4ab1ab3](https://github.com/Camilotg810/Inventario---Tienda/commit/4ab1ab3), corregí que el desempate por nombre distinguía mayúsculas y tildes.

**Caso 4: pruebas que pasaban pero dejaban un hueco (fase: pruebas).**
- **Qué propuso la IA:** 25 pruebas para HU-02 (ingreso de lotes). Pasaron a la primera y una mutación manual de 9 cambios las atrapó todas.
- **Qué estaba mal:** ninguna probaba el mismo producto escrito con otras mayúsculas o espacios. `Ibuprofeno 400mg` e `ibuprofeno 400mg ` contaban como productos distintos: el mismo código de lote se aceptaba dos veces y el stock salía 10 con un nombre y 0 con el otro.
- **Cómo lo detecté:** la revisión con IA lo señaló y lo reproduje ejecutando dos ingresos con el nombre escrito distinto. Escribí 13 pruebas nuevas, vistas en rojo antes de corregir.
- **Qué hice:** el nombre se compara sin mayúsculas ni espacios de más. Pruebas en rojo [21f5051](https://github.com/Camilotg810/Inventario---Tienda/commit/21f5051), corrección [69f2253](https://github.com/Camilotg810/Inventario---Tienda/commit/69f2253). El informe [revision_seguridad.md](https://github.com/Camilotg810/Inventario---Tienda/blob/main/revision_seguridad.md) tiene la tabla completa (H-01 a H-12) y también lo que la IA no encontró: que HU-02 es solo del Administrador y nada lo comprueba todavía.

**Sugerencias de la IA que rechacé** (entradas de la [bitácora](https://github.com/Camilotg810/Inventario---Tienda/blob/main/bitacora_ia.md)): convertir con `int()` los datos mal escritos «para ser tolerante» (entrada 6), decidir en el código si el reporte muestra lotes vencidos o con 0 unidades, que el documento no define (entrada 15), sumar las unidades de un lote repetido (entrada 21) y poner un tope de 10.000 unidades por lote, que sería una regla inventada (entrada 26).

## 5. Estado final del sistema

- **Arquitectura:** PWA con Django y PostgreSQL, decidida en el [ADR-001](https://github.com/Camilotg810/Inventario---Tienda/blob/main/docs/03_diseno_S4.pdf) (puntajes 4,15 contra 3,8 del escritorio local y 2,85 de los microservicios; la decisión solo cambia si el modo sin conexión pesa casi la mitad). **Está diseñada, no construida**: no hay servidor, base de datos ni interfaz.
- **Funcionalidades terminadas:** de las cinco historias Must (HU-01, 02, 03, 07, 09) **solo HU-02 está implementada**. También HU-04 (prioridad Should) y la función de reposición HU-R1, que no es una de las 9 historias. HU-01, 03, 05, 06, 07, 08 y 09 no están implementadas.
- **Pruebas:** 83 pruebas (HU-02: 25 + 13 de revisión, HU-04: 27, reposición: 18) que cubren la lógica de esas funciones, no el sistema completo. Última ejecución del pipeline: [#1 en `main`](https://github.com/Camilotg810/Inventario---Tienda/actions/runs/46033127026), verde en Python 3.12 y 3.14.
- **Pendientes y por qué no alcanzaron:**
  - Control de acceso de HU-02 con su prueba de abuso (un cajero no debe poder ingresar lotes): necesita la capa de API, que no existe.
  - Plan de pruebas, guía de despliegue y plan de operación de los módulos 5 y 6: no los elaboré. La tarea de la semana 7 (suite de pruebas generada con IA y registro de pruebas) no figura como entregada en Q10, que la cerró el 26/11.
  - Validar los requisitos con un cliente real y resolver las preguntas P-01 a P-09.
  - Fijar las acciones de GitHub Actions por commit (GitHub avisa que usan Node.js 20, en desuso) y elegir una licencia del código.
  - Las semanas 5 y 6 se entregaron primero con el inventario de una tienda y rehice la versión de FarmaStock el 26 y 27 de noviembre, después de las fechas límite; las fechas de los commits lo muestran.

## 6. Reflexión ética y legal

| Principio | Decisión en mi proyecto | Evidencia |
|---|---|---|
| Datos personales (Ley 1581 de 2012) | El código actual no maneja datos personales: solo productos y lotes. El diseño sí tendrá nombre del cliente, su cupo y su deuda (fiado), y un historial de compras de medicamentos ligado a un cliente, que se acerca a datos de salud (sensibles según la ley). Decisiones: el cliente guarda solo nombre y cupo (sin documento ni teléfono); las ventas sin conexión son solo en efectivo, sin cliente; `cliente_id` es opcional en la venta; no se guarda contraseña en texto sino un hash bcrypt. Pendiente: aviso de privacidad y autorización del titular antes de registrar clientes. Todos los nombres de los ejemplos son inventados | [modelo de datos](https://github.com/Camilotg810/Inventario---Tienda/blob/main/docs/03_diseno_S4.pdf) (sección 5), [RNF-03](https://github.com/Camilotg810/Inventario---Tienda/blob/main/docs/02_requisitos_S3.pdf) |
| Sesgo | El sistema no usa modelos de IA para decidir. La regla del descuento del 10 % a adultos mayores (HU-06) es fija y por grupo de cliente, no por una estimación. El sesgo que sí apareció fue técnico: el orden por nombre trataba distinto las tildes y mayúsculas del español (H-01); lo corregí. La `ñ` se ordena como `n` y quedó como pendiente | commit [4ab1ab3](https://github.com/Camilotg810/Inventario---Tienda/commit/4ab1ab3), [revision_seguridad.md](https://github.com/Camilotg810/Inventario---Tienda/blob/main/revision_seguridad.md) |
| Transparencia | El uso de IA está declarado en el README (sección 7) y en la bitácora de 28 entradas con su decisión y su verificación; los commits recientes llevan la línea `Co-Authored-By`. Los requisitos se declaran «por validar» y las preguntas sin respuesta (P-05 a P-09) están escritas, no decididas en el código | [bitácora](https://github.com/Camilotg810/Inventario---Tienda/blob/main/bitacora_ia.md), [README](https://github.com/Camilotg810/Inventario---Tienda/blob/main/README.md) |
| Responsabilidad | Respondo yo por el código y las decisiones, no la IA. En una farmacia un error de stock o de vencimiento puede llevar a vender un medicamento vencido: HU-02 rechaza lotes caducados con un mensaje claro, y el reporte de HU-04 es una ayuda que no reemplaza el criterio del regente de farmacia. Los datos inválidos se rechazan en vez de corregirse en silencio | commits [22340a5](https://github.com/Camilotg810/Inventario---Tienda/commit/22340a5), [4847cf9](https://github.com/Camilotg810/Inventario---Tienda/commit/4847cf9) |
| Propiedad intelectual y política de uso | El código lo escribí con ayuda de IA y debo poder explicarlo línea por línea. Las herramientas de desarrollo (pytest, ruff y pip-audit) tienen versión fijada y licencias de código abierto permisivas. El repositorio todavía no tiene licencia: lo dejo declarado como pendiente en el README en vez de asumir una | [requirements.txt](https://github.com/Camilotg810/Inventario---Tienda/blob/main/requirements.txt), README sección 8 |

**El dilema más importante.** La semana 3 pedía partir de una entrevista con un cliente y yo entregué un documento que decía que la había hecho, cuando no fue así. El dilema fue si seguir construyendo sobre ese documento o corregirlo. Lo resolví declarándolo: los requisitos pasaron a ser «por validar», lo que el documento no define quedó como preguntas pendientes y no como reglas del código, la semana 4 se rehízo desde cero con esos requisitos, y esta sección es mi corrección. Costó tiempo y entregas fuera de fecha, pero evita que el diseño y las pruebas parezcan respaldados por un cliente que no existió.

## 7. Aprendizajes

Ahora sé escribir el contrato y las pruebas antes del código, medir si las pruebas sirven rompiendo el código a propósito (mutación) y revisar con una lista de seguridad y un linter, en vez de fiarme de que «todo está en verde». Confié de más en la IA en dos cosas: en que unas pruebas que pasaban a la primera ya cubrían todo (el caso 4 lo desmintió) y en que un documento de requisitos redactado por ella equivalía a una entrevista (no lo es). La IA tampoco vio lo que más importa para la seguridad futura: que HU-02 es solo del Administrador y nada lo comprueba todavía. Lo que haría distinto: entrevistar a un cliente real antes de pedir requisitos, escribir yo los primeros casos de prueba antes de pedirle ideas a la IA, y no dejar para el final las tareas de pruebas y operación (plan de pruebas, despliegue, operación). Si la IA dejara de existir, podría mantener este código: son funciones pequeñas con contrato, pruebas y documentación, y sé explicar cada decisión.

## 8. Anexos

- Bitácora de uso de IA: [bitacora_ia.md](https://github.com/Camilotg810/Inventario---Tienda/blob/main/bitacora_ia.md)
- Revisión de código y seguridad: [revision_seguridad.md](https://github.com/Camilotg810/Inventario---Tienda/blob/main/revision_seguridad.md)
- Documentos de cada módulo: [carpeta docs/](https://github.com/Camilotg810/Inventario---Tienda/tree/main/docs) (propuesta y banco de prompts, requisitos y bitácora de la semana 3, diseño con ADR)
- Última ejecución del pipeline: https://github.com/Camilotg810/Inventario---Tienda/actions/runs/46033127026
