"""
04_intuicion_hipotesis.py
Que es realmente una prueba de hipotesis, demostrado con simulacion.
Diseno de Experimentos
"""
import numpy as np
from scipy import stats

rng = np.random.default_rng(2026)

# =====================================================================
print("=" * 68)
print("DEMO 1: EL ERROR TIPO I es literalmente alpha")
print("=" * 68)
print("Simulamos un mundo donde H0 ES VERDADERA (mu realmente = 20).")
print("Si el metodo esta bien, deberiamos rechazar por error ~5% de veces.\n")

MU0, SIGMA, N, ALPHA = 20, 6, 64, 0.05
REPS = 20_000

# Mundo donde H0 es CIERTA
muestras = rng.normal(MU0, SIGMA, size=(REPS, N))
z = (muestras.mean(axis=1) - MU0) / (SIGMA / np.sqrt(N))

z_izq = stats.norm.ppf(ALPHA)             # -1.645
z_dos = stats.norm.ppf(1 - ALPHA / 2)     #  1.96

print(f"  Cola izquierda (rechazo si z < {z_izq:.3f}):")
print(f"     rechazos = {(z < z_izq).mean()*100:.2f} %   <- esto ES alpha (error tipo I)")
print(f"  Dos colas      (rechazo si |z| > {z_dos:.3f}):")
print(f"     rechazos = {(np.abs(z) > z_dos).mean()*100:.2f} %")
print("\n  >> alpha NO es 'la probabilidad de equivocarse'.")
print("     Es la tasa de FALSAS ALARMAS cuando H0 es cierta.")

# =====================================================================
print()
print("=" * 68)
print("DEMO 2: EL ERROR TIPO II y la POTENCIA")
print("=" * 68)
print("Ahora H0 es FALSA (mu real = 18, pero seguimos probando contra 20).")
print("Cuantas veces logramos detectarlo?\n")

for mu_real in (20, 19.5, 19, 18.5, 18, 17):
    m = rng.normal(mu_real, SIGMA, size=(REPS, N))
    zz = (m.mean(axis=1) - MU0) / (SIGMA / np.sqrt(N))
    potencia = (zz < z_izq).mean()
    print(f"  mu real = {mu_real:5.1f}  ->  potencia = {potencia*100:5.2f} %"
          f"   (error tipo II = {100-potencia*100:5.2f} %)")

print("\n  >> Entre mas LEJOS este la verdad de H0, mas facil detectarla.")
print("     Diferencias chiquitas necesitan MUCHOS datos para verse.")

# =====================================================================
print()
print("=" * 68)
print("DEMO 3: el tamano de muestra cambia TODO")
print("=" * 68)
print("Misma diferencia real (mu=19 vs H0: mu=20), distintos n:\n")

for n in (16, 64, 144, 400, 1000):
    m = rng.normal(19, SIGMA, size=(5000, n))
    zz = (m.mean(axis=1) - MU0) / (SIGMA / np.sqrt(n))
    print(f"  n = {n:5d}  ->  potencia = {(zz < z_izq).mean()*100:5.2f} %")

print("\n  >> Con n chico una diferencia real pasa desapercibida.")
print("     Con n enorme hasta diferencias irrelevantes salen 'significativas'.")

# =====================================================================
print()
print("=" * 68)
print("DEMO 4: la DUALIDAD prueba de hipotesis <-> intervalo de confianza")
print("=" * 68)
print("Son la misma cosa vista de dos formas.\n")

xbar, sigma, n = 56, 16, 36
mu0 = 60
ee = sigma / np.sqrt(n)
zc = stats.norm.ppf(0.975)
li, ls = xbar - zc * ee, xbar + zc * ee
zstat = (xbar - mu0) / ee

print(f"  Prueba 2 colas: z = ({xbar}-{mu0})/{ee:.4f} = {zstat:.4f}")
print(f"     |z| = {abs(zstat):.4f} vs 1.96  ->  {'RECHAZO' if abs(zstat)>zc else 'NO rechazo'}")
print(f"  IC95% = [{li:.4f} , {ls:.4f}]")
print(f"     contiene mu0={mu0}? {'SI' if li<=mu0<=ls else 'NO'}"
      f"  ->  {'NO rechazo' if li<=mu0<=ls else 'RECHAZO'}")
print("\n  >> Coinciden SIEMPRE. Si mu0 cae DENTRO del IC -> no rechazas.")
print("     Si cae FUERA -> rechazas. Es la misma decision.")

# =====================================================================
print()
print("=" * 68)
print("DEMO 5: valores criticos que necesitas memorizar (alpha=0.05)")
print("=" * 68)
print(f"  Z cola izquierda : {stats.norm.ppf(0.05):+.4f}")
print(f"  Z cola derecha   : {stats.norm.ppf(0.95):+.4f}")
print(f"  Z dos colas      : +/-{stats.norm.ppf(0.975):.4f}")
print()
print("  t (una cola, 0.05)        t (dos colas, 0.05)")
for n in (5, 9, 16, 25, 30, 64):
    gl = n - 1
    print(f"   n={n:3d} gl={gl:3d}   {stats.t.ppf(0.95, gl):+.4f}"
          f"              +/-{stats.t.ppf(0.975, gl):.4f}")
