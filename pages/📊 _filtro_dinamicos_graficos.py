import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la página (solo una vez)
st.set_page_config(page_title="Análisis de Temperaturas", layout="wide")

st.title("🌡️ Evolución del cambio de temperatura (1961–2019)")
st.write("Visualización del cambio mensual de temperatura por país usando datos históricos.")

@st.cache_data
def cargar_datos():
    df = pd.read_csv("static/Environment_Temperature_change_E_All_Data_NOFLAG.csv", encoding="latin1")
    df = df[df["Element"] == "Temperature change"]
    return df

# Cargar datos solo una vez
df_temp = cargar_datos()

# Lista de países
paises = sorted(df_temp["Area"].unique())

# Selección de país (por defecto "Colombia" si está en la lista)
pais_seleccionado = st.selectbox("Selecciona un país", paises, index=paises.index("Colombia") if "Colombia" in paises else 0)

# Filtrar datos para el país seleccionado
df_pais = df_temp[df_temp["Area"] == pais_seleccionado]

# Transformar columnas de año a filas
df_long = df_pais.melt(
    id_vars=["Area", "Months"],
    value_vars=[col for col in df_temp.columns if col.startswith("Y")],
    var_name="Año",
    value_name="Temperatura"
)
df_long["Año"] = df_long["Año"].str[1:].astype(int)

# --- Gráfico de líneas ---
st.subheader(f"📈 Cambio de temperatura mensual en {pais_seleccionado}")

fig, ax = plt.subplots(figsize=(14, 6))
sns.lineplot(data=df_long, x="Año", y="Temperatura", hue="Months", palette="tab10", ax=ax)
ax.set_title(f"Evolución del cambio de temperatura en {pais_seleccionado} (1961–2019)")
ax.set_xlabel("Año")
ax.set_ylabel("Cambio de temperatura (°C)")
ax.grid(True)
ax.legend(title="Mes", bbox_to_anchor=(1.05, 1), loc="upper left")
st.pyplot(fig)

# --- Mapa de calor ---
st.subheader(f"🔥 Mapa de calor de temperatura en {pais_seleccionado}")

# Convertir datos al formato de matriz para heatmap
df_pivot = df_long.pivot(index="Months", columns="Año", values="Temperatura")

# Reordenar meses para que tengan el orden lógico
orden_meses = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
df_pivot = df_pivot.reindex(orden_meses)

# Crear y mostrar heatmap
fig, ax = plt.subplots(figsize=(15, 6))
sns.heatmap(df_pivot, cmap="coolwarm", linewidths=0.5, annot=False, ax=ax)
ax.set_title(f"Cambio de temperatura mensual en {pais_seleccionado} (1961–2019)")
st.pyplot(fig)

# --- Boxplot mensual ---
st.subheader(f"📦 Distribución del cambio de temperatura por mes en {pais_seleccionado}")

fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=df_long, x="Months", y="Temperatura", order=orden_meses, palette="Set2", ax=ax)
ax.set_title("Distribución mensual del cambio de temperatura")
ax.set_xlabel("Mes")
ax.set_ylabel("Cambio de temperatura (°C)")
ax.grid(True)
st.pyplot(fig)

# --- Gráfico de barras (promedio anual) ---
st.subheader(f"📊 Promedio anual del cambio de temperatura en {pais_seleccionado}")

df_anual = df_long.groupby("Año")["Temperatura"].mean().reset_index()

fig, ax = plt.subplots(figsize=(14, 6))
sns.barplot(data=df_anual, x="Año", y="Temperatura", palette="viridis", ax=ax)
ax.set_title("Promedio anual del cambio de temperatura")
ax.set_xlabel("Año")
ax.set_ylabel("Cambio de temperatura (°C)")
ax.tick_params(axis='x', labelsize=8)
plt.xticks(rotation=45)
st.pyplot(fig)
