from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException 
import pandas as pd
from datetime import datetime

# Cargar el DataFrame previamente creado
datos = pd.read_csv('errorif_200a600_2023-09-25_12-31-18.csv')

# Obtener la fecha y hora actual
now = datetime.now()

# Formatear la fecha y hora como una cadena en el formato que desees
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

# Crear el nombre del archivo reseña
info = f"info_prueb_{timestamp}.csv"

# Crear el nombre del archivo error
errorif = f"errorif_prueb_{timestamp}.csv"

# Inicializar el navegador
driver = webdriver.Chrome()  # Asegúrate de tener el driver de Chrome instalado

# Lista para almacenar la info de todos los productos
info_list = []
error_inf = []

# Iniciar el proceso para cada enlace en la columna "Enlace" del DataFrame
for enlace in datos['Enlace']:

    max_attempts = 3
    attempts = 0
    success = False

    while attempts < max_attempts and not success:
        try:
        
            driver.get(enlace)
            time.sleep(2)

            driver.get(enlace)
            time.sleep(2)

            # Sacar el Titulo
            xpaths_id = ['//*[@id="header"]/div/div[2]/h1',
                         '//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/h1', 
                        '//*[@id="ui-pdp-main-container"]/div[1]/div[1]/div[2]/div[1]/div/div[1]/h1', 
                        '//*[@id="header"]/div/div[2]/h1',
                ]
            for i, xpath_template in enumerate(xpaths_id, start=1):
                try:
                    xpath_titulo = xpath_template.format(i)
                    elemento_titulo = driver.find_element(By.XPATH, xpath_titulo)
                    print("titulo", i)
                    break
                except NoSuchElementException:
                    print("No encontre el titulo", i)
                    continue

            titulo = elemento_titulo.text

            #ID
            words = titulo.split()
            id = ''.join([word[0] for word in words])
            print("El id es: " + id)

            # Ventas

            xpaths_ventas = ['//*[@id="header"]/div/div[1]/span', '/html/body/main/div[2]/div[5]/div/div[1]/div/div[1]/div/div[1]/div[1]/span', 
                '//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/span',
                '/html/body/div[5]', '//*[@id="header"]/div/div[1]/span'
                ]

            for i, xpaths_venta in enumerate(xpaths_ventas, start=1):
                try:
                    elemento_vendidos_estatus = driver.find_element(By.XPATH, xpaths_venta)
                    break
                except NoSuchElementException:
                    continue

            # Extrae el texto completo
            vendido_estatus_completo = elemento_vendidos_estatus.text
            indice_mas = vendido_estatus_completo.index('+')
            # Extrae el número de la cadena a partir del índice del '+'
            numero_vendidos = vendido_estatus_completo[indice_mas + 1:].split()[0]

            #Precio

            xpaths_precios = ['//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[1]/span[1]/span[3]',
                            '//*[@id="price"]/div/div[1]/div[1]/span[1]/span[3]',
                            '/html/body/main/div[2]/div[5]/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div[1]/span/span[3]',
                            '//*[@id="price"]/div/div[1]/div[1]/div/div/span[1]/span[3]'
            ]

            xpaths_centavos = ['//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[1]/span[1]/span[5]', 
            '//*[@id="price"]/div/div[1]/div[1]/span[1]/span[5]',
            '//*[@id="header"]/div/div[1]/span',
            '/html/body/div[5]',
            '//*[@id="price"]/div/div[1]/div[1]/div/div/span[1]/span[5]'
            ]

            #Precio        
            elemento_centavos = None 
            precio = "0"  

            for i, xpaths_precio in enumerate(xpaths_precios, start=1):
                try:
                    elemento_precio = driver.find_element(By.XPATH, xpaths_precio)
                    break
                except NoSuchElementException:
                    continue

            for i, xpaths_centavo in enumerate(xpaths_centavos, start=1):
                try:
                    elemento_centavos = driver.find_element(By.XPATH, xpaths_centavo)
                    break
                except NoSuchElementException:
                    centavos = "0"  # Si no hay centavos, es 0
                    continue

            precio = elemento_precio.text

            if elemento_centavos:
                centavos = elemento_centavos.text
                precio_value = precio + "." + centavos
            else:
                precio_value = precio

            # Crear un diccionario para almacenar la info de este producto
            product_info = {
                "id": id,
                "Vendidos": numero_vendidos,
                "Precio": precio_value,
                "Número de resenas": 0,
            }
            success = True
            time.sleep(4)
        except:
            attempts += 1
            time.sleep(4)  # Pausa antes de reintentar

    if not success:
        error_inf.append({"Enlace": enlace})
        pass
            
# Crear un DataFrame a partir de la lista de datos
df = pd.DataFrame(info_list)

# Crear un DataFrame a partir de la lista de errores
error = pd.DataFrame(error_inf)

# Guardar los datos en un archivo CSV
df.to_csv(info, index=False)

# Guardar los datos de erroresen un archivo CSV
error.to_csv(errorif, index=False)

# Cerrar el controlador de Selenium
driver.quit()
            
            
