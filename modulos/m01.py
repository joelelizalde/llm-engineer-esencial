MODULE = {
    "num": "01",
    "title": "El gemelo digital",
    "sub": "Qué construimos, por qué y con qué arquitectura",
    "lessons": [
        {
            "id": "llm1l1",
            "lnum": 1,
            "title": "Qué es un LLM Twin y qué problema resuelve",
            "minutes": 6,
            "lead": "Un LLM Twin no es un chatbot que sabe de todo, sino un sistema que escribe y razona como una persona concreta porque se alimenta de su contenido. La diferencia entre esa promesa y un asistente genérico está menos en el modelo que en los datos, la recuperación y el producto que lo rodea.",
            "diagram": ("flow", ["Tu contenido", "Recuperación", "Modelo ajustado", "Tu voz"]),
            "caption": "El gemelo se construye de izquierda a derecha: primero el corpus, después el índice, luego el ajuste y por último el sistema que responde.",
            "sections": [
                {
                    "h": "Un gemelo, no un asistente genérico",
                    "p": [
                        "Un LLM Twin es una aplicación que imita la forma de escribir, los temas y el criterio de una persona. Para lograrlo se recopila su obra pública —artículos, notas, código, entrevistas—, se limpia y se indexa, se ajusta un modelo con ese material y se construye una interfaz que recupera fragmentos relevantes antes de responder. El modelo aporta lenguaje; el corpus aporta identidad.",
                        "La palabra «gemelo» invita a una expectativa equivocada: que el sistema será una copia exacta de la persona. No lo será. Un gemelo útil reproduce el estilo y la postura ante problemas conocidos, y falla cuando se le pide opinar sobre algo que esa persona nunca escribió. Reconocer ese límite es el primer paso para diseñar un producto honesto.",
                        "La utilidad aparece en tareas concretas: redactar un primer borrador con tu tono, responder preguntas sobre tu obra, generar documentación técnica con tus convenciones o preparar material de formación a partir de tus cursos. En todas ellas el valor está en reducir el tiempo hasta un borrador aceptable, no en sustituir el juicio final.",
                    ],
                },
                {
                    "h": "Por qué no basta con ChatGPT",
                    "p": [
                        "Un modelo general conoce mucho del mundo, pero no conoce tu archivo privado ni distingue cuál de tus artículos es reciente. Si le pides que escriba «como tú», improvisará un estilo plausible a partir de la descripción que le des. Un gemelo, en cambio, ha visto tus textos y puede citarlos; la diferencia se nota en los detalles: giros, ejemplos recurrentes, temas que evitas.",
                        "También hay razones de control. Un sistema propio permite decidir qué documentos entran, cómo se versionan, qué se registra y qué no sale del perímetro. Para una empresa, eso puede ser más importante que unos puntos de calidad en un benchmark. La pregunta correcta no es si el modelo general es mejor, sino si el sistema resuelve el problema con las restricciones reales.",
                        "Y hay una razón económica: un modelo pequeño ajustado con tus datos y apoyado en recuperación puede ser suficiente para tu dominio, con latencia y coste menores que enviar contextos enormes a un modelo de frontera en cada petición. Esa combinación —modelo especializado más recuperación— es el corazón del curso.",
                    ],
                },
                {
                    "h": "Definir el MVP antes de escribir código",
                    "p": [
                        "El libro propone empezar por un producto mínimo viable: la versión más pequeña que entrega valor y permite aprender. Para el gemelo, el MVP puede ser un asistente que responde preguntas sobre un conjunto cerrado de artículos y devuelve siempre la fuente. No incluye agentes autónomos, ni múltiples usuarios, ni una interfaz perfecta. Incluye un corpus, un índice, un modelo y una forma de evaluar.",
                        "Ese recorte tiene consecuencias técnicas. Si el MVP solo responde sobre artículos, el esquema de documentos puede ser sencillo y la recuperación se limita a una colección. Si además debe escribir con tu estilo, hace falta ajuste fino. Si debe citar, el índice necesita metadatos y el prompt debe exigir referencias verificables. Cada requisito del producto se traduce en una pieza del sistema.",
                        "El error más caro es construir primero la infraestructura y definir el producto al final. Un pipeline elegante para un caso que nadie usa es deuda técnica disfrazada de ingeniería. Escribe en una página qué pregunta responde el sistema, con qué datos, con qué latencia y cómo sabrás que funciona. Esa página guiará todas las decisiones siguientes.",
                    ],
                },
            ],
            "brief": [
                "El gemelo imita estilo y criterio, no omnisciencia",
                "El corpus y la recuperación aportan lo que el modelo no sabe",
                "El MVP fija alcance, datos, latencia y evaluación",
            ],
            "keys": [
                "Un LLM Twin combina un modelo ajustado con un corpus propio indexado y recuperable.",
                "El valor está en acelerar borradores y respuestas sobre un dominio concreto, no en clonar a una persona.",
                "El control sobre datos, permisos y registro puede pesar más que la calidad bruta del modelo.",
                "Definir el MVP antes de programar evita construir infraestructura para un caso que nadie necesita.",
            ],
            "example": "Una consultora independiente quiere un asistente que redacte propuestas con su tono. El MVP ingiere sus 40 propuestas anteriores, las indexa por servicio y sector, recupera las tres más parecidas y pide al modelo un borrador que cite esos documentos. No necesita ajuste fino para la primera versión: necesita recuperación y una plantilla de prompt bien diseñada.",
            "caution": "Prometer un «clon digital» que responde cualquier pregunta lleva a decepción y a riesgos legales. Delimita el alcance, muestra las fuentes y deja claro cuándo el sistema no sabe.",
            "search": "LLM Twin gemelo digital corpus recuperación estilo criterio MVP producto mínimo viable ChatGPT control datos privados coste latencia",
        },
        {
            "id": "llm1l2",
            "lnum": 2,
            "title": "Los tres pipelines: feature, training e inference",
            "minutes": 7,
            "lead": "La mayoría de los sistemas de machine learning no fallan por el algoritmo, sino por la fontanería: datos que se transforman de una forma al entrenar y de otra al servir, experimentos que nadie puede reproducir y modelos que no se pueden volver a entrenar. La arquitectura FTI existe para separar esas responsabilidades sin perder el hilo.",
            "diagram": ("stack", ["Fuentes de datos", "Feature pipeline", "Almacén de features", "Training pipeline", "Inference pipeline"]),
            "caption": "Los tres pipelines comparten contratos de datos. El almacén de features es la frontera entre lo que se entrena y lo que se sirve.",
            "sections": [
                {
                    "h": "El problema de los sistemas ad hoc",
                    "p": [
                        "Un cuaderno que descarga datos, entrena y muestra una gráfica es perfecto para explorar y terrible para operar. Cuando hay que reentrenar, nadie recuerda qué filtro se aplicó; cuando hay que servir, alguien reescribe la limpieza en otro lenguaje y aparecen diferencias sutiles. Ese fenómeno se llama desajuste entre entrenamiento y servicio, y es una fuente silenciosa de degradación.",
                        "El problema se agrava con los LLM porque hay más piezas móviles: corpus, chunking, embeddings, índice vectorial, modelo base, adaptadores, prompt. Si cada una vive en un script distinto, reproducir una versión es una excavación arqueológica. La arquitectura no elimina la complejidad; la hace visible y repetible.",
                        "La solución no es un framework mágico, sino un contrato: cada etapa recibe entradas definidas y produce salidas versionadas. Así se puede probar por separado, reemplazar una pieza y volver atrás cuando algo empeora.",
                    ],
                },
                {
                    "h": "Feature, training e inference",
                    "p": [
                        "El pipeline de features transforma datos crudos en features útiles. En un sistema clásico pueden ser columnas de un dataframe; en un sistema RAG son documentos limpios, chunks y embeddings almacenados en una base vectorial. Puede ejecutarse por lotes, de forma incremental o en streaming, y su salida debe ser la misma que verá el modelo en producción.",
                        "El pipeline de entrenamiento toma esas features, construye el dataset de instrucciones o de preferencias, entrena o ajusta el modelo, lo evalúa y lo registra. No debería ocuparse de descargar datos ni de servir peticiones. Su producto es un artefacto con métricas, configuración y linaje: qué datos, qué hiperparámetros y qué versión del código lo produjeron.",
                        "El pipeline de inferencia atiende cada petición. Recibe la pregunta, la transforma con el mismo tokenizador y el mismo modelo de embeddings que se usaron para indexar, recupera contexto, arma el prompt, genera y devuelve la respuesta. También registra trazas y aplica filtros. Su contrato con los otros dos pipelines es el esquema de datos y las versiones de los artefactos.",
                    ],
                },
                {
                    "h": "Por qué separarlas compensa",
                    "p": [
                        "Separar permite escalar cada parte según su carga. La indexación puede correr en lote durante la noche; la inferencia necesita responder en segundos y escalar con el tráfico. También permite reemplazar el modelo sin tocar la recolección de datos, o cambiar el chunking y reindexar sin reentrenar. Esa independencia es lo que hace mantenible un sistema que cambia cada mes.",
                        "La separación mejora la depuración. Si una respuesta es mala, se puede comprobar si el documento correcto estaba en el corpus, si se recuperó, si el prompt lo incluyó y si el modelo lo usó. Sin pipelines separados, todo es una caja negra. Con ellas, cada fallo tiene una etapa sospechosa.",
                        "El coste es cierta ceremonia: definir esquemas, versionar artefactos y orquestar pasos. Para un prototipo de una tarde puede ser excesivo. Para un sistema que alguien va a usar durante meses, es la diferencia entre iterar y reconstruir.",
                    ],
                },
            ],
            "brief": [
                "Features, entrenamiento e inferencia tienen contratos distintos",
                "El desajuste entre entrenar y servir degrada en silencio",
                "Separar permite escalar, reemplazar y depurar por partes",
            ],
            "keys": [
                "El pipeline de features produce los datos transformados que verán entrenamiento e inferencia.",
                "El pipeline de entrenamiento produce un modelo evaluado, versionado y con linaje.",
                "El pipeline de inferencia reutiliza las mismas transformaciones y artefactos que el entrenamiento.",
                "La separación añade ceremonia, pero reduce el desajuste y hace posible la depuración.",
            ],
            "example": "Un equipo cambia el modelo de embeddings para mejorar la recuperación. Con FTI, reindexa la colección y evalúa el pipeline de inferencia sin volver a entrenar el modelo generativo. Sin esa separación, el cambio obligaría a reconstruir todo el sistema y a repetir experimentos que ya estaban resueltos.",
            "caution": "Tres pipelines no significan tres repositorios inconexos. Si los esquemas y las versiones no están documentados, la separación solo reparte el desorden.",
            "search": "FTI feature pipeline training pipeline inference pipeline desajuste entrenamiento servicio reproducibilidad artefactos linaje escalar depurar",
        },
        {
            "id": "llm1l3",
            "lnum": 3,
            "title": "La arquitectura del LLM Twin de principio a fin",
            "minutes": 7,
            "lead": "Con el concepto y los pipelines claros, falta el mapa físico: qué servicios intervienen, qué datos viajan entre ellos y dónde se rompe el sistema cuando algo falla. Este recorrido es también el índice del curso: cada módulo profundiza en una casilla de este diagrama.",
            "diagram": ("stack", ["Recolección", "Limpieza y chunking", "Embeddings y Qdrant", "Ajuste fino y evaluación", "RAG, API y monitoreo"]),
            "caption": "Arquitectura de referencia del curso. Cada capa puede ejecutarse por separado y se comunica mediante artefactos versionados.",
            "sections": [
                {
                    "h": "Del mundo exterior al corpus",
                    "p": [
                        "La recolección obtiene documentos de fuentes como Medium, Substack, GitHub o LinkedIn, además de feeds RSS y APIs. Un crawler descubre enlaces, descarga el HTML, respeta los límites de cada sitio y guarda el resultado con metadatos: URL, fecha, autor, idioma y origen. La salida no es un texto limpio, sino un documento crudo con procedencia.",
                        "La limpieza convierte HTML en texto útil: elimina navegación, anuncios y comentarios; conserva bloques de código y encabezados; normaliza espacios y codificación. Después deduplica, detecta el idioma y valida el esquema. El resultado se guarda en MongoDB, que actúa como almacén de documentos y permite consultar por metadatos antes de pasar a la siguiente etapa.",
                        "Separar crudo y limpio permite reprocesar. Si mañana mejora el extractor, se vuelve a ejecutar sobre los documentos originales sin volver a descargar el sitio. Esa capacidad de repetición vale más que cualquier optimización prematura.",
                    ],
                },
                {
                    "h": "Del corpus al modelo",
                    "p": [
                        "El pipeline de features divide cada documento en chunks, calcula embeddings y los inserta en Qdrant con un payload que incluye el identificador del documento, la URL, el autor y la fecha. Esa colección es la memoria del sistema: lo que el modelo podrá consultar en tiempo de inferencia. El chunking y el modelo de embeddings deben versionarse junto con el índice.",
                        "El pipeline de entrenamiento construye un dataset de instrucciones a partir de los documentos, ajusta un modelo base con SFT y, si hay datos de preferencias, continúa con DPO. Después evalúa con un conjunto reservado y registra el adaptador y sus métricas. El modelo no se entrena con todo el corpus: se entrena con ejemplos derivados y se apoya en la recuperación para los hechos.",
                        "La evaluación es una etapa, no un informe final. Cada versión del modelo, del prompt y del índice se compara contra un golden dataset. Si la calidad baja, se sabe qué cambió. Sin esa disciplina, cada mejora es una apuesta.",
                    ],
                },
                {
                    "h": "Del modelo al producto",
                    "p": [
                        "El pipeline de inferencia recibe la pregunta, la convierte en embedding, recupera los chunks más relevantes, aplica filtros por autor o fecha, arma el prompt con instrucciones y citas, y llama al modelo. La respuesta se devuelve con las fuentes y se registra la traza: qué se recuperó, qué prompt se envió, cuántos tokens costó y cuánto tardó.",
                        "El despliegue empaqueta ese flujo en un servicio HTTP con Docker y lo publica en un endpoint de SageMaker o en un contenedor equivalente. Un pipeline de CI/CD prueba, construye la imagen y despliega; el monitoreo vigila latencia, errores, coste y calidad. La infraestructura se declara como código para que el entorno sea reproducible.",
                        "El ciclo se cierra con LLMOps: se recogen señales de uso, se revisan respuestas fallidas, se actualizan prompts y datos, y se vuelve a evaluar. El gemelo no está «terminado»: se mantiene. La arquitectura del curso está pensada para que ese mantenimiento sea aburrido, que es la mejor señal de que funciona.",
                    ],
                },
            ],
            "brief": [
                "Recolectar, limpiar y almacenar con procedencia",
                "Indexar para recuperar; entrenar para el estilo",
                "Servir con trazas, evaluación y despliegue reproducible",
            ],
            "keys": [
                "El corpus crudo se conserva para poder reprocesar sin volver a descargar.",
                "Qdrant guarda chunks y metadatos; el payload permite filtrar y citar.",
                "El ajuste fino aporta estilo y formato; la recuperación aporta hechos y actualidad.",
                "El sistema se completa con despliegue, observabilidad y un ciclo de mejora continua.",
            ],
            "example": "Cuando un usuario pregunta «¿qué opinas del RAG multi-modelo?», la inferencia recupera dos artículos donde la autora lo trata, filtra por fecha para no citar una versión obsoleta, construye un prompt que exige referencias y devuelve una respuesta con enlaces. La traza permite comprobar que el documento correcto estaba entre los recuperados.",
            "caution": "Un diagrama bonito no garantiza un sistema fiable. Si no se versionan el índice, el prompt y el modelo a la vez, reproducir una respuesta será imposible.",
            "search": "arquitectura LLM Twin recolección limpieza MongoDB chunking Qdrant embeddings SFT DPO evaluación inferencia RAG despliegue SageMaker monitoreo LLMOps",
        },
    ],
    "quiz": {
        "id": "llm1q",
        "title": "Cierre del módulo 01",
        "summary": [
            "Un LLM Twin imita el estilo y el criterio de una persona a partir de su corpus, no es un oráculo universal.",
            "La arquitectura FTI separa features, entrenamiento e inferencia con contratos y artefactos versionados.",
            "El recorrido del sistema va de la recolección al corpus limpio, del índice al modelo y del modelo al servicio.",
            "La reproducibilidad y la evaluación acompañan al sistema durante toda su vida útil.",
        ],
        "questions": [
            {
                "q": "¿Qué aporta principalmente la recuperación de documentos a un LLM Twin?",
                "options": [
                    "Aumenta el número de parámetros del modelo",
                    "Aporta hechos y citas que el modelo no memorizó",
                    "Sustituye por completo al ajuste fino",
                    "Elimina la necesidad de evaluar las respuestas",
                ],
                "answer": 1,
                "why": "La recuperación inserta fragmentos del corpus en el contexto; así el sistema puede apoyarse en datos actuales y citarlos.",
            },
            {
                "q": "¿Cuál es el síntoma típico de no separar los pipelines de entrenamiento e inferencia?",
                "options": [
                    "El modelo tarda más en descargarse",
                    "Las transformaciones difieren y el rendimiento cae en producción",
                    "El repositorio tiene demasiados archivos",
                    "El índice vectorial se vuelve más pequeño",
                ],
                "answer": 1,
                "why": "El desajuste entre entrenamiento y servicio hace que el modelo reciba datos con otra distribución o formato del que aprendió.",
            },
            {
                "q": "¿Para qué sirve conservar el documento crudo además del limpio?",
                "options": [
                    "Para ocupar más espacio en disco",
                    "Para poder reprocesar con un extractor o un esquema mejor",
                    "Para entrenar directamente sin limpieza",
                    "Para evitar versionar el índice",
                ],
                "answer": 1,
                "why": "El crudo es la fuente de verdad: permite repetir la limpieza y comparar resultados sin volver a rastrear la web.",
            },
        ],
        "exercises": [
            "Escribe en una página el MVP de tu propio gemelo: qué responde, con qué datos, con qué latencia y cómo sabrás que funciona.",
            "Dibuja los tres pipelines FTI para ese MVP e indica qué artefacto produce cada una y quién lo consume.",
            "Elige una respuesta mala que hayas visto de un asistente y localiza en qué etapa del recorrido pudo originarse.",
        ],
        "search": "evaluación cierre LLM Twin FTI MVP corpus recuperación índice entrenamiento inferencia reproducibilidad arquitectura",
    },
}
