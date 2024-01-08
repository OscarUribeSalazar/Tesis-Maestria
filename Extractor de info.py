from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException 
import pandas as pd

# Cargar el DataFrame previamente creado
datos = pd.read_csv('datos.csv')

# Inicializar el navegador
driver = webdriver.Chrome()  # Asegúrate de tener el driver de Chrome instalado

# Lista para almacenar la info de todos los productos
info_list = []
error_inf = []

# Iniciar el proceso para cada enlace en la columna "Enlace" del DataFrame
for enlace in datos['Enlace'][200:300]:

    max_attempts = 3
    attempts = 0
    success = False

    while attempts < max_attempts and not success:
        try:
    
            driver.get(enlace)
            time.sleep(2)

            driver.get(enlace)
            time.sleep(2)

            # Titulo
            try:
                xpath_titulo = f'//*[@id="header"]/div/div[2]/h1'
                elemento_titulo = driver.find_element(By.XPATH, xpath_titulo)
            except NoSuchElementException:
                xpath_titulo = f'//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/h1'
                elemento_titulo = driver.find_element(By.XPATH, xpath_titulo)
            
            #ID
            titulo = elemento_titulo.text
            words = titulo.split()
            id = ''.join([word[0] for word in words])

            # Ventas
            try:
                xpath_vendidos_estatus = '/html/body/main/div[2]/div[5]/div/div[1]/div/div[1]/div/div[1]/div[1]/span'
                elemento_vendidos_estatus = driver.find_element(By.XPATH, xpath_vendidos_estatus)
            except NoSuchElementException:
                try:
                    xpath_vendidos_estatus = '//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/span'
                    elemento_vendidos_estatus = driver.find_element(By.XPATH, xpath_vendidos_estatus)
                except NoSuchElementException:
                    try:
                        xpath_vendidos_estatus = '//*[@id="header"]/div/div[1]/span'
                        elemento_vendidos_estatus = driver.find_element(By.XPATH, xpath_vendidos_estatus)
                    except NoSuchElementException:
                        xpath_vendidos_estatus = '/html/body/div[5]'
                        elemento_vendidos_estatus = driver.find_element(By.XPATH, xpath_vendidos_estatus)

            # Extrae el texto completo
            vendido_estatus_completo = elemento_vendidos_estatus.text
            indice_mas = vendido_estatus_completo.index('+')
            # Extrae el número de la cadena a partir del índice del '+'
            numero_vendidos = vendido_estatus_completo[indice_mas + 1:].split()[0]

            #Precio
            elemento_centavos = None  # Inicializar elemento_centavos fuera de los bloques try-except
            precio = "0"  # Inicializar precio con un valor predeterminado

            try:
                xpath_precio = f'//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[1]/span[1]/span[3]'
                xpath_centavos = f'//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[1]/span[1]/span[5]'
                elemento_precio = driver.find_element(By.XPATH, xpath_precio)
                elemento_centavos = driver.find_element(By.XPATH, xpath_centavos)
                precio = elemento_precio.text
            except NoSuchElementException:
                try:
                    xpath_precio = f'//*[@id="price"]/div/div[1]/div[1]/span[1]/span[3]'
                    xpath_centavos = f'//*[@id="price"]/div/div[1]/div[1]/span[1]/span[5]'
                    elemento_precio = driver.find_element(By.XPATH, xpath_precio)
                    elemento_centavos = driver.find_element(By.XPATH, xpath_centavos)
                    precio = elemento_precio.text
                except NoSuchElementException:
                    try:
                        xpath_precio = f'//*[@id="price"]/div/div[1]/div[1]/span[1]/span[3]'
                        elemento_precio = driver.find_element(By.XPATH, xpath_precio)
                        precio = elemento_precio.text
                    except NoSuchElementException:
                        xpath_precio = f'/html/body/main/div[2]/div[5]/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div[1]/span/span[3]'
                        elemento_precio = driver.find_element(By.XPATH, xpath_precio)
                        precio = elemento_precio.text
                        centavos = "0"  # Si no hay centavos, es 0

            if elemento_centavos:
                centavos = elemento_centavos.text
                precio_value = precio + "." + centavos
            else:
                precio_value = precio

            #Calificacion promedio
            try:
                xpath_calificacion = f'//*[@id="reviews_capability_v3"]/div/section/div/div[1]/article/div/div[1]/div[1]/p'
                elemento_calificacion = driver.find_element(By.XPATH, xpath_calificacion)
                calificacion  = elemento_calificacion.text
            
                #Número de calificaciones
                xpath_num_calificacion = f'//*[@id="reviews_capability_v3"]/div/section/div/div[1]/article/div/div[1]/div[2]/div[2]/p'
                elemento_num_calificacion = driver.find_element(By.XPATH, xpath_num_calificacion)
                num_calificacion  = elemento_num_calificacion.text
                numero_calificaciones = num_calificacion.split()[0]
            except NoSuchElementException:
                calificacion = "0"
                numero_calificaciones = "0"
            
            # Crear un diccionario para almacenar la info de este producto
            product_info = {
                "id": id,
                "Vendidos": numero_vendidos,
                "Precio": precio_value,
                "Calificación promedio": calificacion,
                "Número de calificaciones": numero_calificaciones,
            }

            # Características y calificaciones
            caracteristicas_dict = {}
            try:
                xpath_caracteristicas = '//*[@id="reviews_capability_v3"]/div/section/div/div[1]/div/table'
                print("Encontré Características")
                tabla = driver.find_element(By.XPATH, xpath_caracteristicas)
                filas = tabla.find_elements(By.TAG_NAME, "tr")  # Obtener todas las filas de la tabla

                for idx, fila in enumerate(filas):
                    # Obtener los elementos td (columnas) de la fila actual
                    columnas = fila.find_elements(By.TAG_NAME, "td")
                    num_columnas = len(columnas)

                    if num_columnas >= 2:  # Asegurarse de que haya al menos 2 columnas en la fila
                        titulo = columnas[0].text

                        for col_idx in range(1, num_columnas):
                            calificacion_texto = columnas[col_idx].find_element(By.CSS_SELECTOR, "div p").text

                            # Agregar los datos al diccionario de características y calificaciones
                            caracteristicas_dict[f"Carac_{idx + 1}"] = titulo
                            caracteristicas_dict[f"CalfC_{idx + 1}"] = calificacion_texto.split("de")[0].strip()

                # Agregar cada característica y calificación como columnas separadas en product_info
                for key, value in caracteristicas_dict.items():
                    product_info[key] = value

            except NoSuchElementException:
                print("No hay características")

            # Agregar el diccionario de info del producto a la lista
            info_list.append(product_info)
            
            
            success = True
            time.sleep(2)
        except:
            attempts += 1
            time.sleep(2)  # Pausa antes de reintentar
    
    if not success:
        error_inf.append({"Enlace": enlace})
        pass

# Crear un DataFrame a partir de la lista de datos
df = pd.DataFrame(info_list)

# Crear un DataFrame a partir de la lista de errores
error = pd.DataFrame(error_inf)

# Guardar los datos en un archivo CSV
df.to_csv('info_2.csv', index=False)

# Guardar los datos de erroresen un archivo CSV
error.to_csv('error_inf_2.csv', index=False)

# Cerrar el controlador de Selenium
driver.quit()
            
