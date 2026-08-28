"""
03_solucion_cuestionario_1.py
Solucion completa del Cuestionario 1 - Intervalos de Confianza
Diseno de Experimentos
"""
import numpy as np
from scipy import stats
import importlib.util, pathlib

_spec = importlib.util.spec_from_file_location(
    "herr", pathlib.Path(__file__).parent / "02_herramientas.py")
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)


def titulo(n, txt):
    print(f"\n{'='*68}\nPREGUNTA {n}: {txt}\n{'='*68}")


# =====================================================================
titulo(1, "Gasolineras, n=100, xbar=995 cc, sigma=10 cc  ->  z")
li, ls, z, e = h.ic_media_z(995, 10, 100, 0.95)
print("  Datos: xbar=995, sigma=10 (el +/-10cc de la ley), n=100, 95%")
print(f"  z = {z:.4f}   error estandar = 10/sqrt(100) = {10/np.sqrt(100):.4f}")
print(f"  margen = z*ee = {e:.4f}")
print(f"  IC95% = 995 +/- {e:.4f} = {h.fmt(li,ls)} cc")
print(f"  Contiene 1000 cc? {'SI' if li<=1000<=ls else 'NO'}  -> HAY FRAUDE, sirven de menos")

# =====================================================================
titulo(2, "Igual pero n=25 con distribucion t")
li, ls, t, e = h.ic_media_t(995, 10, 25, 0.95)
print("  Datos: xbar=995, s=10, n=25, gl=24, 95%")
print(f"  t(0.975, 24) = {t:.4f}   ee = 10/sqrt(25) = {10/5:.4f}")
print(f"  margen = {e:.4f}")
print(f"  IC95% = {h.fmt(li,ls)} cc")
print(f"  Contiene 1000? {'SI' if li<=1000<=ls else 'NO'}")
print(f"  Nota: con n=25 el intervalo es mas ancho ({ls-li:.2f}) que con n=100 (3.92)")

# =====================================================================
titulo(3, "Atencion al paciente: n=20, xbar=34 min, S=2.3")
li, ls, t, e = h.ic_media_t(34, 2.3, 20, 0.95)
print("  sigma DESCONOCIDA (nos dan S) -> t con gl = 20-1 = 19")
print(f"  t(0.975, 19) = {t:.4f}   ee = 2.3/sqrt(20) = {2.3/np.sqrt(20):.4f}")
print(f"  margen = {e:.4f}")
print(f"  IC95% = 34 +/- {e:.4f} = {h.fmt(li,ls)} minutos")

# =====================================================================
titulo(4, "Varianza: n=25, S^2 = 82 min^2  ->  chi-cuadrado")
li, ls, ci, cs = h.ic_varianza(82, 25, 0.95)
gl = 24
print(f"  gl = 24     (n-1)*S^2 = 24*82 = {gl*82}")
print(f"  chi2(0.025, 24) = {ci:.4f}     chi2(0.975, 24) = {cs:.4f}")
print(f"  LI = {gl*82}/{cs:.4f} = {li:.4f}")
print(f"  LS = {gl*82}/{ci:.4f} = {ls:.4f}")
print(f"  IC95% para sigma^2 = {h.fmt(li,ls)} min^2")
print(f"  (para sigma: [{np.sqrt(li):.4f} , {np.sqrt(ls):.4f}] min)")

# =====================================================================
titulo(5, "Interpretacion del IC99%")
print("  RESPUESTA: incluye la media poblacional el 99% de las ocasiones")
print("  Razon: mu es un valor FIJO. Lo aleatorio es el intervalo (depende")
print("         de la muestra). Al repetir el muestreo, 99 de cada 100")
print("         intervalos construidos contendran a mu.")

# =====================================================================
titulo(6, "Interpretacion del IC95%")
print("  RESPUESTA: hay una confianza del 95% de que el parametro mu este")
print("             en el intervalo")
print("  Por que las otras NO:")
print("   x 95% de los casos estan dentro     -> confunde datos con la media")
print("   x el 95% de los casos estarian dentro -> mismo error")
print("   x probabilidad del 5% de que mu no este -> mu no es aleatoria;")
print("     en el enfoque frecuentista se dice CONFIANZA, no probabilidad")

# =====================================================================
titulo(7, "Kiosco: n=1000, xbar=4000, S^2=4000, confianza 95.5%")
s = np.sqrt(4000)
li, ls, z, e = h.ic_media_z(4000, s, 1000, 0.955)
print(f"  S = sqrt(4000) = {s:.4f}")
print(f"  n=1000 grande -> z. Al 95.5% -> z = {z:.4f} (el clasico 2 sigmas)")
print(f"  ee = {s:.4f}/sqrt(1000) = {s/np.sqrt(1000):.4f}")
print(f"  margen = {e:.4f}")
print(f"  IC95.5% = {h.fmt(li,ls,2)} pts/hora")
li2, ls2 = h.ic_media_z(4000, s, 1000, 0.95)[:2]
print(f"  (si pidieran 95% exacto con z=1.96: {h.fmt(li2,ls2,2)})")

# =====================================================================
titulo(8, "Proporcion: 180 de 400 amas de casa, 99%")
li, ls, p, z, e = h.ic_proporcion(180, 400, 0.99)
print(f"  p_gorro = 180/400 = {p}")
print(f"  z(99%) = {z:.4f}")
print(f"  ee = sqrt({p}*{1-p}/400) = {np.sqrt(p*(1-p)/400):.6f}")
print(f"  margen = {e:.6f}")
print(f"  IC99% = {h.fmt(li,ls)}  ->  ({li*100:.2f}% , {ls*100:.2f}%)")

# =====================================================================
titulo(9, "Proporcion: 80 de 100 no leen periodico, 99%")
li, ls, p, z, e = h.ic_proporcion(80, 100, 0.99)
print(f"  p_gorro = 80/100 = {p}")
print(f"  z(99%) = {z:.4f}    ee = sqrt(0.8*0.2/100) = {np.sqrt(.8*.2/100):.4f}")
print(f"  margen = {e:.6f}")
print(f"  IC99% = {h.fmt(li,ls)}  ->  ({li*100:.2f}% , {ls*100:.2f}%)")
fpc = np.sqrt((1000 - 100) / (1000 - 1))
print(f"  Opcional (poblacion finita N=1000, factor {fpc:.4f}):")
print(f"     -> ({(p-e*fpc)*100:.2f}% , {(p+e*fpc)*100:.2f}%)")

# =====================================================================
titulo(10, "Errores de red: 10 dias, alpha = 1%")
datos = np.array([2, 3, 4, 5, 4, 3, 5, -1.98, 1.98, 1])
n = len(datos)
xbar = datos.mean()
s = datos.std(ddof=1)
li, ls, t, e = h.ic_media_t(xbar, s, n, 0.99)
print(f"  Datos: {[float(x) for x in datos]}")
print(f"  n = {n}   suma = {datos.sum():.2f}   xbar = {xbar:.4f}")
print(f"  S (muestral, ddof=1) = {s:.4f}")
print(f"  sigma desconocida -> t con gl = 9;  t(0.995, 9) = {t:.4f}")
print(f"  ee = {s:.4f}/sqrt(10) = {s/np.sqrt(10):.4f}    margen = {e:.4f}")
print(f"  IC99% = {h.fmt(li,ls)} errores/dia")

# =====================================================================
titulo(11, "Tamano de muestra: sigma=0.05 s, error<=0.01 s, 99%")
n_ent, n_exac, z = h.n_para_media(0.05, 0.01, 0.99)
print(f"  n >= (z*sigma/E)^2 = ({z:.4f}*0.05/0.01)^2 = ({z*0.05/0.01:.4f})^2")
print(f"  n >= {n_exac:.4f}   ->  se REDONDEA HACIA ARRIBA")
print(f"  n minimo = {n_ent} conductores")

# =====================================================================
titulo(12, "Fotocopias: n=9, sigma=12 (CONOCIDA), 95%")
g = np.array([100, 150, 90, 70, 75, 105, 200, 120, 80])
xbar = g.mean()
li, ls, z, e = h.ic_media_z(xbar, 12, 9, 0.95)
print(f"  Datos: {[int(x) for x in g]}    suma = {g.sum()}")
print(f"  xbar = {g.sum()}/9 = {xbar:.4f} (miles)")
print("  sigma es CONOCIDA (=12) -> se usa z aunque n=9 sea pequeno")
print(f"  z = {z:.4f}   ee = 12/3 = {12/3:.4f}   margen = {e:.4f}")
print(f"  IC95% = {h.fmt(li,ls)} (miles)")

# =====================================================================
titulo(13, "Electrodomesticos: mu=100, sigma=12, P(90<=xbar<=110)>=0.98")
z = stats.norm.ppf(0.99)   # 0.98 central -> 1% en cada cola
n_ex = (z * 12 / 10) ** 2
print("  Semiamplitud deseada E = 110-100 = 10 meses")
print(f"  Confianza 0.98 -> alpha/2 = 0.01 -> z = {z:.4f}")
print(f"  n >= (z*sigma/E)^2 = ({z:.4f}*12/10)^2 = {n_ex:.4f}")
print(f"  n minimo = {int(np.ceil(n_ex))} electrodomesticos")
print(f"  Verificacion n=8: P = {2*stats.norm.cdf(10/(12/np.sqrt(8)))-1:.4f} >= 0.98  OK")
print(f"  Verificacion n=7: P = {2*stats.norm.cdf(10/(12/np.sqrt(7)))-1:.4f} <  0.98  NO")

# =====================================================================
titulo(14, "Sandias: sigma=750 gr, error<300 gr, 95%")
n_ent, n_exac, z = h.n_para_media(750, 300, 0.95)
print("  Paso 1: el error de estimacion es E = z*sigma/sqrt(n)")
print("  Paso 2: despejamos n  ->  n >= (z*sigma/E)^2")
print(f"  Paso 3: z(95%) = {z:.4f}")
print(f"  Paso 4: n >= ({z:.4f}*750/300)^2 = ({z*750/300:.4f})^2 = {n_exac:.4f}")
print(f"  Paso 5: redondear HACIA ARRIBA -> n minimo = {n_ent} sandias")
print("  (con z=1.96 da 24.01, por eso 25 y no 24)")

print("\n" + "=" * 68)
