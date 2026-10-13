"""Material interactivo para un curso de Diseño Experimental."""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# Metadata centralizada para orientar la navegación y presentar los diseños.
DISENOS = {
    "Inicio": {"sigla": "DOE", "descripcion": "Panorama del curso"},
    "DCA": {"sigla": "DCA", "descripcion": "Un factor, asignación aleatoria"},
    "DBCA": {"sigla": "DBCA", "descripcion": "Tratamientos con bloqueo"},
    "DCL": {"sigla": "DCL", "descripcion": "Dos fuentes de bloqueo"},
    "DPD": {"sigla": "DPD", "descripcion": "Parcela principal y subparcela"},
    "Factoriales": {"sigla": "FD", "descripcion": "Efectos e interacciones"},
    "MSR": {"sigla": "MSR", "descripcion": "Optimización y curvatura"},
}

st.set_page_config(page_title="Diseño Experimental", page_icon="📊", layout="wide")


def configurar_pagina(titulo, parrafo_1, parrafo_2, modelo, fuentes):
    """Presenta el marco teórico y la tabla de grados de libertad."""
    st.title(titulo)
    st.write(parrafo_1)
    st.write(parrafo_2)
    st.subheader("Modelo estadístico")
    st.latex(modelo)
    st.subheader("Estructura del ANOVA")
    st.dataframe(
        pd.DataFrame(fuentes, columns=["Fuente de variación", "Grados de libertad"]),
        hide_index=True,
        width="stretch",
    )


def mostrar_ejercicio(pregunta, opciones, correcta, explicacion, clave):
    """Permite responder una pregunta y mostrar retroalimentación."""
    st.subheader("Comprueba lo aprendido")
    respuesta = st.radio(pregunta, opciones, key=f"respuesta_{clave}")
    if st.button("Revisar respuesta", key=f"boton_{clave}"):
        if respuesta == correcta:
            st.success(f"Correcto. {explicacion}")
        else:
            st.error(f"Aún no. {explicacion}")


def pagina_inicio():
    st.title("Diseño Experimental | Laboratorio interactivo")
    st.write(
        "Este material acompaña un curso de Diseño Experimental mediante modelos "
        "estadísticos, ejemplos reproducibles y preguntas de repaso."
    )
    st.write(
        "El objetivo es conectar la estructura de cada experimento con su tabla "
        "ANOVA y con la interpretación visual de los datos. Los ejemplos son "
        "didácticos: sus valores no sustituyen el análisis de un estudio real."
    )
    st.subheader("Diseños disponibles")
    st.dataframe(
        pd.DataFrame(
            [{"Diseño": nombre, **datos} for nombre, datos in DISENOS.items() if nombre != "Inicio"]
        ),
        hide_index=True,
        width="stretch",
    )
    st.info("Selecciona un diseño en la barra lateral. En cada página encontrarás teoría, modelo, grados de libertad, un ejemplo y una actividad.")


def pagina_dca():
    configurar_pagina(
        "DCA | Diseño Completamente al Azar",
        "El DCA compara varios tratamientos cuando las unidades experimentales son suficientemente homogéneas. Cada unidad recibe un tratamiento mediante asignación aleatoria, lo que ayuda a evitar sesgos sistemáticos.",
        "La variación que no explica el tratamiento se agrupa en el error experimental. La inferencia habitual supone errores independientes, de varianza común y aproximadamente normales; conviene revisar estos supuestos antes de concluir.",
        r"Y_{ij}=\mu+\tau_i+\varepsilon_{ij},\quad \sum_i\tau_i=0,\quad \varepsilon_{ij}\sim N(0,\sigma^2)",
        [("Tratamiento", "a - 1 = 2"), ("Error", "N - a = 6"), ("Total", "N - 1 = 8")],
    )
    datos = pd.DataFrame(
        {"Dieta": np.repeat(["A", "B", "C"], 3), "Ganancia (kg)": [4.2, 4.5, 4.1, 5.0, 5.3, 5.1, 5.8, 6.0, 5.7]}
    )
    st.subheader("Ejemplo: ganancia de peso con tres dietas")
    st.dataframe(datos, hide_index=True, width="stretch")
    resumen = datos.groupby("Dieta")["Ganancia (kg)"].agg(media="mean", sd="std", n="count").reset_index()
    resumen["IC 95%"] = 1.96 * resumen["sd"] / np.sqrt(resumen["n"])
    figura = go.Figure(
        go.Bar(
            x=resumen["Dieta"],
            y=resumen["media"],
            error_y={"type": "data", "array": resumen["IC 95%"], "visible": True},
            marker_color=["#167d8d", "#e18a3b", "#527a55"],
        )
    )
    figura.update_layout(
        title="Ganancia media por dieta e intervalo aproximado del 95%",
        xaxis_title="Dieta",
        yaxis_title="Ganancia media (kg)",
    )
    st.plotly_chart(figura, width="stretch")
    mostrar_ejercicio(
        "¿Cuántos grados de libertad tiene el error con 9 observaciones y 3 dietas?",
        ["2", "6", "8"],
        "6",
        "El error tiene N-a=9-3=6 grados de libertad.",
        "dca",
    )


def pagina_dbca():
    configurar_pagina(
        "DBCA | Diseño en Bloques Completamente al Azar",
        "El DBCA incorpora bloques para controlar una fuente conocida de variación ajena al tratamiento, como la posición del terreno. Dentro de cada bloque se comparan todos los tratamientos.",
        "El bloqueo suele reducir el error residual cuando los bloques son internamente homogéneos. El modelo aditivo supone que no hay interacción tratamiento-bloque; si esa interacción es importante, el diseño y su análisis deben reconsiderarse.",
        r"Y_{ij}=\mu+\tau_i+\beta_j+\varepsilon_{ij}",
        [("Fertilizante", "t - 1 = 3"), ("Bloque", "b - 1 = 2"), ("Error", "(t-1)(b-1) = 6"), ("Total", "tb - 1 = 11")],
    )
    tratamientos = ["F1", "F2", "F3", "F4"]
    bloques = ["Bloque 1", "Bloque 2", "Bloque 3"]
    valores = np.array([[21, 24, 26, 28], [23, 25, 27, 30], [20, 23, 25, 27]])
    datos = pd.DataFrame(
        [
            {"Bloque": bloque, "Fertilizante": tratamiento, "Rendimiento": valores[j, i]}
            for j, bloque in enumerate(bloques)
            for i, tratamiento in enumerate(tratamientos)
        ]
    )
    st.subheader("Ejemplo: cuatro fertilizantes en tres bloques")
    st.dataframe(datos, hide_index=True, width="stretch")
    figura = px.line(
        datos,
        x="Fertilizante",
        y="Rendimiento",
        color="Bloque",
        markers=True,
        title="Rendimiento por tratamiento dentro de cada bloque",
        color_discrete_sequence=["#167d8d", "#e18a3b", "#527a55"],
    )
    figura.update_layout(yaxis_title="Rendimiento", xaxis_title="Fertilizante")
    st.plotly_chart(figura, width="stretch")
    mostrar_ejercicio(
        "¿Qué función cumplen los bloques en este diseño?",
        ["Controlar una fuente conocida de variación", "Aumentar el número de tratamientos", "Eliminar la aleatorización"],
        "Controlar una fuente conocida de variación",
        "El bloque absorbe variación sistemática que no es el objetivo principal.",
        "dbca",
    )


def pagina_dcl():
    configurar_pagina(
        "DCL | Diseño en Cuadro Latino",
        "El cuadro latino compara p tratamientos y controla simultáneamente dos fuentes de variación, organizadas como filas y columnas. Cada tratamiento aparece exactamente una vez en cada fila y en cada columna.",
        "Este doble control local permite separar los efectos de fila y columna del efecto de tratamiento. Requiere igual número de niveles para los tres factores y no estima interacciones; la asignación de tratamientos debe aleatorizarse respetando la estructura latina.",
        r"Y_{ijk}=\mu+\tau_i+\beta_j+\gamma_k+\varepsilon_{ijk}",
        [("Filas", "p - 1 = 3"), ("Columnas", "p - 1 = 3"), ("Tratamientos", "p - 1 = 3"), ("Error", "(p-1)(p-2) = 6"), ("Total", "p^2 - 1 = 15")],
    )
    arreglo = np.array(
        [["A", "B", "C", "D"], ["B", "C", "D", "A"], ["C", "D", "A", "B"], ["D", "A", "B", "C"]]
    )
    respuestas = np.array([[18, 21, 24, 27], [20, 23, 25, 22], [25, 28, 19, 22], [27, 20, 23, 26]])
    st.subheader("Ejemplo 4×4: tratamientos A, B, C y D")
    st.write("Cada celda indica tratamiento y respuesta observada; las filas y columnas representan las dos fuentes de bloqueo.")
    figura = go.Figure()
    colores = {"A": "#167d8d", "B": "#e18a3b", "C": "#527a55", "D": "#b84c4c"}
    for fila in range(4):
        for columna in range(4):
            tratamiento = arreglo[fila, columna]
            figura.add_annotation(
                x=columna,
                y=3 - fila,
                text=f"<b>{tratamiento}</b><br>{respuestas[fila, columna]}",
                showarrow=False,
                font={"color": "white", "size": 15},
            )
            figura.add_shape(
                type="rect",
                x0=columna - 0.48,
                x1=columna + 0.48,
                y0=2.52 - fila,
                y1=3.48 - fila,
                fillcolor=colores[tratamiento],
                line={"color": "white", "width": 2},
            )
    figura.update_xaxes(title="Columnas", tickmode="array", tickvals=list(range(4)), ticktext=["1", "2", "3", "4"], range=[-0.6, 3.6])
    figura.update_yaxes(title="Filas", tickmode="array", tickvals=list(range(4)), ticktext=["4", "3", "2", "1"], range=[-0.6, 3.6], scaleanchor="x")
    figura.update_layout(title="Arreglo latino y respuestas", height=430, showlegend=False)
    st.plotly_chart(figura, width="stretch")
    mostrar_ejercicio(
        "¿Qué controla el cuadro latino además de los tratamientos?",
        ["Dos fuentes de variación, filas y columnas", "Solo la variación entre tratamientos", "La interacción entre todos los factores"],
        "Dos fuentes de variación, filas y columnas",
        "Las filas y columnas son los dos controles locales.",
        "dcl",
    )


def pagina_dpd():
    configurar_pagina(
        "DPD | Diseño en Parcelas Divididas",
        "En parcelas divididas, un factor difícil de aplicar se asigna a parcelas principales y otro factor a subparcelas dentro de ellas. Por ejemplo, el riego puede aplicarse a una parcela grande y las variedades distribuirse dentro de cada parcela.",
        "La aleatorización ocurre en dos etapas y genera dos escalas de error. El factor de parcela principal se prueba contra error(a), mientras que el factor de subparcela y la interacción se evalúan con error(b); usar un único error puede dar conclusiones incorrectas.",
        r"Y_{ijk}=\mu+R_k+A_i+u_{ik}+B_j+(AB)_{ij}+\varepsilon_{ijk}",
        [("Bloque", "r - 1 = 2"), ("Riego", "a - 1 = 1"), ("Error(a)", "(r-1)(a-1) = 2"), ("Variedad", "b - 1 = 2"), ("Riego × variedad", "(a-1)(b-1) = 2"), ("Error(b)", "a(r-1)(b-1) = 8"), ("Total", "rab - 1 = 17")],
    )
    riegos = ["Bajo", "Alto"]
    variedades = ["V1", "V2", "V3"]
    base = {"Bajo": [40, 43, 45], "Alto": [48, 54, 57]}
    desplazamientos = [-1, 0, 1]
    filas = []
    for bloque, ajuste in enumerate(desplazamientos, start=1):
        for riego in riegos:
            for indice, variedad in enumerate(variedades):
                filas.append({"Bloque": f"B{bloque}", "Riego": riego, "Variedad": variedad, "Rendimiento": base[riego][indice] + ajuste})
    datos = pd.DataFrame(filas)
    st.subheader("Ejemplo agrícola: riego × variedad")
    st.dataframe(datos, hide_index=True, width="stretch")
    resumen = datos.groupby(["Riego", "Variedad"], as_index=False)["Rendimiento"].mean()
    figura = px.line(
        resumen,
        x="Variedad",
        y="Rendimiento",
        color="Riego",
        markers=True,
        title="Rendimiento medio por variedad y nivel de riego",
        color_discrete_sequence=["#167d8d", "#e18a3b"],
    )
    st.plotly_chart(figura, width="stretch")
    mostrar_ejercicio(
        "¿Contra qué error se evalúa el efecto del riego?",
        ["Error(a), de parcela principal", "Error(b), de subparcela", "El total"],
        "Error(a), de parcela principal",
        "El riego se aplica a parcelas principales y se contrasta con error(a).",
        "dpd",
    )


def pagina_factoriales():
    configurar_pagina(
        "Diseños Factoriales | Efectos e interacciones",
        "Un diseño factorial estudia simultáneamente dos o más factores, cada uno con niveles definidos. Así se estiman efectos principales y se aprovechan todas las combinaciones de niveles.",
        "La interacción indica que el efecto de un factor cambia según el nivel de otro. En ese caso, interpretar solo los promedios globales puede ocultar patrones importantes; el gráfico de interacción ayuda a detectarlos.",
        r"Y_{ijk}=\mu+\alpha_i+\beta_j+(\alpha\beta)_{ij}+\varepsilon_{ijk}",
        [("Temperatura", "a - 1 = 1"), ("Catalizador", "b - 1 = 2"), ("Interacción", "(a-1)(b-1) = 2"), ("Error", "ab(r-1) = 12"), ("Total", "abr - 1 = 17")],
    )
    medias = {("Baja", "C1"): 61, ("Baja", "C2"): 66, ("Baja", "C3"): 70, ("Alta", "C1"): 68, ("Alta", "C2"): 73, ("Alta", "C3"): 81}
    filas = [
        {"Temperatura": temperatura, "Catalizador": catalizador, "Rendimiento": media + ruido}
        for (temperatura, catalizador), media in medias.items()
        for ruido in (-1, 0, 1)
    ]
    datos = pd.DataFrame(filas)
    st.subheader("Ejemplo: temperatura × catalizador sobre rendimiento")
    st.dataframe(datos, hide_index=True, width="stretch")
    resumen = datos.groupby(["Temperatura", "Catalizador"], as_index=False)["Rendimiento"].mean()
    figura = px.line(
        resumen,
        x="Catalizador",
        y="Rendimiento",
        color="Temperatura",
        markers=True,
        title="Gráfico de interacción",
        color_discrete_sequence=["#167d8d", "#e18a3b"],
    )
    figura.update_layout(yaxis_title="Rendimiento medio (%)")
    st.plotly_chart(figura, width="stretch")
    mostrar_ejercicio(
        "Si las líneas del gráfico no son paralelas, ¿qué sugiere?",
        ["Una posible interacción", "Que no existe efecto alguno", "Que falta un nivel de respuesta"],
        "Una posible interacción",
        "La falta de paralelismo sugiere que el efecto del catalizador depende de la temperatura.",
        "factorial",
    )


def pagina_msr():
    configurar_pagina(
        "MSR | Metodología de Superficies de Respuesta",
        "La MSR modela la respuesta en función de factores cuantitativos para comprender tendencias y localizar condiciones de operación convenientes. Un modelo de primer orden aproxima una región casi plana o inclinada.",
        "Cuando aparece curvatura, se utiliza un modelo de segundo orden con términos cuadráticos e interacciones. Un Diseño Central Compuesto combina puntos factoriales, puntos axiales y réplicas centrales para estimar esos términos y valorar el ajuste local.",
        r"Y=\beta_0+\sum_i\beta_iX_i+\sum_i\beta_{ii}X_i^2+\sum_{i<j}\beta_{ij}X_iX_j+\varepsilon",
        [("Términos lineales", "k = 2"), ("Términos cuadráticos", "k = 2"), ("Interacción", "k(k-1)/2 = 1"), ("Error residual", "n - 6 = 7"), ("Total", "n - 1 = 12")],
    )
    st.caption("Para el CCD de ejemplo hay 13 corridas: 4 factoriales, 4 axiales y 5 centrales. La tabla ANOVA resume los 5 grados de libertad del modelo cuadrático.")
    corridas = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1.414, 0), (1.414, 0), (0, -1.414), (0, 1.414)] + [(0, 0)] * 5
    datos = pd.DataFrame(corridas, columns=["Temperatura codificada", "Catalizador codificado"])
    x, y = datos.iloc[:, 0], datos.iloc[:, 1]
    datos["Rendimiento"] = 82 + 5 * x + 4 * y - 6 * x**2 - 4 * y**2 + 2 * x * y
    datos["Rendimiento"] += np.array([0.2, -0.4, 0.3, -0.1, 0.5, -0.2, 0.1, -0.3, 0.1, -0.1, 0.0, 0.2, -0.2])
    st.subheader("Ejemplo: CCD con dos factores")
    st.dataframe(datos.round(2), hide_index=True, width="stretch")
    eje = np.linspace(-1.5, 1.5, 45)
    xx, yy = np.meshgrid(eje, eje)
    zz = 82 + 5 * xx + 4 * yy - 6 * xx**2 - 4 * yy**2 + 2 * xx * yy
    contorno = go.Figure(
        go.Contour(
            x=eje,
            y=eje,
            z=zz,
            colorscale="Tealgrn",
            contours={"showlabels": True, "labelfont": {"size": 10}},
        )
    )
    contorno.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            marker={"color": "#b84c4c", "size": 8, "line": {"color": "white", "width": 1}},
            name="Corridas CCD",
        )
    )
    contorno.update_layout(title="Contorno de rendimiento y corridas", xaxis_title="Temperatura codificada", yaxis_title="Catalizador codificado")
    st.plotly_chart(contorno, width="stretch")
    superficie = go.Figure(go.Surface(x=xx, y=yy, z=zz, colorscale="Tealgrn", showscale=True))
    superficie.update_layout(
        title="Superficie de respuesta estimada",
        scene={"xaxis_title": "Temperatura", "yaxis_title": "Catalizador", "zaxis_title": "Rendimiento"},
    )
    st.plotly_chart(superficie, width="stretch")
    mostrar_ejercicio(
        "¿Qué términos permiten modelar la curvatura en un modelo de segundo orden?",
        ["Términos cuadráticos", "Solo el intercepto", "Únicamente el error"],
        "Términos cuadráticos",
        "Los términos X_i² permiten representar curvatura en la respuesta.",
        "msr",
    )


PAGINAS = {
    "Inicio": pagina_inicio,
    "DCA": pagina_dca,
    "DBCA": pagina_dbca,
    "DCL": pagina_dcl,
    "DPD": pagina_dpd,
    "Factoriales": pagina_factoriales,
    "MSR": pagina_msr,
}

st.sidebar.title("Diseño Experimental")
pagina = st.sidebar.radio(
    "Selecciona una página",
    list(DISENOS.keys()),
    format_func=lambda nombre: f"{DISENOS[nombre]['sigla']} · {nombre}",
)
PAGINAS[pagina]()
st.divider()
st.warning("⚠️ Recuerda detener tu Codespace al terminar para no consumir horas")
