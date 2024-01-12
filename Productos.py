import requests
import pandas as pd
import time
from datetime import datetime

# https://auth.mercadolibre.com.mx/authorization?response_type=code&client_id=7740131767656174&redirect_uri=https://reypi.com.br
app = 'APP_USR-7740131767656174-011208-4f929ce1b04eba6437746f2924f50fce-17228348'

id_categoria = 'MLM455214'

# Obtener la fecha y hora actual para guardar el dataframe con la fecha que se extrajo
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
# Crear el nombre del archivo información
nombre_archivo_csv = f"Productos {id_categoria} - {timestamp}.csv"

limit = 50

url = f"https://api.mercadolibre.com/sites/MLM/search?limit={limit}&category={id_categoria}&offset=0"

payload = {}
headers = {
    'Authorization': 'Bearer APP_USR-7740131767656174-011208-4f929ce1b04eba6437746f2924f50fce-17228348'
}

response = requests.request("GET", url, headers=headers, data=payload, timeout=50)
data = response.json()
num_resultados = 3950

info_categoria = []

for j in range(0, num_resultados, 50):
    offset_3 = j
    url = f"https://api.mercadolibre.com/sites/MLM/search?limit={limit}&category={id_categoria}&offset={offset_3}"
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            response = requests.request("GET", url, headers=headers, data=payload, timeout=50)
            response.raise_for_status()  # Lanzará una excepción si la solicitud no fue exitosa (código de estado diferente de 2xx)
            data = response.json()
            break
        except requests.exceptions.RequestException as e:
            print(f"Intento {attempt + 1} fallido. Razón: {str(e)}")
        if attempt < max_attempts - 1:
            print("Reintentando en 5 segundos...")
            time.sleep(5)  # Espera 5 segundos antes de intentar nuevamente
        else:
            print("Número máximo de intentos alcanzado. La solicitud no se pudo completar.")

    resultados = len(data['results'])
    if resultados == 0:
        break  # Rompe el bucle si no hay más reseñas

    for i in range(resultados):
        elemento = data['results'][i]
        id = elemento['id']
        print(id)

        #Agregar los datos al Dataframe
        info_categoria.append({
            "ID": id,
        })  

# Crear un DataFrame a partir de la lista de reseñas
categoria_df = pd.DataFrame(info_categoria)

# Guardar los datos en un archivo CSV
categoria_df.to_csv(nombre_archivo_csv, index=False)