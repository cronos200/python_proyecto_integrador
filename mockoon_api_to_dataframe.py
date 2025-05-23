import requests
import pandas as pd

# URL de la API mock de Mockoon
url = "http://localhost:3000/users"

try:
    # Hacer la solicitud GET a la API
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    response.raise_for_status()

    # Convertir la respuesta JSON en una lista de diccionarios
    data = response.json()

    # Crear un DataFrame con los datos
    df = pd.DataFrame(data)

    # Mostrar las primeras filas del DataFrame
    print("Primeras 5 filas del DataFrame:")
    print(df.head())

    # Guardar el DataFrame como CSV
    df.to_csv("mockoon_users.csv", index=False)
    print("Datos guardados en 'mockoon_users.csv'")

except requests.exceptions.HTTPError as http_err:
    print(f"Error HTTP: {http_err}")
except requests.exceptions.ConnectionError as conn_err:
    print(f"Error de conexión: {conn_err}")
except requests.exceptions.Timeout as timeout_err:
    print(f"Error de timeout: {timeout_err}")
except requests.exceptions.RequestException as req_err:
    print(f"Error en la solicitud: {req_err}")
except ValueError as json_err:
    print(f"Error al procesar JSON: {json_err}")