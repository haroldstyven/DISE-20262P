"""
01_intuicion.py
Demostracion visual/numerica de QUE ES un intervalo de confianza.
Materia: Diseno de Experimentos
"""
import numpy as np
from scipy import stats

rng = np.random.default_rng(2026)

# ---------------------------------------------------------------
# EL TARRO DE CARAMELOS: aqui SI conocemos la verdad (hacemos trampa)
# ---------------------------------------------------------------
MU_VERDADERA = 4.0      # peso medio real de un caramelo (gramos)
SIGMA         = 0.5     # desviacion real
N             = 100     # tamano de cada punado

print("=" * 62)
print("DEMO 1: un solo experimento")
print("=" * 62)

muestra = rng.normal(MU_VERDADERA, SIGMA, N)
xbar = muestra.mean()
s    = muestra.std(ddof=1)          # ddof=1 -> divide entre n-1 (muestral!)
ee   = s / np.sqrt(N)               # error estandar
t_c  = stats.t.ppf(0.975, df=N - 1) # valor critico t al 95%

li, ls = xbar - t_c * ee, xbar + t_c * ee

print(f"  Verdad oculta  mu = {MU_VERDADERA}")
print(f"  Mi estimacion  xbar = {xbar:.4f}   (me equivoque por {abs(xbar-MU_VERDADERA):.4f} g)")
print(f"  s = {s:.4f}   error estandar = s/sqrt(n) = {ee:.4f}")
print(f"  t critico (gl={N-1}) = {t_c:.4f}")
print(f"  IC95% = [{li:.4f} , {ls:.4f}]   ancho = {ls-li:.4f}")
print(f"  -> Atrapo a mu? {'SI' if li <= MU_VERDADERA <= ls else 'NO'}")

# ---------------------------------------------------------------
# DEMO 2: que significa REALMENTE el 95%
# ---------------------------------------------------------------
print()
print("=" * 62)
print("DEMO 2: repetimos el experimento 10,000 veces")
print("=" * 62)

REPS = 10_000
datos = rng.normal(MU_VERDADERA, SIGMA, size=(REPS, N))
medias = datos.mean(axis=1)
eses   = datos.std(axis=1, ddof=1)
margen = t_c * eses / np.sqrt(N)
atrapan = np.abs(medias - MU_VERDADERA) <= margen

print(f"  Intervalos construidos : {REPS}")
print(f"  Que SI atraparon a mu  : {atrapan.sum()}  ({100*atrapan.mean():.2f} %)")
print(f"  Que la dejaron escapar : {(~atrapan).sum()}  ({100*(~atrapan).mean():.2f} %)")
print()
print("  >> El '95%' es una propiedad del METODO a la larga,")
print("     NO una probabilidad sobre TU intervalo particular.")

# primeros 12 intervalos, para verlo
print()
print("  Primeros 12 intervalos (| = mu verdadera):")
for i in range(12):
    lo, hi = medias[i] - margen[i], medias[i] + margen[i]
    ok = "OK  " if atrapan[i] else "FALLA"
    print(f"    [{lo:.3f} , {hi:.3f}]  {ok}")

# ---------------------------------------------------------------
# DEMO 3: los dos trade-offs
# ---------------------------------------------------------------
print()
print("=" * 62)
print("DEMO 3: que hace mas ANGOSTO el intervalo?")
print("=" * 62)

print("\n  (a) Subir la confianza lo hace mas ANCHO  (n=100, sigma=0.5)")
for conf in (0.80, 0.90, 0.95, 0.99, 0.999):
    z = stats.norm.ppf(1 - (1 - conf) / 2)
    ancho = 2 * z * SIGMA / np.sqrt(100)
    print(f"      {conf*100:5.1f}%  ->  z = {z:.4f}   ancho = {ancho:.4f}")

print("\n  (b) Subir n lo hace mas ANGOSTO, pero con rendimientos decrecientes (1/sqrt(n))")
z95 = stats.norm.ppf(0.975)
for n in (10, 25, 100, 400, 1600):
    ancho = 2 * z95 * SIGMA / np.sqrt(n)
    print(f"      n = {n:5d}  ->  ancho = {ancho:.4f}")
print("      (x4 el tamano de muestra  ->  la MITAD de ancho)")

print("\n  (c) t vs z: la t es mas ancha con pocos datos, iguala a z con muchos")
for n in (5, 10, 20, 30, 60, 120, 1000):
    print(f"      n = {n:5d}  gl = {n-1:5d}  t = {stats.t.ppf(0.975, n-1):.4f}   z = {z95:.4f}")
