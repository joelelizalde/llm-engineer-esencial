MODULE = {
    "num": "07",
    "title": "RAG en producción",
    "sub": "Inferencia, despliegue y LLMOps",
    "lessons": [
        {
            "id": "llm7l1",
            "lnum": 1,
            "title": "El pipeline de inferencia RAG",
            "minutes": 7,
            "lead": "En producción, la pregunta del usuario recorre seis o siete etapas antes de convertirse en respuesta. Cada una puede mejorar o arruinar el resultado, y cada una añade latencia. Diseñar el pipeline es decidir qué se hace siempre, qué se hace a veces y qué se evita para no gastar el presupuesto en tokens innecesarios.",
            "diagram": ("flow", ["Pregunta", "Contexto", "Generación", "Respuesta citada"]),
            "caption": "La respuesta final depende de la recuperación, del prompt y del posprocesamiento, no solo del modelo.",
            "sections": [
                {
                    "h": "De la pregunta al contexto",
                    "p": [
                        "El pipeline empieza por normalizar la pregunta: limpiar espacios, detectar idioma y, si el producto lo permite, resolver referencias a turnos anteriores. En una conversación, «¿y eso cuánto cuesta?» no significa nada sin el historial. La reescritura de la consulta convierte esa dependencia en una pregunta autónoma antes de buscar.",
                        "La búsqueda usa el mismo modelo de embeddings que el índice y aplica filtros de metadatos: autor, fecha, tipo de documento o permisos del usuario. Los permisos son críticos: un empleado no debe recuperar documentos de otro departamento. El filtrado debe ocurrir en la base vectorial o antes de insertar el contexto, nunca después de generar.",
                        "Los resultados se ordenan, se deduplican y se recortan. Si varios chunks pertenecen al mismo documento, conviene agruparlos para no repetir la misma fuente. Un límite de tokens para el contexto evita que la petición crezca sin control y deja espacio para la respuesta.",
                    ],
                },
                {
                    "h": "Del contexto a la respuesta",
                    "p": [
                        "La plantilla de prompt tiene cuatro partes: instrucciones de sistema, contexto delimitado, pregunta del usuario y formato de salida. Las instrucciones deben decir qué hacer cuando el contexto no alcanza —abstenerse o pedir aclaración— y cómo citar. El contexto se etiqueta con identificadores para que el modelo pueda referenciarlos.",
                        "La generación se controla con temperatura, límite de tokens y, si el proveedor lo permite, formato estructurado. Para respuestas factuales, una temperatura baja reduce variabilidad. Para redacción creativa, una temperatura algo mayor produce textos menos rígidos. La elección se evalúa, no se hereda de un tutorial.",
                        "El posprocesamiento verifica que las citas existen, elimina secciones vacías y aplica guardrails: filtros de contenido, comprobaciones de PII y límites de tema. También puede añadir enlaces y un aviso de que la respuesta se generó con asistencia. La respuesta debe poder auditarse: qué se recuperó, qué se envió y qué se devolvió.",
                    ],
                },
                {
                    "h": "Caché, streaming y degradación",
                    "p": [
                        "La caché semántica reutiliza respuestas cuando una pregunta nueva es muy parecida a una anterior. Ahorra latencia y coste, pero puede devolver una respuesta desactualizada o de otro usuario. Se aplica con cuidado: misma intención, mismos permisos y una ventana de validez. Para datos que cambian, es mejor cachear el contexto recuperado que la respuesta completa.",
                        "El streaming envía la respuesta por partes mientras se genera. Mejora la percepción de velocidad, aunque el tiempo total sea el mismo. Obliga a manejar cortes, errores a mitad de respuesta y posprocesamiento incremental. No todos los guardrails pueden aplicarse token a token; algunos requieren la respuesta completa.",
                        "Todo sistema necesita degradación elegante. Si el índice no responde, se puede responder con el modelo sin RAG y avisar de que no hay fuentes. Si el modelo grande falla, se puede usar uno más pequeño. Si la cola crece, se puede rechazar con un mensaje claro. Lo que no se puede es dejar al usuario esperando sin explicación.",
                    ],
                },
            ],
            "brief": [
                "Normaliza, reescribe y filtra antes de buscar",
                "Delimita el contexto y exige citas verificables",
                "Caché y streaming con límites; degrada con elegancia",
            ],
            "keys": [
                "La reescritura de consulta resuelve referencias conversacionales antes de recuperar.",
                "Los permisos se aplican en la recuperación, no después de generar.",
                "El prompt debe definir qué hacer cuando el contexto no basta.",
                "La caché semántica ahorra coste pero exige invalidación y aislamiento por usuario.",
            ],
            "example": "Un usuario pregunta «¿y para el año que viene?». El pipeline recupera el historial, reescribe la pregunta como «¿cuál es el presupuesto de formación para 2027?», filtra por su departamento, recupera dos fragmentos y responde citando la política. Sin la reescritura, la búsqueda habría devuelto documentos sobre presupuestos genéricos.",
            "caution": "Aplicar los permisos después de generar significa que el modelo ya vio el documento restringido. El filtro debe estar en la consulta, no en la salida.",
            "search": "inferencia RAG normalización reescritura consulta filtros permisos contexto prompt citas temperatura streaming caché semántica degradación guardrails",
        },
        {
            "id": "llm7l2",
            "lnum": 2,
            "title": "Desplegar el pipeline: API, Docker y CI/CD",
            "minutes": 7,
            "lead": "Un notebook que funciona no es un servicio. Desplegar significa empaquetar el pipeline en una imagen reproducible, exponerlo con un contrato claro, probarlo antes de publicar y poder volver atrás cuando algo falla. La infraestructura importa porque el producto depende de ella.",
            "diagram": ("flow", ["Commit", "Build", "Test", "Deploy"]),
            "caption": "Cada cambio recorre el mismo camino: se construye la imagen, se prueba el contrato y se despliega con posibilidad de reversión.",
            "sections": [
                {
                    "h": "La API como contrato",
                    "p": [
                        "FastAPI es una elección habitual porque define esquemas con Pydantic, genera documentación y soporta asincronía. El endpoint recibe una pregunta, un identificador de conversación y opciones acotadas; devuelve respuesta, fuentes, latencia y un identificador de traza. Los campos de entrada se validan y se limitan: longitud máxima, idioma permitido, número de resultados.",
                        "El contrato debe incluir los errores. ¿Qué devuelve el servicio si el índice está caído, si el modelo tarda demasiado o si la pregunta está fuera de alcance? Un código HTTP y un mensaje útil permiten que el cliente reaccione. Un 500 genérico obliga al usuario a adivinar.",
                        "La API no debe exponer detalles internos: rutas de S3, nombres de colecciones o claves. Los logs tampoco. La traza interna puede guardar mucho, pero el cliente recibe solo lo necesario para entender la respuesta y citar las fuentes.",
                    ],
                },
                {
                    "h": "Imagen, configuración y despliegue",
                    "p": [
                        "Docker empaqueta el código, las dependencias y el entorno de ejecución. La imagen se construye desde el lock, con una base fija y sin secretos. Se etiqueta con la versión o el commit para poder rastrear qué está corriendo. Cuanto más pequeña sea, más rápido se despliega y menos superficie de ataque tiene.",
                        "SageMaker permite desplegar la imagen en un endpoint con escalado y monitoreo, o ejecutar entrenamientos con roles de IAM. También se puede desplegar en ECS, Kubernetes o un servidor propio. La decisión depende de lo que ya use el equipo y del SLA. Lo importante es que el entorno sea reproducible y el escalado esté probado.",
                        "La infraestructura como código describe buckets, roles, endpoints y alarmas en archivos versionados. Aplicar el mismo stack en dos cuentas debería dar el mismo resultado. Si la infraestructura se crea a mano, el día que haya que reconstruirla se descubrirán dependencias invisibles.",
                    ],
                },
                {
                    "h": "CI/CD y reversión",
                    "p": [
                        "El pipeline de integración ejecuta lint, pruebas unitarias, pruebas de contrato y una evaluación mínima con el golden set. Si la calidad baja de un umbral, el despliegue se detiene. Esa compuerta convierte la evaluación en parte del proceso, no en un informe que se lee después.",
                        "El despliegue puede ser canario: se envía un porcentaje del tráfico a la versión nueva y se comparan latencia, errores y métricas de calidad. Si algo empeora, se vuelve a la versión anterior. Para que la reversión funcione, la versión anterior debe seguir disponible y la base de datos debe ser compatible con ambas.",
                        "Las migraciones de índice y de esquema necesitan su propio plan. Cambiar la dimensión de un vector o el nombre de un campo puede romper la versión antigua. Despliega primero el código compatible con ambos formatos, migra después y elimina lo viejo cuando ya nadie lo usa.",
                    ],
                },
            ],
            "brief": [
                "API con esquema, errores y trazas claras",
                "Imagen reproducible sin secretos y infraestructura como código",
                "CI/CD con compuerta de calidad y reversión",
            ],
            "keys": [
                "El contrato de la API incluye entradas, salidas, errores y límites.",
                "La imagen se construye desde el lock y se etiqueta con la versión del código.",
                "La evaluación puede bloquear un despliegue si la calidad cae por debajo del umbral.",
                "Canario y reversión exigen compatibilidad entre versiones y migraciones planificadas.",
            ],
            "example": "Un equipo despliega una versión canaria al 5 % del tráfico. A las dos horas, la latencia p95 sube un 40 % y las respuestas sin cita aumentan. El sistema vuelve a la versión anterior automáticamente. La causa era un cambio en el prompt que alargaba las respuestas; la compuerta de calidad lo detectó antes de afectar a todos.",
            "caution": "Un despliegue sin reversión es una apuesta. Si la versión nueva falla y no puedes volver en minutos, el incidente se mide en horas.",
            "search": "despliegue FastAPI Docker SageMaker ECR CI/CD canario reversión infraestructura como código IAM secretos salud migración índice",
        },
        {
            "id": "llm7l3",
            "lnum": 3,
            "title": "LLMOps: observar, evaluar y mejorar",
            "minutes": 7,
            "lead": "El sistema no termina cuando el endpoint responde 200. Los datos cambian, los prompt se desactualizan, los modelos se actualizan y los usuarios encuentran formas nuevas de preguntar. LLMOps es la disciplina de detectar esos cambios antes de que el producto pierda calidad.",
            "diagram": ("loop", ["Instrumentar", "Evaluar", "Detectar", "Mejorar"]),
            "caption": "El ciclo se repite con cada versión: se observa, se evalúa, se detecta la causa y se mejora con evidencia.",
            "sections": [
                {
                    "h": "Observabilidad: trazas, métricas y coste",
                    "p": [
                        "Una traza completa de una petición incluye la pregunta, el historial, la consulta reescrita, los documentos recuperados, el prompt final, la respuesta, la latencia por etapa y el coste estimado. Con esa información se puede reconstruir qué pasó sin pedir al usuario que repita la conversación.",
                        "Las métricas operativas —errores, latencia p50 y p95, saturación, tokens por petición— detectan problemas de servicio. Las métricas de calidad —fidelidad, abstención, citas correctas, satisfacción— detectan problemas de producto. Un panel que solo muestra latencia puede estar verde mientras las respuestas empeoran.",
                        "El coste se mide por petición y por usuario, no solo por factura mensual. Un cambio de prompt que añade 800 tokens de contexto puede parecer inocente y duplicar la factura. La observabilidad debe atribuir el coste a la etapa que lo genera: recuperación, contexto, generación o reintentos.",
                    ],
                },
                {
                    "h": "Deriva y evaluación continua",
                    "p": [
                        "La deriva de datos aparece cuando las preguntas o los documentos cambian respecto a lo que se evaluó. La deriva de prompt, cuando el prompt que llega a producción no es el que se probó: una variable, un idioma o una versión distinta. La deriva de modelo, cuando el proveedor actualiza el modelo sin cambiar el nombre.",
                        "Para detectarla se ejecuta una evaluación periódica con el golden set y se comparan distribuciones de preguntas, temas y longitudes. Si aumenta la proporción de preguntas fuera de dominio, quizá el producto se está usando para otra cosa. Si las citas fallan más, puede que el índice esté desactualizado.",
                        "La evaluación continua no requiere reentrenar cada día. Requiere muestrear tráfico, etiquetar una parte y revisar las trazas de las respuestas peores. Un sistema con revisión semanal de veinte casos suele detectar más que un panel con cien métricas que nadie interpreta.",
                    ],
                },
                {
                    "h": "Mejora con evidencia y gobierno",
                    "p": [
                        "Cada mejora debe tener una hipótesis y una métrica. «Añadir reranking mejorará la fidelidad en preguntas comparativas» es una hipótesis comprobable. «Cambiar el prompt para que sea más moderno» no lo es. El ciclo se cierra volviendo a evaluar y comparando contra la versión anterior.",
                        "El gobierno incluye versionar prompts, modelos, índices y datasets; documentar quién cambió qué; y definir quién aprueba un despliegue. También incluye la retirada de datos y la respuesta a incidentes. Un sistema que genera respuestas sobre personas o decisiones sensibles necesita revisión humana y límites claros.",
                        "El objetivo final no es un sistema perfecto, sino un sistema que mejore de forma controlada. La calidad sube cuando las decisiones se basan en trazas y evaluaciones, y baja cuando se basa en impresiones. LLMOps es la infraestructura que hace que la evidencia esté disponible a tiempo.",
                    ],
                },
            ],
            "brief": [
                "Traza cada petición y atribuye coste por etapa",
                "Vigila deriva de datos, prompt y modelo",
                "Mejora con hipótesis, métrica y revisión",
            ],
            "keys": [
                "Una traza completa permite reconstruir la causa de una respuesta sin acceso al usuario.",
                "Las métricas operativas y las de calidad deben convivir en el mismo panel.",
                "La deriva de prompt ocurre cuando producción no usa el prompt evaluado.",
                "Cada cambio necesita hipótesis, métrica y una comparación contra la versión anterior.",
            ],
            "example": "Un lunes, la tasa de respuestas sin cita sube del 4 % al 18 %. La traza muestra que el recuperador devuelve fragmentos de una colección antigua porque el alias no se actualizó tras una migración. El problema no era el modelo; era una pieza de infraestructura que el panel de calidad detectó en horas.",
            "caution": "Guardar trazas con datos personales sin política de retención crea un riesgo de privacidad. Anonimiza, limita el acceso y define cuánto tiempo se conservan.",
            "search": "LLMOps observabilidad trazas métricas coste deriva prompt drift evaluación continua gobierno versionado prompts retención incidentes",
        },
    ],
    "quiz": {
        "id": "llm7q",
        "title": "Cierre del módulo 07",
        "summary": [
            "La inferencia RAG normaliza, recupera con permisos, arma el prompt, genera y posprocesa con citas.",
            "El despliegue empaqueta una imagen reproducible, expone un contrato y se prueba antes de publicar.",
            "La reversión y el canario reducen el impacto de una versión defectuosa.",
            "LLMOps observa trazas, detecta deriva y mejora con hipótesis y métricas.",
        ],
        "questions": [
            {
                "q": "¿Dónde deben aplicarse los permisos de un usuario en un sistema RAG?",
                "options": [
                    "Después de generar, filtrando la respuesta",
                    "Antes o durante la recuperación, para no incluir documentos restringidos",
                    "Solo en la interfaz de usuario",
                    "En el prompt, pidiendo al modelo que no los use",
                ],
                "answer": 1,
                "why": "Si el documento restringido entra en el contexto, el modelo ya lo vio; el filtro debe impedir la recuperación.",
            },
            {
                "q": "¿Qué ventaja aporta un despliegue canario?",
                "options": [
                    "Elimina la necesidad de pruebas",
                    "Envía una parte del tráfico a la versión nueva y permite comparar antes de generalizar",
                    "Reduce el tamaño de la imagen",
                    "Cambia el modelo automáticamente",
                ],
                "answer": 1,
                "why": "El canario limita la exposición y genera datos comparables; si algo falla, se revierte con impacto acotado.",
            },
            {
                "q": "¿Qué es la deriva de prompt?",
                "options": [
                    "Que el modelo cambie de idioma",
                    "Que el prompt de producción no coincida con el que se evaluó",
                    "Que el índice crezca demasiado",
                    "Que el usuario escriba prompts más largos",
                ],
                "answer": 1,
                "why": "Una variable, una versión o una ruta distinta pueden hacer que producción use un prompt no validado, y las métricas dejan de representar el sistema real.",
            },
        ],
        "exercises": [
            "Diseña el contrato de tu endpoint: entrada, salida, errores, límites y campos de traza.",
            "Escribe un plan de despliegue canario con umbrales de latencia, errores y calidad, y el criterio de reversión.",
            "Elige tres métricas de LLMOps que revisarías cada semana y explica qué decisión tomarías con cada una.",
        ],
        "search": "evaluación cierre inferencia RAG permisos despliegue canario reversión LLMOps trazas deriva prompt drift métricas gobierno",
    },
}
