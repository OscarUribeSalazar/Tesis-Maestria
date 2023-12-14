from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException 
import pandas as pd
from datetime import datetime

# Cargar el DataFrame previamente creado
datos = pd.read_csv('datos.csv')

# Obtener la fecha y hora actual
now = datetime.now()

# Formatear la fecha y hora como una cadena en el formato que desees
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

# Crear el nombre del archivo reseña
info = f"info_1800aend_2023{timestamp}.csv"

# Crear el nombre del archivo error
errorif = f"errorif_1800aend_2023{timestamp}.csv"

# Inicializar el navegador
driver = webdriver.Chrome()  # Asegúrate de tener el driver de Chrome instalado

# Lista para almacenar la info de todos los productos
info_list = []
error_inf = []

# Iniciar el proceso para cada enlace en la columna "Enlace" del DataFrame
for enlace in datos['Enlace'][1800:]:

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
            xpaths_id = ['//*[@id="header"]/div/div[2]/h1','//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/h1', 
                '//*[@id="ui-pdp-main-container"]/div[1]/div[1]/div[2]/div[1]/div/div[1]/h1', '//*[@id="header"]/div/div[2]/h1'
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
            print(numero_vendidos)

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
            
            print(precio_value)
 
            #Datos que aveces no hay
            try:
                #Calificacion promedio

                xpaths_calfs = ['//*[@id="reviews_capability_v3"]/div/section/div/div[1]/article/div/div[1]/div[1]/p']

                for i, xpaths_calf in enumerate(xpaths_calfs, start=1):
                    try:
                        elemento_cal_prom= driver.find_element(By.XPATH, xpaths_calf)
                        break
                    except NoSuchElementException:
                        continue

                calf_prom = elemento_cal_prom.text
                print(calf_prom)

                #Num reseñas

                xpaths_resenas = ['//*[@id="reviews_capability_v3"]/div/section/div/div[1]/article/div/div[1]/div[2]/div[2]/p']


                for i, xpaths_resena in enumerate(xpaths_resenas, start=1):
                    try:
                        elemento_num_calificacion = driver.find_element(By.XPATH, xpaths_resena)
                        break
                    except NoSuchElementException:
                        continue

                num_resena  = elemento_num_calificacion.text
                num_resenas = num_resena.split()[0]
                            
                # Crear un diccionario para almacenar la info de este producto
                product_info = {
                    "id": id,
                    "Vendidos": numero_vendidos,
                    "Precio": precio_value,
                    "Calificación promedio": calf_prom,
                    "Número de resenas": num_resenas,
                }

                for num_elemento_calfs in range(1, 6):  # Iterar del 1 al 5
                    xpaths_num_elemt_calfs = [f'//*[@id="reviews_capability_v3"]/div/section/div/div[1]/article/div/div[2]/ul/li[{num_elemento_calfs}]/div[1]/div/span[2]']

                    for xpaths_num_elemt_calf in xpaths_num_elemt_calfs:
                        try:
                            elemnt_li_calfs = driver.find_element(By.XPATH, xpaths_num_elemt_calf)
                            break
                        except NoSuchElementException:
                            continue
                    
                    texto_clafs = elemnt_li_calfs.get_attribute("style")
                    resultado = texto_clafs.split()[1]  
                    clave_columna = f"Calf_int_{num_elemento_calfs}"  
                    product_info[clave_columna] = resultado
                    
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
                                caracteristicas_dict[f"CalfC_{idx + 1}"] = calificacion_texto.split("de")[0][13:16].strip()

                    # Agregar cada característica y calificación como columnas separadas en product_info
                    for key, value in caracteristicas_dict.items():
                        product_info[key] = value

                except:
                    print("No hay características")

                # Agregar el diccionario de info del producto a la lista
                info_list.append(product_info)
            
                success = True
                time.sleep(4)
            except:
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
            
            
