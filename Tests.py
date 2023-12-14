# ## Reseñas

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime

# Inicializar el navegador
driver = webdriver.Chrome()

enlace = 'https://articulo.mercadolibre.com.mx/MLM-1641749069-cadena-de-luces-con-pilas-20-leds-para-diy-decoracione12pcs-_JM#position=36&search_layout=stack&type=item&tracking_id=6c69b787-6e43-4ecd-9344-415560e28fac'

driver.get(enlace)
time.sleep(1)
print("Entre 1vez a la pagina")

#2da carga para que se completen los datos ciempre
driver.get(enlace)
time.sleep(1)
print("Entre 2vez a la pagina")

#Sacar el ID
xpaths_id = ['//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/h1', 
             '//*[@id="header"]/div/div[2]/h1',
             '//*[@id="ui-pdp-main-container"]/div[1]/div[1]/div[2]/div[1]/div/div[1]/h1'
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
print(elemento_titulo)

titulo = elemento_titulo.text
words = titulo.split()
id = ''.join([word[0] for word in words])
print("El id es: " + id)

# Obtener el tamaño de la ventana del navegador
window_size = driver.get_window_size()
window_height = window_size["height"]
print("Obtuve el tamaño de ventana")

while True:
    # Scroll hacia abajo
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1) 
    
    # Obtener posición actual del scroll
    current_scroll = driver.execute_script("return window.scrollY")
    # Si no hay más desplazamiento posible, salir del bucle
    if current_scroll + window_height >= driver.execute_script("return document.body.scrollHeight"):
        break

print("Hice Scrolll hasta abajo")   

#Encontrar el boton de "show more" y dar click        
search_criteria = [
    (By.XPATH, '//*[@id="reviews_capability_v3"]/div/section/div/div[2]/div[3]/button'),
    (By.CLASS_NAME, "show-more-click")
]

show_more_button = None  # Inicializa la variable show_more_button

for criteria in search_criteria:
    try:
        show_more_button = driver.find_element(*criteria)
        break  # Sal del bucle si se encuentra una coincidencia exitosa
    except NoSuchElementException:
        continue  # Si no se encuentra, continúa con el siguiente criterio de búsqueda

if show_more_button is not None:
    show_more_button.click()
else:
    print("No se pudo encontrar el botón de show more")

#Cambiar el iframe de reseñas
driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="ui-pdp-iframe-reviews"]'))
print("Me cambie de iframe de show more")

for num_elemento in range(2, 7):  # Iterar del 2 al 6)

    xpath_ordenar = [
        '//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[1]/div[2]/div/button',
        '//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[1]/div[2]/div/button',
        '//*[@id="reviews-capability.desktop"]/section/div/div[2]/div/div[1]/div[2]/div/button'
    ]

    boton_ordenar = None

    for xpath_ordena in xpath_ordenar:
        try:
            boton_ordenar = driver.find_element(By.XPATH, xpath_ordena)
            break
        except NoSuchElementException:
            continue

    if boton_ordenar is not None:
        boton_ordenar.click()
        print("hice clic en botón ordenar")
        #Tiempo para que carguen los elementos
        time.sleep(1)
    
    #Encontrar en la lista el número de elemento entre 5 a 1 estreñas
    xpath_estrenas = [
        f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div/div[1]/div[2]/div[2]/ul/li[{num_elemento}]',
        f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[1]/div[2]/div[2]/ul/li[{num_elemento}]',
        f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[1]/div[2]/div[2]/ul/li[{num_elemento}]'
    ]
    print("1")
    boton_estrenas = None

    for xpath_estrena in xpath_estrenas:
        try:
            boton_estrenas = driver.find_element(By.XPATH, xpath_estrena)
            print("2")
            break
        except NoSuchElementException:
            print("3")
            continue

    if boton_estrenas is not None:
        boton_estrenas.click()
        print("hice clic en botón estreñas")
        #Tiempo para que carguen los elementos
        time.sleep(1) 

    #Realiza el scroll hacia abajo para que vuela a iterar
    while True:
        previous_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        print("Haciendo scroll...")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == previous_height:
            break
    
    #Tiempo para que carguen los elementos
    time.sleep(1)
    #Termine scroll de reseñas            
    print("Realice scroll hacia abajo para encontrar todas las reseñas")

    # Encontrar los articles

    xpath_articles = [
        '//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[2]/div/div/div/article',
        '//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[2]/div/div/div/article',
        '//*[@id="reviews-capability.desktop"]/section/div/div[2]/div/div[2]/div/div/div/article'
    ]

    articles = []

    for xpath_article in xpath_articles:
        try:
            article = driver.find_element(By.XPATH, xpath_article)
            articles.append(article)
        except NoSuchElementException:
            continue

    if article:
        # Enumerate and process the articles
        print("Empezando a sacar datos")
        for i, element_article in enumerate(articles, start=1):
            
            #Calificación
            xpath_calificaciones = [
                f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[2]/div/div/div/article[{i}]/div[1]/div/div/p',
                f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[2]/div/div/div/article[{i}]/div[1]/div/div/p',
                f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div/div[2]/div/div/div/article[{i}]/div[1]/div/div/p'
            ]

            element_calificacion = None  

            for xpath_calificacion in xpath_calificaciones:
                try:
                    element_calificacion = driver.find_element(By.XPATH, xpath_calificacion)
                    break  
                except NoSuchElementException:
                    continue  

            if element_calificacion is not None:
                calificacion_text = element_calificacion.text
                calificacion_numero = calificacion_text.split()[1]
                print("Calificación: " + str(calificacion_numero))

            #Fecha

            xpath_fechas = [
                f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[2]/div/div/div/article[{i}]/div[1]/div/span',
                f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[2]/div/div/div/article[{i}]/div[1]/div/span',
                f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div/div[2]/div/div/div/article[{i}]/div[1]/div/span'
            ]       

            element_fecha = None  

            for xpath_fecha in xpath_fechas:
                try:
                    element_fecha = driver.find_element(By.XPATH, xpath_fecha)
                    break  
                except NoSuchElementException:
                    continue  

            if element_calificacion is not None:
                fecha_text = element_fecha.text
                print(fecha_text)   

            #Resena

            xpath_resenas = [
                f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[2]/div/div/div/article[{i}]/p',
                f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[2]/div/div/div/article[{i}]/p',
                f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div/div[2]/div/div/div/article[{i}]/p'
            ]      

            element_resena = None  

            for xpath_resena in xpath_resenas:
                try:
                    element_resena = driver.find_element(By.XPATH, xpath_resena)
                    break  
                except NoSuchElementException:
                    continue  

            if element_resena is not None:
                resena = element_resena.text
                print(resena)
                    

            #Comprobar si existe imagenes y= = 3 si no y = 2
            xpath_imagenes = [
                f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[2]/div/div/div/article[{i}]/div[2]/section/div[2]',
                f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[2]/div/div/div/article[{i}]/div[2]/section/div[2]',
                f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div/div[2]/div/div/div/article[{i}]/div[2]/section/div[2]'
            ]

            contenedor_imagenes = None

            for xpath_template in xpath_imagenes:
                try:
                    xpath_imagen = xpath_template.format(i)  # Reemplaza {} con el valor actual de 'i'
                    contenedor_imagenes = driver.find_element(By.XPATH, xpath_imagen)
                    break  # Si encontramos el contenedor de imágenes, salimos del bucle
                except NoSuchElementException:
                    continue  # Si no encontramos el contenedor, continuamos con la siguiente ruta XPath

            if contenedor_imagenes is not None:
                imagenes = contenedor_imagenes.find_elements(By.TAG_NAME, 'img')
                cantidad_imagenes = len(imagenes)
                print("Cantidad de imágenes: " + str(cantidad_imagenes))
                y = "3"
            else:
                cantidad_imagenes = 0
                print("Cantidad de imágenes: " + str(cantidad_imagenes))
                y = "2"

            #Utilidad

            xpath_utilidades = [
                f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[2]/div/div/div/article[{i}]/div[{y}]/div[1]/button[1]/span/p',
                f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[2]/div/div/div/article[{i}]/div[{y}]/div[1]/button[1]/span/p',
                f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div/div[2]/div/div/div/article[{i}]/div[{y}]/div[1]/button[1]/span/p'
            ]


            element_utilidad = None

            for xpath_utilidad in xpath_utilidades:
                try:
                    element_utilidad = driver.find_element(By.XPATH, xpath_utilidad)
                    utilidad = element_utilidad.text
                    print("Utilidad: " + str(utilidad))
                    break
                except NoSuchElementException:
                    continue
            if element_utilidad is None:
                print("No se encontró el elemento de utilidad.")

        pass
    else:
        print("no se encontraron articulos")

    while True:
        previous_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, 0)")
        print("Haciendo scroll hacia arriba...")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == previous_height:
            break
    #Regresando arriba            
    print("Realice scroll hacia arriba para encontrar el boton de ordenar y guarde los datos")            
    #Tiempo para que carguen los elementos
    time.sleep(1)

#Cerrar el controlador de Selenium
driver.quit()

# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # import time
# # from selenium.common.exceptions import NoSuchElementException 
# # import pandas as pd

# # Cargar el DataFrame previamente creado

# # enlace = 'https://www.mercadolibre.com.mx/series-luces-led-de-50-metros-decoracion-ambar-vintage-blanco-frio-bodas-navidad-xv-anos-hogar-fiestas-bautizos/p/MLM22022992?pdp_filters=category:MLM1631#reviews'

# # # Inicializar el navegador
# # driver = webdriver.Chrome()  # Asegúrate de tener el driver de Chrome instalado

# # driver.get(enlace)
# # time.sleep(2)

# # driver.get(enlace)
# # time.sleep(2)

# # # Titulo
# # try:
# #     xpath_titulo = f'//*[@id="header"]/div/div[2]/h1'
# #     elemento_titulo = driver.find_element(By.XPATH, xpath_titulo)
# # except NoSuchElementException:
# #     xpath_titulo = f'//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/h1'
# #     elemento_titulo = driver.find_element(By.XPATH, xpath_titulo)

# # #ID
# # titulo = elemento_titulo.text
# # words = titulo.split()
# # id = ''.join([word[0] for word in words])

# # # Ventas
# # try:
# #     xpath_vendidos_estatus = '/html/body/main/div[2]/div[5]/div/div[1]/div/div[1]/div/div[1]/div[1]/span'
# #     elemento_vendidos_estatus = driver.find_element(By.XPATH, xpath_vendidos_estatus)
# # except NoSuchElementException:
# #     try:
# #         xpath_vendidos_estatus = '//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/span'
# #         elemento_vendidos_estatus = driver.find_element(By.XPATH, xpath_vendidos_estatus)
# #     except NoSuchElementException:
# #         try:
# #             xpath_vendidos_estatus = '//*[@id="header"]/div/div[1]/span'
# #             elemento_vendidos_estatus = driver.find_element(By.XPATH, xpath_vendidos_estatus)
# #         except NoSuchElementException:
# #             xpath_vendidos_estatus = '/html/body/div[5]'
# #             elemento_vendidos_estatus = driver.find_element(By.XPATH, xpath_vendidos_estatus)

# # # Extrae el texto completo
# # vendido_estatus_completo = elemento_vendidos_estatus.text
# # indice_mas = vendido_estatus_completo.index('+')
# # # Extrae el número de la cadena a partir del índice del '+'
# # numero_vendidos = vendido_estatus_completo[indice_mas + 1:].split()[0]

# # #Precio
# # elemento_centavos = None  # Inicializar elemento_centavos fuera de los bloques try-except
# # precio = "0"  # Inicializar precio con un valor predeterminado

# # try:
# #     xpath_precio = f'//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[1]/span[1]/span[3]'
# #     xpath_centavos = f'//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[1]/span[1]/span[5]'
# #     elemento_precio = driver.find_element(By.XPATH, xpath_precio)
# #     elemento_centavos = driver.find_element(By.XPATH, xpath_centavos)
# #     precio = elemento_precio.text
# # except NoSuchElementException:
# #     try:
# #         xpath_precio = f'//*[@id="price"]/div/div[1]/div[1]/span[1]/span[3]'
# #         xpath_centavos = f'//*[@id="price"]/div/div[1]/div[1]/span[1]/span[5]'
# #         elemento_precio = driver.find_element(By.XPATH, xpath_precio)
# #         elemento_centavos = driver.find_element(By.XPATH, xpath_centavos)
# #         precio = elemento_precio.text
# #     except NoSuchElementException:
# #         try:
# #             xpath_precio = f'//*[@id="price"]/div/div[1]/div[1]/span[1]/span[3]'
# #             elemento_precio = driver.find_element(By.XPATH, xpath_precio)
# #             precio = elemento_precio.text
# #         except NoSuchElementException:
# #             xpath_precio = f'/html/body/main/div[2]/div[5]/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div[1]/span/span[3]'
# #             elemento_precio = driver.find_element(By.XPATH, xpath_precio)
# #             precio = elemento_precio.text
# #             centavos = "0"  # Si no hay centavos, es 0

# # if elemento_centavos:
# #     centavos = elemento_centavos.text
# #     precio_value = precio + "." + centavos
# # else:
# #     precio_value = precio

# # #Calificacion promedio
# # try:
# #     xpath_calificacion = f'//*[@id="reviews_capability_v3"]/div/section/div/div[1]/article/div/div[1]/div[1]/p'
# #     elemento_calificacion = driver.find_element(By.XPATH, xpath_calificacion)
# #     calificacion  = elemento_calificacion.text

# #     #Número de calificaciones
# #     xpath_num_calificacion = f'//*[@id="reviews_capability_v3"]/div/section/div/div[1]/article/div/div[1]/div[2]/div[2]/p'
# #     elemento_num_calificacion = driver.find_element(By.XPATH, xpath_num_calificacion)
# #     num_calificacion  = elemento_num_calificacion.text
# #     numero_calificaciones = num_calificacion.split()[0]
# # except NoSuchElementException:
# #     calificacion = "0"
# #     numero_calificaciones = "0"

# # # Crear un diccionario para almacenar la info de este producto

# # print(id,)
# # print(numero_vendidos)
# # print(precio_value)
# # print(calificacion)
# # print(numero_calificaciones)

# # # Características y calificaciones
# # caracteristicas_dict = {}
# # try:
# #     xpath_caracteristicas = '//*[@id="reviews_capability_v3"]/div/section/div/div[1]/div/table'
# #     print("Encontré Características")
# #     tabla = driver.find_element(By.XPATH, xpath_caracteristicas)
# #     filas = tabla.find_elements(By.TAG_NAME, "tr")  # Obtener todas las filas de la tabla

# #     for idx, fila in enumerate(filas):
# #         # Obtener los elementos td (columnas) de la fila actual
# #         columnas = fila.find_elements(By.TAG_NAME, "td")
# #         num_columnas = len(columnas)

# #         if num_columnas >= 2:  # Asegurarse de que haya al menos 2 columnas en la fila
# #             titulo = columnas[0].text

# #             for col_idx in range(1, num_columnas):
# #                 calificacion_texto = columnas[col_idx].find_element(By.CSS_SELECTOR, "div p").text

# #                 # Agregar los datos al diccionario de características y calificaciones
# #                 print(titulo)
# #                 print(calificacion_texto.split("de")[0].strip())
# # except NoSuchElementException:
# #     print("No hay características")

# # print("Termine")
# # # Cerrar el controlador de Selenium
# # driver.quit()
            
