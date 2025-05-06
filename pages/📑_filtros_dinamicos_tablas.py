import streamlit as st
import pandas as pd

st.header('Promedio anual de cambio de temperatura por país🌡️')
st.text('Queremos obtener, para cada país, el promedio del cambio de temperatura desde 1961 hasta 2019, usando solo los valores donde Element sea "Temperature change".')
df = pd.read_csv('static/Environment_Temperature_change_E_All_Data_NOFLAG.csv', encoding='latin1')

df_temp = df[df["Element"] == "Temperature change"]
columnas_anios = [col for col in df_temp.columns if col.startswith("Y")]
df_promedios = df_temp.groupby("Area")[columnas_anios].mean()
df_promedios["Promedio General"] = df_promedios.mean(axis=1)
st.dataframe(df_promedios)

st.header('🔆Evolución de temperatura en un país específico:')
st.text('Queremos obtener el cambio de temperatura o desviación estándar seleccionando el país en un mes específico.')
paises = df['Area'].unique().tolist()
elementos = df['Element'].unique().tolist()
meses = df['Months'].unique().tolist()

pais = st.selectbox('Selecciona un país', paises)
elemento = st.selectbox('Selecciona un elemento', elementos)
mes = st.selectbox('Selecciona un mes', meses)
filtro = (df['Area'] == pais) & (df['Element'] == elemento) & (df['Months'] == mes)
df_filtrado = df[filtro]
st.subheader('Datos filtrados')
st.dataframe(df_filtrado)



st.header("Filtro por País y Año - Cambio de Temperatura")
st.text('Seleccionar datos de un año y comparar el cambio de temperatura entre los diferentes países')
columnas_año = [col for col in df.columns if col.startswith('Y')]
pais_seleccionado = st.selectbox("Selecciona un país:", sorted(paises))
anio_seleccionado = st.selectbox("Selecciona un Año:", sorted(columnas_año))
df_filtrado = df[df['Area'] == pais_seleccionado]
promedio = df_filtrado[anio_seleccionado].mean()
st.markdown(f"### Cambio de temperatura en *{pais_seleccionado}* en *{anio_seleccionado}*")
st.metric(label="Temperatura promedio (°C)", value=f"{promedio:.2f}")
st.dataframe(df_filtrado[['Months', anio_seleccionado]].rename(columns={anio_seleccionado: 'Temperatura (°C)'}))



st.header('Pais con la mayor y menor temperatura en un año y mes específicos.')
df_temp = df[df["Element"] == "Temperature change"]
columnas_anios = [col for col in df_temp.columns if col.startswith("Y")]
df_melted = df_temp.melt(
    id_vars=["Area", "Months", "Element"],
    value_vars=columnas_anios,
    var_name="Year",
    value_name="TemperatureChange"
)

df_melted.dropna(subset=["TemperatureChange"], inplace=True)
fila_max = df_melted.loc[df_melted["TemperatureChange"].idxmax()]
fila_min = df_melted.loc[df_melted["TemperatureChange"].idxmin()]
tabla_max = fila_max[["Area", "Year", "Months", "TemperatureChange"]].to_frame().T
tabla_min = fila_min[["Area", "Year", "Months", "TemperatureChange"]].to_frame().T

st.subheader("🥵 Pais y fecha más afectada por el cambio climático:")
st.dataframe(tabla_max)
st.subheader("\n🌞 Pais y fecha menos afectada por el cambio climático:")
st.dataframe(tabla_min)



st.header('🔍Variabilidad de Temperatura (Desviación Estándar) por País y Mes')
year_columns = [col for col in df.columns if col.startswith('Y')]

df_melted = df.melt(
    id_vars=[col for col in df.columns if col not in year_columns],
    value_vars=year_columns,
    var_name='Year',
    value_name='Standard Deviation'
)

df_melted['Year'] = df_melted['Year'].str.replace('Y', '')
df_std = df_melted[df_melted['Element'] == 'Standard Deviation']
tabla_std = df_std.groupby(['Area', 'Months'])['Standard Deviation'].mean().reset_index()

paises = ['Todos'] + sorted(tabla_std['Area'].unique())
meses = ['Todos'] + sorted(tabla_std['Months'].unique())

pais_sel = st.selectbox("Filtrar por país:", paises)
mes_sel = st.selectbox("Filtrar por mes:", meses)


if pais_sel != 'Todos':
    tabla_std = tabla_std[tabla_std['Area'] == pais_sel]
if mes_sel != 'Todos':
    tabla_std = tabla_std[tabla_std['Months'] == mes_sel]

tabla_std = tabla_std.sort_values(by='Standard Deviation', ascending=False)

st.dataframe(tabla_std)