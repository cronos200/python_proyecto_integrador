import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine


# Configuración de la conexión a la base de datos
import pandas as pd

DB_CONFIG = {
    'user': 'sql5799726',
    'password': '4ULUABLR5l',
    'host': 'sql5.freesqldatabase.com',
    'database': 'sql5799726'
}

# 1. Establecer la conexión y crear un cursor
try:
    cnn = mysql.connector.connect(**DB_CONFIG)
    cursor = cnn.cursor()

    # # Mostrar todas las tablas de la BD
    # cursor.execute("SHOW TABLES;")
    # print("Tablas en la base de datos:")
    # for (tabla,) in cursor.fetchall():
    #     print("   -", tabla)

    # 2. Consulta a la tabla countries
    query = "SELECT * FROM countries;"
    df = pd.read_sql_query(query, cnn)
    
    #consulta de la tabla eventos_climaticos
    eventos_climaticos = 'select * from event_types'
    df_climaticos = pd.read_sql_query(eventos_climaticos, cnn)

    # consulta de la tabla eventos economicos 
    eventos_economicos = 'select * from event_economics'
    df_economia = pd.read_sql_query(eventos_economicos, cnn)

    #consulta de la tabla energy_data
    datos_energeticos = 'select * from energy_data'
    df_energia = pd.read_sql_query(datos_energeticos, cnn)

    #consulta de la tabla event_impacts
    eventos_impactos = 'select * from event_impacts'
    df_impactos = pd.read_sql_query(eventos_impactos, cnn)

    #consulta de la tabla events
    eventos = 'select * from events'
    df_eventos = pd.read_sql_query(eventos, cnn)

    # # Consulta combinada con joins
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

    df_resumen = pd.read_sql_query(consulta, cnn)


    # 3. Mostrar los datos
    # print("Datos de la tabla 'countries':")
    # print(df_climaticos)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        print("La base de datos no existe.")
    elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Usuario o contraseña incorrectos.")
    else:
        print(f"Error de conexión: {err}")
    exit()
cursor.close()
cnn.close()



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

# Mostrar resultado en Streamlit
st.title("Resumen por País")
st.dataframe(df_resumen)

st.title("🌍 Inversión Energética vs Impacto Económico por País")

st.dataframe(df)

df_melt = df_resumen.melt(
    id_vars="pais", 
    value_vars=["inversion_energia_millones_usd", "impacto_economico_millones_usd"],
    var_name="tipo", value_name="millones_usd"
)

plt.figure(figsize=(18,6))
sns.lineplot(
    data=df_melt, 
    x="pais", 
    y="millones_usd", 
    hue="tipo", 
    marker="o"   # opcional: pone puntos en cada dato
)
plt.xticks(rotation=45)
plt.ylabel("Millones de USD")
plt.xlabel("País")
plt.title("Inversión energética vs Impacto económico")
st.pyplot(plt)


