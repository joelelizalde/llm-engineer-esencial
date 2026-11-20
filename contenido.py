"""Contenido del curso «Ingeniería de LLM esencial».

Cada módulo vive en modulos/mNN.py y expone un diccionario MODULE.
Este archivo los reúne y añade los metadatos del curso y el glosario.
"""

from modulos import m01, m02, m03, m04, m05, m06, m07

MODULES = [
    m01.MODULE,
    m02.MODULE,
    m03.MODULE,
    m04.MODULE,
    m05.MODULE,
    m06.MODULE,
    m07.MODULE,
]

COURSE = {
    "title": "Ingeniería de LLM",
    "brand": "LE",
    "subtitle": "Edición esencial",
    "tagline": "Del cuaderno al sistema en producción",
    "description": (
        "Edición esencial en español de «LLM Engineer's Handbook», de Paul Iusztin y "
        "Maxime Labonne: arquitectura, datos, RAG, ajuste fino, evaluación y despliegue "
        "de un gemelo digital, con criterio y sin relleno."
    ),
    "book": "LLM Engineer's Handbook",
    "author": "Paul Iusztin y Maxime Labonne",
    "pdf": "Ingenieria-de-LLM-Esencial.pdf",
    "year": "2026",
}

# Glosario: (término, definición breve, id de lección donde se desarrolla)
GLOSARIO = [
    ("Ajuste fino supervisado", "Entrenamiento con pares de instrucción y respuesta para especializar un modelo base.", "llm5l2"),
    ("Alineación", "Técnicas que acercan el comportamiento del modelo a lo que las personas prefieren.", "llm5l3"),
    ("Alucinación", "Respuesta fluida y plausible que no está respaldada por los datos ni por el contexto.", "llm6l1"),
    ("ANN", "Búsqueda aproximada de vecinos: localiza vectores parecidos sin recorrer toda la colección.", "llm4l3"),
    ("Artefacto", "Salida versionada de un paso de pipeline: un dataset, un índice o un modelo.", "llm2l2"),
    ("Autoscaling", "Ajuste automático del número de instancias según la carga del servicio.", "llm6l3"),
    ("Benchmark", "Conjunto estandarizado de tareas y métricas para comparar modelos.", "llm6l3"),
    ("Búsqueda híbrida", "Combinación de recuperación densa por embeddings y recuperación léxica por palabras.", "llm4l1"),
    ("Caché de claves y valores", "Memoria de las claves y valores ya calculados que acelera la generación token a token.", "llm6l2"),
    ("Caché semántica", "Reutilización de una respuesta anterior cuando la nueva pregunta es suficientemente parecida.", "llm7l1"),
    ("Chat template", "Formato con marcadores de rol que convierte una conversación en una secuencia entrenable.", "llm5l1"),
    ("Chunk", "Fragmento de documento que se indexa y se recupera como unidad mínima de contexto.", "llm4l2"),
    ("Chunking", "Proceso de dividir documentos en fragmentos con tamaño y solapamiento controlados.", "llm4l2"),
    ("CI/CD", "Integración y entrega continuas: construir, probar y desplegar de forma automática.", "llm7l2"),
    ("Comet", "Plataforma de seguimiento de experimentos, métricas y artefactos de entrenamiento.", "llm2l2"),
    ("Crawler", "Programa que descubre y descarga páginas de forma automatizada y respetuosa.", "llm3l1"),
    ("Cross-encoder", "Modelo que puntúa un par pregunta-documento leyendo ambos textos juntos.", "llm4l1"),
    ("Cuantización", "Reducción de la precisión numérica de los pesos para ahorrar memoria y ganar velocidad.", "llm6l2"),
    ("Data lake", "Almacenamiento barato de archivos crudos o procesados, sin esquema rígido.", "llm3l3"),
    ("Data warehouse", "Almacén estructurado y consultable que sirve datos limpios a los equipos.", "llm3l3"),
    ("Decodificación especulativa", "Generación con un modelo borrador que propone tokens y un modelo grande que los valida.", "llm6l2"),
    ("Deduplicación", "Eliminación de documentos o fragmentos repetidos, exactos o casi idénticos.", "llm3l2"),
    ("Deriva", "Cambio gradual de datos, consultas o comportamiento que degrada el sistema.", "llm7l3"),
    ("Destilación", "Entrenamiento de un modelo pequeño para imitar las salidas de uno grande.", "llm6l2"),
    ("DPO", "Optimización directa de preferencias: aprende de pares elegido-rechazado sin modelo de recompensa.", "llm5l3"),
    ("Embedding", "Vector denso que representa el significado de un texto para compararlo con otros.", "llm4l2"),
    ("Endpoint", "Servicio HTTP desplegado que recibe peticiones y devuelve predicciones.", "llm7l2"),
    ("Evaluación offline", "Medición con un conjunto fijo de casos antes de desplegar un cambio.", "llm6l1"),
    ("Evaluación online", "Medición con tráfico real y señales de uso después de desplegar.", "llm7l3"),
    ("Fidelidad", "Grado en que una respuesta se apoya en el contexto recuperado y no inventa datos.", "llm6l1"),
    ("FTI", "Arquitectura de pipelines de features, entrenamiento e inferencia separadas y conectadas.", "llm1l2"),
    ("Golden dataset", "Conjunto curado de preguntas y respuestas de referencia para comparar versiones.", "llm6l1"),
    ("Guardrail", "Filtro o regla que limita lo que el sistema puede responder o hacer.", "llm7l1"),
    ("HNSW", "Estructura de grafo jerárquico que acelera la búsqueda aproximada en Qdrant.", "llm4l3"),
    ("Idempotencia", "Propiedad de una operación que puede repetirse sin duplicar ni corromper datos.", "llm3l1"),
    ("LLM Twin", "Sistema que reproduce el estilo y el criterio de una persona usando sus propios datos.", "llm1l1"),
    ("LLM-as-judge", "Uso de un modelo fuerte para puntuar respuestas según una rúbrica explícita.", "llm6l1"),
    ("LoRA", "Ajuste eficiente que congela el modelo base y entrena adaptadores de bajo rango.", "llm5l2"),
    ("Reindexación", "Proceso de reconstruir un índice cuando cambian los datos, el chunking o el modelo de embeddings.", "llm4l3"),
    ("MongoDB", "Base de documentos JSON que aquí guarda el corpus crudo y el limpio.", "llm2l3"),
    ("MVP", "Producto mínimo viable: la versión más pequeña que entrega valor y permite aprender.", "llm1l1"),
    ("Observabilidad", "Capacidad de reconstruir qué pasó en el sistema a partir de trazas, logs y métricas.", "llm7l3"),
    ("Opik", "Herramienta de trazas y evaluación de aplicaciones LLM, prompts y recuperación.", "llm2l2"),
    ("Orquestador", "Componente que ejecuta pasos de pipeline en orden, con artefactos y reintentos.", "llm2l2"),
    ("Overfitting", "Memorización del conjunto de entrenamiento que empeora el rendimiento en datos nuevos.", "llm5l2"),
    ("Payload", "Metadatos asociados a un vector en Qdrant que permiten filtrar y citar resultados.", "llm4l3"),
    ("Pipeline de features", "Proceso que transforma datos crudos en features listas para entrenar y servir.", "llm1l2"),
    ("Pipeline de inferencia", "Proceso que atiende una petición: recupera contexto, genera y devuelve la respuesta.", "llm7l1"),
    ("Pipeline de entrenamiento", "Proceso que toma features y produce un modelo evaluado y versionado.", "llm1l2"),
    ("Plantilla de prompt", "Estructura con instrucciones, contexto y pregunta que se rellena en cada petición.", "llm5l1"),
    ("Poe", "Ejecutor de tareas de Poetry que estandariza los comandos del proyecto.", "llm2l1"),
    ("Poetry", "Gestor de dependencias y entornos que fija versiones con un archivo de bloqueo.", "llm2l1"),
    ("Preferencias", "Pares de respuestas donde una se considera mejor que la otra para el mismo prompt.", "llm5l3"),
    ("Prompt drift", "Desalineación entre el prompt que se evaluó y el que realmente llega a producción.", "llm7l3"),
    ("Qdrant", "Base de datos vectorial con filtros por metadatos y búsqueda aproximada.", "llm2l3"),
    ("QLoRA", "LoRA sobre un modelo base cuantizado a 4 bits, para ajustar con poca memoria.", "llm5l2"),
    ("RAG", "Generación aumentada por recuperación: se buscan documentos y se añaden al contexto.", "llm4l1"),
    ("Reranking", "Reordenación de los documentos recuperados con un modelo más preciso y más caro.", "llm4l1"),
    ("SageMaker", "Servicio de AWS para entrenar, registrar y desplegar modelos.", "llm2l3"),
    ("Secreto", "Credencial que se inyecta en tiempo de ejecución y nunca se escribe en el repositorio.", "llm2l1"),
    ("Streaming", "Envío de la respuesta por partes mientras el modelo la genera.", "llm7l1"),
    ("Throughput", "Número de peticiones o tokens que el sistema sirve por unidad de tiempo.", "llm6l3"),
    ("TTFT", "Tiempo hasta el primer token: lo que percibe el usuario como velocidad de arranque.", "llm6l3"),
    ("vLLM", "Servidor de inferencia con gestión eficiente de memoria y batching continuo.", "llm6l2"),
    ("ZenML", "Framework de orquestación de pipelines con artefactos, stacks y linaje.", "llm2l2"),
]
