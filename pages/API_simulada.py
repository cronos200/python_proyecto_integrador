import pandas as pd
import streamlit as st
from mockoon_api_to_dataframe import obtener_datos_mockoon

df = obtener_datos_mockoon()
st.header('Consumo de Una API simulada con mockoon')
st.dataframe(df)

