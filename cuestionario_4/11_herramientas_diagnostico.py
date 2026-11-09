"""
11_herramientas_diagnostico.py
Diagnostico de supuestos del DCA + alternativa no parametrica.
Reutiliza la caja de herramientas ANOVA del cuestionario 3.
Diseno de Experimentos
"""
import numpy as np
from scipy import stats
import importlib.util, pathlib

# --- se reutiliza tal cual la caja del cuestionario 3 -----------------
_p = pathlib.Path(__file__).resolve().parent.parent / "cuestionario_3" / "08_herramientas_dca.py"
_spec = importlib.util.spec_from_file_location("hd", _p)
DCA = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(DCA)

anova_dca = DCA.anova_dca
tabla_anova = DCA.tabla_anova
tukey_hsd = DCA.tukey_hsd
lsd_fisher = DCA.lsd_fisher
comparar_pares = DCA.comparar_pares


def residuales(r):
    """eij = Yij - media_i   (lo que sobra despues de quitar el efecto)."""
    return np.concatenate([x - x.mean() for x in r["grupos"]])


def ajustados(r):
    """Yij_gorro = media_i  (el valor que el modelo predice para cada dato)."""
    return np.concatenate([np.full(len(x), x.mean()) for x in r["grupos"]])


def diagnostico(r, alpha=0.05):
    """Los 4 chequeos que siempre se piden despues de un ANOVA."""
    e = residuales(r)
    aj = ajustados(r)

    sw = stats.shapiro(e)
    lev = stats.levene(*r["grupos"], center="mean")
    bar = stats.bartlett(*r["grupos"])

    print("  1) NORMALIDAD de los residuales   -> grafico Q-Q  |  Shapiro-Wilk")
    print(f"     W = {sw.statistic:.4f}   p = {sw.pvalue:.4f}  -> "
          f"{'OK' if sw.pvalue > alpha else 'FALLA (usar Kruskal-Wallis o transformar)'}")
    print("  2) HOMOCEDASTICIDAD               -> residuos vs valores ajustados | Levene/Bartlett")
    print(f"     Levene   W  = {lev.statistic:.4f}   p = {lev.pvalue:.4f}")
    print(f"     Bartlett X2 = {bar.statistic:.4f}   p = {bar.pvalue:.4f}")
    print("     Varianzas por tratamiento: " +
          "  ".join(f"{n}={v:.3f}" for n, v in zip(r["nombres"], r["varianzas"])))
    print("  3) INDEPENDENCIA                  -> se garantiza por la ALEATORIZACION")
    print("     (si hay orden temporal: residuos vs orden / Durbin-Watson)")
    print("  4) MEDIA CERO de los residuales   -> siempre se cumple por construccion")
    print(f"     suma de residuales = {e.sum():.10f}")
    print(f"     rango de ajustados = [{aj.min():.2f}, {aj.max():.2f}]")


def kruskal_wallis(r):
    """Alternativa no parametrica al ANOVA (compara medianas por rangos)."""
    k = stats.kruskal(*r["grupos"])
    print(f"  Kruskal-Wallis H = {k.statistic:.4f}   gl = {r['k']-1}   p = {k.pvalue:.3e}")
    print(f"  Chi2 critico(0.05, {r['k']-1}) = {stats.chi2.ppf(0.95, r['k']-1):.4f}")
    print(f"  -> {'RECHAZAR H0' if k.pvalue < 0.05 else 'NO RECHAZAR H0'}"
          "  (H0: las k poblaciones tienen la misma distribucion/mediana)")
    return k


def residuos_vs_ajustados(r, ancho=50):
    """Version en texto del grafico residuos vs ajustados (busca forma de embudo)."""
    e, aj = residuales(r), ajustados(r)
    lim = max(abs(e).max(), 1e-9)
    print(f"  ajustado |{'-'*(ancho//2)}0{'-'*(ancho//2)}|   (residual)")
    for m, nom in sorted(zip(r["medias"], r["nombres"])):
        fila = [" "] * (ancho + 1)
        for ei in e[aj == m]:
            pos = int(round((ei / lim) * (ancho / 2) + ancho / 2))
            fila[pos] = "*" if fila[pos] == " " else "#"
        print(f"  {m:8.2f} |{''.join(fila)}|  {nom}")
    print("  >> bandas de ancho PARECIDO = varianza constante (homocedasticidad OK)")
    print("  >> forma de embudo / cono   = la varianza crece con la media (FALLA)")


if __name__ == "__main__":
    r = anova_dca([[15, 17, 16, 14, 18, 16, 15, 17], [20, 22, 21, 19, 23, 21, 20, 22],
                   [25, 27, 26, 24, 28, 26, 25, 27], [22, 24, 23, 21, 25, 23, 22, 24]],
                  ["Control", "Organico", "Quimico", "Mixto"])
    tabla_anova(r)
    residuos_vs_ajustados(r)
