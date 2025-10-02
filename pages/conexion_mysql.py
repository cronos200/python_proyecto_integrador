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

# Consulta numero 1 combinada
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


#consulta numero 2
consulta_2 = """
SELECT 
    c.country,
    ed.year,
    ed.co2_emissions_kt,
    ed.renewable_share
FROM 
    energy_data ed
JOIN countries c ON ed.country_id = c.country_id
ORDER BY 
    ed.year, ed.renewable_share DESC;
"""
df_resumen2 = pd.read_sql(consulta_2, engine)

#consulta numero 3
consulta_3 = """
SELECT 
    c.country,
    ed.year,
    ed.access_to_electricity,
    ed.access_to_clean_fuels,
    ed.gdp_per_capita
FROM 
    energy_data ed
JOIN 
    countries c ON ed.country_id = c.country_id
WHERE 
    ed.year BETWEEN 2000 AND 2020
ORDER BY 
    c.country, ed.year;
"""
df_resumen3 = pd.read_sql(consulta_3, engine)


#consulta numero 4
consulta_4 = """
SELECT 
    c.country,
    ed.gdp_per_capita,
    ed.population_density,
    SUM(ei.affected_population) AS total_affected,
    SUM(ei.deaths) AS total_deaths,
    SUM(ei.injuries) AS total_injuries
FROM 
    events e
JOIN 
    countries c ON e.country_id = c.country_id
JOIN 
    event_impacts ei ON e.event_id = ei.event_id
JOIN 
    energy_data ed ON ed.country_id = c.country_id AND ed.year = YEAR(e.date)
GROUP BY 
    c.country, ed.gdp_per_capita, ed.population_density
ORDER BY 
    total_affected DESC;
"""
df_resumen4 = pd.read_sql(consulta_4, engine)

# Liberar conexiones
engine.dispose()

# Mostrar tablas en Streamlit
st.header("Tablas de la base de datos") 
subtabs = st.tabs([ "Countries", "Event Types", "Event Economics", "Energy Data", "Event Impacts", "Events" ]) 
with subtabs[0]: st.dataframe(df) 
with subtabs[1]: st.dataframe(df_climaticos) 
with subtabs[2]: st.dataframe(df_economia) 
with subtabs[3]: st.dataframe(df_energia) 
with subtabs[4]: st.dataframe(df_impactos) 
with subtabs[5]: st.dataframe(df_eventos)


# Mostrar resumen
st.subheader("consulta #1 Resumen por País")
mostrar_codigo = """
consulta = ""
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
    c.country;""
df_resumen = pd.read_sql(consulta, engine)
"""
st.code(mostrar_codigo, language='Python')
# se muestra la primera consulta
st.dataframe(df_resumen)



st.subheader("🌍 Inversión Energética vs Impacto Económico por País")
mostrar_codigo = """
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
"""
st.code(mostrar_codigo, language='Python')
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

#mostrar la consulta numero 2
st.subheader('Relación entre emisiones de CO₂ y renovables')
mostrar_codigo = """
consulta_2 =""
SELECT 
    c.country,
    ed.year,
    ed.co2_emissions_kt,
    ed.renewable_share
FROM 
    energy_data ed
JOIN countries c ON ed.country_id = c.country_id
ORDER BY 
    ed.year, ed.renewable_share DESC;""

df_resumen2 = pd.read_sql(consulta_2, engine)
"""
st.code(mostrar_codigo, language='Python')
st.text('Objetivo: ¿Disminuyen las emisiones a medida que aumenta la energía limpia?')
st.dataframe(df_resumen2)

mostrar_codigo = """
fig2, ax2 = plt.subplots(figsize=(10,6))

sns.scatterplot(
    data=df_resumen2,
    x="renewable_share",
    y="co2_emissions_kt",
    hue="country",
    alpha=0.7,
    ax=ax2
)

plt.xlabel("Participación de renovables (%)")
plt.ylabel("Emisiones de CO₂ (kt)")
plt.title("Relación entre energías renovables y emisiones de CO₂")
st.pyplot(fig2)
"""
st.code(mostrar_codigo, language='python')

fig2, ax2 = plt.subplots(figsize=(10,6))

sns.scatterplot(
    data=df_resumen2,
    x="renewable_share",
    y="co2_emissions_kt",
    hue="country",
    alpha=0.7,
    ax=ax2
)

plt.xlabel("Participación de renovables (%)")
plt.ylabel("Emisiones de CO₂ (kt)")
plt.title("Relación entre energías renovables y emisiones de CO₂")
st.pyplot(fig2)


# mostrar la consulta numero 3
st.subheader('PIB y su relacion a las energias limpias')
mostrar_codigo = """
consulta_3 =""
SELECT 
    c.country,
    ed.year,
    ed.access_to_electricity,
    ed.access_to_clean_fuels,
    ed.gdp_per_capita
FROM 
    energy_data ed
JOIN 
    countries c ON ed.country_id = c.country_id
WHERE 
    ed.year BETWEEN 2000 AND 2020
ORDER BY 
    c.country, ed.year;""

df_resumen3 = pd.read_sql(consulta_3, engine)
"""
st.code(mostrar_codigo, language= 'python')
st.text('¿Tener mejor acceso a electricidad/energías limpias se asocia a un mayor PIB per cápita?')
st.dataframe(df_resumen3)

mostrar_codigo = """
fig1, ax1 = plt.subplots(figsize=(12,6))

sns.lineplot(
    data=df_resumen3,
    x="year",
    y="access_to_electricity",
    hue="country",
    ax=ax1
)
sns.lineplot(
    data=df_resumen3,
    x="year",
    y="access_to_clean_fuels",
    hue="country",
    ax=ax1,
    linestyle="--"
)

plt.title("Acceso a electricidad y combustibles limpios (2000-2020)")
plt.ylabel("Porcentaje de la población (%)")
plt.xlabel("Año")
plt.legend(title="Indicador / País")
st.pyplot(fig1)
"""

st.code(mostrar_codigo, language= 'Python')
fig1, ax1 = plt.subplots(figsize=(12,6))

sns.lineplot(
    data=df_resumen3,
    x="year",
    y="access_to_electricity",
    hue="country",
    ax=ax1
)
sns.lineplot(
    data=df_resumen3,
    x="year",
    y="access_to_clean_fuels",
    hue="country",
    ax=ax1,
    linestyle="--"
)

plt.title("Acceso a electricidad y combustibles limpios (2000-2020)")
plt.ylabel("Porcentaje de la población (%)")
plt.xlabel("Año")
plt.legend(title="Indicador / País")
st.pyplot(fig1)


# Mostrar consulta numero 4
st.subheader("Impacto humano vs PIB per cápita y densidad poblacional")
mostrar_codigo = """
consulta_4 = ""
SELECT 
    c.country,
    ed.gdp_per_capita,
    ed.population_density,
    SUM(ei.affected_population) AS total_affected,
    SUM(ei.deaths) AS total_deaths,
    SUM(ei.injuries) AS total_injuries
FROM 
    events e
JOIN 
    countries c ON e.country_id = c.country_id
JOIN 
    event_impacts ei ON e.event_id = ei.event_id
JOIN 
    energy_data ed ON ed.country_id = c.country_id AND ed.year = YEAR(e.date)
GROUP BY 
    c.country, ed.gdp_per_capita, ed.population_density
ORDER BY 
    total_affected DESC;""

df_resumen4 = pd.read_sql(consulta_4, engine)
"""

st.code(mostrar_codigo, language='python')
st.text('Ver si países con menos desarrollo (PIB per cápita bajo) tienen mayor afectación humana.')
st.dataframe(df_resumen4)

mostrar_codigo = """
fig4, ax4 = plt.subplots(figsize=(12,7))

# Gráfico de burbujas: PIB vs densidad poblacional, tamaño = población afectada
sns.scatterplot(
    data=df_resumen4,
    x="gdp_per_capita",
    y="population_density",
    size="total_affected",
    hue="country",
    alpha=0.7,
    sizes=(50, 2000),  # escala del tamaño de burbujas
    ax=ax4
)

plt.xlabel("PIB per cápita (USD)")
plt.ylabel("Densidad poblacional (hab/km²)")
plt.title("Impacto en la población vs PIB y densidad")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
st.pyplot(fig4)
"""

st.code(mostrar_codigo, language='python')


fig4, ax4 = plt.subplots(figsize=(12,7))

# Gráfico de burbujas: PIB vs densidad poblacional, tamaño = población afectada
sns.scatterplot(
    data=df_resumen4,
    x="gdp_per_capita",
    y="population_density",
    size="total_affected",
    hue="country",
    alpha=0.7,
    sizes=(50, 2000),  # escala del tamaño de burbujas
    ax=ax4
)

plt.xlabel("PIB per cápita (USD)")
plt.ylabel("Densidad poblacional (hab/km²)")
plt.title("Impacto en la población vs PIB y densidad")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
st.pyplot(fig4)
