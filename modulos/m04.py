MODULE = {
    "num": "04",
    "title": "Pipeline de features RAG",
    "sub": "Chunking, embeddings, Qdrant e indexación",
    "lessons": [
        {
            "id": "llm4l1",
            "lnum": 1,
            "title": "RAG sin mitos: qué resuelve y qué no",
            "minutes": 7,
            "lead": "RAG se ha convertido en la respuesta universal a cualquier problema con LLM. Bien usado, conecta el modelo con conocimiento privado y actual; mal usado, es un buscador mediocre delante de un generador que ignora lo que encuentra. Entender el mecanismo es lo que separa una demo de un sistema.",
            "diagram": ("flow", ["Pregunta", "Recuperar", "Prompt", "Respuesta"]),
            "caption": "RAG no entrena al modelo: en cada petición recupera contexto y lo inserta en el prompt antes de generar.",
            "sections": [
                {
                    "h": "Qué es y qué no es RAG",
                    "p": [
                        "La generación aumentada por recuperación consiste en buscar documentos relevantes para una consulta y añadirlos al contexto del modelo. El modelo sigue siendo el mismo; lo que cambia es la información que ve en el momento de responder. Por eso RAG puede citar fuentes y hablar de datos que no estaban en su entrenamiento.",
                        "RAG no añade conocimiento a los pesos ni garantiza que el modelo use el contexto. Tampoco sustituye al ajuste fino: si el problema es el formato, el tono o la obediencia a instrucciones, recuperar más documentos no lo arregla. La división práctica es: recuperación para hechos y actualidad, ajuste para comportamiento y estilo.",
                        "Un sistema RAG tiene dos evaluaciones distintas. La de recuperación pregunta si los documentos correctos aparecen entre los primeros. La de generación pregunta si la respuesta usa esos documentos y no inventa. Confundirlas lleva a culpar al modelo de un fallo de índice o al índice de un fallo de prompt.",
                    ],
                },
                {
                    "h": "El recorrido de una petición",
                    "p": [
                        "La pregunta se normaliza y, a veces, se reescribe para mejorar la búsqueda. Se calcula su embedding con el mismo modelo que se usó para indexar. Se consulta la base vectorial con un límite de resultados y filtros de metadatos. Los documentos recuperados se ordenan, se recortan y se insertan en una plantilla junto con la pregunta y las instrucciones.",
                        "El prompt resultante es más largo que la pregunta original, y eso afecta a coste y latencia. También introduce un riesgo: si el contexto contiene instrucciones maliciosas o texto irrelevante, el modelo puede seguirlas o distraerse. Los sistemas maduros delimitan el contexto, etiquetan las fuentes y piden al modelo que ignore instrucciones dentro de los documentos.",
                        "La respuesta se posprocesa: se comprueban citas, se eliminan formatos roto, se aplican filtros. En un producto real, también se registra qué se recuperó y qué se respondió. Sin esa traza, mejorar el sistema es adivinar.",
                    ],
                },
                {
                    "h": "RAG avanzado: cuándo añadir complejidad",
                    "p": [
                        "El RAG básico falla por tres motivos: la consulta no expresa lo que el usuario quiere, el chunk no contiene la respuesta o el ranking prioriza documentos parecidos pero inútiles. Cada fallo tiene una técnica. La reescritura de consultas y la expansión ayudan con el primero; el chunking consciente de estructura con el segundo; el reranking y la búsqueda híbrida con el tercero.",
                        "La búsqueda híbrida combina similitud densa con coincidencia léxica. Es útil cuando hay nombres propios, códigos o términos raros que los embeddings difuminan. El reranking aplica un cross-encoder que lee pregunta y documento juntos y puntúa la relevancia con más precisión; es más caro, así que se usa sobre un conjunto pequeño ya recuperado.",
                        "Cada añadido tiene coste de latencia, complejidad y evaluación. La regla es añadir una técnica solo cuando una métrica de recuperación muestra el fallo que esa técnica corrige. Un pipeline con diez mejoras sin medición es más frágil que uno simple que se entiende.",
                    ],
                },
            ],
            "brief": [
                "RAG recupera contexto; no entrena ni garantiza uso",
                "Recuperación y generación se evalúan por separado",
                "Añade reescritura, híbrida o reranking solo con evidencia",
            ],
            "keys": [
                "RAG inserta documentos en el prompt; el modelo y sus pesos no cambian.",
                "La recuperación aporta hechos y citas; el ajuste fino aporta formato y comportamiento.",
                "La calidad de recuperación se mide con recall y ranking; la de generación, con fidelidad y relevancia.",
                "La complejidad de RAG avanzado se justifica por métricas, no por moda.",
            ],
            "example": "Un asistente interno responde sobre políticas de empresa. La pregunta «¿cuántos días de vacaciones tengo?» recupera tres fragmentos: uno de 2021, uno de 2024 y otro de un país distinto. El filtro por país y fecha, más un reranking, deja el fragmento correcto. Sin esos filtros, el modelo responde con la política equivocada y con total seguridad.",
            "caution": "Meter todos los documentos recuperados en el prompt no mejora la respuesta: diluye la señal, encarece la petición y aumenta el riesgo de que el modelo cite lo irrelevante.",
            "search": "RAG recuperación generación aumentada conocimiento privado citas reescritura consulta búsqueda híbrida reranking cross-encoder evaluación recuperación",
        },
        {
            "id": "llm4l2",
            "lnum": 2,
            "title": "Chunking y embeddings con criterio",
            "minutes": 7,
            "lead": "El chunk es la unidad de memoria del sistema. Si es demasiado grande, contiene la respuesta pero también mucho ruido; si es demasiado pequeño, pierde el contexto que le da sentido. El embedding, por su parte, decide qué significa «parecido». Ambas decisiones se toman juntas y se evalúan juntas.",
            "diagram": ("stack", ["Documento", "Chunks con solapamiento", "Embeddings", "Colección"]),
            "caption": "El documento se divide, cada chunk se convierte en un vector y la colección conserva vector más metadatos.",
            "sections": [
                {
                    "h": "Estrategias de chunking",
                    "p": [
                        "El chunking fijo corta cada N tokens con un solapamiento para no perder frases en la frontera. Es simple y reproducible, pero parte tablas, listas y argumentos por la mitad. El chunking por estructura respeta encabezados, párrafos y bloques de código; suele producir fragmentos más coherentes y mejores citas.",
                        "El chunking semántico agrupa oraciones por similitud hasta alcanzar un tamaño objetivo. Puede mejorar la coherencia, pero es más caro y menos predecible. Para código, conviene cortar por funciones o clases; para documentación, por secciones; para transcripciones, por turnos. No hay una estrategia universal: hay una estrategia adecuada al documento y a la pregunta.",
                        "El tamaño se elige con evaluación. Chunks de 300 a 600 tokens suelen funcionar bien en prosa técnica; para preguntas que necesitan varios párrafos, conviene recuperar más chunks o usar un resumen jerárquico. El solapamiento ayuda a la continuidad, pero duplica contenido y aumenta el índice. Mide el recall antes de duplicar por duplicar.",
                    ],
                },
                {
                    "h": "Modelos de embeddings",
                    "p": [
                        "Un embedding es un vector que representa el significado de un texto. Los modelos de embeddings se entrenan para acercar textos relacionados y alejar los no relacionados. La dimensión, el idioma, la longitud máxima de entrada y el dominio importan. Un modelo entrenado en inglés puede funcionar en español, pero uno multilingüe suele ser mejor elección.",
                        "La comparación se hace con similitud del coseno si los vectores están normalizados. Normalizar evita que la magnitud del vector domine el ranking. También conviene usar el mismo modelo, la misma versión y la misma instrucción de prefijo para indexar y para consultar; mezclar versiones produce vectores incompatibles.",
                        "El coste del embedding es mucho menor que el de la generación, pero no es gratis. Indexar un corpus grande exige lotes, reintentos y control de límites. Para modelos locales, la GPU o la CPU marcan el ritmo; para APIs, la cuota y la latencia. Calcula el coste antes de indexar y guárdalo junto con la versión del modelo.",
                    ],
                },
                {
                    "h": "Evaluar antes de escalar",
                    "p": [
                        "La métrica básica de recuperación es recall@k: qué proporción de las preguntas tiene su documento relevante entre los k primeros. También se usa MRR, que premia que el documento correcto aparezca pronto, y nDCG, que considera el orden y los grados de relevancia. Para empezar, un conjunto de cincuenta preguntas con su documento correcto ya revela mucho.",
                        "Ese conjunto debe incluir preguntas fáciles, difíciles y ambiguas, y preguntas cuya respuesta no está en el corpus. Las últimas son esenciales: un sistema que siempre recupera algo parece funcionar hasta que inventa una respuesta sobre un tema inexistente. La abstención también se evalúa.",
                        "Compara configuraciones con el mismo conjunto: tamaños de chunk, solapamientos, modelos de embeddings, con y sin filtros. Registra los resultados. La mejora que no se mide es solo una preferencia estética.",
                    ],
                },
            ],
            "brief": [
                "El chunk debe contener la respuesta sin diluirla",
                "El embedding fija qué significa «parecido»",
                "Recall@k y un conjunto de preguntas guían la decisión",
            ],
            "keys": [
                "El chunking por estructura suele superar al corte fijo en documentos con encabezados y código.",
                "Tamaño y solapamiento se eligen con evaluación, no con una receta universal.",
                "Indexar y consultar deben usar el mismo modelo, versión y normalización.",
                "Un conjunto de evaluación debe incluir preguntas sin respuesta en el corpus.",
            ],
            "example": "Un corpus de tutoriales mezcla prosa y bloques de código. Con chunks fijos de 500 tokens, muchas funciones quedan partidas. Al cortar por sección y por bloque de código, el recall@5 sube y las respuestas citan ejemplos completos. El tamaño medio baja, pero la calidad sube.",
            "caution": "Cambiar el modelo de embeddings sin reindexar deja vectores de espacios distintos en la misma colección. La búsqueda devuelve resultados aparentemente aleatorios.",
            "search": "chunking fijo semántico estructura solapamiento tamaño tokens embeddings dimensión multilingüe normalización coseno recall@k MRR nDCG evaluación",
        },
        {
            "id": "llm4l3",
            "lnum": 3,
            "title": "Qdrant, metadatos e indexación incremental",
            "minutes": 7,
            "lead": "Una colección vectorial no es una carpeta donde se tiran vectores. Es un índice con esquema, versión y ciclo de vida. La diferencia entre un prototipo y un sistema aparece cuando hay que actualizar un documento, filtrar por fecha o reconstruir el índice sin apagar el servicio.",
            "diagram": ("stack", ["Chunks", "Embeddings", "Colección Qdrant", "Filtros y payload", "Resultados citables"]),
            "caption": "La colección conserva el vector y el payload. Los filtros y la cita se resuelven sin volver al documento original.",
            "sections": [
                {
                    "h": "Diseñar la colección",
                    "p": [
                        "Cada colección se define por la dimensión del vector y la métrica de distancia. También por los índices de payload que se van a usar en filtros. Un índice mal elegido obliga a recrear la colección, y recrear significa recalcular todos los embeddings o migrarlos. Diseña el esquema de metadatos antes de insertar el primer punto.",
                        "El identificador del punto debe ser estable y derivado del documento y del chunk, por ejemplo un hash de la URL más la posición. Así una reindexación actualiza en lugar de duplicar. El payload incluye doc_id, url, título, autor, fecha, sección, idioma y versión del chunker. Esos campos permiten filtrar, citar y auditar.",
                        "La búsqueda puede ser exacta o aproximada. HNSW es el índice por defecto para colecciones grandes; sus parámetros equilibran recall y latencia. Para un corpus pequeño, la búsqueda exacta es más simple y no pierde recall. Mide antes de optimizar: la latencia de un índice aproximado mal ajustado puede ser peor que la de uno exacto bien dimensionado.",
                    ],
                },
                {
                    "h": "Indexación incremental y versionado",
                    "p": [
                        "La indexación completa es fácil de razonar y cara de ejecutar. La incremental procesa solo documentos nuevos o modificados. Para lograrlo necesitas una marca de versión por documento y un registro de qué chunks se insertaron. Cuando un documento cambia, se borran sus puntos anteriores y se insertan los nuevos en una operación idempotente.",
                        "El versionado del índice incluye el modelo de embeddings, el tamaño de chunk, el solapamiento y la versión del código. Si cambia cualquiera de esos, el índice anterior deja de ser comparable. Una práctica útil es crear una colección nueva, indexar en paralelo, evaluar y cambiar el alias de lectura cuando la nueva versión supera a la anterior.",
                        "El cambio de alias permite volver atrás sin reindexar. También permite comparar dos índices con el mismo conjunto de preguntas. Sin esa capacidad, cada mejora del chunking se convierte en un salto de fe.",
                    ],
                },
                {
                    "h": "Indexar código, tablas y documentos largos",
                    "p": [
                        "El código no se comporta como la prosa. Conviene cortar por funciones, clases o bloques completos, conservar el nombre del archivo y el lenguaje en el payload, y no separar una firma de su cuerpo. Un chunk que empieza a mitad de una función pierde las variables y el contexto que explican qué hace. Para repositorios grandes, indexa también el README y los ejemplos de uso: suelen responder mejor las preguntas de «cómo se usa».",
                        "Las tablas y los documentos largos necesitan otra estrategia. Una tabla partida en filas sueltas pierde la cabecera y el significado de cada columna; es mejor conservar la tabla completa o convertirla en una representación con encabezados repetidos. En informes extensos, la recuperación padre-hijo funciona bien: se buscan fragmentos pequeños, pero se entrega al modelo la sección que los contiene.",
                        "La evaluación debe separar tipos de documento. Un tamaño de chunk que mejora los artículos puede empeorar el código o las tablas. Mide recall y calidad de respuesta por categoría antes de fijar una configuración global; si las diferencias son grandes, usa estrategias distintas por colección o por campo de payload.",
                    ],
                },
            ],
            "brief": [
                "Diseña dimensión, distancia y payload antes de indexar",
                "Indexa de forma incremental e idempotente",
                "Adapta el chunking al tipo de documento, no al revés",
            ],
            "keys": [
                "El id del punto debe derivarse del documento y del chunk para permitir actualizaciones limpias.",
                "El payload convierte la búsqueda en algo filtrable, citable y auditable.",
                "Una colección nueva con alias permite evaluar y volver atrás sin reindexar dos veces.",
                "Código, tablas y documentos largos piden estrategias de corte distintas.",
            ],
            "example": "Un equipo reindexa con un modelo multilingüe nuevo. Crea la colección articulos_v2, indexa en paralelo, evalúa con las mismas cien preguntas y comprueba que el recall@5 sube de 0,71 a 0,84. Solo entonces cambia el alias de lectura. Si hubiera empeorado, habría vuelto al índice anterior en un minuto.",
            "caution": "Borrar y recrear la colección en producción sin alias ni copia de seguridad deja el servicio sin recuperación durante toda la indexación.",
            "search": "Qdrant colección dimensión distancia payload índices HNSW búsqueda exacta incremental versionado alias código tablas documentos largos recuperación padre-hijo",
        },
    ],
    "quiz": {
        "id": "llm4q",
        "title": "Cierre del módulo 04",
        "summary": [
            "RAG recupera contexto y lo inserta en el prompt; no modifica los pesos del modelo.",
            "El chunking y el modelo de embeddings se eligen con evaluación de recuperación.",
            "Qdrant organiza vectores con payload, filtros y un ciclo de vida versionado.",
            "La indexación incremental y los alias permiten actualizar sin romper el servicio.",
        ],
        "questions": [
            {
                "q": "¿Qué mide recall@k en un sistema RAG?",
                "options": [
                    "La probabilidad de que el modelo alucine",
                    "La proporción de preguntas cuyo documento relevante aparece entre los k primeros",
                    "El número de tokens que consume el prompt",
                    "La velocidad de la base vectorial",
                ],
                "answer": 1,
                "why": "Recall@k evalúa la recuperación: si el documento correcto está entre los k resultados devueltos.",
            },
            {
                "q": "¿Qué ocurre si se indexa con un modelo de embeddings y se consulta con otro?",
                "options": [
                    "La búsqueda mejora porque se combinan espacios",
                    "Los vectores son incompatibles y el ranking pierde sentido",
                    "Qdrant cambia la dimensión automáticamente",
                    "El payload se actualiza solo",
                ],
                "answer": 1,
                "why": "Cada modelo define su propio espacio vectorial; mezclar versiones invalida la similitud entre consulta y documentos.",
            },
            {
                "q": "¿Cuál es la ventaja de una colección nueva con alias sobre borrar y recrear la existente?",
                "options": [
                    "Ocupa menos memoria",
                    "Permite evaluar la nueva versión y volver atrás sin dejar el servicio sin índice",
                    "Evita tener que calcular embeddings",
                    "Hace que el chunking sea innecesario",
                ],
                "answer": 1,
                "why": "La colección nueva se construye en paralelo; el alias cambia cuando la evaluación confirma la mejora, y volver atrás es inmediato.",
            },
        ],
        "exercises": [
            "Diseña dos estrategias de chunking para un corpus mixto de artículos y código, y explica qué documento partiría cada una.",
            "Escribe el payload mínimo de un chunk para citar la fuente y filtrar por autor y fecha.",
            "Prepara diez preguntas de evaluación, incluyendo dos cuya respuesta no esté en el corpus, y define qué esperarías del sistema.",
        ],
        "search": "evaluación cierre RAG chunking embeddings Qdrant payload recall@k indexación incremental alias tipos de documento",
    },
}
