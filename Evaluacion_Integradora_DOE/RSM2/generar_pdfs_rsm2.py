import html, subprocess, pathlib
from collections import Counter
from banco_rsm2 import P, S
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
aqui=pathlib.Path(__file__).parent
CSS="""
@page{size:A4 landscape;margin:12mm}
body{font-family:-apple-system,Helvetica,Arial,sans-serif;color:#1e293b;font-size:10.5px}
h1{font-size:20px;margin:0 0 4px;color:#4a235a} h2{font-size:14px;margin:16px 0 6px;color:#6c3483}
.sub{color:#64748b;margin-bottom:10px}
table{border-collapse:collapse;width:100%} th{background:#8e44ad;color:#fff;text-align:left;padding:5px 6px}
td{border-bottom:1px solid #e2e8f0;padding:5px 6px;vertical-align:top} tr{page-break-inside:avoid}
.ok{color:#1e8449;font-weight:700}.ctx{color:#b9770e;font-weight:700}.nv{color:#c0392b;font-weight:700}
.box{background:#f5eef8;border-left:4px solid #8e44ad;padding:8px 12px;margin:8px 0}
.n{font-size:9.5px;color:#475569}
.cards{display:flex;gap:10px;margin:8px 0}.card{flex:1;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:8px;text-align:center}
.card b{font-size:20px;display:block}
"""
def pdf(nombre,titulo,cuerpo):
    h=aqui/f"{nombre}.html"
    h.write_text(f"<!doctype html><meta charset=utf-8><title>{titulo}</title><style>{CSS}</style>{cuerpo}",encoding="utf-8")
    subprocess.run([CHROME,"--headless=new","--disable-gpu","--no-pdf-header-footer",f"--print-to-pdf={aqui/(nombre+'.pdf')}",h.as_uri()],check=True,capture_output=True)
    h.unlink()
e=html.escape
f="<h1>Evaluación RSM (Superficie de Respuesta, DCC) — Clave extraída del código fuente</h1>"
f+="<div class=sub>Campo <code>correcta</code> de cada pregunta en el HTML de la evaluación (maestro-jseferino.netlify.app, diseno-rsm2). Opción múltiple: índice → letra (0=A, 1=B, 2=C, 3=D). Cálculo: valor numérico con tolerancia ±0.5.</div>"
f+="<table><tr><th>#</th><th>Sección</th><th>Competencia</th><th>Pregunta (resumen)</th><th>Respuesta correcta en el código</th></tr>"
for p in P: f+=f"<tr><td>{p[0]}</td><td>{e(S[p[1]])}</td><td>{e(p[2])}</td><td>{e(p[3])}</td><td><b>{e(p[4])}</b></td></tr>"
f+="</table>"
mc=[p for p in P if not p[4][0].isdigit()]
c=Counter(p[4][0] for p in mc)
f+=f"<div class=box>{len(P)} preguntas en 4 secciones: {len(P)-len(mc)} de cálculo (18, 1.68, 10, 62.86) y {len(mc)} de opción múltiple. Letras correctas: "+", ".join(f"{k}: {v}" for k,v in sorted(c.items()))+".</div>"
pdf("1_Respuestas_codigo_fuente_RSM2","Clave RSM2",f)
n=Counter(p[7] for p in P)
f="<h1>Correlación: nuestras respuestas vs. clave del código fuente (RSM2)</h1>"
f+="<div class=sub>Respuestas propias a partir de la teoría de RSM/DCC vista y del contexto de cada sección. A diferencia de la evaluación 2^5, aquí no hay una calculadora ni datos con los que reproducir las cifras del artículo (CO2).</div>"
f+=f"<div class=cards><div class=card><b class=ok>{n['OK']}</b>Coinciden (teoría/contexto)</div><div class=card><b class=ctx>{n['CTX']}</b>Coinciden, sólo por el contexto</div><div class=card><b class=nv>{n['NV']}</b>Sin respuesta propia</div><div class=card><b>{n['OK']+n['CTX']}/{len(P)}</b>Respuestas iguales a la clave</div></div>"
f+="<h2>Detalle por pregunta</h2><table><tr><th>#</th><th>Pregunta</th><th>Clave del código</th><th>Nuestra respuesta</th><th>Razonamiento</th><th>Estado</th></tr>"
etq={"OK":'<span class=ok>✔ Coincide</span>',"CTX":'<span class=ctx>≈ Coincide*</span>',"NV":'<span class=nv>— No verificable</span>'}
for p in P:
    obs=f"<div class=n><b>Obs.:</b> {e(p[8])}</div>" if p[8] else ""
    f+=f"<tr><td>{p[0]}</td><td>{e(p[3])}</td><td>{e(p[4])}</td><td><b>{e(p[5])}</b></td><td>{e(p[6])}{obs}</td><td>{etq[p[7]]}</td></tr>"
f+="</table><h2>Hallazgos</h2>"
f+="""<div class=box><b>1. Cálculos (Q4, Q5, Q9):</b> 18, 1.68 y 10 se obtienen directamente (8+6+4; 8^0.25 = 1.6818; 18−8). Coinciden con la clave.</div>
<div class=box><b>2. Q13 (62.86):</b> es un dato del artículo; no se puede reproducir sin sus corridas, por lo que no hay respuesta propia.</div>
<div class=box><b>3. Q2:</b> la clave dice A; el contexto describe A y C como 'imponentes', así que sin el Pareto no se puede distinguir entre las dos.</div>
<div class=box><b>4. Coherencia del contexto:</b> con R²=0.9841, n=18 y 8 términos, R²aj≈0.970 (coincide con 0.9703) pero F≈69.6, no 19.03. Y Q9 usa 8 parámetros, cuando un cuadrático completo con k=3 tiene 10. No cambia ninguna respuesta, pero los números del enunciado no son totalmente consistentes entre sí.</div>
<div class=box><b>5. Q7:</b> el R² ajustado no es estrictamente 'porcentaje de variabilidad explicada', pero A es la única opción defendible.</div>
<p class=n>* ≈ Coincide: misma opción que la clave, pero sostenida sólo por el texto del contexto.</p>"""
pdf("2_Correlacion_respuestas_vs_codigo_RSM2","Correlación RSM2",f)
print(dict(n))
