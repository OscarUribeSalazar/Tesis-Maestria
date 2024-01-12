import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime

id_producto = 'MLM1910972743'

ruta_productos = 'Productos MLM455214 - 2024-01-12_06-05-45.csv'
df = pd.read_csv(ruta_productos)

# Obtener la fecha y hora actual para guardar el dataframe con la fecha que se extrajo
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
# Crear el nombre del archivo información
nombre_archivo_csv = f"Info_Productos_{timestamp}.csv"

info_producto = []

for id_producto in df['ID'][:10]:
    print(id_producto)

    url = f"https://api.mercadolibre.com/items/{id_producto}"

    payload = {}
    headers = {
    'Authorization': 'Bearer APP_USR-7740131767656174-011208-4f929ce1b04eba6437746f2924f50fce-17228348'
    }

    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            response1 = requests.request("GET", url, headers=headers, data=payload, timeout=10)
            response1.raise_for_status()  # Lanzará una excepción si la solicitud no fue exitosa (código de estado diferente de 2xx)
            data = response1.json()
            break
        except requests.exceptions.RequestException as e:
            print(f"Intento {attempt + 1} fallido. Razón: {str(e)}")
        if attempt < max_attempts - 1:
            print("Reintentando en 5 segundos...")
            time.sleep(5)  # Espera 5 segundos antes de intentar nuevamente
        else:
            print("Número máximo de intentos alcanzado. La solicitud no se pudo completar.")

    url = f"https://api.mercadolibre.com/items/{id_producto}/description"

    payload = {}
    headers = {
    'Authorization': 'Bearer APP_USR-7740131767656174-011208-4f929ce1b04eba6437746f2924f50fce-17228348'
    }

    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            response2 = requests.request("GET", url, headers=headers, data=payload, timeout=10)
            response2.raise_for_status()  # Lanzará una excepción si la solicitud no fue exitosa (código de estado diferente de 2xx)
            descripcion_json = response2.json()
            break
        except requests.exceptions.RequestException as e:
            print(f"Intento {attempt + 1} fallido. Razón: {str(e)}")
        if attempt < max_attempts - 1:
            print("Reintentando en 5 segundos...")
            time.sleep(5)  # Espera 5 segundos antes de intentar nuevamente
        else:
            print("Número máximo de intentos alcanzado. La solicitud no se pudo completar.")

    descripcion = descripcion_json['plain_text']

    catalogo_id = data['catalog_product_id']

    url = f"https://api.mercadolibre.com/products/{catalogo_id}"

    payload = {}
    headers = {
    'Authorization': 'Bearer APP_USR-7740131767656174-011208-4f929ce1b04eba6437746f2924f50fce-17228348'
    }

    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            response3 = requests.request("GET", url, headers=headers, data=payload, timeout=10)
            response3.raise_for_status()  # Lanzará una excepción si la solicitud no fue exitosa (código de estado diferente de 2xx)
            catalago_id = response3.json()
            break
        except requests.exceptions.RequestException as e:
            print(f"Intento {attempt + 1} fallido. Razón: {str(e)}")
        if attempt < max_attempts - 1:
            print("Reintentando en 5 segundos...")
            time.sleep(5)  # Espera 5 segundos antes de intentar nuevamente
        else:
            print("Número máximo de intentos alcanzado. La solicitud no se pudo completar.")

    ventas2 = catalago_id['sold_quantity']

    id = data['id']
    title = data['title']
    seller_id = data['seller_id']
    precio = data['price']
    inventario_inicial = data['initial_quantity']
    link = data['permalink']
    fecha_creacion = data['date_created']
    ultima_actializacion = data['last_updated']
    atributos = data['attributes']
    categoria = data['category_id']
    lista_atributos = []
    for i in range(len(atributos)):
        atributo = atributos[i]
        name = atributo['name']
        value_name = atributo['value_name']
        lista_atributos.append({"":[name, value_name]})
    salud = data['health']

    # #Agregar los datos al Dataframe
    info_producto.append({
        "ID": id,
        'Titulo': title,
        'ID_Seller': seller_id,
        'Precio': precio,
        'Inventario_Inicial': inventario_inicial,
        'link': link,
        'Fecha de Creacion': fecha_creacion,
        'Ultima_Actualizacion': ultima_actializacion,
        'Salud': salud,
        'Categoria': categoria,
        'Ventas': ventas2,
        'Atributos': lista_atributos,
        'Descripción': descripcion
    })  

# Crear un DataFrame a partir de la lista de reseñas
info_producto_df = pd.DataFrame(info_producto)

# Guardar los datos en un archivo CSV
info_producto_df.to_csv(nombre_archivo_csv, index=False)
