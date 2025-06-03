import pandas as pd
import streamlit as st
import altair as alt
from mockoon_api_to_dataframe import obtener_datos_mockoon

df = obtener_datos_mockoon()
st.header('🗃️Consumo de Una API simulada con mockoon')
st.markdown("""
**Explora el mundo sin salir de tu pantalla.**  
En este archivo encontrarás una recopilación realista y detallada de más de 1000 destinos turísticos internacionales, ideal para inspirar tu próximo viaje o analizar patrones de turismo global con herramientas como Python, Pandas o Streamlit.

Cada entrada contiene información rica y curada, incluyendo:

- 🌍 País y ciudad de destino  
- 🏞️ Lugar turístico recomendado, con una descripción que destaca su historia, belleza natural o importancia cultural  
- 🏨 Hotel sugerido, con calificación por estrellas y una descripción detallada de su estilo, servicios o ubicación  
- 💵 Precio promedio por noche en USD  
- 📅 Fechas disponibles para reservar el viaje

Este conjunto de datos está diseñado para alimentar APIs simuladas (como Mockoon) y sirve como base para construir dashboards, sistemas de recomendación, o entrenar modelos de análisis turístico.
""")

st.dataframe(df)
st.header('🧭Analisis exploratorio')
st.subheader('Muestra las primeras 5 filas')
st.dataframe(df.head())
st.subheader('Muestra las ultimas 5 filas')
st.dataframe(df.tail())
st.subheader('Muestra las estadísticas descriptivas de columnas numéricas')
st.dataframe(df.describe())

st.header('🔍Filtros dinamicos')
st.title("🌍 Explorador de destinos turísticos")
st.markdown("Filtra los destinos según tus preferencias de viaje:")

# 🔍 Filtros dinámicos
# FILTRO POR PAÍS
paises = df['País'].dropna().unique()
pais_seleccionado = st.selectbox("Selecciona un país", ["Todos"] + list(sorted(paises)))

# FILTRO POR CIUDAD
ciudades_filtradas = df[df['País'] == pais_seleccionado]['Ciudad'].unique() if pais_seleccionado != "Todos" else df['Ciudad'].unique()
ciudades_seleccionadas = st.multiselect("Selecciona una o más ciudades", opciones := list(sorted(ciudades_filtradas)), default=opciones)

# FILTRO POR PRECIO POR NOCHE
precio_min = int(df["Precio por Noche (USD)"].min())
precio_max = int(df["Precio por Noche (USD)"].max())
rango_precio = st.slider("Rango de precio por noche (USD)", precio_min, precio_max, (precio_min, precio_max))

# ✅ Aplicar filtros
df_filtrado = df.copy()

if pais_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["País"] == pais_seleccionado]

if ciudades_seleccionadas:
    df_filtrado = df_filtrado[df_filtrado["Ciudad"].isin(ciudades_seleccionadas)]

df_filtrado = df_filtrado[
    (df_filtrado["Precio por Noche (USD)"] >= rango_precio[0]) &
    (df_filtrado["Precio por Noche (USD)"] <= rango_precio[1])
]

# 📊 Mostrar resultados filtrados
st.subheader("🌐 Resultados")
st.write(f"{len(df_filtrado)} resultados encontrados.")
st.dataframe(df_filtrado)

# 📦 Exportar
st.download_button("📥 Descargar CSV", df_filtrado.to_csv(index=False).encode("utf-8"), file_name="viajes_filtrados.csv", mime="text/csv")


st.header('Graficos dinamicos')
st.subheader("📊 Gráficos y visualización")

# Gráfico de barras: Precio promedio por país
st.markdown("### 💵 Precio promedio por país")
precio_promedio = df_filtrado.groupby("País")["Precio por Noche (USD)"].mean().reset_index()

bar_chart = alt.Chart(precio_promedio).mark_bar().encode(
    x=alt.X("País:N", sort="-y"),
    y=alt.Y("Precio por Noche (USD):Q"),
    tooltip=["País", "Precio por Noche (USD)"]
).properties(width=700, height=400)

st.altair_chart(bar_chart)

st.markdown("### 🎯 Precio por lugar turístico (Scatter Plot)")

# Asegurarse que las columnas no tengan tildes ni espacios
df['Lugar Turístico Recomendado'] = df['Lugar Turístico Recomendado'].astype(str)

# Gráfico de dispersión
scatter_chart = alt.Chart(df).mark_circle(size=80).encode(
    x=alt.X("Lugar Turístico Recomendado:N", title="Lugar Turístico", sort=None),
    y=alt.Y("Precio por Noche (USD):Q", title="Precio por Noche (USD)"),
    color="País:N",
    tooltip=["País", "Ciudad", "Lugar Turístico Recomendado", "Precio por Noche (USD)"]
).properties(width=800, height=400).interactive()

st.altair_chart(scatter_chart, use_container_width=True)