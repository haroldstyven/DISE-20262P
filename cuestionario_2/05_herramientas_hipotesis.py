"""
05_herramientas_hipotesis.py
Caja de herramientas para pruebas de hipotesis sobre una media.
"""
import numpy as np
from scipy import stats

COLAS = ("izquierda", "derecha", "dos")


def prueba_z(xbar, mu0, sigma, n, cola="dos", alpha=0.05):
    """Prueba de hipotesis para la media con SIGMA CONOCIDA."""
    ee = sigma / np.sqrt(n)
    z = (xbar - mu0) / ee
    if cola == "izquierda":
        vc = stats.norm.ppf(alpha);           rechaza = z < vc;  p = stats.norm.cdf(z)
    elif cola == "derecha":
        vc = stats.norm.ppf(1 - alpha);       rechaza = z > vc;  p = stats.norm.sf(z)
    else:
        vc = stats.norm.ppf(1 - alpha / 2);   rechaza = abs(z) > vc; p = 2 * stats.norm.sf(abs(z))
    return dict(est=z, ee=ee, vc=vc, rechaza=bool(rechaza), p=p, dist="Z", gl=None)


def prueba_t(xbar, mu0, s, n, cola="dos", alpha=0.05):
    """Prueba de hipotesis para la media con SIGMA DESCONOCIDA (usa s)."""
    gl = n - 1
    ee = s / np.sqrt(n)
    t = (xbar - mu0) / ee
    if cola == "izquierda":
        vc = stats.t.ppf(alpha, gl);          rechaza = t < vc;  p = stats.t.cdf(t, gl)
    elif cola == "derecha":
        vc = stats.t.ppf(1 - alpha, gl);      rechaza = t > vc;  p = stats.t.sf(t, gl)
    else:
        vc = stats.t.ppf(1 - alpha / 2, gl);  rechaza = abs(t) > vc; p = 2 * stats.t.sf(abs(t), gl)
    return dict(est=t, ee=ee, vc=vc, rechaza=bool(rechaza), p=p, dist="t", gl=gl)


def reporte(nombre, r, mu0, cola, alpha=0.05):
    """Imprime el desarrollo completo de una prueba."""
    d, e, vc = r["dist"], r["est"], r["vc"]
    signos = {"izquierda": ("<", "mu <"), "derecha": (">", "mu >"), "dos": ("!=", "mu !=")}
    op, ha = signos[cola]
    gl = f", gl={r['gl']}" if r["gl"] is not None else ""

    print(f"  H0: mu = {mu0}    Ha: {ha} {mu0}    ({cola}, alpha={alpha}{gl})")
    print(f"  error estandar = {r['ee']:.4f}")
    print(f"  {d} = {e:+.4f}")
    if cola == "dos":
        print(f"  valor critico = +/-{vc:.4f}   ->  |{d}| = {abs(e):.4f} "
              f"{'>' if abs(e) > vc else '<'} {vc:.4f}")
    else:
        print(f"  valor critico = {vc:+.4f}   ->  {d} = {e:+.4f} "
              f"{'cae' if r['rechaza'] else 'NO cae'} en la region de rechazo")
    print(f"  p-valor = {r['p']:.6f}  {'<' if r['p'] < alpha else '>'} {alpha}")
    print(f"  DECISION: {'** RECHAZAR H0 **' if r['rechaza'] else '** NO RECHAZAR H0 **'}")


if __name__ == "__main__":
    print("Prueba de la caja de herramientas:")
    reporte("demo", prueba_z(18, 20, 6, 64, "izquierda"), 20, "izquierda")
