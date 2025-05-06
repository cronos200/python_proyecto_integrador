import streamlit as st
import pandas as pd

st.header('Proyecto integrador')
df = pd.read_csv('static/Environment_Temperature_change_E_All_Data_NOFLAG.csv', encoding='latin1')
st.text('📁Daostos del CSV del proyecto')
st.dataframe(df)