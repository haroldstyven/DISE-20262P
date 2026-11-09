"""
10_intuicion_supuestos.py
Los supuestos del ANOVA: que son los residuales, que grafico ve cada supuesto,
y que pasa de verdad cuando uno falla.
Diseno de Experimentos
"""
import numpy as np
from scipy import stats

rng = np.random.default_rng(2026)
ALPHA, REPS = 0.05, 5000

# =====================================================================
print("=" * 68)
print("DEMO 1: EL RESIDUAL ES LO QUE EL MODELO NO EXPLICA")
print("=" * 68)
datos = [[15, 17, 16, 14, 18, 16, 15, 17], [20, 22, 21, 19, 23, 21, 20, 22],
         [25, 27, 26, 24, 28, 26, 25, 27], [22, 24, 23, 21, 25, 23, 22, 24]]
nombres = ["Control", "Organico", "Quimico", "Mixto"]
print("  Modelo: Yij = mu + tau_i + eij    ->    eij = Yij - media_i")
print(f"  {'trat':<10}{'media (ajustado)':>18}   residuales")
for nom, g in zip(nombres, datos):
    g = np.array(g, float)
    print(f"  {nom:<10}{g.mean():>18.2f}   " + " ".join(f"{e:+.1f}" for e in g - g.mean()))
print("\n  >> Los residuales SIEMPRE suman cero dentro de cada grupo.")
print("     Todos los supuestos (normalidad, varianza constante, independencia)")
print("     se verifican sobre los RESIDUALES, no sobre los datos crudos.")
print("     Por eso: Q-Q plot de residuales, y residuos vs ajustados.")

# =====================================================================
print()
print("=" * 68)
print("DEMO 2: QUE GRAFICO DETECTA QUE COSA")
print("=" * 68)
print("  Q-Q plot (residual vs cuantil normal)  -> NORMALIDAD")
print("     puntos sobre la recta = normal ; cola curvada = sesgo/colas pesadas")
print("  Residuos vs valores ajustados          -> HOMOCEDASTICIDAD")
print("     banda horizontal uniforme = OK ; EMBUDO = la varianza crece con la media")
print("  Residuos vs orden de corrida           -> INDEPENDENCIA")
print("     patron o tendencia = los errores estan correlacionados\n")

for etiqueta, factor in [("varianza CONSTANTE (OK)", 0.0), ("EMBUDO (falla)", 0.35)]:
    print(f"  {etiqueta}")
    for m in (16, 21, 23, 26):
        s = 1.3 + factor * (m - 16)
        e = rng.normal(0, s, 8)
        fila = [" "] * 51
        for ei in e:
            fila[int(np.clip(round(ei / 6 * 25 + 25), 0, 50))] = "*"
        print(f"    ajustado={m:5.1f} |{''.join(fila)}|  sd={s:.2f}")
    print()

# =====================================================================
print("=" * 68)
print("DEMO 3: QUE PASA SI LOS SUPUESTOS FALLAN (H0 es CIERTA)")
print("=" * 68)
print("Mundo donde los 4 grupos tienen la MISMA media. Un metodo honesto")
print(f"deberia rechazar solo el {ALPHA*100:.0f}% de las veces.\n")

escenarios = {
    "ideal: normal y varianzas iguales": lambda: [rng.normal(30, 2, 8) for _ in range(4)],
    "varianzas MUY distintas (2 vs 10)": lambda: [rng.normal(30, s, 8) for s in (2, 2, 10, 10)],
    "n desbalanceado + varianzas dist.": lambda: [rng.normal(30, s, n)
                                                  for s, n in ((2, 15), (2, 15), (10, 4), (10, 4))],
    "residuos NO normales (exponencial)": lambda: [rng.exponential(5, 8) + 25 for _ in range(4)],
}
for nom, gen in escenarios.items():
    rech_f = rech_k = 0
    for _ in range(REPS):
        g = gen()
        rech_f += stats.f_oneway(*g).pvalue < ALPHA
        rech_k += stats.kruskal(*g).pvalue < ALPHA
    print(f"  {nom:<36} ANOVA F: {rech_f/REPS*100:5.2f} %   Kruskal-Wallis: {rech_k/REPS*100:5.2f} %")

print("\n  >> El ANOVA aguanta bastante la falta de normalidad (es robusto),")
print("     pero se descompone cuando las varianzas difieren Y el diseno esta")
print("     DESBALANCEADO: ahi alpha real se dispara muy por encima del 5%.")
print("     Moraleja: n igual por tratamiento + revisar Levene.")

# =====================================================================
print()
print("=" * 68)
print("DEMO 4: LA TRANSFORMACION LOG ARREGLA EL EMBUDO")
print("=" * 68)
print("Datos donde la desviacion crece proporcional a la media (caso tipico):\n")
grupos = [rng.lognormal(mean=np.log(m), sigma=0.45, size=12) for m in (10, 20, 40, 80)]
print(f"  {'trat':<6}{'media':>10}{'sd':>10}{'sd log':>10}")
for i, g in enumerate(grupos):
    print(f"  {i+1:<6}{g.mean():>10.2f}{g.std(ddof=1):>10.2f}{np.log(g).std(ddof=1):>10.2f}")
print(f"\n  Levene datos crudos : p = {stats.levene(*grupos, center='mean').pvalue:.4f}")
print(f"  Levene en log(Y)    : p = {stats.levene(*[np.log(g) for g in grupos], center='mean').pvalue:.4f}")
print("  >> en escala log las sd se igualan -> ya se puede hacer el ANOVA.")
