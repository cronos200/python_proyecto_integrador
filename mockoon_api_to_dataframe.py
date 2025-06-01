import requests
import pandas as pd

def obtener_datos_mockoon():
    url = "http://localhost:3000/users"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)

        print("Primeras 5 filas del DataFrame:")
        print(df.head())

        df.to_csv("mockoon_users.csv", index=False)
        print("Datos guardados en 'mockoon_users.csv'")

        return df  # 🔥 ESTA LÍNEA ES LA CLAVE

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

    return None  # Si algo falla, devuelves None
