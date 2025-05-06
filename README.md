# 🌡️ Análisis del Cambio de Temperatura Global (1961–2019)

Este proyecto utiliza Python y Pandas para analizar un conjunto de datos sobre el cambio de temperatura global mensual por país desde 1961 hasta 2019. El objetivo es identificar tendencias climáticas, países más afectados, y patrones estacionales de cambio de temperatura.

## 📁 Dataset
- pagina del CSV: kggle
- Fuente: FAO - Organización de las Naciones Unidas para la Alimentación y la Agricultura.
- Años: 1961–2019
- Columnas principales: `Area`, `Months`, `Element`, `Y1961`–`Y2019`

## 📊 Análisis Realizados

- Evolución de temperatura en países específicos
- Comparaciones entre países para un año dado
- Cambios promedio por mes
- Análisis de la desviación estándar del cambio climático

## 🛠️ Tecnologías usadas

- Python
- Pandas
- Streamlit

## 🚀 Cómo usar

1. Clona este repositorio.
2. crea el entorno de virtual en Python (opcional pero recomendado):
   ```python -m venv .venv

3.  Activa el entorno virtual:
   - En Windows:
     ```
     .venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```
     source .venv/bin/activate
     ```

4. Instala las dependencias con:
   ```pip install -r requirements.txt

5. Para ejecutar la aplicación:
   ```streamlit run Inicio.py
