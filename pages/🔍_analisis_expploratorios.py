import streamlit as st
import pandas as pd

st.header('Proyecto integrador')
st.text('El dominio de cambio de temperatura de FAOSTAT difunde estadísticas de la variación de la temperatura media de la superficie por país, con actualizaciones anuales. La difusión actual abarca el período 1961-2019. Se dispone de estadísticas para las anomalías de la temperatura media mensual, estacional y anual, es decir, el cambio de temperatura con respecto a una climatología de referencia, correspondiente al período 1951-1980. También está disponible la desviación estándar del cambio de temperatura de la metodología de referencia. Los datos se basan en los datos GISTEMP disponibles públicamente, los datos del cambio de temperatura de la superficie global distribuidos por el Instituto Goddard de Estudios Espaciales de la Administración Nacional de Aeronáutica y el Espacio (NASA-GISS).')
df = pd.read_csv('static/Environment_Temperature_change_E_All_Data_NOFLAG.csv', encoding='latin1')
st.text('📁Daostos del CSV del proyecto')
st.dataframe(df)

st.subheader('Estadisticas descriptivas del archivo CSV')
st.write(df.describe())