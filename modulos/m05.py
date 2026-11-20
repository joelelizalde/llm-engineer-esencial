MODULE = {
    "num": "05",
    "title": "Ajuste fino supervisado",
    "sub": "Del dataset de instrucciones al modelo que sigue tu formato",
    "lessons": [
        {
            "id": "llm5l1",
            "lnum": 1,
            "title": "Construir un dataset de instrucciones",
            "minutes": 7,
            "lead": "El ajuste fino no empieza en el bucle de entrenamiento, sino en una tabla de ejemplos. Si esos ejemplos son pocos, repetitivos o inconsistentes, el modelo aprenderá exactamente eso. La calidad del dataset marca un techo que ningún hiperparámetro puede romper.",
            "diagram": ("flow", ["Documentos", "Plantillas", "Generar pares", "Filtrar"]),
            "caption": "Los documentos alimentan plantillas; un modelo genera pares; los filtros dejan solo ejemplos útiles y diversos.",
            "sections": [
                {
                    "h": "Qué es un par de instrucción",
                    "p": [
                        "Un ejemplo de ajuste supervisado tiene tres partes: una instrucción, una entrada opcional y una respuesta esperada. La instrucción describe la tarea; la entrada aporta el material; la respuesta muestra lo que el modelo debe producir. En un gemelo, la instrucción puede ser «responde como el autor» y la entrada una pregunta sobre un artículo.",
                        "La respuesta no debe ser un resumen genérico. Debe exhibir el comportamiento que quieres: estructura, longitud, tono, uso de ejemplos y forma de citar. Si el dataset contiene respuestas de estilos distintos, el modelo aprenderá una mezcla. La coherencia estilística importa más que el volumen.",
                        "También importa lo que no incluyes. Si todos los ejemplos son positivos y entusiastas, el modelo no sabrá mostrar desacuerdo. Si todos son largos, responderá largo incluso cuando la pregunta pida una línea. El dataset es un currículo: enseña lo que contiene y omite lo que no.",
                    ],
                },
                {
                    "h": "Generar ejemplos con un modelo más fuerte",
                    "p": [
                        "Una técnica práctica es usar un modelo grande para generar pares a partir de tus documentos. Se le da un fragmento y una plantilla, y se le pide que produzca preguntas plausibles con respuestas basadas solo en ese fragmento. Luego se filtran y se revisan. Así se escala la creación sin perder el anclaje en el corpus.",
                        "La generación sintética tiene riesgos conocidos: preguntas demasiado fáciles, respuestas que copian el fragmento, sesgos del modelo generador y errores factuales. Los filtros deben cubrir diversidad de tareas, longitud, dificultad y formato. Una muestra revisada a mano calibra el resto y detecta patrones repetidos.",
                        "La licencia del corpus y del modelo generador también cuenta. No es lo mismo generar ejemplos a partir de textos propios que de contenido de terceros con restricciones. Documenta la procedencia de cada ejemplo y evita mezclar datos que no puedes usar.",
                    ],
                },
                {
                    "h": "Formato, plantilla y particiones",
                    "p": [
                        "El dataset debe estar en el formato que espera el entrenador: JSONL con campos de instrucción, entrada y salida, o una lista de mensajes con roles. La plantilla de chat convierte esos mensajes en una secuencia con marcadores de sistema, usuario y asistente. Esa plantilla debe ser exactamente la que se usará en inferencia.",
                        "Las particiones se hacen por documento, no por ejemplo, para evitar fugas. Si un artículo aparece en entrenamiento y otro fragmento del mismo artículo en validación, la métrica será optimista. Reserva también un conjunto de prueba que no se toque hasta el final y un conjunto de preguntas sin respuesta para evaluar la abstención.",
                        "El desbalance es otra trampa. Si el 80 % de los ejemplos son de un tema, el modelo se especializará en exceso. Muestrea por tema, por tipo de tarea y por longitud. Guarda las estadísticas del dataset junto con el modelo: sin ellas, comparar dos entrenamientos es comparar cajas negras.",
                    ],
                },
            ],
            "brief": [
                "Instrucción, entrada y respuesta coherentes en estilo",
                "La generación sintética se filtra y se revisa",
                "Particiones por documento y plantilla de chat única",
            ],
            "keys": [
                "El dataset define el comportamiento que el modelo puede aprender; el algoritmo solo lo ajusta.",
                "Los ejemplos sintéticos necesitan diversidad, verificación factual y revisión humana.",
                "La plantilla de chat debe coincidir entre entrenamiento e inferencia.",
                "Particionar por documento evita fugas y métricas engañosas.",
            ],
            "example": "Un equipo genera 1.200 pares a partir de 80 artículos. Al revisar, descubre que 400 empiezan con «En este artículo…», un patrón del generador. Los elimina, reequilibra temas y añade 60 respuestas cortas. El modelo final deja de imitar la muletilla y responde con longitudes más variadas.",
            "caution": "Entrenar con respuestas generadas por un modelo y evaluar con el mismo modelo produce una puntuación alta que no refleja la calidad real. Usa jueces distintos y revisión humana.",
            "search": "dataset instrucciones par instrucción entrada respuesta generación sintética filtros diversidad plantilla chat JSONL particiones fuga documento desbalance",
        },
        {
            "id": "llm5l2",
            "lnum": 2,
            "title": "SFT en la práctica: LoRA, QLoRA y paciencia",
            "minutes": 8,
            "lead": "El ajuste supervisado toma un modelo que sabe continuar texto y le enseña a seguir instrucciones con un formato concreto. En la práctica, la diferencia entre un ajuste útil y uno que arruina el modelo está en detalles poco vistosos: qué se enmascara en la pérdida, cuántas épocas se aguantan y qué se mide además de la pérdida.",
            "diagram": ("curve", {"x": "pasos", "y": "pérdida", "a": "entrenamiento", "b": "validación"}),
            "caption": "La pérdida de entrenamiento siempre baja; la de validación es la que avisa de que el modelo está memorizando.",
            "sections": [
                {
                    "h": "Ajuste completo, LoRA y QLoRA",
                    "p": [
                        "El ajuste completo actualiza todos los pesos. Da la máxima capacidad de adaptación y el máximo coste de memoria. Para modelos pequeños puede ser viable; para modelos de miles de millones de parámetros, exige varias GPU y un cuidado extremo con el estado del optimizador.",
                        "LoRA congela el modelo base e inserta matrices de bajo rango en determinadas capas. Solo se entrenan esas matrices, así que el estado del optimizador se reduce drásticamente y el adaptador resultante ocupa megabytes. El rango controla la capacidad: uno muy bajo aprende poco; uno muy alto se acerca al ajuste completo y pierde la ventaja.",
                        "QLoRA cuantiza el modelo base a 4 bits y entrena adaptadores LoRA encima. Permite ajustar modelos grandes en una sola GPU con memoria moderada. La contrapartida es algo de calidad y de velocidad, y una configuración más delicada. Para un gemelo personal, suele ser el punto de partida razonable.",
                    ],
                },
                {
                    "h": "Enmascarar, empaquetar y elegir épocas",
                    "p": [
                        "En el ajuste por instrucciones, la pérdida debe calcularse solo sobre los tokens de la respuesta, no sobre la instrucción ni el contexto. Si no se enmascara, el modelo aprende a predecir también el prompt y dedica capacidad a algo que en inferencia no genera. La máscara se construye a partir de la plantilla de chat.",
                        "El empaquetado —packing— une varios ejemplos cortos en una secuencia larga para aprovechar la GPU. Bien hecho, reduce el relleno y acelera; mal hecho, mezcla ejemplos y confunde la máscara. Si tu framework no lo soporta con claridad, empieza sin packing: es más lento, pero más fácil de depurar.",
                        "El número de épocas depende del dataset y del modelo. Con pocos ejemplos, una o dos épocas suelen bastar; más allá, el modelo memoriza y pierde generalidad. La pérdida de validación y, sobre todo, una evaluación cualitativa de respuestas son las señales que importan. Un modelo que repite literalmente frases del entrenamiento está sobreajustado, aunque su pérdida sea baja.",
                    ],
                },
                {
                    "h": "Olvido catastrófico y evaluación",
                    "p": [
                        "El ajuste fino puede degradar capacidades que el modelo ya tenía: seguir instrucciones generales, razonar, mantener el idioma. Es el olvido catastrófico. Se mitiga mezclando ejemplos generales con los específicos, usando tasas de aprendizaje bajas y adaptadores pequeños, y evaluando tareas que no forman parte del ajuste.",
                        "La evaluación no termina en la pérdida. Hay que revisar formato, tono, fidelidad al contexto, longitud, tasa de abstención y latencia. Un modelo ajustado que responde bien pero tarda el triple puede ser peor producto. Guarda muestras antes y después, y compáralas a ciegas cuando sea posible.",
                        "El adaptador se versiona junto con la plantilla, el dataset y la configuración. Un adaptador sin esa información es un archivo opaco. Y si el modelo base cambia, el adaptador puede no cargar o comportarse distinto: fija la revisión exacta del modelo base en la configuración.",
                    ],
                },
            ],
            "brief": [
                "LoRA entrena adaptadores; QLoRA añade cuantización",
                "Enmascara la pérdida y cuida el packing",
                "Mide olvido y calidad, no solo pérdida",
            ],
            "keys": [
                "LoRA reduce el coste porque congela el modelo base y entrena matrices pequeñas.",
                "QLoRA permite ajustar modelos grandes en menos memoria a cambio de configuración y algo de calidad.",
                "La pérdida debe calcularse sobre la respuesta, no sobre la instrucción.",
                "El sobreajuste se detecta con validación y con revisión de respuestas, no solo con la curva de entrenamiento.",
            ],
            "example": "Un equipo ajusta un modelo de 7B con QLoRA en una GPU de 24 GB. Usa rango 16, una época y una tasa de 2e-4. La pérdida de validación baja durante los primeros 300 pasos y luego sube. Se queda con el checkpoint de 300, no con el último, y recupera respuestas más naturales.",
            "caution": "Comparar adaptadores con la pérdida de entrenamiento es engañoso: un modelo que memoriza tiene pérdida casi cero y respuestas peores. Evalúa con datos que no vio.",
            "search": "SFT ajuste supervisado LoRA QLoRA rango adaptador enmascarar pérdida packing épocas sobreajuste olvido catastrófico checkpoint evaluación",
        },
        {
            "id": "llm5l3",
            "lnum": 3,
            "title": "Alineación con preferencias: DPO y alternativas",
            "minutes": 7,
            "lead": "El ajuste supervisado enseña a imitar ejemplos, pero no distingue entre una respuesta aceptable y una excelente. La alineación con preferencias añade esa comparación: dado un par de respuestas, el modelo aprende a preferir la que las personas eligen. Es el paso que pule el estilo y reduce respuestas que, sin ser falsas, no son útiles.",
            "diagram": ("flow", ["SFT", "Pares elegido/rechazado", "DPO", "Modelo alineado"]),
            "caption": "DPO parte de un modelo ya ajustado y aprende de comparaciones; no necesita un modelo de recompensa separado.",
            "sections": [
                {
                    "h": "Por qué hacen falta preferencias",
                    "p": [
                        "En SFT, cada pregunta tiene una respuesta «correcta». En la realidad, varias respuestas pueden ser correctas y distintas en calidad: una es más clara, otra más breve, otra cita mejor. Las preferencias capturan ese orden. Un par elegido-rechazado dice al modelo qué dirección mejorar sin fijar una única salida.",
                        "RLHF clásico entrena un modelo de recompensa con esas comparaciones y luego optimiza la política contra él. Es potente, pero añade un modelo, un bucle de optimización y riesgos de recompensa adversaria. DPO simplifica: usa los pares directamente para ajustar la política con una función que favorece el elegido y penaliza el rechazado.",
                        "La ventaja práctica de DPO es que se entrena como un ajuste supervisado, con pares y una referencia al modelo original para no alejarse demasiado. La desventaja es que depende de la calidad y la cobertura de los pares: si todos comparan longitud, el modelo aprenderá a escribir más largo, no mejor.",
                    ],
                },
                {
                    "h": "Construir pares que enseñen algo",
                    "p": [
                        "Un par útil tiene el mismo prompt y dos respuestas que difieren en un aspecto relevante: fidelidad, claridad, formato o seguridad. Si las diferencias son aleatorias, el modelo aprende ruido. Si todas favorecen respuestas largas, aprende a divagar. La diversidad de criterios es tan importante como la cantidad.",
                        "Los pares se pueden obtener de revisión humana, de comparaciones entre modelos o de un modelo juez con una rúbrica. La opción humana es la más fiable y la más cara; la automática escala, pero hereda sesgos. Una práctica razonable es generar con varios modelos, filtrar por criterios objetivos y revisar una muestra estratificada.",
                        "El desacuerdo entre anotadores es información, no un error. Si dos personas prefieren respuestas distintas, el par es ambiguo y probablemente no debería usarse para entrenar sin discusión. Guardar el acuerdo y el motivo de cada elección ayuda a auditar el dataset y a detectar criterios contradictorios.",
                    ],
                },
                {
                    "h": "DPO, ORPO y el arte de no pasarse",
                    "p": [
                        "DPO introduce un parámetro beta que controla cuánto puede alejarse el modelo del de referencia. Un beta alto limita el cambio; uno bajo permite adaptarse más y arriesga degeneración. Al igual que en SFT, el número de épocas y la tasa de aprendizaje importan: demasiadas vueltas sobre los mismos pares producen respuestas rígidas.",
                        "ORPO combina el ajuste supervisado y la preferencia en un solo objetivo, sin modelo de referencia. Es más simple de configurar y útil cuando no quieres mantener dos etapas. Otras variantes —KTO, IPO— cambian la forma de tratar los pares. Ninguna elimina la necesidad de evaluar con datos reservados.",
                        "El riesgo principal es optimizar la señal equivocada. Si el juez prefiere listas, el modelo hará listas; si prefiere seguridad, responderá «no puedo» a todo. La evaluación debe incluir casos donde el modelo anterior era mejor y comprobar que no se ha degradado la utilidad general. Alinear no es complacer.",
                    ],
                },
            ],
            "brief": [
                "Las preferencias ordenan respuestas, no solo las imitan",
                "Pares con diferencias relevantes y diversos en criterio",
                "DPO y ORPO simplifican RLHF, pero no lo sustituyen sin evaluación",
            ],
            "keys": [
                "Un par de preferencias comparte prompt y difiere en calidad, no en tema.",
                "DPO aprende directamente de pares y usa el modelo SFT como referencia.",
                "Beta, épocas y tasa controlan cuánto se aleja el modelo de su punto de partida.",
                "La alineación puede degradar utilidad general; evalúa también casos que no forman parte del ajuste.",
            ],
            "example": "Un gemelo responde con demasiada longitud. El equipo crea pares donde la respuesta breve y precisa es la elegida y la versión larga y repetitiva es la rechazada, manteniendo el mismo contenido. Tras DPO con beta moderado, la longitud media baja un 30 % sin perder fidelidad en el conjunto de prueba.",
            "caution": "Si todos los pares premian el mismo rasgo superficial, el modelo aprende ese atajo. Varía criterios y revisa qué está aprendiendo realmente.",
            "search": "alineación preferencias RLHF DPO ORPO beta pares elegido rechazado modelo recompensa longitud sesgo evaluación utilidad",
        },
    ],
    "quiz": {
        "id": "llm5q",
        "title": "Cierre del módulo 05",
        "summary": [
            "El dataset de instrucciones define estilo, formato y cobertura; los filtros evitan ruido y repetición.",
            "LoRA y QLoRA reducen el coste del ajuste; la máscara y las épocas deciden si el resultado es útil.",
            "La pérdida no basta: hay que evaluar respuestas, olvido y abstención.",
            "DPO y ORPO aprenden de pares de preferencias y requieren pares diversos y una evaluación honesta.",
        ],
        "questions": [
            {
                "q": "¿Sobre qué tokens debe calcularse la pérdida en un ajuste por instrucciones?",
                "options": [
                    "Sobre todos los tokens de la secuencia",
                    "Sobre los tokens de la respuesta esperada",
                    "Solo sobre el primer token",
                    "Sobre los tokens del sistema y del usuario",
                ],
                "answer": 1,
                "why": "El modelo debe aprender a generar la respuesta; incluir instrucción y contexto en la pérdida desvía capacidad hacia texto que no se genera.",
            },
            {
                "q": "¿Qué ventaja ofrece QLoRA frente a LoRA?",
                "options": [
                    "Elimina la necesidad de datos",
                    "Permite ajustar modelos grandes con menos memoria al cuantizar el base",
                    "Garantiza que no haya olvido catastrófico",
                    "Hace innecesaria la evaluación",
                ],
                "answer": 1,
                "why": "QLoRA mantiene el base en 4 bits y entrena adaptadores, reduciendo la memoria necesaria para modelos grandes.",
            },
            {
                "q": "¿Qué hace DPO con un par elegido-rechazado?",
                "options": [
                    "Entrena un modelo de recompensa separado y luego lo usa",
                    "Ajusta la política para favorecer el elegido y alejarse del rechazado",
                    "Borra el rechazado del dataset de preentrenamiento",
                    "Cambia el tokenizador para que el elegido sea más probable",
                ],
                "answer": 1,
                "why": "DPO optimiza directamente la política con pares, usando el modelo de referencia para limitar la desviación; no necesita un reward model aparte.",
            },
        ],
        "exercises": [
            "Diseña una plantilla de instrucción para tu gemelo con tres tipos de tarea y un ejemplo de cada una.",
            "Explica cómo detectarías sobreajuste en un adaptador si solo tuvieras la curva de pérdida y una muestra de respuestas.",
            "Escribe cinco pares de preferencias con criterios distintos y señala qué atajo podría aprender el modelo de cada uno.",
        ],
        "search": "evaluación cierre dataset instrucciones SFT LoRA QLoRA máscara packing DPO ORPO preferencias alineación sobreajuste",
    },
}
