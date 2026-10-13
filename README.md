# Material interactivo de Diseño Experimental

Aplicación didáctica en Streamlit para explorar diseños experimentales, modelos estadísticos, grados de libertad del ANOVA y ejemplos gráficos.

## Requisitos

- Python 3.12 o superior
- `pip`

## Instalación y ejecución

Desde la carpeta del proyecto, instala las dependencias y lanza la aplicación:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit abrirá la aplicación en el navegador. Si no se abre automáticamente, visita la URL local que muestra la terminal, normalmente `http://localhost:8501`.

En la barra lateral puedes navegar por DCA, DBCA, DCL, DPD, diseños factoriales y metodología de superficies de respuesta. Los ejemplos y preguntas son material de práctica.

## Detener la aplicación y el Codespace

- Para detener Streamlit, vuelve a la terminal donde corre y pulsa `Ctrl+C`.
- Para detener el Codespace desde GitHub: menú **Code → Codespaces → Stop codespace**.
- También puedes detener el Codespace desde una terminal con `gh codespace stop -c NOMBRE_DEL_CODESPACE`, usando el nombre que aparece en `gh codespace list`.