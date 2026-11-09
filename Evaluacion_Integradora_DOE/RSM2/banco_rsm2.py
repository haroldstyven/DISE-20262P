# Clave transcrita del código fuente de la evaluación RSM2 (campo `correcta`; opción múltiple = índice 0=A..3=D; NUMERIC = valor, tolerancia ±0.5).
# Fila: (id, sección, competencia, enunciado resumido, clave_texto, mi_respuesta, razonamiento, estado, observación)
# estado: OK = derivable/justificable por teoría o por el contexto del enunciado y coincide
#         CTX = coincide, pero sólo se sostiene con el texto del contexto (no vemos el Pareto/modelo del artículo)
#         NV = no derivable con lo aprendido (dato del artículo); no hay respuesta propia
S = {1:"S1 Factorial 2^3 y análisis inicial", 2:"S2 DCC y modelo cuadrático", 3:"S3 Superficies y contornos", 4:"S4 Análisis crítico y conclusiones"}
P = [
(1,1,"Interpretación","Objetivo de ampliar el 2^3 a un DCC","B. Modelar la curvatura significativa detectada","B",
 "Un 2^3 con puntos centrales sólo ajusta un modelo de 1.er orden (+ prueba de curvatura). Al detectarse curvatura (p<0.0003) se añaden puntos axiales para estimar los términos cuadráticos.","OK",""),
(2,1,"Interpretación","Variable de mayor influencia según el Pareto","C. Relación de concentración (A)","C",
 "El contexto lista A primero entre los significativos y dice que A y C tienen efecto positivo 'imponente'. Entre A y C no hay forma de decidir sin ver el Pareto.","CTX","Sin el diagrama del artículo, A vs. C no se puede comprobar; la respuesta se apoya en el orden del contexto."),
(3,1,"Argumentación","Qué implica una curvatura significativa (7.59%)","B. El modelo de 1.er orden no basta; se requiere uno de 2.º orden","B",
 "Curvatura significativa = la media de los puntos centrales difiere de la predicha por el plano; hay términos cuadráticos.","OK",""),
(4,1,"Cálculo","Corridas del DCC: 8 factoriales + 6 axiales + 4 centrales","18","18","8 + 6 + 4 = 18 (el DCC con k=3 tiene 2^3 + 2·3 + n0).","OK",""),
(5,2,"Cálculo","α rotable con k=3, α=(2^k)^(1/4)","1.68","1.68","(2^3)^(1/4) = 8^0.25 = 1.6818 → 1.68.","OK",""),
(6,2,"Interpretación","Propósito de la rotabilidad","B. Varianza de predicción constante a igual distancia del centro","B",
 "Definición: Var(ŷ) depende sólo de la distancia al centro, no de la dirección.","OK",""),
(7,2,"Interpretación","Significado de R² ajustado = 0.9703","A. El modelo explica el 97.03% de la variabilidad","A",
 "Es la mejor opción; el resto son disparates. Matiz: el R² ajustado penaliza por número de términos, no es estrictamente 'varianza explicada'.","OK","Las demás opciones son claramente falsas, por eso A es la única defendible."),
(8,2,"Argumentación","Precisión adecuada = 30.3150","B. Buena relación señal-ruido; el modelo puede navegar el espacio","B",
 "Adequate Precision = señal/ruido; el umbral habitual es > 4. 30.3 lo supera con holgura.","OK",""),
(9,2,"Cálculo","GL del error con 18 corridas y 8 parámetros","10","10","gl error = n − p = 18 − 8 = 10.","OK","Un cuadrático completo con k=3 tiene 10 parámetros (gl=8); el enunciado fija 8, y se sigue el enunciado."),
(10,3,"Interpretación","Interpretación de la interacción AC","B. Subir A y C a la vez aumenta mucho la absorción","B",
 "Contexto: A y C tienen efecto positivo grande y AC es significativa y positiva (efecto sinérgico).","OK",""),
(11,3,"Argumentación","Efecto de la presión (B)","B. Negativo y menos significativo, posiblemente por el rango estrecho","B",
 "El contexto lo dice literalmente: B significativa, efecto negativo y poco relevante en la región evaluada.","OK",""),
(12,3,"Interpretación","Hacia dónde mover el proceso en el contorno C–T","B. Valores altos de concentración y temperatura","B",
 "Ambos efectos son positivos: la ascensión de máxima pendiente va hacia A y C altos.","OK",""),
(13,3,"Cálculo","Máxima remoción de CO2 reportada","62.86","—",
 "Es un dato del artículo; con lo aprendido (y sin los datos del DCC) no se puede calcular.","NV","Sin respuesta propia: el valor sólo puede tomarse de la clave."),
(14,3,"Argumentación","Por qué aún se está lejos de la región óptima","B. Las curvas de nivel no muestran cambio de curvatura (ni elipse ni silla)","B",
 "Si el contorno sigue siendo casi plano/ascendente, no hay punto estacionario cercano: hay que seguir el camino ascendente (steepest ascent).","OK",""),
(15,4,"Interpretación","F = 19.03, p < 0.0001","B. Modelo de regresión altamente significativo","B","p < 0.0001 → se rechaza H0 de que todos los coeficientes son cero.","OK",
 "Con R²=0.9841, n=18 y 8 términos saldría F≈69.6 (para F=19.03 serían 13 términos). El enunciado no es coherente consigo mismo, pero la conclusión es la misma."),
(16,4,"Interpretación","CV = 4.43%","B. Buena precisión y confiabilidad","B","CV = (RMSE/media)·100; < 10% suele considerarse buena reproducibilidad.","OK",""),
(17,4,"Interpretación","Variable de respuesta del estudio","B. Cambio del % de CO2 en el biogás simulado","B","El contexto de S1 la nombra ΔCO2; es la respuesta, no los factores (presión, temperatura, relación).","OK",""),
(18,4,"Argumentación","R² predicho = 0.8774","A. Explicará ≈87.74% de la variabilidad en nuevos datos","A","R²pred (PRESS) mide la capacidad de predicción; R²pred razonablemente cercano a R²aj indica un modelo estable.","OK",""),
(19,4,"Interpretación","A² significativo (p = 0.0125)","A. La relación A–respuesta no es lineal (curvatura)","A","Un término cuadrático significativo = curvatura en esa dirección.","OK",""),
(20,4,"Argumentación","Conclusión sobre el sistema carbonato-bicarbonato","B. Opción viable para remover CO2 y aumentar la disponibilidad energética del biogás","B","Es la conclusión coherente con la máxima remoción y el modelo significativo; las otras opciones contradicen el contexto.","OK",""),
]
