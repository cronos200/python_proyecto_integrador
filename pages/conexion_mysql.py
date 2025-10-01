import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Configuración de la conexión
DB_CONFIG = {
    'user': 'sql5799726',
    'password': '4ULUABLR5l',
    'host': 'sql5.freesqldatabase.com',
    'database': 'sql5799726'
}

# Crear engine de SQLAlchemy con pymysql
engine = create_engine(
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
)

# Consultas directas con pandas
df = pd.read_sql("SELECT * FROM countries;", engine)
df_climaticos = pd.read_sql("SELECT * FROM event_types;", engine)
df_economia = pd.read_sql("SELECT * FROM event_economics;", engine)
df_energia = pd.read_sql("SELECT * FROM energy_data;", engine)
df_impactos = pd.read_sql("SELECT * FROM event_impacts;", engine)
df_eventos = pd.read_sql("SELECT * FROM events;", engine)

# Consulta combinada
consulta = """
SELECT 
    c.country AS pais,
    ROUND(SUM(DISTINCT ed.financial_flows_usd) / 1000000, 2) AS inversion_energia_millones_usd,
    ROUND(SUM(ee.economic_impact_million_usd), 2) AS impacto_economico_millones_usd
FROM 
    countries c
LEFT JOIN energy_data ed ON ed.country_id = c.country_id
LEFT JOIN events e ON e.country_id = c.country_id
LEFT JOIN event_economics ee ON ee.event_id = e.event_id
GROUP BY 
    c.country
ORDER BY 
    c.country;
"""
df_resumen = pd.read_sql(consulta, engine)

# Liberar conexiones
engine.dispose()

# Mostrar tablas en Streamlit
st.title('Tabla de Countries')
st.dataframe(df)
st.title('Tabla Eventos_Climaticos')
st.dataframe(df_climaticos)
st.title('Tabla Eventos_Economicos')
st.dataframe(df_economia)
st.title('Tabla Energy_Data')
st.dataframe(df_energia)
st.title('Tabla Event_Impacts')
st.dataframe(df_impactos)
st.title('Tabla Events')
st.dataframe(df_eventos)

# Mostrar resumen
st.title("Resumen por País")
st.dataframe(df_resumen)

st.title("🌍 Inversión Energética vs Impacto Económico por País")

# Transformar datos para la gráfica
df_melt = df_resumen.melt(
    id_vars="pais", 
    value_vars=["inversion_energia_millones_usd", "impacto_economico_millones_usd"],
    var_name="tipo", value_name="millones_usd"
)

# Crear gráfica
fig, ax = plt.subplots(figsize=(18,6))
sns.lineplot(
    data=df_melt, 
    x="pais", 
    y="millones_usd", 
    hue="tipo", 
    marker="o",
    palette={"inversion_energia_millones_usd": "blue", 
             "impacto_economico_millones_usd": "green"},
    ax=ax
)
plt.xticks(rotation=45)
plt.ylabel("Millones de USD")
plt.xlabel("País")
plt.title("Inversión energética vs Impacto económico")

# Mostrar en Streamlit
st.pyplot(fig)
