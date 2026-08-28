"""
02_herramientas.py
Caja de herramientas: las 5 formulas de intervalos de confianza.
Importa esto desde otros scripts:  from herramientas import *
"""
import numpy as np
from scipy import stats


def ic_media_z(xbar, sigma, n, conf=0.95):
    """IC para la media cuando SIGMA POBLACIONAL ES CONOCIDA -> Normal (z)."""
    z = stats.norm.ppf(1 - (1 - conf) / 2)
    e = z * sigma / np.sqrt(n)
    return xbar - e, xbar + e, z, e


def ic_media_t(xbar, s, n, conf=0.95):
    """IC para la media con SIGMA DESCONOCIDA (usamos s) -> t de Student, gl = n-1."""
    gl = n - 1
    t = stats.t.ppf(1 - (1 - conf) / 2, gl)
    e = t * s / np.sqrt(n)
    return xbar - e, xbar + e, t, e


def ic_varianza(s2, n, conf=0.95):
    """IC para SIGMA^2 -> chi-cuadrado, gl = n-1. NO es simetrico."""
    gl = n - 1
    a = 1 - conf
    chi_sup = stats.chi2.ppf(1 - a / 2, gl)   # cola derecha -> va en el limite INFERIOR
    chi_inf = stats.chi2.ppf(a / 2, gl)       # cola izquierda -> va en el limite SUPERIOR
    return gl * s2 / chi_sup, gl * s2 / chi_inf, chi_inf, chi_sup


def ic_proporcion(x, n, conf=0.95):
    """IC para una proporcion p (aproximacion normal / Wald)."""
    p = x / n
    z = stats.norm.ppf(1 - (1 - conf) / 2)
    e = z * np.sqrt(p * (1 - p) / n)
    return p - e, p + e, p, z, e


def n_para_media(sigma, error, conf=0.95):
    """Tamano de muestra minimo para que el error de estimacion <= 'error'."""
    z = stats.norm.ppf(1 - (1 - conf) / 2)
    n = (z * sigma / error) ** 2
    return int(np.ceil(n)), n, z


def n_para_proporcion(error, conf=0.95, p=0.5):
    """Tamano de muestra para proporcion. p=0.5 es el peor caso (mas conservador)."""
    z = stats.norm.ppf(1 - (1 - conf) / 2)
    n = z ** 2 * p * (1 - p) / error ** 2
    return int(np.ceil(n)), n, z


def fmt(li, ls, dec=4):
    return f"[{li:.{dec}f} , {ls:.{dec}f}]"


if __name__ == "__main__":
    print("Prueba rapida de la caja de herramientas")
    print(" ic_media_z(100, 15, 36, .95) ->", fmt(*ic_media_z(100, 15, 36)[:2]))
    print(" ic_media_t(100, 15, 36, .95) ->", fmt(*ic_media_t(100, 15, 36)[:2]))
    print(" ic_varianza(225, 36, .95)    ->", fmt(*ic_varianza(225, 36)[:2]))
    print(" ic_proporcion(60, 200, .95)  ->", fmt(*ic_proporcion(60, 200)[:2]))
    print(" n_para_media(15, 2, .95)     ->", n_para_media(15, 2)[0])
