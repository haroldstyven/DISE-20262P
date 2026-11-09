"""
12_solucion_cuestionario_4.py
Solucion completa del Cuestionario 4 - DCA: aplicaciones 3, 4 y 5
Diseno de Experimentos
"""
import numpy as np
from scipy import stats
import importlib.util, pathlib

_spec = importlib.util.spec_from_file_location(
    "hdg", pathlib.Path(__file__).parent / "11_herramientas_diagnostico.py")
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)


def titulo(txt):
    print(f"\n{'='*70}\n{txt}\n{'='*70}")


def sub(txt):
    print(f"\n--- {txt} " + "-" * max(0, 64 - len(txt)))


def totales(r):
    for nom, g, s, m in zip(r["nombres"], r["grupos"], r["sumas"], r["medias"]):
        print(f"  {nom:<10}: n={len(g):<3} suma={s:<6.0f} media={m:.2f}")
    print(f"  Gran total = {r['sumas'].sum():.0f}   N = {r['N']}   k = {r['k']}"
          f"   gran media = {r['gran_media']:.4f}")


def sctrat_detalle(r):
    print(f"  SCTrat = n * suma (media_i - {r['gran_media']:.4f})^2")
    for nom, m in zip(r["nombres"], r["medias"]):
        print(f"     {nom:<10}: ({m:.2f} - {r['gran_media']:.2f})^2 = "
              f"{(m - r['gran_media'])**2:8.4f}")
    tot = sum((m - r["gran_media"]) ** 2 for m in r["medias"])
    print(f"  suma = {tot:.4f}   ->  x {r['n'][0]} = {r['sc_trat']:.4f}")


# #####################################################################
titulo("APLICACION 3 - Fertilizantes y biomasa seca (g)   k=4, n=8, N=32")
# #####################################################################
r3 = H.anova_dca([[15, 17, 16, 14, 18, 16, 15, 17],
                  [20, 22, 21, 19, 23, 21, 20, 22],
                  [25, 27, 26, 24, 28, 26, 25, 27],
                  [22, 24, 23, 21, 25, 23, 22, 24]],
                 ["Control", "Organico", "Quimico", "Mixto"])

sub("Paso 0) Totales por tratamiento")
totales(r3)

sub("P21) Media del tratamiento Quimico")
print("  (25+27+26+24+28+26+25+27)/8 = 208/8 = 26.0")
print("  RESPUESTA: a) 26.0")

sub("P22) Media global")
print(f"  688 / 32 = {r3['gran_media']}")
print("  RESPUESTA: a) 21.5")

sub("P23) SCT")
sctrat_detalle(r3)
print(f"  SCE = suma (Yij - media_i)^2 = 12 por grupo x 4 = {r3['sc_error']:.0f}")
print(f"  SCT = SCTrat + SCE = {r3['sc_trat']:.0f} + {r3['sc_error']:.0f} = {r3['sc_total']:.0f}")
print("  RESPUESTA: 472")

sub("P24-P26) Tabla ANOVA (gl, CM y F, por si los piden)")
print(f"  gl: trat = {r3['gl_trat']} | error = {r3['gl_error']} | total = {r3['gl_total']}")
print(f"  CMTrat = {r3['sc_trat']:.0f}/{r3['gl_trat']} = {r3['cm_trat']:.4f}")
print(f"  CME    = {r3['sc_error']:.0f}/{r3['gl_error']} = {r3['cm_error']:.4f}")
print(f"  F      = {r3['F']:.4f}")
print()
H.tabla_anova(r3)

sub("P27) Conclusion con F_tab(3,28) = 2.95")
print(f"  F = {r3['F']:.2f} >> 2.95  ->  region de rechazo")
print("  RESPUESTA: b) El fertilizante afecta significativamente la biomasa")

sub("P28) Tukey HSD con q_0.05(4,28) = 3.86")
hsd3 = H.tukey_hsd(r3["cm_error"], 8, 3.86)
print(f"  HSD = q * sqrt(CME/n) = 3.86 * sqrt({r3['cm_error']:.4f}/8)")
print(f"      = 3.86 * sqrt({r3['cm_error']/8:.4f}) = 3.86 * {np.sqrt(r3['cm_error']/8):.4f} = {hsd3:.4f}")
print("  RESPUESTA: 1.79")

sub("P29) Par que NO es significativo")
H.comparar_pares(r3["medias"], ["C", "O", "Q", "M"], hsd3, "HSD")
print("  La menor diferencia es O vs M = 2 > 1.79  ->  ninguna queda por debajo del HSD")
print("  RESPUESTA: d) Todos son significativos")

sub("P30) Grafico para homocedasticidad")
print("  RESPUESTA: b) Residuos vs valores ajustados  (se busca que NO haya embudo)")
print("  (Q-Q e histograma -> normalidad; dispersion de medias -> no diagnostica varianza)")
print()
H.residuos_vs_ajustados(r3)

# #####################################################################
titulo("APLICACION 4 - Dosis de antihipertensivo (mmHg)   k=4, n=10, N=40")
# #####################################################################
r4 = H.anova_dca([[2, 3, 1, 4, 2, 3, 2, 1, 3, 2],
                  [5, 6, 4, 7, 5, 6, 4, 5, 6, 5],
                  [10, 11, 9, 12, 10, 11, 9, 10, 11, 10],
                  [14, 15, 13, 16, 14, 15, 13, 14, 15, 14]],
                 ["Placebo", "10mg", "20mg", "30mg"])

sub("Paso 0) Totales")
totales(r4)

sub("P33) SCTrat")
sctrat_detalle(r4)
print("  RESPUESTA: 847.5")

sub("P34) CMError con SCError = 120 y gl_error = 36")
print("  CME = SCE / gl_error = 120 / 36 = 3.3333")
print("  RESPUESTA: b) 3.33")
print(f"  (NOTA: con los datos reales del enunciado SCE = {r4['sc_error']:.1f} y "
      f"CME = {r4['cm_error']:.2f};")
print("   el cuestionario impone SCE=120, asi que para P34/P37 se usa 3.33)")

sub("P35-P36) F y conclusion (F_tab = 2.87)")
cm_trat4 = r4["sc_trat"] / 3
print(f"  CMTrat = 847.5 / 3 = {cm_trat4:.2f}")
print(f"  F (version del cuestionario) = {cm_trat4:.2f} / 3.3333 = {cm_trat4/(120/36):.2f}")
print(f"  F (con los datos reales)     = {r4['F']:.2f}")
print("  En ambos casos F >> 2.87")
print("  RESPUESTA P36: b) La dosis afecta significativamente la presion arterial")
print()
H.tabla_anova(r4)

sub("P37) LSD de Fisher con t_0.025(36) = 2.03")
lsd4 = H.lsd_fisher(120 / 36, 10, 2.03)
print("  LSD = t * sqrt(2*CME/n) = 2.03 * sqrt(2*3.3333/10)")
print(f"      = 2.03 * sqrt(0.6667) = 2.03 * {np.sqrt(0.6667):.4f} = {lsd4:.4f}")
print("  RESPUESTA: 1.66")

sub("P38) Pares que NO son significativos")
H.comparar_pares(r4["medias"], ["P", "10", "20", "30"], lsd4, "LSD")
print("  La menor diferencia es P vs 10 = 3.0 > 1.66")
print("  RESPUESTA: d) Todos son significativos")

sub("P39-P40) Si los residuos no son normales")
print("  RESPUESTA P40: b) Kruskal-Wallis")
print("  (Friedman es para BLOQUES/medidas repetidas; la transformacion log ayuda")
print("   sobre todo cuando el problema es la varianza, no la normalidad)")
H.kruskal_wallis(r4)

# #####################################################################
titulo("APLICACION 5 - Estilos de liderazgo y satisfaccion   k=3, n=8, N=24")
# #####################################################################
r5 = H.anova_dca([[55, 58, 57, 56, 59, 54, 56, 57],
                  [75, 78, 77, 76, 79, 74, 76, 77],
                  [65, 68, 67, 66, 69, 64, 66, 67]],
                 ["Autoritario", "Democratico", "Laissez"])

sub("Paso 0) Totales")
totales(r5)

sub("P41) Media del estilo Democratico")
print("  612 / 8 = 76.5")
print("  RESPUESTA: b) 76.5")

sub("P42) Media global")
print(f"  1596 / 24 = {r5['gran_media']}")
print("  RESPUESTA: b) 66.5")

sub("P43) SCT")
sctrat_detalle(r5)
print(f"  SCE = 18 por grupo x 3 = {r5['sc_error']:.0f}")
print(f"  SCT = {r5['sc_trat']:.0f} + {r5['sc_error']:.0f} = {r5['sc_total']:.0f}")
print("  RESPUESTA: 1654")

sub("P44-P45) F con gl_error = 21, CMError = 9.52 y CMTrat = 800")
print(f"  CMTrat = SCTrat/gl = {r5['sc_trat']:.0f}/{r5['gl_trat']} = {r5['cm_trat']:.0f}  (coincide con el 800 del enunciado)")
print(f"  F = 800 / 9.52 = {800/9.52:.2f}")
print("  RESPUESTA: 84.03")
print(f"  (NOTA: con los datos reales CME = {r5['cm_error']:.3f} y F = {r5['F']:.1f};")
print("   el cuestionario impone CME=9.52, asi que se responde 84.03)")
print()
H.tabla_anova(r5)

sub("P46) Conclusion (F_tab = 3.47)")
print("  84.03 > 3.47  ->  rechazar H0")
print("  RESPUESTA: b) El liderazgo afecta la satisfaccion laboral")
print("  (c) 'solo el democratico es diferente' no se puede afirmar con la F;")
print("   eso lo dice la comparacion multiple posterior)")

sub("P47-P49) Supuestos")
H.diagnostico(r5)
print("  P49 RESPUESTA: b) Independencia de los errores")
print("  (aleatorizar la asignacion es lo que hace que los errores no esten correlacionados)")

sub("P50) Grafico para normalidad de residuos")
print("  RESPUESTA: b) Grafico Q-Q (normal probability plot)")

titulo("RESUMEN DE RESPUESTAS")
for q, a in [("21", "a) 26.0"), ("22", "a) 21.5"), ("23", "472"),
             ("27", "b) el fertilizante afecta la biomasa"), ("28", "1.79"),
             ("29", "d) todos son significativos"), ("30", "b) residuos vs ajustados"),
             ("33", "847.5"), ("34", "b) 3.33"),
             ("36", "b) la dosis afecta la presion arterial"), ("37", "1.66"),
             ("38", "d) todos son significativos"), ("40", "b) Kruskal-Wallis"),
             ("41", "b) 76.5"), ("42", "b) 66.5"), ("43", "1654"), ("45", "84.03"),
             ("46", "b) el liderazgo afecta la satisfaccion"),
             ("49", "b) independencia de los errores"), ("50", "b) grafico Q-Q")]:
    print(f"  P{q:<3} -> {a}")
