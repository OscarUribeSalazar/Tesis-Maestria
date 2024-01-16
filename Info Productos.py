import pandas as pd
import requests
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

# https://auth.mercadolibre.com.mx/authorization?response_type=code&client_id=7740131767656174&redirect_uri=https://reypi.com.br

ruta_productos = 'Productos MLM455214 - 2024-01-12_06-05-45.csv'
df = pd.read_csv(ruta_productos)

# Obtener la fecha y hora actual para guardar el dataframe con la fecha que se extrajo
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
# Crear el nombre del archivo información
nombre_archivo_csv = f"Info_Productos_{timestamp}.csv"

info_producto = []
lista_errores =  []

for id_producto in df['ID'][2200:3200]:
    print(id_producto)

    url = f"https://api.mercadolibre.com/items/{id_producto}"

    payload = {}
    headers = {
    'Authorization': 'Bearer APP_USR-7740131767656174-011515-6f612c03ec9c4dc13b8815d24a1bd892-17228348'
    }
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            response1 = requests.request("GET", url, headers=headers, data=payload, timeout=10)
            response1.raise_for_status()  # Lanzará una excepción si la solicitud no fue exitosa (código de estado diferente de 2xx)
            data = response1.json()
            break
        except requests.exceptions.RequestException as e:
            print(f"Intento {attempt + 1} fallido. Razón: {str(e)} obteniendo items")
        if attempt < max_attempts - 1:
            print("Reintentando en 5 segundos...")
            time.sleep(5)  # Espera 5 segundos antes de intentar nuevamente
        else:
            lista_errores.append({"Items": id_producto})
            print("Número máximo de intentos obteniendo Items. La solicitud no se pudo completar.")

    url = f"https://api.mercadolibre.com/items/{id_producto}/description"

    payload = {}
    headers = {
    'Authorization': 'Bearer APP_USR-7740131767656174-011515-6f612c03ec9c4dc13b8815d24a1bd892-17228348'
    }

    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            response2 = requests.request("GET", url, headers=headers, data=payload, timeout=10)
            response2.raise_for_status()  # Lanzará una excepción si la solicitud no fue exitosa (código de estado diferente de 2xx)
            descripcion_json = response2.json()
            descripcion = descripcion_json['plain_text']
            break
        except requests.exceptions.RequestException as e:
            print(f"Intento {attempt + 1} fallido. Razón: {str(e)} obteniendo descripción")
        if attempt < max_attempts - 1:
            print("Reintentando en 5 segundos...")
            time.sleep(5)  # Espera 5 segundos antes de intentar nuevamente
        else:
            lista_errores.append({"Descripción": id_producto})
            descripcion = None
            print("Número máximo de intentos obteniendo de Descripción. La solicitud no se pudo completar.")
    catalogo_id = data.get('catalog_product_id', None)
    id = data.get('id', None)
    title = data.get('title', None)
    seller_id = data.get('seller_id', None)
    precio = data.get('price', None)
    inventario_inicial = data.get('initial_quantity', None)
    link = data.get('permalink', None)
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
    'Authorization': 'Bearer APP_USR-7740131767656174-011515-6f612c03ec9c4dc13b8815d24a1bd892-17228348'
    }

    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            response3 = requests.request("GET", url, headers=headers, data=payload, timeout=10)
            response3.raise_for_status()
            catalago_id = response3.json()
            ventas2 = catalago_id['sold_quantity']
            break
        except requests.exceptions.RequestException as e:
            if "Not Found for url: https://api.mercadolibre.com/products/None" in str(e):
                print("URL no encontrada. Saltando a Selenium...")
                max_attempts_nav = 3
                for attempts_nav in range(max_attempts_nav):
                    try:
                        # Abrir la página web de búsqueda
                        # Configura las opciones de Chrome
                        chrome_options = Options()
                        prefs = {"profile.managed_default_content_settings.images": 2}  # Esto deshabilita las imágenes
                        chrome_options.add_experimental_option("prefs", prefs)
                        # Inicia el navegador con las opciones configuradas
                        driver = webdriver.Chrome(options=chrome_options)
                        driver.get(link)
                        elemento = driver.find_element(By.CLASS_NAME, 'ui-pdp-subtitle')
                        ventas2 = elemento.text
                        # Cerrar el controlador de Selenium
                        driver.quit()
                        break
                    except NoSuchElementException as e:
                        print(f"Intento {attempts_nav + 1} fallido. Razón: {str(e)}")
                        if attempts_nav < max_attempts_nav - 1:
                            print("Reintentando en 2 segundos...")
                            time.sleep(2)
                        else:
                            lista_errores.append({"Descripción": id_producto})
                            ventas2 = 0
                            print("Número máximo de intentos alcanzado. La solicitud no se pudo completar.")
                break
            else:
                print(f"Intento {attempt + 1} fallido. Razón: {str(e)} obteniendo ventas")
                if attempt < max_attempts - 1:
                    print("Reintentando en 2 segundos...")
                    time.sleep(2)
                else:
                    lista_errores.append({"Descripción": id_producto})
                    ventas2 = 0
                    print("Número máximo de intentos alcanzado obteniendo ventas. La solicitud no se pudo completar.")
    
    print(ventas2)

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