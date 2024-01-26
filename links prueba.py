
import requests
from bs4 import BeautifulSoup

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

link = 'https://articulo.mercadolibre.com.mx/MLM-1492758661-estructura-de-cama-tamano-queen-con-plataforma-vecelo-con-ca-_JM'

datos = obtener_datos(link)

print(datos)

    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            response3 = requests.request("GET", url, headers=headers, data=payload, timeout=10)
            response3.raise_for_status()
            catalago_id = response3.json()
            ventas2 = catalago_id['sold_quantity']
            break
        except requests.exceptions.RequestException as e:
            if isinstance(e, Exception) and "Not Found for url: https://api.mercadolibre.com/products/None" in str(e) and link is not None:
                print("URL no encontrada. Saltando a BeautifulSoup...")
                max_attempts_nav = 3
                for attempts_nav in range(max_attempts_nav):
                    try:
                        ventas2 = obtener_datos(link)
                        print('OK')
                        break
                    except NoSuchElementException as e:
                        print(f"Intento {attempts_nav + 1} fallido. Razón: {str(e)}")
                        if attempts_nav < max_attempts_nav - 1:
                            print("Reintentando en 2 segundos...")
                            time.sleep(2)
                        else:
                            lista_errores.append({"Ventas Web": id_producto})
                            ventas2 = 0
                            print("Número máximo de intentos alcanzado. La solicitud no se pudo completar.")
                    break
            else:
                print(f"Intento {attempt + 1} fallido. Razón: {str(e)} obteniendo ventas")
                if attempt < max_attempts - 1:
                    print("Reintentando en 2 segundos...")
                    time.sleep(2)
                else:
                    lista_errores.append({"Ventas API": id_producto})
                    ventas2 = 0
                    print("Número máximo de intentos alcanzado obteniendo ventas. La solicitud no se pudo completar.")
    
# import pandas as pd
# import requests
# import time
# from datetime import datetime
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.chrome.options import Options


# ruta_productos = 'Productos MLM455214 - 2024-01-12_06-05-45.csv'
# df = pd.read_csv(ruta_productos)

# for id_producto in df['ID'][:20]:
#     print(id_producto)

#     url = f"https://api.mercadolibre.com/items/{id_producto}"

#     payload = {}
#     headers = {
#     'Authorization': 'Bearer APP_USR-7740131767656174-011515-6f612c03ec9c4dc13b8815d24a1bd892-17228348'
#     }
#     max_attempts = 5
#     for attempt in range(max_attempts):
#         try:
#             response1 = requests.request("GET", url, headers=headers, data=payload, timeout=50)
#             response1.raise_for_status()  # Lanzará una excepción si la solicitud no fue exitosa (código de estado diferente de 2xx)
#             data = response1.json()
#             break
#         except requests.exceptions.RequestException as e:
#             print(f"Intento {attempt + 1} fallido. Razón: {str(e)} obteniendo items")
#         if attempt < max_attempts - 1:
#             print("Reintentando en 5 segundos...")
#             time.sleep(5)  # Espera 5 segundos antes de intentar nuevamente
#         else:
#             print("Número máximo de intentos obteniendo Items. La solicitud no se pudo completar.")

#     link = data['permalink']

#     # Configura las opciones de Chrome
#     chrome_options = Options()
#     prefs = {"profile.managed_default_content_settings.images": 2}  # Esto deshabilita las imágenes
#     chrome_options.add_experimental_option("prefs", prefs)

#     # Inicia el navegador con las opciones configuradas
#     driver = webdriver.Chrome(options=chrome_options)

#     driver.get(link)

#     # Realiza las operaciones que necesitas en la página
#     elemento = driver.find_element(By.CLASS_NAME, 'ui-pdp-subtitle')
#     ventas2 = elemento.text
#     print(ventas2)

#     # No olvides cerrar el navegador al final
#     driver.quit()

# atributos = None  

# lista_atributos = []
# try:
#     if atributos is not None:
#         for i in range(len(atributos)):
#             atributo = atributos[i]
#             name = atributo.get('name', None)
#             value_name = atributo.get('value_name', None)
#             lista_atributos.append({"": [name, value_name]})
# except (TypeError, IndexError):
#     lista_atributos = None
