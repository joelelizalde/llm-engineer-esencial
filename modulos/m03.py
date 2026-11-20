MODULE = {
    "num": "03",
    "title": "Ingeniería de datos",
    "sub": "Recolectar, limpiar y almacenar el corpus",
    "lessons": [
        {
            "id": "llm3l1",
            "lnum": 1,
            "title": "Diseñar la recolección: crawlers, APIs y límites",
            "minutes": 7,
            "lead": "La calidad del gemelo empieza mucho antes del modelo: empieza en qué decides descargar y en cómo lo haces. Un crawler mal diseñado duplica documentos, bloquea tu IP o recoge basura; uno bien diseñado deja un rastro reproducible de qué se obtuvo, cuándo y por qué.",
            "diagram": ("loop", ["Descubrir URL", "Descargar", "Validar", "Guardar"]),
            "caption": "El ciclo de recolección se repite por cada fuente. La validación y el guardado idempotente evitan duplicados y pérdidas.",
            "sections": [
                {
                    "h": "Elegir las fuentes con intención",
                    "p": [
                        "No todo el contenido de una persona sirve para un gemelo. Los artículos largos aportan estilo y argumentos; los README aportan convenciones técnicas; las notas cortas aportan opiniones, pero también ruido. Antes de programar un crawler, haz un inventario: qué fuentes existen, qué licencia tienen, qué proporción del total aportan y qué se puede usar legalmente.",
                        "Medium, Substack, GitHub y LinkedIn tienen estructuras distintas y reglas distintas. Algunas ofrecen RSS o API; otras obligan a raspar HTML y limitan la frecuencia. LinkedIn es especialmente restrictivo: automatizar el acceso puede violar sus términos. La decisión de incluir una fuente es también una decisión legal y de reputación, no solo técnica.",
                        "Un buen corpus es diverso y está sesgado a propósito. Si solo incluyes artículos técnicos, el gemelo escribirá como un manual. Si incluyes entrevistas, ganará voz. Documenta el criterio de inclusión para poder revisarlo cuando cambie el producto.",
                    ],
                },
                {
                    "h": "Descubrir, descargar y respetar",
                    "p": [
                        "El crawler empieza por una lista de semillas: perfiles, feeds, repositorios. De cada semilla extrae enlaces y decide cuáles seguir según reglas de dominio y profundidad. Un feed RSS evita tener que rastrear; una API paginada es más estable que el HTML. Cuando solo hay HTML, respeta robots.txt, identifícate con un user-agent claro y deja una pausa entre peticiones.",
                        "Los límites de frecuencia no son un obstáculo: son parte del contrato. Implementa reintentos con espera exponencial, respeta los códigos 429 y 503, y guarda el estado para reanudar sin empezar de cero. Si el sitio cambia su estructura, el crawler debe fallar de forma visible y no llenar la base de páginas vacías.",
                        "La idempotencia es la propiedad que salva el proyecto. Cada documento se identifica por una clave estable —URL canónica más hash del contenido— y se inserta o actualiza, nunca se duplica a ciegas. Así puedes relanzar la recolección tras un fallo sin revisar manualmente miles de registros.",
                    ],
                },
                {
                    "h": "Programar y observar la ingesta",
                    "p": [
                        "La recolección se ejecuta de forma programada, no cuando alguien se acuerda. Un cron o un orquestador lanza el trabajo, registra cuántos documentos descubrió, cuántos descargó, cuántos fallaron y por qué. Esas métricas detectan pronto un cambio de HTML o un bloqueo.",
                        "Conviene separar la descarga de la limpieza. La primera guarda el crudo con su procedencia y su fecha de captura; la segunda se puede repetir sin volver a la red. Esa separación permite auditar qué se descargó y reconstruir el corpus si un extractor tenía un error.",
                        "Por último, piensa en el crecimiento. Un crawler que hoy procesa cien artículos debe poder procesar diez mil sin reescribirse: paginación, concurrencia limitada, colas y checkpoints. La escala no cambia la lógica, pero sí expone las decisiones que se tomaron a la ligera.",
                    ],
                },
            ],
            "brief": [
                "Elige fuentes por valor, licencia y diversidad",
                "Respeta robots, límites y reintentos",
                "Guarda crudo, procedencia y estado de forma idempotente",
            ],
            "keys": [
                "El corpus se diseña: qué entra y qué queda fuera afecta al estilo y a los sesgos del gemelo.",
                "RSS y APIs son más estables que el raspado de HTML, pero también tienen límites y condiciones.",
                "La espera exponencial, los checkpoints y la idempotencia hacen que la ingesta se pueda reanudar.",
                "Separar descarga y limpieza permite reprocesar sin volver a rastrear la web.",
            ],
            "example": "Un crawler de Substack recorre el feed del autor, guarda cada entrada con su URL canónica y un hash del HTML. Al relanzarlo una semana después, detecta que tres artículos cambiaron y actualiza solo esos, en lugar de duplicar los doscientos restantes.",
            "caution": "Ignorar robots.txt o los términos de uso puede costarte el acceso y el proyecto. La técnica más rápida no sirve si la fuente te bloquea o te reclama.",
            "search": "crawler recolección fuentes Medium Substack GitHub LinkedIn RSS API robots.txt rate limit reintentos espera exponencial idempotencia checkpoint ingesta",
        },
        {
            "id": "llm3l2",
            "lnum": 2,
            "title": "De HTML a documento limpio",
            "minutes": 7,
            "lead": "Una página web contiene mucho más que el artículo: menús, banners, comentarios, enlaces sociales y anuncios. Si ese ruido entra en el índice, la recuperación devuelve fragmentos inútiles y el modelo aprende a escribir como una plantilla de cookies. La limpieza es una etapa de producto, no un detalle de fontanería.",
            "diagram": ("flow", ["HTML", "Extraer", "Normalizar", "Documento"]),
            "caption": "La extracción conserva el contenido principal; la normalización unifica formato y metadatos; el documento resultante es la unidad que se almacena.",
            "sections": [
                {
                    "h": "Extraer el contenido principal",
                    "p": [
                        "La forma robusta de extraer es combinar reglas por dominio con un extractor genérico de contenido. Para un sitio conocido, los selectores CSS son precisos; para uno desconocido, un algoritmo de legibilidad detecta el bloque central y descarta navegación. Si ambos fallan, es mejor guardar el crudo y marcar el documento para revisión que indexar basura.",
                        "El texto se convierte a Markdown o a texto plano con estructura. Conserva encabezados, listas, tablas y bloques de código: son señales para el chunking y para el modelo. Una tabla aplanada en una línea de texto pierde su significado; un bloque de código sin delimitadores se mezcla con la prosa.",
                        "Elimina el boilerplate restante: pies de página, avisos de cookies, «comparte en», biografías repetidas. Un truco útil es comparar varias páginas del mismo sitio y restar las líneas que aparecen en todas. También conviene quitar los enlaces de navegación y conservar solo el texto ancla cuando aporte.",
                    ],
                },
                {
                    "h": "Normalizar, deduplicar y validar",
                    "p": [
                        "La normalización unifica espacios, saltos de línea, comillas y codificación. Corrige entidades HTML, elimina caracteres de control y decide qué hacer con el idioma: si el corpus es en español, un artículo en inglés puede ser útil para código, pero no para imitar la voz. Detecta el idioma y guárdalo como metadato.",
                        "La deduplicación tiene dos niveles. El exacto compara hashes del texto normalizado. El casi duplicado detecta versiones con cambios menores mediante shingles y MinHash, o mediante similitud de embeddings. Los duplicados no solo inflan el índice: sesgan el ajuste fino hacia el contenido repetido y desperdician almacenamiento.",
                        "La validación comprueba que el documento tiene los campos obligatorios, una longitud mínima y una fecha plausible. Un esquema con tipos y reglas evita que un cambio en el crawler introduzca registros silenciosamente incompletos. Los documentos que no pasan se apartan con un motivo, no se borran: quizá el extractor necesita una regla nueva.",
                    ],
                },
                {
                    "h": "Privacidad y trazabilidad",
                    "p": [
                        "Un corpus puede contener datos personales, correos, teléfonos o información de terceros. Antes de indexar, decide qué se elimina o se enmascara. No porque el modelo vaya a «filtrarlos» de forma deliberada, sino porque pueden aparecer en una respuesta y porque el cumplimiento normativo lo exige.",
                        "Cada documento debe conservar su procedencia: URL original, fecha de captura, fecha de publicación, autor, licencia y versión del extractor. Esa trazabilidad permite citar, retirar contenido si alguien lo pide y reproducir el corpus en una fecha concreta. Sin ella, el sistema es una colección de textos sin origen.",
                        "La limpieza también se evalúa. Toma una muestra de veinte documentos y comprueba a mano qué se perdió y qué se coló. Esa revisión detecta problemas que ninguna métrica automática ve: un extractor que corta el final de los artículos, una tabla convertida en sopa o un bloque de código tratado como prosa.",
                    ],
                },
            ],
            "brief": [
                "Extrae el contenido central y conserva estructura",
                "Normaliza, deduplica y valida con un esquema",
                "Enmascara datos personales y conserva procedencia",
            ],
            "keys": [
                "El HTML crudo se guarda antes de limpiar para poder reprocesar y auditar.",
                "Markdown con encabezados, listas y código preserva señales útiles para el chunking.",
                "La deduplicación exacta y casi exacta evita sesgos y desperdicio de índice.",
                "Procedencia, licencia y versión del extractor hacen el corpus citable y reversible.",
            ],
            "example": "Un artículo de Medium se descarga con su menú lateral y su aviso de suscripción. El extractor conserva el título, los subtítulos y el bloque de código; elimina el menú y el aviso. El documento limpio pesa un tercio del HTML y su hash coincide con el de una copia publicada en Substack, así que se marca como duplicado y no se indexa dos veces.",
            "caution": "Un extractor demasiado agresivo puede borrar el contexto que da sentido a una cita. Revisa muestras antes de indexar miles de documentos.",
            "search": "HTML extracción legibilidad boilerplate Markdown normalización deduplicación MinHash hash idioma validación esquema privacidad trazabilidad licencia",
        },
        {
            "id": "llm3l3",
            "lnum": 3,
            "title": "El data warehouse y la capa cruda",
            "minutes": 6,
            "lead": "Guardar documentos en una carpeta no es una arquitectura de datos. Para que el corpus se pueda consultar, reprocesar y auditar, necesita capas con responsabilidades claras: una zona cruda, una limpia y un almacén desde el que consumen el índice y el entrenamiento.",
            "diagram": ("stack", ["Fuentes", "Zona cruda", "Limpieza", "Almacén", "Consumo"]),
            "caption": "El dato avanza por capas. Cada una conserva la anterior y añade transformaciones reproducibles.",
            "sections": [
                {
                    "h": "Data lake, warehouse y documentos",
                    "p": [
                        "Un data lake guarda archivos en su formato original o en formatos abiertos como Parquet y JSON. Es barato y flexible, y sirve como archivo histórico. Un data warehouse organiza datos estructurados para consultas analíticas rápidas. MongoDB ocupa un espacio intermedio: guarda documentos con esquema flexible y permite consultas por campo y metadatos.",
                        "En este curso, MongoDB actúa como almacén operativo de documentos y metadatos; S3 guarda artefactos, versiones y copias; el índice vectorial vive en Qdrant. No es una arquitectura única para todos los casos, pero cubre las necesidades del gemelo sin introducir un lago de datos completo antes de necesitarlo.",
                        "La clave es que cada capa tenga un contrato. La cruda conserva lo que llegó; la limpia garantiza campos y tipos; la de consumo ofrece lo que necesitan el indexador y el generador de datasets. Si una capa mezcla responsabilidades, cualquier cambio se propaga de forma impredecible.",
                    ],
                },
                {
                    "h": "ETL, ELT y cambios incrementales",
                    "p": [
                        "ETL transforma antes de cargar; ELT carga primero y transforma dentro del almacén. Para un corpus pequeño, la diferencia es filosófica; para uno grande, afecta al coste y a la capacidad de reprocesar. Guardar el crudo y transformar después es una forma de ELT que facilita la auditoría.",
                        "Las actualizaciones incrementales evitan reprocesar todo. Se detectan por fecha de modificación, por hash o por un campo de versión. La captura de cambios —CDC— permite propagar inserciones, actualizaciones y borrados sin recorrer la colección entera. En MongoDB, los change streams ofrecen esa señal, aunque requieren un replica set.",
                        "El borrado es tan importante como la inserción. Si un autor elimina un artículo o pide que no se use, el sistema debe poder retirarlo del almacén, del índice y de los datasets de entrenamiento. Un pipeline que solo añade acumula contenido obsoleto y riesgos legales.",
                    ],
                },
                {
                    "h": "Linaje, particiones y reproducción",
                    "p": [
                        "El linaje responde a la pregunta «¿de dónde salió este dato y quién lo transformó?». Se implementa con identificadores de ejecución, versiones de código y registros de transformación. Sin linaje, un modelo con un comportamiento extraño es imposible de investigar.",
                        "Las particiones por fecha, fuente o idioma mejoran las consultas y permiten reprocesar solo una parte. También facilitan la retención: los datos antiguos pueden archivarse en S3 y los recientes quedan accesibles. La partición debe elegirse por el patrón de consulta real, no por una idea abstracta de orden.",
                        "La reproducción es la prueba final: ¿puedes reconstruir el corpus que alimentó un modelo concreto? Si la respuesta es sí, tienes un sistema de datos. Si depende de lo que quedó en una carpeta temporal, tienes una demo. La diferencia se nota el día en que hay que explicar una respuesta o volver a entrenar.",
                    ],
                },
            ],
            "brief": [
                "Capas cruda, limpia y de consumo con contratos",
                "Actualizaciones incrementales y borrados propagados",
                "Linaje, particiones y capacidad de reproducir",
            ],
            "keys": [
                "El data lake conserva archivos; el warehouse estructura consultas; MongoDB sirve documentos operativos.",
                "Guardar el crudo y transformar después facilita la auditoría y el reprocesamiento.",
                "CDC y los hashes permiten actualizar sin recorrer todo el corpus.",
                "El borrado debe propagarse al índice y a los datasets, no solo al almacén.",
            ],
            "example": "Un autor pide retirar dos artículos. El equipo marca los documentos como retirados en MongoDB, elimina sus chunks de Qdrant y regenera el dataset de instrucciones excluyéndolos. La siguiente versión del modelo ya no los contiene y la traza conserva el motivo del cambio.",
            "caution": "Un índice construido una vez y nunca reconciliado con el almacén acaba citando documentos que ya no existen. Programa una comprobación periódica de consistencia.",
            "search": "data lake data warehouse MongoDB S3 capas crudo limpio ETL ELT CDC change streams borrado linaje particiones reproducir corpus",
        },
    ],
    "quiz": {
        "id": "llm3q",
        "title": "Cierre del módulo 03",
        "summary": [
            "La recolección elige fuentes, respeta límites y guarda procedencia con idempotencia.",
            "La limpieza extrae contenido, normaliza, deduplica y enmascara datos sensibles.",
            "El corpus vive en capas con contratos: crudo, limpio y consumo.",
            "Linaje, particiones y borrados propagados hacen el sistema auditable y reproducible.",
        ],
        "questions": [
            {
                "q": "¿Por qué conviene guardar el HTML crudo antes de limpiarlo?",
                "options": [
                    "Porque ocupa menos que el texto limpio",
                    "Para poder reprocesar con un extractor mejor sin volver a descargar",
                    "Porque el modelo necesita el HTML para generar",
                    "Para evitar tener que deduplicar",
                ],
                "answer": 1,
                "why": "El crudo es la fuente de verdad; permite repetir la limpieza y comparar versiones del extractor.",
            },
            {
                "q": "¿Qué problema resuelve la deduplicación casi exacta?",
                "options": [
                    "Que el índice tenga varios idiomas",
                    "Que versiones con cambios menores inflen el corpus y sesguen el ajuste",
                    "Que el crawler respete robots.txt",
                    "Que MongoDB use menos colecciones",
                ],
                "answer": 1,
                "why": "Los casi duplicados desperdician espacio y sobre-representan contenido repetido en el entrenamiento y la recuperación.",
            },
            {
                "q": "Un autor pide retirar un artículo. ¿Qué debe ocurrir?",
                "options": [
                    "Solo borrarlo de la carpeta local",
                    "Borrarlo del almacén, del índice y de los datasets que lo usaron",
                    "Cambiar la URL por otra",
                    "Dejarlo pero añadir una nota en el prompt",
                ],
                "answer": 1,
                "why": "El borrado debe propagarse a todas las capas donde el contenido pueda aparecer en una respuesta o en un entrenamiento.",
            },
        ],
        "exercises": [
            "Diseña el esquema mínimo de un documento con campos obligatorios, metadatos de procedencia y hash.",
            "Escribe las reglas de un crawler para un blog con feed RSS y para un sitio sin feed, incluyendo reintentos y pausas.",
            "Propón cómo verificarías que el índice y el almacén siguen siendo consistentes después de un mes de cambios.",
        ],
        "search": "evaluación cierre recolección crawler limpieza deduplicación capas data lake warehouse linaje borrado reproducibilidad",
    },
}
