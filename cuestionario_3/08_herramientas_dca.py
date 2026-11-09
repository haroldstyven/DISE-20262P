"""
08_herramientas_dca.py
Caja de herramientas para el Diseno Completamente al Azar (DCA / ANOVA de 1 factor).
Diseno de Experimentos
"""
import numpy as np
from scipy import stats


def anova_dca(grupos, nombres=None):
    """ANOVA de un factor. 'grupos' = lista de listas (un tratamiento por lista).

    Devuelve todo lo que aparece en la tabla ANOVA, calculado a mano
    (no con atajos) para poder copiar el desarrollo al cuaderno.
    """
    g = [np.asarray(x, dtype=float) for x in grupos]
    nombres = nombres or [chr(65 + i) for i in range(len(g))]

    k = len(g)                       # numero de tratamientos
    n = np.array([len(x) for x in g])
    N = int(n.sum())                 # total de observaciones

    medias = np.array([x.mean() for x in g])
    sumas = np.array([x.sum() for x in g])
    varianzas = np.array([x.var(ddof=1) for x in g])
    gran_media = np.concatenate(g).mean()

    # Sumas de cuadrados
    sc_trat = float(np.sum(n * (medias - gran_media) ** 2))
    sc_error = float(sum(((x - x.mean()) ** 2).sum() for x in g))
    sc_total = float(((np.concatenate(g) - gran_media) ** 2).sum())

    # Grados de libertad
    gl_trat, gl_error, gl_total = k - 1, N - k, N - 1

    # Cuadrados medios y F
    cm_trat = sc_trat / gl_trat
    cm_error = sc_error / gl_error          # <- estimador de sigma^2
    F = cm_trat / cm_error

    return dict(nombres=nombres, k=k, n=n, N=N, medias=medias, sumas=sumas,
                varianzas=varianzas, gran_media=gran_media,
                sc_trat=sc_trat, sc_error=sc_error, sc_total=sc_total,
                gl_trat=gl_trat, gl_error=gl_error, gl_total=gl_total,
                cm_trat=cm_trat, cm_error=cm_error, F=F,
                p=float(stats.f.sf(F, gl_trat, gl_error)),
                grupos=g)


def tabla_anova(r, alpha=0.05):
    """Imprime la tabla ANOVA clasica + decision."""
    f_tab = stats.f.ppf(1 - alpha, r["gl_trat"], r["gl_error"])
    print(f"  {'Fuente':<14}{'SC':>12}{'gl':>6}{'CM':>12}{'F':>10}")
    print("  " + "-" * 54)
    print(f"  {'Tratamientos':<14}{r['sc_trat']:>12.4f}{r['gl_trat']:>6}"
          f"{r['cm_trat']:>12.4f}{r['F']:>10.4f}")
    print(f"  {'Error':<14}{r['sc_error']:>12.4f}{r['gl_error']:>6}{r['cm_error']:>12.4f}")
    print(f"  {'Total':<14}{r['sc_total']:>12.4f}{r['gl_total']:>6}")
    print(f"  F_tab({r['gl_trat']},{r['gl_error']}) con alpha={alpha}: {f_tab:.4f}"
          f"    p-valor = {r['p']:.3e}")
    print(f"  DECISION: {'** RECHAZAR H0 **' if r['F'] > f_tab else '** NO RECHAZAR H0 **'}")
    return f_tab


def tukey_hsd(cm_error, n, q):
    """HSD de Tukey (grupos balanceados):  HSD = q * sqrt(CME / n)."""
    return q * np.sqrt(cm_error / n)


def lsd_fisher(cm_error, n, t_crit):
    """LSD de Fisher (balanceado):  LSD = t * sqrt(2*CME / n)."""
    return t_crit * np.sqrt(2 * cm_error / n)


def comparar_pares(medias, nombres, umbral, etiqueta="HSD"):
    """Compara todas las parejas contra un umbral (HSD o LSD)."""
    k = len(medias)
    for i in range(k):
        for j in range(i + 1, k):
            d = abs(medias[i] - medias[j])
            sig = d > umbral
            print(f"  |{nombres[i]} - {nombres[j]}| = {d:6.3f}  "
                  f"{'>' if sig else '<'} {etiqueta}={umbral:.3f}  ->  "
                  f"{'DIFERENTES (significativo)' if sig else 'iguales (no significativo)'}")


def supuestos(r, alpha=0.05):
    """Los 3 supuestos del modelo Yij = mu + tau_i + eij."""
    res = np.concatenate([x - x.mean() for x in r["grupos"]])   # residuales
    sw = stats.shapiro(res)
    lev = stats.levene(*r["grupos"], center="mean")
    bar = stats.bartlett(*r["grupos"])
    print(f"  Normalidad  Shapiro-Wilk (residuales): W={sw.statistic:.4f} p={sw.pvalue:.4f}"
          f"  -> {'OK' if sw.pvalue > alpha else 'FALLA'}")
    print(f"  Homocedast. Levene:  W={lev.statistic:.4f} p={lev.pvalue:.4f}"
          f"  -> {'OK' if lev.pvalue > alpha else 'FALLA'}")
    print(f"  Homocedast. Bartlett: X2={bar.statistic:.4f} p={bar.pvalue:.4f}"
          f"  -> {'OK' if bar.pvalue > alpha else 'FALLA'}")
    print("  Independencia: por el ALEATORIZADO del experimento (o Durbin-Watson si hay orden)")


if __name__ == "__main__":
    r = anova_dca([[28, 31, 29, 30, 32], [34, 33, 35, 32, 36],
                   [38, 40, 37, 39, 41], [44, 43, 45, 42, 46]], list("ABCD"))
    tabla_anova(r)
