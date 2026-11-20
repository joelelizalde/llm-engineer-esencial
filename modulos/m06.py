MODULE = {
    "num": "06",
    "title": "Evaluación y optimización",
    "sub": "Medir antes de creer y servir sin arruinarte",
    "lessons": [
        {
            "id": "llm6l1",
            "lnum": 1,
            "title": "Evaluar un LLM y un sistema RAG",
            "minutes": 8,
            "lead": "Un modelo que responde bonito no es un modelo que responde bien. La evaluación convierte «me gusta más» en una comparación reproducible: mismas preguntas, mismos criterios y un registro de qué versión produjo qué resultado. Sin eso, cada cambio es una opinión.",
            "diagram": ("flow", ["Golden set", "Modelo", "Juez", "Informe"]),
            "caption": "El conjunto reservado alimenta al modelo; el juez puntúa con una rúbrica; el informe compara versiones.",
            "sections": [
                {
                    "h": "Qué evaluar y con qué datos",
                    "p": [
                        "En un sistema RAG hay tres capas que evaluar. La recuperación: ¿aparecen los documentos correctos? La generación: ¿la respuesta usa el contexto y contesta la pregunta? El producto: ¿el usuario obtiene valor, tarda poco y confía en la respuesta? Cada capa tiene métricas distintas y un fallo en una no se arregla optimizando otra.",
                        "El golden dataset es un conjunto curado de preguntas con respuestas de referencia y, cuando aplica, los documentos que deberían recuperarse. Debe cubrir el dominio, incluir casos fáciles y difíciles, y contener preguntas cuya respuesta no está en el corpus. Este último grupo es el que revela si el sistema sabe abstenerse.",
                        "La evaluación offline se ejecuta antes de desplegar y compara versiones con las mismas condiciones. La online usa tráfico real y señales como clics, reformulaciones o valoraciones. Ninguna sustituye a la otra: la offline es reproducible pero estrecha; la online es real pero ruidosa y difícil de atribuir.",
                    ],
                },
                {
                    "h": "Métricas de recuperación y generación",
                    "p": [
                        "Para recuperación se usan recall@k, MRR y nDCG. Para generación, además de métricas de tarea —exactitud, formato, solapamiento— se usan métricas específicas de RAG: fidelidad, que comprueba si la respuesta se apoya en el contexto; relevancia de la respuesta, que mide si contesta la pregunta; y relevancia del contexto, que mide si lo recuperado era útil.",
                        "La fidelidad es especialmente importante en un gemelo: una respuesta puede ser correcta según el mundo y, aun así, no estar respaldada por las fuentes citadas. Si el sistema afirma algo que no aparece en los documentos, el usuario no puede verificarlo. La métrica debe detectar esa distancia entre lo dicho y lo recuperado.",
                        "Las métricas automáticas tienen límites. El solapamiento de palabras premia copiar; las métricas semánticas pueden puntuar alto una respuesta vaga. Por eso se combinan con revisión humana en una muestra y con casos de regresión que recogen errores ya vistos.",
                    ],
                },
                {
                    "h": "LLM-as-judge con rúbrica",
                    "p": [
                        "Un modelo fuerte puede actuar como juez si se le da una rúbrica explícita y ejemplos calibrados. La rúbrica define los criterios y sus niveles: por ejemplo, fidelidad de 1 a 5, donde 5 exige que toda afirmación factual esté en el contexto. Sin rúbrica, el juez improvisa y las puntuaciones cambian entre ejecuciones.",
                        "El juez tiene sesgos: prefiere respuestas largas, formatos con listas y estilos que se parecen a su propio entrenamiento. Se mitiga pidiendo comparaciones por pares en orden aleatorio, usando varios jueces y validando contra anotaciones humanas. Un juez que no coincide con las personas no es una métrica, es una opinión con formato JSON.",
                        "La evaluación debe versionarse. Guarda el prompt del juez, el modelo, la temperatura y el conjunto de datos. Si cambias el juez, los números anteriores dejan de ser comparables. Un panel que mezcla versiones sin avisar es peor que no tener panel.",
                    ],
                },
            ],
            "brief": [
                "Evalúa recuperación, generación y producto por separado",
                "Golden set con casos difíciles y preguntas sin respuesta",
                "Juez con rúbrica, sesgos conocidos y versión fija",
            ],
            "keys": [
                "La recuperación se mide con recall y ranking; la generación, con fidelidad y relevancia.",
                "Un golden dataset debe incluir preguntas que el corpus no puede responder.",
                "La evaluación offline compara versiones; la online mide valor real con ruido.",
                "El LLM-as-judge es útil si la rúbrica, el modelo y el conjunto quedan versionados.",
            ],
            "example": "Un sistema sube su puntuación de relevancia tras cambiar el prompt, pero la fidelidad baja. Al revisar, el nuevo prompt anima al modelo a «explicar con tus palabras», y este añade datos que no están en las fuentes. La métrica de relevancia celebraba respuestas más completas; la de fidelidad detectó el coste.",
            "caution": "Evaluar con las mismas preguntas que se usaron para construir el prompt infla los resultados. Reserva un conjunto que nadie haya visto durante el desarrollo.",
            "search": "evaluación LLM RAG golden dataset recall fidelidad relevancia contexto LLM-as-judge rúbrica sesgo offline online regresión",
        },
        {
            "id": "llm6l2",
            "lnum": 2,
            "title": "Optimizar la inferencia sin romper la calidad",
            "minutes": 8,
            "lead": "Un modelo que tarda ocho segundos y cuesta céntimos por pregunta puede ser inviable aunque sea excelente. La optimización de inferencia busca reducir latencia, memoria o coste manteniendo la calidad dentro de un margen aceptable. Casi todas las técnicas cambian algo; la pregunta es qué estás dispuesto a ceder.",
            "diagram": ("bars", [("Base", 1.0), ("8 bits", 0.55), ("4 bits", 0.32)]),
            "caption": "Huella relativa de memoria al reducir la precisión de los pesos. La calidad no baja de forma lineal y debe medirse en tu dominio.",
            "sections": [
                {
                    "h": "Cuantización: menos bits, menos memoria",
                    "p": [
                        "Los pesos de un modelo suelen almacenarse en 16 bits. La cuantización los reduce a 8 o 4 bits, con lo que caben en menos memoria y se mueven más rápido. En modelos grandes, la diferencia permite pasar de varias GPU a una. En modelos pequeños, puede degradar más de lo que ahorra.",
                        "Hay cuantización de solo pesos, de pesos y activaciones, y variantes como GPTQ, AWQ o bitsandbytes. Cada una tiene su receta y su sensibilidad. La evaluación debe hacerse en el dominio: un modelo cuantizado puede mantener el promedio y fallar en los casos límite que más importan, como cálculos o citas exactas.",
                        "La cuantización no es un interruptor binario. Prueba 8 bits primero; si necesitas más ahorro, prueba 4 bits con un método robusto y compara respuestas, no solo perplejidad. Guarda la configuración exacta junto al artefacto para poder reproducir el servicio.",
                    ],
                },
                {
                    "h": "Destilación, poda y modelos más pequeños",
                    "p": [
                        "La destilación entrena un modelo pequeño para imitar las salidas de uno grande en un dominio. No copia los pesos: copia el comportamiento en las tareas que le muestras. Puede dar muy buenos resultados en un dominio estrecho y perder generalidad fuera de él. Es una excelente opción cuando el producto tiene un alcance definido.",
                        "La poda elimina pesos o estructuras poco importantes. La poda no estructurada ahorra parámetros pero no siempre acelera en hardware real; la estructurada elimina cabezas o capas y sí puede reducir cómputo. En ambos casos hace falta un ajuste posterior para recuperar calidad.",
                        "A veces la mejor optimización es elegir un modelo base más pequeño desde el principio. Un modelo de 3B bien ajustado y bien evaluado puede superar a un 7B genérico en tu tarea, con una fracción del coste. La comparación debe hacerse con el mismo prompt, el mismo conjunto y la misma métrica.",
                    ],
                },
                {
                    "h": "Acelerar la generación",
                    "p": [
                        "La caché de claves y valores evita recalcular la atención de los tokens ya procesados. Sin ella, cada token nuevo costaría como toda la secuencia. Con ella, el coste por token baja, aunque la memoria crece con la longitud del contexto. Servidores como vLLM gestionan esa memoria por bloques y permiten batching continuo.",
                        "FlashAttention reduce el coste de memoria de la atención sin cambiar el resultado matemático. La decodificación especulativa usa un modelo pequeño para proponer varios tokens y el grande los valida en paralelo; si acierta, gana velocidad. El batching agrupa peticiones para aprovechar la GPU, a costa de aumentar la latencia del último en llegar.",
                        "Cada técnica tiene un perfil: unas mejoran el tiempo hasta el primer token, otras el throughput, otras la memoria. Mide por separado. Una optimización que duplica el throughput pero empeora la latencia percibida puede ser un mal negocio para un chat.",
                    ],
                },
            ],
            "brief": [
                "Cuantizar ahorra memoria; evalúa en tu dominio",
                "Destilar y podar cambian el modelo, no solo el despliegue",
                "KV cache, FlashAttention y speculative decoding atacan cuellos distintos",
            ],
            "keys": [
                "La cuantización reduce precisión y memoria; su efecto en calidad depende del dominio y del método.",
                "La destilación copia comportamiento en un dominio, no conocimiento general.",
                "La caché de claves y valores acelera la generación a cambio de memoria.",
                "Mide TTFT, throughput y memoria por separado antes de elegir una técnica.",
            ],
            "example": "Un servicio con un modelo de 7B en 16 bits necesita dos GPU. Al cuantizar a 4 bits, cabe en una y el coste por hora baja casi a la mitad. La evaluación muestra una caída mínima en preguntas generales, pero un fallo nuevo en preguntas que exigen fechas exactas. El equipo añade una comprobación de fechas contra el contexto antes de responder.",
            "caution": "Optimizar solo con perplejidad oculta fallos en tareas específicas. La perplejidad promedio puede mejorar mientras las respuestas útiles empeoran.",
            "search": "inferencia cuantización 8 bits 4 bits GPTQ AWQ bitsandbytes destilación poda modelo pequeño KV cache FlashAttention speculative decoding vLLM throughput",
        },
        {
            "id": "llm6l3",
            "lnum": 3,
            "title": "Elegir modelo y hardware: coste, latencia y calidad",
            "minutes": 7,
            "lead": "No existe «el mejor modelo», solo el mejor equilibrio para un producto. La decisión combina calidad en tu dominio, tiempo de respuesta, coste por petición y capacidad de operar el sistema. Los benchmarks generales orientan; la evaluación propia decide.",
            "diagram": ("flow", ["Calidad", "Latencia", "Coste", "Decisión"]),
            "caption": "Los tres vértices se miden con el mismo conjunto de casos y se ponderan según el producto, no según la moda.",
            "sections": [
                {
                    "h": "Del benchmark a tu dominio",
                    "p": [
                        "Los benchmarks públicos permiten descartar modelos que no saben razonar o que fallan en código, pero no dicen cómo se comportará un modelo en tu corpus. Un modelo puede liderar una tabla general y perder frente a uno más pequeño en preguntas sobre normativa interna, porque el pequeño fue ajustado con ese vocabulario.",
                        "La comparación justa usa el mismo prompt, la misma temperatura, el mismo contexto y el mismo juez. Si cambias una variable, cambias el resultado. Guarda las respuestas crudas, no solo las puntuaciones: los promedios esconden patrones que una lectura de veinte ejemplos revela.",
                        "Incluye en la comparación el coste de la recuperación, no solo el de la generación. Un modelo barato que necesita contextos largos puede salir más caro que uno que responde con menos tokens. Y un modelo lento puede destruir la experiencia aunque sea más preciso.",
                    ],
                },
                {
                    "h": "Latencia, throughput y capacidad",
                    "p": [
                        "El tiempo hasta el primer token —TTFT— es lo que el usuario percibe como velocidad de arranque. Los tokens por segundo determinan cuánto tarda en completarse la respuesta. El throughput mide cuántas peticiones atiende el sistema por unidad de tiempo. Un chat interactivo prioriza TTFT y fluidez; un proceso por lotes prioriza throughput.",
                        "La memoria necesaria no depende solo de los parámetros. La caché de claves y valores crece con la longitud del contexto y el número de peticiones concurrentes. Un modelo que cabe en una GPU con contexto corto puede no caber con contextos largos o con diez usuarios simultáneos. Calcula el peor caso, no el promedio.",
                        "El escalado automático añade instancias cuando sube la carga, pero tarda en arrancar. Para picos previsibles, conviene mantener capacidad de reserva; para picos raros, aceptar algo de cola. El autoscaling no sustituye a un límite de concurrencia ni a una cola bien diseñada.",
                    ],
                },
                {
                    "h": "Diseñar el equilibrio",
                    "p": [
                        "Una estrategia útil es la cascada: un modelo pequeño responde primero; si la confianza es baja o la pregunta es compleja, se deriva a uno grande. Otra es el enrutamiento por tipo de tarea: código a un modelo, prosa a otro, clasificación a un tercero. Ambas reducen coste medio sin bajar la calidad en los casos difíciles.",
                        "El SLA debe escribirse antes de elegir hardware: latencia objetivo, disponibilidad, coste máximo por petición y comportamiento ante fallos. Si el SLA dice «menos de dos segundos para el primer token», el modelo y la infraestructura se eligen bajo esa restricción. Si no hay SLA, cualquier discusión sobre modelos es abstracta.",
                        "Por último, reserva margen para crecer. Un sistema al 90 % de memoria y al 80 % de CPU no tiene espacio para un pico ni para una versión más grande. La capacidad ociosa no es desperdicio: es la diferencia entre responder y caerse el día del lanzamiento.",
                    ],
                },
            ],
            "brief": [
                "Benchmarks orientan; tu conjunto decide",
                "TTFT, tokens/s y throughput miden cosas distintas",
                "Cascadas y enrutamiento reducen coste medio",
            ],
            "keys": [
                "La comparación de modelos debe usar el mismo prompt, contexto y juez.",
                "La memoria crece con contexto y concurrencia, no solo con los parámetros.",
                "Un SLA escrito antes de elegir hardware evita decisiones abstractas.",
                "Cascadas y enrutamiento permiten gastar más solo cuando hace falta.",
            ],
            "example": "Un asistente de soporte recibe 10.000 preguntas al día. El 70 % son FAQ que un modelo de 3B responde bien; el 30 % restante se enruta a un modelo mayor. El coste medio baja un 60 % y la calidad en los casos difíciles se mantiene, porque la derivación se decide con una señal de confianza y se evalúa por separado.",
            "caution": "Elegir hardware por el modelo más grande que te gustaría usar lleva a pagar por capacidad que no aprovechas. Empieza por el SLA y por el modelo más pequeño que cumple.",
            "search": "benchmark dominio latencia TTFT tokens por segundo throughput memoria KV cache concurrencia autoscaling cascada enrutamiento SLA coste",
        },
    ],
    "quiz": {
        "id": "llm6q",
        "title": "Cierre del módulo 06",
        "summary": [
            "La evaluación separa recuperación, generación y producto, con un golden set reservado.",
            "La fidelidad comprueba que la respuesta se apoya en el contexto recuperado.",
            "La cuantización, la destilación y las técnicas de generación optimizan cosas distintas.",
            "El equilibrio entre calidad, latencia y coste se decide con el SLA y la evaluación propia.",
        ],
        "questions": [
            {
                "q": "¿Qué mide la fidelidad en un sistema RAG?",
                "options": [
                    "La velocidad de la base vectorial",
                    "Si la respuesta se apoya en el contexto recuperado",
                    "El número de documentos en el índice",
                    "La longitud media del prompt",
                ],
                "answer": 1,
                "why": "La fidelidad detecta afirmaciones que no están respaldadas por las fuentes incluidas en el contexto.",
            },
            {
                "q": "¿Qué técnica reduce la memoria del modelo cambiando la precisión de sus pesos?",
                "options": [
                    "Reranking",
                    "Cuantización",
                    "Chunking",
                    "Búsqueda híbrida",
                ],
                "answer": 1,
                "why": "La cuantización almacena pesos en menos bits, reduciendo la huella de memoria a cambio de posible pérdida de calidad.",
            },
            {
                "q": "¿Por qué no basta con un benchmark público para elegir modelo?",
                "options": [
                    "Porque los benchmarks no se actualizan",
                    "Porque no reflejan el dominio, el corpus ni las restricciones del producto",
                    "Porque solo miden modelos de código abierto",
                    "Porque siempre favorecen al modelo más grande",
                ],
                "answer": 1,
                "why": "El benchmark mide tareas generales; la decisión depende del rendimiento en tus casos, tu latencia y tu coste.",
            },
        ],
        "exercises": [
            "Define el golden set de tu sistema: treinta preguntas, respuestas esperadas y los documentos que deberían recuperarse.",
            "Calcula la memoria aproximada de un modelo de 7B en 16, 8 y 4 bits, y añade una estimación de la caché para 4.000 tokens.",
            "Escribe un SLA para tu producto y explica qué modelo y qué infraestructura elegirías bajo esa restricción.",
        ],
        "search": "evaluación cierre fidelidad golden set recuperación cuantización destilación KV cache TTFT throughput SLA coste latencia",
    },
}
