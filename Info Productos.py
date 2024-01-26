import pandas as pd
import requests
import time
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException


import requests
from bs4 import BeautifulSoup
# https://auth.mercadolibre.com.mx/authorization?response_type=code&client_id=7740131767656174&redirect_uri=https://reypi.com.br
app = 'Bearer APP_USR-7740131767656174-012313-481ef8a182c73f73f35dfedf021b1085-17228348'
id_categoria = 'MLM191825'
ruta_productos = 'Productos MLM191825 - 2024-01-23_08-03-09.csv'

def obtener_datos(link):
    # Envía una solicitud HTTP al sitio web
    respuesta = requests.get(link)

    # Comprueba si la solicitud fue exitosa
    if respuesta.status_code != 200:
        print(f"Error al acceder a {link}")
        return None

    # Analiza el HTML con BeautifulSoup
    soup = BeautifulSoup(respuesta.text, 'html.parser')

    # Busca el elemento deseado por su clase
    elemento = soup.find(class_='ui-pdp-subtitle')

    # Extrae y retorna el texto si el elemento existe
    return elemento.get_text(strip=True) if elemento else "No encontrado"

df = pd.read_csv(ruta_productos)

# Obtener la fecha y hora actual para guardar el dataframe con la fecha que se extrajo
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
# Crear el nombre del archivo información
nombre_archivo_csv = f"Info_Productos_{id_categoria}_{timestamp}.csv"

info_producto = []
lista_errores =  []

for id_producto in df['ID'][:1000]:
    print(id_producto)
    url = f"https://api.mercadolibre.com/items/{id_producto}"

    payload = {}
    headers = {
    'Authorization': app
    }
    max_attempts = 4
    for attempt in range(max_attempts):
        try:
            response1 = requests.request("GET", url, headers=headers, data=payload, timeout=10)
            response1.raise_for_status()  # Lanzará una excepción si la solicitud no fue exitosa (código de estado diferente de 2xx)
            data = response1.json()
            print('OK')
            break
        except requests.exceptions.RequestException as e:
            print(f"Intento {attempt + 1} fallido. Razón: {str(e)} obteniendo items")
        if attempt < max_attempts - 1:
            print("Reintentando en 2 segundos...")
            time.sleep(2)  # Espera 2 segundos antes de intentar nuevamente
        else:
            lista_errores.append({"Items": id_producto})
            print("Número máximo de intentos obteniendo Items. La solicitud no se pudo completar.")

    url = f"https://api.mercadolibre.com/items/{id_producto}/description"

    payload = {}
    headers = {
    'Authorization': app
    }

    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            response2 = requests.request("GET", url, headers=headers, data=payload, timeout=10)
            response2.raise_for_status()  # Lanzará una excepción si la solicitud no fue exitosa (código de estado diferente de 2xx)
            descripcion_json = response2.json()
            descripcion = descripcion_json['plain_text']
            print('OK')
            break
        except requests.exceptions.HTTPError as http_err:
            if response2.status_code == 404:
                print(f"Intento {attempt + 1} fallido. Razón: {http_err}. Recurso no encontrado (404). Obteniendo descripción")
                break
            else:
                print(f"Intento {attempt + 1} fallido. Razón: {http_err}. Obteniendo descripción")
        except requests.exceptions.RequestException as e:
            print(f"Intento {attempt + 1} fallido. Razón: {str(e)} obteniendo descripción")
        if attempt < max_attempts - 1:
            print("Reintentando en 2 segundos...")
            time.sleep(2)  # Espera 2 segundos antes de intentar nuevamente
        else:
            lista_errores.append({"Descripción": id_producto})
            descripcion = None
            print("Número máximo de intentos obteniendo de Descripción. La solicitud no se pudo completar.")
    catalogo_id = data.get('catalog_product_id', None)
    print(catalogo_id)
    id = data.get('id', None)
    title = data.get('title', None)
    seller_id = data.get('seller_id', None)
    precio = data.get('price', None)
    inventario_inicial = data.get('initial_quantity', None)
    link = data.get('permalink', None)
    print(link)
    fecha_creacion = data.get('date_created', None)
    ultima_actualizacion = data.get('last_updated', None)
    atributos = data.get('attributes', [])
    categoria = data.get('category_id', None)
    salud = data.get('health', None)
      
    lista_atributos = []
    for i in range(len(atributos)):
        atributo = atributos[i]
        name = atributo.get('name', None)
        value_name = atributo.get('value_name', None)
        lista_atributos.append({"": [name, value_name]})

    

    url = f"https://api.mercadolibre.com/products/{catalogo_id}"

    payload = {}
    headers = {
    'Authorization': app
    }
    print(link)
    max_attempts = 1
    for attempt in range(max_attempts):
        try:
            response3 = requests.get(url, headers=headers, timeout=10)
            response3.raise_for_status()
            catalogo_id = response3.json()
            ventas2 = catalogo_id['sold_quantity']
            print('Ventas con Api:', ventas2)
            break
        except requests.exceptions.RequestException as e:
            print(f"Intento {attempt + 1} fallido. Razón: {str(e)} obteniendo ventas2")
        if attempt < max_attempts - 1:
            print("Reintentando en 2 segundos...")
            time.sleep(2)
        else:
            print("Número máximo de intentos alcanzado obteniendo ventas. La solicitud no se pudo completar.")
            ventas2 = 'bt'   
    if link is not None:
        if ventas2 == 'bt':
            max_attempts = 2
            for attempt in range(max_attempts):
                try: 
                    ventas2 = obtener_datos(link)
                    print('Ventas con Beauti', ventas2)
                    break
                except NoSuchElementException as e:
                    print(f"Error al usar obtener_datos. Razón: {str(e)}")
                    print(f"Intento {attempt + 1} fallido. Razón: {str(e)} obteniendo ventas")
                if attempt < max_attempts - 1:
                    print("Reintentando en 2 segundos...")
                    time.sleep(2)
                else:
                    print("Número máximo de intentos alcanzado obteniendo ventas. La solicitud no se pudo completar.")
                    ventas2 = 0
                    lista_errores.append({"Ventas Web": id_producto})
    else:
        ventas2 = 0
        lista_errores.append({"Link None": id_producto})
    

    # #Agregar los datos al Dataframe
    info_producto.append({
        "ID": id,
        'Titulo': title,
        'ID_Seller': seller_id,
        'Precio': precio,
        'Inventario_Inicial': inventario_inicial,
        'link': link,
        'Fecha de Creacion': fecha_creacion,
        'Ultima_Actualizacion': ultima_actualizacion,
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

print(lista_errores)

end = datetime.now()
time_work = end - now
print(time_work)