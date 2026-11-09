import html, subprocess, pathlib
from banco import P, S
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
aqui=pathlib.Path(__file__).parent
CSS="""
@page{size:A4 landscape;margin:12mm}
body{font-family:-apple-system,Helvetica,Arial,sans-serif;color:#1e293b;font-size:10.5px}
h1{font-size:20px;margin:0 0 4px;color:#4a235a} h2{font-size:14px;margin:16px 0 6px;color:#6c3483}
.sub{color:#64748b;margin-bottom:10px}
table{border-collapse:collapse;width:100%} th{background:#8e44ad;color:#fff;text-align:left;padding:5px 6px}
td{border-bottom:1px solid #e2e8f0;padding:5px 6px;vertical-align:top} tr{page-break-inside:avoid}
.ok{color:#1e8449;font-weight:700}.dato{color:#b9770e;font-weight:700}.x{color:#c0392b;font-weight:700}
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
# ---------- PDF 1: clave del código fuente ----------
f=""
sec=None
f+="<h1>Evaluación Integradora DOE 2^5 y Fraccionados — Clave extraída del código fuente</h1>"
f+="<div class=sub>Valores del campo <code>correcta</code> de cada pregunta en el HTML de la evaluación. Opción múltiple: índice → letra (0=A, 1=B, 2=C, 3=D). Preguntas de cálculo: valor numérico con tolerancia ±0.5 (por defecto del código).</div>"
f+="<table><tr><th>#</th><th>Sección</th><th>Competencia</th><th>Pregunta (resumen)</th><th>Respuesta correcta en el código</th></tr>"
for p in P:
    f+=f"<tr><td>{p[0]}</td><td>{e(S[p[1]])}</td><td>{e(p[2])}</td><td>{e(p[3])}</td><td><b>{e(p[4])}</b></td></tr>"
f+="</table>"
mc=sum(1 for p in P if not p[4][0].isdigit()); nm=len(P)-mc
f+=f"<div class=box>{len(P)} preguntas: {nm} de cálculo (numéricas) y {mc} de opción múltiple. Distribución de letras correctas: "
from collections import Counter
c=Counter(p[4][0] for p in P if not p[4][0].isdigit()); f+=", ".join(f"{k}: {v}" for k,v in sorted(c.items()))+".</div>"
pdf("1_Respuestas_codigo_fuente","Clave código fuente",f)
# ---------- PDF 2: correlación ----------
ok=sum(1 for p in P if p[7]=="OK"); dato=sum(1 for p in P if p[7]=="DATO"); x=sum(1 for p in P if p[7]=="X")
f="<h1>Correlación: nuestras respuestas vs. clave del código fuente</h1>"
f+="<div class=sub>Nuestras respuestas se obtuvieron de los análisis hechos en la calculadora del profesor (pestaña Diseño Interactivo) y en los notebooks <code>Experimento_2k5_No_Replicado.ipynb</code> y <code>Experimento_2k5-1_Fraccion.ipynb</code>; después se compararon con la clave.</div>"
f+=f"<div class=cards><div class=card><b class=ok>{ok}</b>Coinciden sin reparos</div><div class=card><b class=dato>{dato}</b>Misma respuesta, dato citado no reproducible</div><div class=card><b class=x>{x}</b>No coinciden</div><div class=card><b>{ok+dato}/{len(P)}</b>Respuestas iguales a la clave</div></div>"
f+="<h2>Detalle por pregunta</h2><table><tr><th>#</th><th>Pregunta</th><th>Clave del código</th><th>Nuestra respuesta</th><th>Razonamiento y evidencia</th><th>Estado</th></tr>"
etq={"OK":'<span class=ok>✔ Coincide</span>',"DATO":'<span class=dato>≈ Coincide*</span>',"X":'<span class=x>✖ Difiere</span>'}
for p in P:
    obs=f"<div class=n><b>Obs.:</b> {e(p[8])}</div>" if p[8] else ""
    f+=f"<tr><td>{p[0]}</td><td>{e(p[3])}</td><td>{e(p[4])}</td><td><b>{e(p[5])}</b></td><td>{e(p[6])}{obs}</td><td>{etq[p[7]]}</td></tr>"
f+="</table>"
f+="""<h2>Hallazgos de la correlación</h2>
<div class=box><b>1. Sección 1 (Q1–Q5):</b> coinciden exactamente con la calculadora y los notebooks (SS_A = 1001.28, SS_B = 8877.78, SS_AB = 586.53, SS_error = 102.25, 16 g.l.).</div>
<div class=box><b>2. Conceptuales (Q6–Q8, Q10–Q14, Q16–Q17, Q23, Q26, Q28–Q30):</b> todas coinciden; son consistentes con lo observado (A, B, C y AB activos en el 2^5 y en la fracción; 2^(5-1) V saturado; complementaria para desmezclar).</div>
<div class=box><b>3. Q9 no coincide:</b> la clave da 139.16, pero con la fórmula de la pista el resultado es 174.78 (y 165.75 colapsando exactamente a un 2^3). Ninguna ruta reproduce 139.16.</div>
<div class=box><b>4. Datos citados no reproducibles (*):</b> Q15 (SS_A = 676.0), Q18 (SST = 5392.015), Q19 (B 29.0, A 13.0, AB 12.5), Q20 (CD = 5.25, BE = −5.25), Q24 (R² aj. 84.5%), Q25 (p = 0.0123) y Q27 (13.0 y 16.875). Con la Tabla 8.4 los valores son otros (p. ej. fracción principal: B = 32.375, A = 9.625, AB = 8.375; SST = 5326.94), pero la respuesta correcta es la misma. Q27 es notable: con nuestros datos, (9.625 + 12.75)/2 = 11.1875 reproduce exactamente el efecto de A del factorial completo.</div>
<div class=box><b>5. Q20:</b> con I = ABCDE, CD se confunde con ABE y BE con ACD (no entre sí); la opción B solo es 'correcta' en sentido amplio de aliasing.</div>
<div class=box><b>6. Datos de entrada:</b> el enunciado de la evaluación usa e = 18 (Tabla 6.14); la Tabla 8.4 impresa en el libro dice e = 8.0. Usamos 18. Con e = 8.0 la fracción principal da otros valores (SS_A = 473.06), tampoco iguales a 676.0.</div>"""
f+="<p class=n>* ≈ Coincide: misma opción/valor final que la clave, pero el dato numérico que cita el enunciado no se obtiene con nuestros datos.</p>"
pdf("2_Correlacion_respuestas_vs_codigo","Correlación",f)
print(ok,dato,x)
