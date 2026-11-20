# Ingeniería de LLM — Edición esencial en español

Manual de estudio estático (sin build para el lector y sin dependencias en el navegador) para diseñar, construir y operar un sistema LLM de principio a fin.
Alineado temáticamente con *LLM Engineer's Handbook*, de Paul Iusztin y Maxime Labonne, pero con texto, ejemplos y diagramas originales.

## Qué incluye

- **21 lecciones** en **7 módulos** (3 lecciones y 1 evaluación por módulo), siguiendo el recorrido del libro: gemelo digital y arquitectura FTI → herramientas → datos → RAG → ajuste fino → evaluación → despliegue y LLMOps.
- Lectura continua: botón «Completar y seguir», navegación con ← y →, temario lateral siempre disponible.
- **7 evaluaciones** de 3 preguntas con explicaciones y **21 ejercicios** aplicados.
- Progreso guardado en `localStorage`, glosario con buscador y modo claro/oscuro.
- Buscador global con atajo `⌘K` / `Ctrl+K`.
- **21 diagramas originales** en SVG (flujo, capas, bucle, curvas y barras).
- Manual en PDF: `Ingenieria-de-LLM-Esencial.pdf` (57 páginas).
- Tipografías locales (Fraunces + Inter), sin depender de Google Fonts.

## Estructura

```
index.html                     Portada y temario completo
llm1l1.html … llm7q.html       21 lecciones y 7 evaluaciones
glosario.html                  Glosario con búsqueda y filtro por letra
progreso.html                  Progreso por módulo
css/curso.css                  Diseño editorial responsive
js/curso.js                    Navegación, progreso, búsqueda y quizzes
assets/fonts/                  Tipografías locales
modulos/m01.py … m07.py        Contenido de cada módulo
contenido.py                   Reúne módulos, metadatos y glosario
build_site.py                  Generador del sitio
build_pdf.py                   Generador del PDF (WeasyPrint)
Ingenieria-de-LLM-Esencial.pdf
```

## Regenerar

```bash
python3 build_site.py          # solo el sitio
python3 build_site.py --pdf    # sitio + manual en PDF
```

El PDF se compone con WeasyPrint (probado con 70.x) a partir del mismo contenido y las mismas fuentes.

## Añadir o editar contenido

Cada módulo vive en `modulos/mNN.py` y expone un diccionario `MODULE`:

- `num`, `title`, `sub`
- `lessons`: lista de lecciones con `id`, `lnum`, `title`, `minutes`, `lead`, `diagram`, `caption`, `sections`, `brief`, `keys`, `example`, `caution`, `search`.
- `quiz`: `id`, `title`, `summary`, `questions`, `exercises`, `search`.

Los diagramas se declaran como tuplas: `("flow", [...])`, `("stack", [...])`, `("loop", [...])`, `("attention", [...])`, `("matrix", {...})`, `("curve", {...})` o `("bars", [...])`.
Al cambiar contenido, vuelve a ejecutar `build_site.py --pdf` para regenerar páginas y PDF.

## Atajos

| Tecla | Acción |
|---|---|
| ← / → | Lección anterior / siguiente |
| `C` | Marcar la lección actual como completada |
| `/` o `⌘K` | Abrir el buscador |
| `Esc` | Cerrar buscador o menú |
| `?` | Recordatorio de atajos |

## Publicar en GitHub Pages

1. Crea un repositorio con el contenido de esta carpeta en la raíz.
2. **Settings → Pages → Deploy from a branch → main → / (root)**.
3. El sitio quedará en `https://<usuario>.github.io/<repositorio>/`.

No subas claves ni tokens al repositorio: el curso es estático y no necesita credenciales.

## Créditos

Manual original de estudio en español, alineado con los temas de *LLM Engineer's Handbook* de Paul Iusztin y Maxime Labonne.
No reproduce el texto ni las figuras del libro. Uso educativo.
