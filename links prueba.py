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

atributos = None  

lista_atributos = []
try:
    if atributos is not None:
        for i in range(len(atributos)):
            atributo = atributos[i]
            name = atributo.get('name', None)
            value_name = atributo.get('value_name', None)
            lista_atributos.append({"": [name, value_name]})
except (TypeError, IndexError):
    lista_atributos = None
