#!/usr/bin/env python3
"""Genera el PDF de «Ingeniería de LLM · Edición esencial» con WeasyPrint.

Uso:
    python3 build_pdf.py

Requiere WeasyPrint (probado con 70.x). Escribe el PDF en la raíz del proyecto.
"""

import os
from contenido import COURSE, GLOSARIO, MODULES
from build_site import render_diagram, esc, slug, TOTAL

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, COURSE["pdf"])

CSS = r"""
@font-face{font-family:Fraunces;src:url(assets/fonts/Fraunces-500.ttf);font-weight:500}
@font-face{font-family:Fraunces;src:url(assets/fonts/Fraunces-700.ttf);font-weight:700}
@font-face{font-family:Inter;src:url(assets/fonts/Inter-400.ttf);font-weight:400}
@font-face{font-family:Inter;src:url(assets/fonts/Inter-500.ttf);font-weight:500}
@font-face{font-family:Inter;src:url(assets/fonts/Inter-600.ttf);font-weight:600}
@font-face{font-family:Inter;src:url(assets/fonts/Inter-700.ttf);font-weight:700}

@page{
  size:A4;
  margin:18mm 18mm 18mm;
  @top-left{content:string(chapter);font:500 7.5pt Inter;letter-spacing:.12em;text-transform:uppercase;color:#8a7f6d}
  @top-right{content:"Ingeniería de LLM · Edición esencial";font:500 7.5pt Inter;letter-spacing:.06em;color:#8a7f6d}
  @bottom-center{content:counter(page);font:500 8.5pt Inter;color:#6f6555}
}
@page cover{margin:0;@top-left{content:none}@top-right{content:none}@bottom-center{content:none}}
@page front{margin:22mm 20mm;@top-left{content:none}@top-right{content:none}}

html{font-family:Inter;font-size:9.4pt;line-height:1.52;color:#2b261f}
body{margin:0}
a{color:#a83b16;text-decoration:none}
h1,h2,h3,h4{font-family:Fraunces;font-weight:500;letter-spacing:-.01em;color:#18140f}
p{margin:0 0 .7em;orphans:3;widows:3}
strong{font-weight:600;color:#18140f}
em{font-style:italic}
ul,ol{margin:0 0 .8em;padding-left:1.2em}
li{margin:.2em 0}

/* Portada */
.cover{page:cover;height:297mm;background:#18140f;color:#f5f1e8;padding:26mm 22mm;box-sizing:border-box;position:relative;page-break-after:always}
.cover .mark{width:16mm;height:16mm;border:1px solid #c9481b;border-radius:2.5mm;display:flex;align-items:center;justify-content:center;font-family:Fraunces;font-weight:700;font-size:15pt;color:#f5f1e8}
.cover .eyebrow{margin-top:12mm;font:600 8pt Inter;letter-spacing:.22em;text-transform:uppercase;color:#d9a184}
.cover h1{font-size:44pt;line-height:1.0;color:#f5f1e8;margin:8mm 0 6mm;letter-spacing:-.03em}
.cover h1 em{font-style:italic;color:#e86f3f}
.cover .lede{font-size:12pt;line-height:1.6;color:#cfc5b3;max-width:120mm}
.cover .book{margin-top:8mm;font-size:9.5pt;color:#a99d88;max-width:120mm}
.cover .book em{color:#e9e1d1}
.cover .foot{position:absolute;left:22mm;right:22mm;bottom:22mm;border-top:1px solid rgba(255,255,255,.16);padding-top:5mm;display:flex;justify-content:space-between;font:500 8pt Inter;letter-spacing:.12em;text-transform:uppercase;color:#9b8f7b}
.cover .stats{display:flex;gap:12mm;margin-top:14mm}
.cover .stats b{display:block;font-family:Fraunces;font-size:22pt;font-weight:500;color:#f5f1e8;line-height:1}
.cover .stats span{font:500 7.5pt Inter;letter-spacing:.14em;text-transform:uppercase;color:#9b8f7b}

/* Portadilla / índice */
.front{page:front}
.front h1{font-size:30pt;margin:0 0 4mm}
.front .kicker{font:600 8pt Inter;letter-spacing:.2em;text-transform:uppercase;color:#c9481b}
.front .intro{font-size:10pt;color:#5b5244;max-width:140mm;margin-bottom:6mm;line-height:1.5}
.toc-grid{columns:2;column-gap:11mm}
.toc-mod{margin:0 0 3.4mm;break-inside:avoid}
.toc-mod .mh{display:flex;gap:4mm;align-items:baseline;border-bottom:1px solid #d8ccb8;padding-bottom:.8mm;margin-bottom:.8mm}
.toc-mod .mh b{font-family:Fraunces;font-size:13pt;color:#c9481b;font-weight:500}
.toc-mod .mh span{font-weight:600;font-size:10.5pt;color:#18140f}
.toc-row{display:flex;gap:3mm;font-size:8.8pt;color:#3a342b;padding:.3mm 0;line-height:1.35}
.toc-row .n{font-family:Inter;font-size:8pt;color:#8a7f6d;min-width:8mm}
.toc-row .t{flex:1}
.toc-row .t em{font-style:italic;color:#6f6555}
.toc-row a{margin-left:auto}
.toc-row a::after{content:target-counter(attr(href),page);font-size:8pt;color:#8a7f6d}

/* Lecciones */
.chapter{break-before:page}
.kicker{display:flex;align-items:center;gap:3mm;font:600 8pt Inter;letter-spacing:.18em;text-transform:uppercase;color:#c9481b;margin-bottom:3mm}
.kicker::before{content:"";display:inline-block;width:8mm;height:.4mm;background:#c9481b}
.chapter h1{font-size:24pt;line-height:1.06;margin:0 0 3mm;string-set:chapter content();letter-spacing:-.02em}
.meta{display:flex;gap:6mm;font:500 7.5pt Inter;letter-spacing:.1em;text-transform:uppercase;color:#8a7f6d;border-top:1px solid #d8ccb8;border-bottom:1px solid #d8ccb8;padding:1.8mm 0;margin-bottom:5mm}
.lead{font-size:10.3pt;line-height:1.56;color:#3a342b;margin-bottom:1em}

.brief{background:#f3eee3;border-left:2px solid #c9481b;padding:3mm 4mm;margin:4mm 0 5mm;break-inside:avoid}
.brief .k{font:600 7.5pt Inter;letter-spacing:.16em;text-transform:uppercase;color:#8a7f6d;margin-bottom:2mm}
.brief ul{columns:2;column-gap:8mm;margin:0;padding-left:4mm;font-size:9pt;color:#3a342b}

figure.diagram{margin:3mm 0 3.5mm;padding:2.6mm;background:#fffdf7;border:1px solid #ddd2bf;border-radius:2mm;break-inside:avoid}
figure.diagram svg{width:100%;height:auto}
figcaption{font-size:8pt;color:#786e5e;border-top:1px solid #e4dac8;margin-top:2mm;padding-top:2mm;line-height:1.45}

h2.sec{font-size:15pt;margin:5.5mm 0 2mm;padding-top:2.5mm;border-top:1px solid #e0d5c2;break-after:avoid}
h2.sec .sn{display:block;font:600 7.5pt Inter;letter-spacing:.18em;color:#c9481b;margin-bottom:1.5mm}
.body p{font-size:9.4pt;line-height:1.55;color:#2b261f;margin-bottom:.6em}

.box{margin:4mm 0;padding:3mm 4mm;border-radius:2mm;break-inside:avoid}
.extras{display:flex;gap:4mm;margin:3.4mm 0;break-inside:avoid}
.extras .box{flex:1;margin:0}
.box h3{font-family:Inter;font-weight:600;font-size:8.2pt;letter-spacing:.14em;text-transform:uppercase;margin:0 0 1.6mm}
.box ul{margin:0;padding-left:4mm;font-size:8.8pt}
.box p{margin:0;font-size:9pt;line-height:1.5}
.keys{background:#eef3f1;border:1px solid #cfe0db}
.keys h3{color:#0d6a61}
.example{background:#f7f2e6;border:1px solid #e2d6bf}
.example h3{color:#8a6a24}
.caution{background:#fbeee8;border:1px solid #efd3c6}
.caution h3{color:#a83b16}

/* Evaluación */
.quiz-q{border-top:1px solid #e0d5c2;padding-top:2mm;margin-top:2.2mm;break-inside:avoid}
.quiz-q .qq{font-weight:600;font-size:9.4pt;margin-bottom:1.2mm}
.quiz-q .qn{font:600 8pt Inter;letter-spacing:.1em;color:#c9481b;margin-right:2mm}
.quiz-q ol{list-style:none;padding:0;margin:0;font-size:9pt;line-height:1.45;color:#3a342b}
.quiz-q ol li{margin:.35mm 0;padding-left:6mm;position:relative}
.quiz-q ol li::before{content:attr(data-letter);position:absolute;left:0;font:600 8pt Inter;color:#8a7f6d}
.answers{margin-top:4mm;padding:3mm 4mm;background:#f3eee3;border:1px solid #ddd2bf;break-inside:avoid;columns:2;column-gap:6mm}
.answers h3{font:600 8pt Inter;letter-spacing:.16em;text-transform:uppercase;color:#8a7f6d;margin:0 0 1.6mm;column-span:all}
.answers p{font-size:8.4pt;line-height:1.45;margin:0 0 1.5mm;break-inside:avoid}
.answers b{color:#a83b16}
.exercise{margin-top:4mm;break-inside:avoid}
.exercise h3{font:600 8pt Inter;letter-spacing:.16em;text-transform:uppercase;color:#8a7f6d;margin:0 0 1.5mm}
.exercise ol{font-size:8.8pt;line-height:1.45;color:#3a342b;margin-bottom:0}

/* Glosario */
.gloss{margin-top:3mm}
.gloss .term{break-inside:avoid;border-bottom:1px solid #ebe2d2;padding:2.2mm 0}
.gloss h3{font-family:Inter;font-weight:600;font-size:9.8pt;margin:0 0 .6mm}
.gloss p{margin:0;font-size:9.2pt;color:#4a4338}
"""


def cover():
    hours = ("%.1f" % (sum(l["minutes"] for m in MODULES for l in m["lessons"]) / 60)).replace(".", ",")
    return f'''<section class="cover">
  <div class="mark">LE</div>
  <div class="eyebrow">Edición esencial · Español · {COURSE["year"]}</div>
  <h1>Un gemelo<br>digital,<br>de punta a <em>punta</em>.</h1>
  <p class="lede">{esc(COURSE["description"])}</p>
  <p class="book">Basado en los temas de <em>{esc(COURSE["book"])}</em>, de {esc(COURSE["author"])}. Texto y diagramas originales: no reproduce el libro.</p>
  <div class="stats">
    <div><b>{sum(len(m["lessons"]) for m in MODULES)}</b><span>Lecciones</span></div>
    <div><b>{len(MODULES)}</b><span>Módulos</span></div>
    <div><b>{hours}</b><span>Horas</span></div>
    <div><b>{sum(1 for m in MODULES for l in m["lessons"] if l.get("diagram"))}</b><span>Diagramas</span></div>
  </div>
  <div class="foot"><span>{esc(COURSE["title"])} · {esc(COURSE["subtitle"])}</span><span>Manual en PDF</span></div>
</section>'''


def front():
    parts = [f'''<section class="front">
  <div class="kicker">Manual esencial</div>
  <h1>Contenido</h1>
  <p class="intro">Siete módulos que siguen el recorrido del libro: el gemelo digital y la arquitectura FTI, las herramientas, la ingeniería de datos, el pipeline RAG, el ajuste fino, la evaluación y la optimización, y por último el despliegue y LLMOps. Cada módulo cierra con una evaluación y ejercicios.</p>
''']
    parts.append('<div class="toc-grid">')
    for m in MODULES:
        parts.append('<div class="toc-mod"><div class="mh">'
                     f'<b>{m["num"]}</b><span>{esc(m["title"])}</span></div>')
        for l in m["lessons"]:
            parts.append(f'<div class="toc-row"><span class="n">{m["num"]}.{l["lnum"]}</span>'
                         f'<span class="t">{esc(l["title"])}</span><a href="#{l["id"]}"></a></div>')
        q = m["quiz"]
        parts.append(f'<div class="toc-row"><span class="n">{m["num"]}.{len(m["lessons"]) + 1}</span>'
                     f'<span class="t"><em>{esc(q["title"])}</em></span><a href="#{q["id"]}"></a></div>')
        parts.append('</div>')
    parts.append('<div class="toc-mod"><div class="mh"><b>—</b><span>Glosario</span></div>'
                 '<div class="toc-row"><span class="n"></span><span class="t">Términos del curso</span><a href="#glosario"></a></div></div>')
    parts.append('</div></section>')
    return "\n".join(parts)


def lesson_html(m, l):
    out = [f'<section class="chapter" id="{l["id"]}">']
    out.append(f'<div class="kicker">Módulo {m["num"]} · Lección {l["lnum"]} de {len(m["lessons"])}</div>')
    out.append(f'<h1>{esc(l["title"])}</h1>')
    out.append(f'<div class="meta"><span>{l["minutes"]} min de lectura</span><span>{len(l["sections"])} apartados</span><span>{esc(m["title"])}</span></div>')
    out.append(f'<p class="lead">{esc(l["lead"])}</p>')
    out.append('<div class="brief"><div class="k">En esta lección</div><ul>'
               + ''.join(f'<li>{esc(b)}</li>' for b in l["brief"]) + '</ul></div>')
    out.append(render_diagram(l["diagram"], l.get("caption", "")))
    out.append('<div class="body">')
    for i, sec in enumerate(l["sections"], 1):
        out.append(f'<h2 class="sec"><span class="sn">{i:02d}</span>{esc(sec["h"])}</h2>')
        for p in sec["p"]:
            out.append(f'<p>{esc(p)}</p>')
    out.append('</div>')
    out.append('<div class="box keys"><h3>Ideas clave</h3><ul>'
               + ''.join(f'<li>{esc(k)}</li>' for k in l["keys"]) + '</ul></div>')
    out.append('<div class="extras">')
    out.append(f'<div class="box example"><h3>Caso concreto</h3><p>{esc(l["example"])}</p></div>')
    out.append(f'<div class="box caution"><h3>Cuidado</h3><p>{esc(l["caution"])}</p></div>')
    out.append('</div>')
    out.append('</section>')
    return "\n".join(out)


def quiz_html(m, q):
    letters = "abcd"
    out = [f'<section class="chapter" id="{q["id"]}">']
    out.append(f'<div class="kicker">Módulo {m["num"]} · Evaluación</div>')
    out.append(f'<h1>{esc(q["title"])}</h1>')
    out.append('<div class="meta"><span>10 min</span>'
               f'<span>{len(q["questions"])} preguntas</span><span>2 de 3 para aprobar</span></div>')
    out.append('<div class="body quiz-summary">')
    for p in q["summary"]:
        out.append(f'<p>{esc(p)}</p>')
    out.append('</div>')
    for qi, question in enumerate(q["questions"], 1):
        out.append('<div class="quiz-q">')
        out.append(f'<p class="qq"><span class="qn">{qi:02d}</span>{esc(question["q"])}</p>')
        out.append('<ol>' + ''.join(
            f'<li data-letter="{letters[oi]})">{esc(opt)}</li>'
            for oi, opt in enumerate(question["options"])) + '</ol>')
        out.append('</div>')
    out.append('<div class="answers"><h3>Respuestas y explicaciones</h3>')
    for qi, question in enumerate(q["questions"], 1):
        correct = letters[question["answer"]]
        out.append(f'<p><b>{qi:02d} · {correct})</b> {esc(question["why"])}</p>')
    out.append('</div>')
    out.append('<div class="exercise"><h3>Ejercicios para practicar</h3><ol>'
               + ''.join(f'<li>{esc(e)}</li>' for e in q["exercises"]) + '</ol></div>')
    out.append('</section>')
    return "\n".join(out)


def glossary_html():
    terms = sorted(GLOSARIO, key=lambda t: slug(t[0]))
    out = ['<section class="chapter" id="glosario">',
           '<div class="kicker">Referencia rápida</div>',
           '<h1>Glosario</h1>',
           '<p class="lead">Los términos que aparecen una y otra vez en el curso, explicados en una frase.</p>',
           '<div class="gloss">']
    for term, definition, _lid in terms:
        out.append(f'<div class="term"><h3>{esc(term)}</h3><p>{esc(definition)}</p></div>')
    out.append('</div></section>')
    return "\n".join(out)


def build():
    body = [cover(), front()]
    for m in MODULES:
        for l in m["lessons"]:
            body.append(lesson_html(m, l))
        body.append(quiz_html(m, m["quiz"]))
    body.append(glossary_html())
    doc = f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<title>{esc(COURSE["title"])} · {esc(COURSE["subtitle"])}</title>
<style>{CSS}</style></head>
<body>
{"".join(body)}
</body></html>'''
    from weasyprint import HTML
    HTML(string=doc, base_url=ROOT + "/").write_pdf(OUT)
    size = os.path.getsize(OUT) / 1024
    print(f"PDF generado: {OUT} ({size:.0f} KB)")


if __name__ == "__main__":
    build()
