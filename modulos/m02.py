MODULE = {
    "num": "02",
    "title": "Herramientas y entorno",
    "sub": "Poetry, ZenML, Comet, Opik, MongoDB, Qdrant y AWS",
    "lessons": [
        {
            "id": "llm2l1",
            "lnum": 1,
            "title": "Un proyecto reproducible con Poetry y Poe",
            "minutes": 7,
            "lead": "Antes del primer embedding hay que resolver una pregunta poco glamurosa: ¿cómo garantizas que el código que funciona en tu portátil funcione igual en el servidor dentro de tres meses? La respuesta empieza por fijar dependencias, estandarizar comandos y sacar los secretos del repositorio.",
            "diagram": ("flow", ["pyproject", "poetry.lock", "Tareas Poe", "CI"]),
            "caption": "La reproducibilidad se construye en capas: dependencias fijadas, comandos uniformes y una integración continua que repite lo mismo.",
            "sections": [
                {
                    "h": "Dependencias que no se mueven solas",
                    "p": [
                        "Poetry declara las dependencias en pyproject.toml y resuelve versiones concretas en poetry.lock. El archivo de bloqueo es el que se versiona y el que se instala en todos los entornos; sin él, una actualización silenciosa de una librería puede cambiar el comportamiento de un tokenizador o de una API. La regla es simple: el rango vive en pyproject, la verdad vive en el lock.",
                        "Conviene separar grupos: dependencias de ejecución, de desarrollo, de entrenamiento y de despliegue. Un contenedor de inferencia no necesita pytest ni notebooks; una imagen de entrenamiento no necesita el servidor web. Esa separación reduce tamaño, superficie de ataque y tiempo de construcción. También conviene fijar la versión de Python, porque el comportamiento de algunas librerías cambia entre menores.",
                        "Los entornos virtuales se crean con el propio Poetry o con la herramienta que prefiera el equipo, pero nunca se activan a mano en producción. El despliegue instala desde el lock y ejecuta comandos declarados, no una secuencia de pasos que alguien recuerda.",
                    ],
                },
                {
                    "h": "Comandos que todo el mundo ejecuta igual",
                    "p": [
                        "Poe es un ejecutor de tareas que se apoya en Poetry. Declara comandos como poe lint, poe test, poe format o poe ingest en un archivo de configuración. La ventaja no es la sintaxis, sino el contrato: la CI, el equipo y la documentación usan el mismo nombre para la misma operación. Cuando cambia el comando subyacente, se cambia en un sitio.",
                        "Ese contrato también ayuda a documentar. Un README que dice «ejecuta poe test» es más útil que uno que enumera cinco variables de entorno y tres rutas. Y permite que un recién llegado compruebe el proyecto sin adivinar qué versión de la herramienta de turno está instalada.",
                        "Junto a Poe conviene tener pre-commit con formateadores y linters, y Ruff como herramienta rápida de lint y formato. Las revisiones se centran en el diseño, no en discusiones sobre comas. mypy o pyright añaden una red de seguridad en los bordes del sistema, donde los esquemas de datos son más frágiles.",
                    ],
                },
                {
                    "h": "Configuración y secretos fuera del código",
                    "p": [
                        "Las credenciales de MongoDB, Qdrant, Hugging Face o AWS no se escriben en el repositorio. Se cargan de variables de entorno o de un gestor de secretos, con un archivo .env solo para desarrollo y siempre ignorado por Git. En producción, el servicio recibe permisos mediante un rol de IAM o un secreto inyectado, no un archivo copiado a mano.",
                        "La configuración no secreta —nombres de colecciones, tamaños de chunk, rutas de modelos— se valida al arrancar. Si falta una variable o tiene un tipo incorrecto, el proceso debe fallar de inmediato con un mensaje claro. Un error de configuración detectado en el arranque cuesta minutos; detectado a mitad de un entrenamiento, horas.",
                        "Por último, versiona también el entorno: imagen base, versión de CUDA y sistema operativo. La reproducibilidad no termina en las dependencias de Python. Un modelo que solo entrena con una combinación específica de controladores es un riesgo, no un detalle.",
                    ],
                },
            ],
            "brief": [
                "Poetry fija el árbol de dependencias en un lock",
                "Poe estandariza los comandos del equipo y la CI",
                "Los secretos se inyectan, nunca se versionan",
            ],
            "keys": [
                "pyproject.toml declara intenciones; poetry.lock fija la instalación real.",
                "Separar grupos de dependencias reduce el tamaño y la superficie de las imágenes.",
                "Poe convierte comandos dispersos en una interfaz estable para el equipo y la CI.",
                "La configuración se valida al arrancar y los secretos se cargan del entorno.",
            ],
            "example": "Un proyecto tiene un script que descarga datos con una versión antigua de requests y otro que sirve la API con una nueva. Al fijar ambas en el lock y separar los grupos, la incompatibilidad aparece en la resolución y no en producción. La CI instala cada grupo en su propia imagen y prueba el camino correspondiente.",
            "caution": "Un lock desactualizado también es un riesgo: fija versiones con vulnerabilidades conocidas. Actualiza de forma programada y vuelve a ejecutar las pruebas y la evaluación.",
            "search": "Poetry pyproject lock dependencias grupos Poe tareas pre-commit Ruff mypy pytest configuración secretos .env IAM reproducibilidad",
        },
        {
            "id": "llm2l2",
            "lnum": 2,
            "title": "Orquestación y experimentos: ZenML, Comet y Opik",
            "minutes": 7,
            "lead": "Un pipeline de LLM tiene pasos que tardan, fallan y producen artefactos que hay que comparar. Sin orquestación, cada ejecución es un script irrepetible; sin registro de experimentos, no sabes qué cambió; sin trazas de prompts, no puedes explicar por qué una respuesta salió mal.",
            "diagram": ("flow", ["Step", "Artefacto", "Pipeline", "Experimento"]),
            "caption": "Cada paso produce un artefacto; el pipeline encadena pasos; el experimento compara configuraciones y resultados.",
            "sections": [
                {
                    "h": "ZenML: pasos, pipelines y artefactos",
                    "p": [
                        "ZenML organiza el trabajo en steps y pipelines. Un step es una función con entradas y salidas tipadas; un pipeline conecta steps y decide qué se ejecuta. Cada salida se guarda como artefacto en el almacén configurado, con versión y linaje. Eso significa que un modelo puede rastrearse hasta el dataset y el código que lo produjeron.",
                        "La idea de stack separa la definición del pipeline de la infraestructura que lo ejecuta: orquestador, almacén de artefactos, contenedor y tracker. En local se usa un stack sencillo; en la nube se cambia el orquestador o el almacén sin reescribir los pasos. Esa portabilidad es especialmente útil cuando el entrenamiento necesita GPU y la ingesta no.",
                        "ZenML también aporta caché: si un step ya se ejecutó con las mismas entradas y configuración, puede reutilizar el artefacto. En pipelines de datos esto ahorra horas. La contrapartida es que hay que versionar bien las entradas; una caché con una clave incompleta devuelve resultados obsoletos con cara de nuevos.",
                    ],
                },
                {
                    "h": "Comet: el cuaderno de experimentos",
                    "p": [
                        "Comet registra parámetros, métricas, artefactos y curvas de entrenamiento. Cada ejecución queda asociada a un experimento y a un proyecto, con la configuración exacta y las versiones del código. Cuando dos modelos difieren en calidad, el registro permite comparar no solo el resultado, sino las condiciones.",
                        "En un curso de LLM, Comet es útil para comparar tamaños de chunk, modelos de embeddings, tasas de aprendizaje y variantes de LoRA. También para guardar muestras cualitativas: una tabla de respuestas generadas vale más que una pérdida de validación cuando se trata de estilo o de formato.",
                        "El registro debe incluir lo que no es una métrica: versión del dataset, hash del índice, plantilla de prompt y commit. Un experimento sin esas coordenadas es una anécdota. La disciplina de registrar el contexto separa un cuaderno de laboratorio de una colección de capturas de pantalla.",
                    ],
                },
                {
                    "h": "Opik: trazas y evaluación de lo que responde",
                    "p": [
                        "Opik se centra en la aplicación, no solo en el entrenamiento. Registra trazas de cada petición: pregunta, documentos recuperados, prompt enviado, respuesta, latencia y coste. Esas trazas permiten reconstruir una conversación y detectar si el fallo estuvo en la recuperación, en el prompt o en el modelo.",
                        "También permite construir datasets de evaluación y ejecutar experimentos con métricas automáticas o con un juez LLM. En lugar de revisar manualmente cien respuestas, se define una rúbrica, se puntúa una muestra y se comparan versiones. La revisión humana sigue siendo necesaria para calibrar, pero deja de ser el único mecanismo.",
                        "La combinación de las tres herramientas cubre el ciclo: ZenML ejecuta, Comet compara entrenamientos, Opik observa el servicio. Ninguna sustituye a las otras, y ninguna sustituye a una pregunta bien formulada sobre qué significa «mejor» en tu producto.",
                    ],
                },
            ],
            "brief": [
                "ZenML encadena pasos y versiona artefactos",
                "Comet registra parámetros, métricas y muestras",
                "Opik traza peticiones y evalúa respuestas",
            ],
            "keys": [
                "Un step de ZenML recibe entradas tipadas y produce artefactos versionados con linaje.",
                "El stack separa la lógica del pipeline de la infraestructura que lo ejecuta.",
                "Comet debe registrar también dataset, índice, prompt y commit, no solo métricas.",
                "Opik conecta la evaluación con la aplicación real mediante trazas y datasets.",
            ],
            "example": "Un equipo sospecha que la calidad bajó tras cambiar el chunking. Comet muestra que la pérdida de validación es similar, pero Opik revela que las respuestas citan fragmentos incompletos. La causa no era el modelo: el nuevo tamaño de chunk partía tablas por la mitad. La traza lo hizo visible en minutos.",
            "caution": "Registrar todo sin criterio produce ruido. Define qué métricas y muestras importan antes de llenar el panel de gráficas que nadie mira.",
            "search": "ZenML steps pipelines artefactos stack orquestador caché Comet experimentos métricas Opik trazas evaluación prompts LLMOps",
        },
        {
            "id": "llm2l3",
            "lnum": 3,
            "title": "Datos y AWS: MongoDB, Qdrant y SageMaker",
            "minutes": 7,
            "lead": "El sistema necesita dos tipos de almacenamiento con personalidades distintas: uno para documentos y metadatos, otro para vectores y búsqueda semántica. Alrededor de ambos, AWS aporta cómputo, almacenamiento de objetos y permisos. Elegir bien estas piezas evita rehacer la arquitectura a mitad del proyecto.",
            "diagram": ("flow", ["Documentos", "MongoDB", "Qdrant", "SageMaker"]),
            "caption": "MongoDB conserva el documento y su procedencia; Qdrant guarda los vectores; SageMaker ejecuta entrenamiento y servicio.",
            "sections": [
                {
                    "h": "MongoDB: el documento como unidad",
                    "p": [
                        "MongoDB almacena documentos JSON con esquema flexible. Es una elección natural para un corpus heterogéneo: un artículo de Medium, un README de GitHub y una entrada de Substack comparten campos básicos —id, url, autor, fecha, texto, origen— pero difieren en detalles. Un esquema rígido obligaría a inventar columnas vacías; uno flexible permite evolucionar.",
                        "La flexibilidad no significa ausencia de contrato. Conviene validar los campos obligatorios al insertar, indexar los campos por los que se consulta y separar colecciones para crudo, limpio y chunks si el volumen lo justifica. También conviene guardar el hash del contenido para detectar duplicados y actualizaciones.",
                        "MongoDB no es el lugar para los vectores de 1.536 dimensiones. Podrías guardarlos, pero la búsqueda por similitud y los filtros combinados se vuelven lentos y difíciles de escalar. La división de responsabilidades —documento en MongoDB, vector en Qdrant— simplifica ambas piezas.",
                    ],
                },
                {
                    "h": "Qdrant: vectores con metadatos",
                    "p": [
                        "Qdrant organiza los vectores en colecciones. Cada punto tiene un id, un vector y un payload con metadatos. La distancia habitual para embeddings normalizados es el coseno, aunque también admite producto interno y distancia euclídea. La dimensión del vector debe coincidir con la del modelo de embeddings elegido y no se puede cambiar sin recrear la colección.",
                        "El payload es lo que convierte una búsqueda vectorial en una búsqueda útil. Permite filtrar por autor, fecha, tipo de documento o etiqueta antes o durante la búsqueda. También permite devolver la URL y el título para citar. Sin payload, el sistema recupera texto anónimo y el usuario no puede verificar nada.",
                        "Los índices HNSW aceleran la búsqueda aproximada a costa de algo de recall. Los parámetros de construcción y búsqueda se ajustan según el tamaño de la colección y la latencia objetivo. Para un corpus pequeño, la búsqueda exacta puede ser suficiente; para millones de chunks, la aproximada es la única opción práctica.",
                    ],
                },
                {
                    "h": "AWS: cómputo, objetos y permisos",
                    "p": [
                        "S3 guarda objetos: datasets, artefactos, modelos, imágenes y registros. Es barato y duradero, pero no es una base de datos: no conviene consultarlo con filtros frecuentes. ECR aloja las imágenes de contenedor que se desplegarán. SageMaker aporta entornos de entrenamiento, registro de modelos y endpoints de inferencia con escalado.",
                        "IAM es la pieza que suele causar más problemas. Cada servicio debe tener un rol con los permisos mínimos: leer un bucket concreto, escribir en otro, invocar un endpoint. Evita claves de acceso de larga duración en el código. Si un contenedor necesita hablar con S3, se le asigna un rol, no un par de claves pegado en una variable.",
                        "El coste se controla con límites: presupuestos, alarmas, instancias spot para entrenamiento, apagado de endpoints ociosos y retención de artefactos. Un endpoint encendido sin tráfico es la forma más silenciosa de gastar dinero. La arquitectura debe incluir el apagado desde el primer día, no como una optimización posterior.",
                    ],
                },
            ],
            "brief": [
                "MongoDB guarda documentos y procedencia",
                "Qdrant guarda vectores, payload y filtros",
                "S3, ECR, SageMaker e IAM sostienen el resto",
            ],
            "keys": [
                "MongoDB encaja con corpus heterogéneos si se valida un esquema mínimo y se indexa lo consultable.",
                "Qdrant separa el vector del documento y permite filtrar por metadatos del payload.",
                "La dimensión del embedding y la métrica de distancia condicionan toda la colección.",
                "IAM con permisos mínimos y presupuestos con alarmas forman parte del diseño, no son un extra.",
            ],
            "example": "Un equipo guarda en MongoDB el artículo completo con su URL y en Qdrant un punto por chunk con payload {doc_id, url, autor, fecha, seccion}. Al responder, recupera cinco chunks, los agrupa por documento y cita la URL. Si el usuario filtra por «solo 2024», la consulta añade una condición sobre el payload sin reindexar nada.",
            "caution": "Cambiar el modelo de embeddings sin recrear la colección mezcla vectores incompatibles y arruina la búsqueda. Versiona el modelo y el índice como una sola unidad.",
            "search": "MongoDB documentos esquema validación índices Qdrant colecciones vectores payload filtros HNSW coseno AWS S3 ECR SageMaker IAM presupuesto",
        },
    ],
    "quiz": {
        "id": "llm2q",
        "title": "Cierre del módulo 02",
        "summary": [
            "Poetry y Poe fijan dependencias y comandos; los secretos se inyectan desde el entorno.",
            "ZenML orquesta pasos y artefactos; Comet compara experimentos; Opik traza y evalúa respuestas.",
            "MongoDB conserva documentos y metadatos; Qdrant indexa vectores y permite filtrar por payload.",
            "AWS aporta almacenamiento, imágenes, entrenamiento y servicio, con permisos mínimos y control de coste.",
        ],
        "questions": [
            {
                "q": "¿Qué archivo garantiza que dos entornos instalen exactamente las mismas versiones de Python?",
                "options": [
                    "README.md",
                    "pyproject.toml",
                    "poetry.lock",
                    "requirements.txt sin versiones",
                ],
                "answer": 2,
                "why": "El lock contiene las versiones resueltas; pyproject declara rangos y el README documenta, pero no fija la instalación.",
            },
            {
                "q": "¿Dónde conviene guardar el vector de un chunk para buscarlo por similitud?",
                "options": [
                    "En un campo de texto de MongoDB",
                    "En una colección de Qdrant con su payload",
                    "En el nombre del archivo de S3",
                    "En una variable de entorno del contenedor",
                ],
                "answer": 1,
                "why": "Qdrant está diseñado para búsqueda vectorial y filtros por metadatos; MongoDB guarda el documento, no la búsqueda semántica.",
            },
            {
                "q": "¿Qué herramienta usarías para reconstruir qué documentos se recuperaron en una petición concreta?",
                "options": [
                    "Comet, porque guarda curvas de pérdida",
                    "Opik, porque registra trazas de la aplicación",
                    "Poetry, porque fija dependencias",
                    "S3, porque almacena objetos",
                ],
                "answer": 1,
                "why": "Las trazas de Opik incluyen pregunta, contexto recuperado, prompt, respuesta y latencia de cada petición.",
            },
        ],
        "exercises": [
            "Crea la estructura mínima de un proyecto con pyproject, lock, grupos de dependencias y tres tareas de Poe.",
            "Diseña el payload de un chunk para que permita filtrar por autor, fecha y tipo de documento, y citar la fuente.",
            "Enumera los permisos de IAM que necesitaría un contenedor de inferencia y justifica cada uno.",
        ],
        "search": "evaluación cierre Poetry Poe ZenML Comet Opik MongoDB Qdrant SageMaker IAM dependencias secretos artefactos",
    },
}
