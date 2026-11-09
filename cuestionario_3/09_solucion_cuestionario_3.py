"""
09_solucion_cuestionario_3.py
Solucion completa del Cuestionario 3 - DCA / ANOVA de un factor
Diseno de Experimentos
"""
import numpy as np
from scipy import stats
import importlib.util, pathlib

_spec = importlib.util.spec_from_file_location(
    "hd", pathlib.Path(__file__).parent / "08_herramientas_dca.py")
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)


def titulo(txt):
    print(f"\n{'='*70}\n{txt}\n{'='*70}")


def sub(txt):
    print(f"\n--- {txt} " + "-" * max(0, 64 - len(txt)))


# #####################################################################
titulo("APLICACION 1 - Tratamientos termicos, resistencia a la traccion (MPa)")
# #####################################################################
A = [28, 31, 29, 30, 32]
B = [34, 33, 35, 32, 36]
C = [38, 40, 37, 39, 41]
D = [44, 43, 45, 42, 46]
r1 = H.anova_dca([A, B, C, D], list("ABCD"))

sub("Paso 0) Totales por tratamiento (de aqui sale TODO)")
for nom, g, s, m in zip(r1["nombres"], [A, B, C, D], r1["sumas"], r1["medias"]):
    print(f"  {nom}: {g}   suma={s:.0f}   n=5   media={m:.2f}")
print(f"  Gran total = {r1['sumas'].sum():.0f}   N = {r1['N']}   k = {r1['k']}")

sub("P1) Media global (gran media)")
print(f"  Y.. / N = {r1['sumas'].sum():.0f} / {r1['N']} = {r1['gran_media']}")
print("  RESPUESTA: b) 36.75 MPa")

sub("P2) Hipotesis nula del DCA")
print("  Modelo: Yij = mu + tau_i + eij")
print("  H0: tau_1 = tau_2 = tau_3 = tau_4 = 0   <=>   H0: mu_1 = mu_2 = mu_3 = mu_4")
print("  Las dos son equivalentes, pero la forma 'correcta' en terminos de MEDIAS es:")
print("  RESPUESTA: b) H0: mu1 = mu2 = mu3 = mu4")
print("  (si el examen pide la forma del modelo de efectos, seria a)")

sub("P3) Suma de Cuadrados Total")
print("  SCT = suma de (Yij - gran_media)^2   sobre las 20 observaciones")
print("      = SCTrat + SCE")
print(f"  SCT = {r1['sc_total']}   ->  se redondea a 594")
print("  RESPUESTA: a) 594   (valor exacto 593.75)")

sub("P4) Suma de Cuadrados de tratamientos")
print("  SCTrat = n * suma de (media_i - gran_media)^2     (n = 5 por grupo)")
for nom, m in zip(r1["nombres"], r1["medias"]):
    print(f"     {nom}: (({m:.0f} - 36.75)^2) = {(m-36.75)**2:8.4f}")
print(f"  suma = {sum((m-36.75)**2 for m in r1['medias']):.4f}  ->  x 5 = {r1['sc_trat']}")
print("  RESPUESTA: 553.75")

sub("P5-P7) Tabla ANOVA completa (por si piden SCE, gl, CM o F)")
print(f"  SCE = SCT - SCTrat = {r1['sc_total']} - {r1['sc_trat']} = {r1['sc_error']}")
print(f"  gl: trat = k-1 = {r1['gl_trat']} | error = N-k = {r1['gl_error']} | total = N-1 = {r1['gl_total']}")
print(f"  CMTrat = {r1['sc_trat']}/{r1['gl_trat']} = {r1['cm_trat']}")
print(f"  CME    = {r1['sc_error']}/{r1['gl_error']} = {r1['cm_error']}   <- estimador de sigma^2")
print(f"  F      = CMTrat/CME = {r1['cm_trat']}/{r1['cm_error']} = {r1['F']:.4f}")
print()
H.tabla_anova(r1)
print("  Conclusion: los 4 tratamientos termicos NO dan la misma resistencia media.")

sub("P8) Tukey HSD con q_0.05(4,16) = 4.05")
hsd = H.tukey_hsd(r1["cm_error"], 5, 4.05)
print(f"  HSD = q * sqrt(CME/n) = 4.05 * sqrt({r1['cm_error']}/5)")
print(f"      = 4.05 * sqrt({r1['cm_error']/5}) = 4.05 * {np.sqrt(0.5):.4f} = {hsd:.4f}")
print("  RESPUESTA: 2.86")

sub("P9) Pares que NO son significativamente diferentes")
H.comparar_pares(r1["medias"], r1["nombres"], hsd, "HSD")
print("  Todas las diferencias (4, 5, 5, 9, 10, 14) superan 2.86")
print("  -> NO hay ningun par 'no significativo'")
print("  RESPUESTA: d) Todos los pares son diferentes")

sub("P10) Prueba de homocedasticidad")
print("  RESPUESTA: b) Levene o Bartlett")
print("  (Shapiro-Wilk = normalidad; Durbin-Watson = independencia; t de Student = medias)")
print()
H.supuestos(r1)

# #####################################################################
titulo("APLICACION 2 - Metodos de capacitacion, productividad (und/dia)")
# #####################################################################
E = [42, 45, 43, 47, 44, 46]
P = [50, 52, 49, 53, 51, 54]
M = [48, 49, 47, 50, 46, 51]
r2 = H.anova_dca([E, P, M], ["E-learning", "Presencial", "Mixto"])

sub("Paso 0) Totales")
for nom, g, s, m in zip(r2["nombres"], [E, P, M], r2["sumas"], r2["medias"]):
    print(f"  {nom:<11}: {g}  suma={s:.0f}  n=6  media={m:.4f}")
print(f"  Gran total = {r2['sumas'].sum():.0f}   N = {r2['N']}   k = {r2['k']}"
      f"   gran media = {r2['gran_media']:.4f}")

sub("P11) Media del metodo Presencial")
print("  (50+52+49+53+51+54)/6 = 309/6 = 51.5")
print("  RESPUESTA: 51.5")

sub("P12) Hipotesis alternativa")
print("  H1: al menos una media poblacional difiere (no todas iguales)")
print("  RESPUESTA: c)")

sub("P13-P15) Sumas de cuadrados")
print("  SCTrat = n * suma (media_i - gran_media)^2, con n=6, gran media = 48.1667")
for nom, m in zip(r2["nombres"], r2["medias"]):
    print(f"     {nom:<11}: ({m:.4f} - 48.1667)^2 = {(m-r2['gran_media'])**2:8.4f}")
print(f"  suma = {sum((m-r2['gran_media'])**2 for m in r2['medias']):.4f}  -> x 6 = {r2['sc_trat']:.4f}")
print("  P14 RESPUESTA: c) 148")
print(f"  SCE = {r2['sc_error']:.4f}   (cada grupo aporta 17.5)")
print(f"  SCT = SCTrat + SCE = {r2['sc_total']:.4f}")

sub("P16) Estadistico F")
print(f"  gl: trat = {r2['gl_trat']}, error = {r2['gl_error']}")
print(f"  CMTrat = 148/2 = {r2['cm_trat']:.4f}")
print(f"  CME    = {r2['sc_error']:.1f}/{r2['gl_error']} = {r2['cm_error']:.4f}")
print(f"  F = {r2['cm_trat']:.2f}/{r2['cm_error']:.4f} = {r2['F']:.4f}   <- valor CORRECTO con los datos")
print("  NINGUNA de las opciones da 21.14  ->  respuesta estricta: NINGUNA")
print("  OJO: el cuestionario asume SCE=80 (CME=80/15=5.333); con eso F=74/5.333=13.87,")
print("       que es la opcion e). Si el resto del cuestionario usa 5.333, marca e).")
print()
H.tabla_anova(r2)

sub("P17) Conclusion con F_tab(2,15) = 3.68")
print(f"  F = {r2['F']:.2f} > 3.68  (y tambien 13.87 > 3.68)  ->  cae en region de rechazo")
print("  RESPUESTA: b) Rechazar H0; hay diferencias entre metodos")

sub("P18) LSD de Fisher con t_0.025(15) = 2.131")
lsd_real = H.lsd_fisher(r2["cm_error"], 6, 2.131)
lsd_cuest = H.lsd_fisher(80 / 15, 6, 2.131)
print("  LSD = t * sqrt(2*CME/n)")
print(f"  Con CME real = {r2['cm_error']:.4f}: 2.131*sqrt(2*{r2['cm_error']:.4f}/6) = {lsd_real:.4f}")
print(f"  Con CME = 5.333 (el del cuestionario): 2.131*sqrt(1.7778) = {lsd_cuest:.4f}")
print("  RESPUESTA a marcar: 2.84   (es la que usa el enunciado de la P19)")

sub("P19) Pares que difieren")
H.comparar_pares(r2["medias"], ["E", "P", "M"], lsd_cuest, "LSD")
print("  7 > 2.84 ; 4 > 2.84 ; 3 > 2.84  ->  los tres pares difieren")
print("  RESPUESTA: a) todos")

titulo("RESUMEN DE RESPUESTAS")
for q, a in [("1", "b) 36.75 MPa"), ("2", "b) H0: mu1=mu2=mu3=mu4"),
             ("3", "a) 594  (593.75)"), ("4", "553.75"), ("8", "2.86"),
             ("9", "d) todos los pares son diferentes"), ("10", "b) Levene o Bartlett"),
             ("11", "51.5"), ("12", "c) al menos una media es diferente"),
             ("14", "c) 148"), ("16", "e) 13.87 segun el cuestionario | F real = 21.14"),
             ("17", "b) Rechazar H0"), ("18", "2.84  (con CME real: 2.30)"),
             ("19", "a) todos")]:
    print(f"  P{q:<3} -> {a}")
