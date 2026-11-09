"""
07_intuicion_dca.py
De donde sale el ANOVA: por que no sirven muchas pruebas t, y que significa F.
Diseno de Experimentos
"""
import numpy as np
from scipy import stats

rng = np.random.default_rng(2026)

# =====================================================================
print("=" * 68)
print("DEMO 1: POR QUE NO COMPARAR CON MUCHAS PRUEBAS t (alpha se infla)")
print("=" * 68)
print("Mundo donde H0 ES CIERTA: los 4 tratamientos tienen la MISMA media.")
print("Hacemos las 6 pruebas t por parejas y vemos cuantas veces")
print("al menos una sale 'significativa' por puro azar.\n")

REPS, K, N, ALPHA = 20_000, 4, 5, 0.05
falsas_t, falsas_F = 0, 0
for _ in range(REPS):
    g = rng.normal(30, 1.6, size=(K, N))
    pares = [stats.ttest_ind(g[i], g[j]).pvalue
             for i in range(K) for j in range(i + 1, K)]
    falsas_t += any(p < ALPHA for p in pares)
    falsas_F += stats.f_oneway(*g).pvalue < ALPHA

print(f"  6 pruebas t por parejas : {falsas_t/REPS*100:5.2f} % de falsas alarmas")
print(f"  1 ANOVA (prueba F)      : {falsas_F/REPS*100:5.2f} % de falsas alarmas")
print(f"  teorico 1-(1-alpha)^6   = {(1-(1-ALPHA)**6)*100:5.2f} %")
print("\n  >> El ANOVA existe para hacer UNA sola prueba global que")
print("     mantiene alpha en 5%. Tukey/LSD vienen DESPUES, y solo si F rechaza.")

# =====================================================================
print()
print("=" * 68)
print("DEMO 2: SCT = SCTrat + SCE  (la identidad que sostiene todo)")
print("=" * 68)
datos = [[28, 31, 29, 30, 32], [34, 33, 35, 32, 36],
         [38, 40, 37, 39, 41], [44, 43, 45, 42, 46]]
todo = np.concatenate(datos)
gm = todo.mean()
print(f"  Gran media = {gm}")
print("  Cada dato se parte en dos pedazos:")
print("     (Yij - gran_media) = (media_i - gran_media) + (Yij - media_i)")
print("       variacion total  =   efecto del trat.   +   ruido (error)\n")

sct = ((todo - gm) ** 2).sum()
sctrat = sum(len(g) * (np.mean(g) - gm) ** 2 for g in datos)
sce = sum(((np.array(g) - np.mean(g)) ** 2).sum() for g in datos)
print(f"  SCT    = {sct:8.2f}   (dispersion de los 20 datos respecto a la gran media)")
print(f"  SCTrat = {sctrat:8.2f}   (se separan las medias de los grupos entre si)")
print(f"  SCE    = {sce:8.2f}   (dispersion DENTRO de cada grupo)")
print(f"  comprobacion: {sctrat:.2f} + {sce:.2f} = {sctrat+sce:.2f} = SCT  OK")
print(f"\n  R^2 = SCTrat/SCT = {sctrat/sct*100:.1f} % de la variabilidad la explica el tratamiento")

# =====================================================================
print()
print("=" * 68)
print("DEMO 3: QUE MIDE F  =  CMTrat / CME")
print("=" * 68)
print("CME  = ruido puro, siempre estima sigma^2.")
print("CMTrat = estima sigma^2 SOLO si H0 es cierta; si no, estima sigma^2 + algo.")
print("Por eso F ~ 1 cuando H0 es cierta, y F >> 1 cuando hay efecto.\n")

for sep in (0.0, 1.0, 3.0, 6.0):
    Fs = []
    for _ in range(3000):
        g = [rng.normal(30 + i * sep, 1.6, N) for i in range(K)]
        Fs.append(stats.f_oneway(*g).statistic)
    Fs = np.array(Fs)
    print(f"  separacion entre medias = {sep:>4.1f}  ->  F promedio = {Fs.mean():8.2f}"
          f"   rechazos = {(Fs > stats.f.ppf(0.95, K-1, K*(N-1))).mean()*100:5.1f} %")
print(f"\n  Valor critico usado: F_0.95({K-1},{K*(N-1)}) = {stats.f.ppf(0.95, K-1, K*(N-1)):.4f}")
print("  >> F grande = las medias estan MAS separadas de lo que el ruido justifica.")
