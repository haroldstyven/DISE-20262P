"""
06_solucion_cuestionario_2.py
Solucion completa del Cuestionario 2 - Pruebas de Hipotesis
Diseno de Experimentos
"""
import numpy as np
from scipy import stats
import importlib.util, pathlib

_spec = importlib.util.spec_from_file_location(
    "hh", pathlib.Path(__file__).parent / "05_herramientas_hipotesis.py")
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)


def titulo(txt):
    print(f"\n{'='*70}\n{txt}\n{'='*70}")


def sub(txt):
    print(f"\n--- {txt} " + "-" * max(0, 64 - len(txt)))


# #####################################################################
titulo("FILA A - Cereal: mu0=20 oz, sigma=6, n=64, xbar=18")
# #####################################################################

sub("A1) Que tipo de prueba?")
print("  El enunciado dice: 'ha DECREMENTADO' y 'no debe ser MENOR que 20'")
print("  -> nos interesa solo el lado bajo")
print("  H0: mu >= 20      Ha: mu < 20")
print("  RESPUESTA: PRUEBA DE COLA IZQUIERDA")

sub("A2) Estadistico de prueba Z")
r = H.prueba_z(18, 20, 6, 64, cola="izquierda", alpha=0.05)
print(f"  ee = sigma/sqrt(n) = 6/sqrt(64) = 6/8 = {6/8}")
print(f"  Z = (xbar - mu0)/ee = (18 - 20)/0.75 = {r['est']:.4f}")
print(f"  RESPUESTA: Z = {r['est']:.4f}  (aprox -2.67)")

sub("A3) Conclusion con alpha = 0.05")
H.reporte("A", r, 20, "izquierda")
print("  RESPUESTA: SE RECHAZA LA HIPOTESIS NULA")
print("  Interpretacion: si hay evidencia de que el peso medio real")
print("  disminuyo por debajo de 20 oz.")

# #####################################################################
titulo("FILA B")
# #####################################################################

sub("B1) Que describe correctamente a H0?")
print("  RESPUESTA: 'Afirma que no hay diferencia ni relacion entre las variables'")
print("  H0 es el statu quo, la posicion por defecto (el 'acusado inocente').")
print("  x 'lo que el investigador desea probar' -> eso es Ha")
print("  x 'existe relacion significativa'       -> eso es Ha")
print("  x 'siempre se acepta'                   -> falso, y ademas nunca se 'acepta'")

sub("B2) Cuando se rechaza H0?")
print("  RESPUESTA: 'Cuando los datos de la muestra apoyan suficientemente")
print("              la hipotesis alternativa (Ha)'")
print("  Es decir: cuando el estadistico cae en la region de rechazo")
print("  (equivalente: p-valor < alpha).")

sub("B3) Error de tipo I")
print("  RESPUESTA: 'Rechazar H0 cuando H0 es VERDADERA'  (falsa alarma)")
print("             Probabilidad = alpha")
print("  El otro error: Tipo II = NO rechazar H0 cuando H0 es FALSA (prob = beta)")

sub("B4) Horas de estudio > 10 (muestra grande)")
print("  Palabra clave: 'MAYOR a 10' -> cola derecha")
print("  RESPUESTA:")
print("     H0: mu <= 10   (o bien  H0: mu = 10)")
print("     Ha: mu >  10")
print("  Prueba Z de cola derecha (muestra grande). Region de rechazo: z > 1.645")

sub("B5) Ingreso difiere de 800")
print("  Palabra clave: 'DIFIERE de' -> dos colas")
print("  RESPUESTA: H0: mu = 800 ; Ha: mu != 800")

sub("B6) n=64, xbar=11.2, sigma=4, mu0=10, alpha=0.05, cola derecha")
r6 = H.prueba_z(11.2, 10, 4, 64, cola="derecha")
H.reporte("B6", r6, 10, "derecha")
print("  RESPUESTA: Rechazar H0 porque z > 1.645")

sub("B7) n=100, xbar=47, sigma=10, mu0=50, alpha=0.05, cola izquierda")
r7 = H.prueba_z(47, 50, 10, 100, cola="izquierda")
H.reporte("B7", r7, 50, "izquierda")
print("  RESPUESTA: Rechazar H0 porque z < -1.645")

sub("B8) n=144, xbar=760, sigma=120, mu0=800, alpha=0.05, dos colas")
r8 = H.prueba_z(760, 800, 120, 144, cola="dos")
H.reporte("B8", r8, 800, "dos")
print("  RESPUESTA: Rechazar H0 porque |z| > 1.96")

sub("B9) n=16, xbar=17, s=4, mu0=15, alpha=0.05, cola derecha -> t")
r9 = H.prueba_t(17, 15, 4, 16, cola="derecha")
print("  s es MUESTRAL y n=16 pequeno -> distribucion t con gl = 15")
H.reporte("B9", r9, 15, "derecha")
print("  RESPUESTA: Rechazar H0 porque t > 1.753")

sub("B10) n=25, xbar=66, s=10, mu0=70, alpha=0.05, cola izquierda -> t")
r10 = H.prueba_t(66, 70, 10, 25, cola="izquierda")
print("  gl = 24")
H.reporte("B10", r10, 70, "izquierda")
print("  RESPUESTA: Rechazar H0 porque t < -1.711")

sub("B11) n=9, xbar=16, s=6, mu0=20, alpha=0.05, dos colas -> t")
r11 = H.prueba_t(16, 20, 6, 9, cola="dos")
print("  gl = 8")
H.reporte("B11", r11, 20, "dos")
print("  RESPUESTA: No rechazar H0 porque |t| < 2.306")
print("  OJO: la diferencia parece grande (16 vs 20) pero con solo n=9")
print("  no alcanza la significancia. Falta potencia.")

sub("B12) n=36, xbar=56, sigma=16, mu0=60, 95% -> dos colas")
r12 = H.prueba_z(56, 60, 16, 36, cola="dos")
H.reporte("B12", r12, 60, "dos")
li = 56 - 1.96 * (16 / 6); ls = 56 + 1.96 * (16 / 6)
print(f"  Comprobacion por IC95%: [{li:.4f} , {ls:.4f}] -> contiene 60, no se rechaza")
print("  RESPUESTA: 'Hay evidencia estadistica que la calificacion media es igual a 60'")
print("  (rigurosamente: NO hay evidencia para afirmar que sea distinta de 60)")

sub("B13) n=100, xbar=64, sigma=16, mu0=60, 95% -> dos colas")
r13 = H.prueba_z(64, 60, 16, 100, cola="dos")
H.reporte("B13", r13, 60, "dos")
li = 64 - 1.96 * 1.6; ls = 64 + 1.96 * 1.6
print(f"  Comprobacion por IC95%: [{li:.4f} , {ls:.4f}] -> NO contiene 60, se rechaza")
print("  RESPUESTA: 'Hay evidencia estadistica que la calificacion media es")
print("              DIFERENTE de 60'")

sub("B14) Baterias: sigma=0.5 CONOCIDA, n=5, poblacion normal")
d = np.array([1.5, 2.5, 2.9, 3.2, 4.0])
print(f"  Datos: {[float(x) for x in d]}   xbar = {d.mean():.2f}")
print("  Clave: la desviacion estandar 0.5 es POBLACIONAL y esta DADA.")
print("  Cuando sigma se conoce y la poblacion es normal -> se usa Z,")
print("  sin importar que n sea pequeno.")
print("  RESPUESTA: 'Z porque la muestra era pequena y se conoce la varianza'")
zc = stats.norm.ppf(0.975)
li = d.mean() - zc * 0.5 / np.sqrt(5); ls = d.mean() + zc * 0.5 / np.sqrt(5)
print(f"  (Extra) IC95% con Z = [{li:.4f} , {ls:.4f}]")
print(f"     contiene mu0=2? {'SI' if li <= 2 <= ls else 'NO'}"
      f" -> {'no se rechaza' if li <= 2 <= ls else 'se rechaza'} que duren 2 anios")

# #####################################################################
titulo("RESUMEN DE RESPUESTAS")
# #####################################################################
resp = [
    ("A1", "Prueba de cola izquierda"),
    ("A2", f"Z = {r['est']:.4f}  (aprox -2.67)"),
    ("A3", "Se rechaza la hipotesis nula"),
    ("B1", "Afirma que no hay diferencia ni relacion entre las variables"),
    ("B2", "Cuando los datos apoyan suficientemente a Ha"),
    ("B3", "Rechazar H0 cuando H0 es verdadera"),
    ("B4", "H0: mu <= 10 ; Ha: mu > 10   (cola derecha)"),
    ("B5", "H0: mu = 800 ; Ha: mu != 800"),
    ("B6", f"Rechazar H0 porque z > 1.645        (z = {r6['est']:+.2f})"),
    ("B7", f"Rechazar H0 porque z < -1.645       (z = {r7['est']:+.2f})"),
    ("B8", f"Rechazar H0 porque |z| > 1.96       (z = {r8['est']:+.2f})"),
    ("B9", f"Rechazar H0 porque t > 1.753        (t = {r9['est']:+.2f})"),
    ("B10", f"Rechazar H0 porque t < -1.711       (t = {r10['est']:+.2f})"),
    ("B11", f"No rechazar H0 porque |t| < 2.306   (t = {r11['est']:+.2f})"),
    ("B12", f"La calificacion media es igual a 60 (z = {r12['est']:+.2f})"),
    ("B13", f"La calificacion media es diferente de 60 (z = {r13['est']:+.2f})"),
    ("B14", "Z porque la muestra era pequena y se conoce la varianza"),
]
for k, v in resp:
    print(f"  {k:>4} | {v}")
print()
