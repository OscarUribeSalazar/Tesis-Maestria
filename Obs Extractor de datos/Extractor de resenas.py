from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime


# Cargar el DataFrame de links
links = pd.read_csv('datos.csv')

# Inicializar el navegador
driver = webdriver.Chrome()

# Obtener la fecha y hora actual
now = datetime.now()

# Formatear la fecha y hora como una cadena en el formato que desees
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

# Crear el nombre del archivo reseña
nombre_resena = f"resena_35_{timestamp}.csv"

# Crear el nombre del archivo error
nombre_error = f"error_35_{timestamp}.csv"

# Crear una lista para almacenar la información
info = []
error = []

# Iniciar el proceso de bucle para eencontrar y sacar las reseñas
for enlace in links['Enlace'][35:36]:

    max_attempts = 3
    attempts = 0
    success = False

    while attempts < max_attempts and not success:
        try:

            driver.get(enlace)
            time.sleep(1)
            print("Entre 1vez a la pagina")

            #2da carga para que se completen los datos ciempre
            driver.get(enlace)
            time.sleep(1)
            print("Entre 2vez a la pagina")

            # Sacar el ID
            try:
                xpath_titulo = f'//*[@id="header"]/div/div[2]/h1'
                elemento_titulo = driver.find_element(By.XPATH, xpath_titulo)
            except NoSuchElementException:
                xpath_titulo = f'//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/h1'
                elemento_titulo = driver.find_element(By.XPATH, xpath_titulo)
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
            try:
                show_more_button = driver.find_element(By.XPATH, '//*[@id="reviews_capability_v3"]/div/section/div/div[2]/div[3]/button').click()
                print("Encontre el botón de show more por dirección")
            except NoSuchElementException:
                show_more_button = driver.find_element(By.CLASS_NAME, "show-more-click").click()
                print("Encontre el botón de show more por class name")

            #Cambiar el iframe de reseñas
            driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="ui-pdp-iframe-reviews"]'))
            print("Me cambie de iframe de show more")

            for num_elemento in range(2, 7):  # Iterar del 2 al 6)
            
                #Encontrar el boton de ordenar
                try:
                    xpath_ordenar = '//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[1]/div[2]/div/button'
                    boton_ordenar = driver.find_element(By.XPATH, xpath_ordenar)
                    print("Encontre el botón de ordenar por dirección 1")
                except NoSuchElementException:
                    try:
                        xpath_ordenar = '//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[1]/div[2]/div/button'
                        boton_ordenar = driver.find_element(By.XPATH, xpath_ordenar)
                        print("Encontre el botón de ordenar por dirección 2")
                    except NoSuchElementException:
                        xpath_ordenar = '//*[@id="reviews-capability.desktop"]/section/div/div[2]/div/div[1]/div[2]/div/button'
                        boton_ordenar = driver.find_element(By.XPATH, xpath_ordenar)
                        print("Encontre el botón de ordenar por dirección 3")
                
                boton_ordenar.click()
                print("hice clic en botón ordenar: " + str(num_elemento))

                #Tiempo para que carguen los elementos
                time.sleep(1) 
                
                # Encontrar en la lista el número de elemento entre 5 a 1 estreñas
                try:
                    xpath_estrenas = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div/div[1]/div[2]/div[2]/ul/li[{num_elemento}]'
                    print("Encontre la lista del elemento por dirección 3: " + str(num_elemento))
                    print(num_elemento)
                except NoSuchElementException:
                    try:
                        xpath_estrenas = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[1]/div[2]/div[2]/ul/li[{num_elemento}]'
                        print("Encontre la lista del elemento por dirección 1: " + str(num_elemento))
                    except NoSuchElementException:
                        xpath_estrenas = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[1]/div[2]/div[2]/ul/li[{num_elemento}]'
                        print("Encontre la lista del elemento por dirección 2: " + str(num_elemento))
                
                boton_estrenas = driver.find_element(By.XPATH, xpath_estrenas)
                boton_estrenas.click()
                print("hice clic en la lista del número elemento")
                
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
                try:
                    article = driver.find_elements(By.XPATH, '//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[2]/div/div/div/article')
                    print("encontre articles 1")
                except NoSuchElementException:
                    try:
                        article = driver.find_elements(By.XPATH, '//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[2]/div/div/div/article')
                        print("encontre articles 2")
                    except NoSuchElementException:
                        article = driver.find_elements(By.XPATH, '//*[@id="reviews-capability.desktop"]/section/div/div[2]/div/div[2]/div/div/div/article')
                        print("encontre articles 3")
                

                #Enumerar todos los articles empezando de 1
                print("Empezando a sacar datos")
                for i, element_article in enumerate(article, start=1):
                    
                    #Rutas            
                    #Calificación
                    try:
                        xpath_calificacion = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[2]/div/div/div/article[{i}]/div[1]/div/div/p'
                        element_calificacion = driver.find_element(By.XPATH, xpath_calificacion)
                        print("Encontre calificación por direccion 1")
                    except NoSuchElementException:
                        try:
                            xpath_calificacion = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[2]/div/div/div/article[{i}]/div[1]/div/div/p'
                            element_calificacion = driver.find_element(By.XPATH, xpath_calificacion)
                            print("Encontre calificación por direccion 2")
                        except NoSuchElementException:
                            try:
                                xpath_calificacion = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div/div[2]/div/div/div/article[{i}]/div[1]/div/div/p'
                                element_calificacion = driver.find_element(By.XPATH, xpath_calificacion)
                                print("Encontre calificación por direccion 3")
                            except NoSuchElementException:
                                xpath_calificacion = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div/div[2]/div/div/div/article[{i}]/div[1]/div/div/p'
                                element_calificacion = driver.find_element(By.XPATH, xpath_calificacion)
                                print("Encontre calificación por direccion 4")

                    #Fecha
                    try:
                        xpath_fecha = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[2]/div/div/div/article[{i}]/div[1]/div/span'
                        element_fecha = driver.find_element(By.XPATH, xpath_fecha)
                        print("Encontre fecha por direccion 1")
                    except NoSuchElementException:
                        try:
                            xpath_fecha = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[2]/div/div/div/article[{i}]/div[1]/div/span'
                            element_fecha = driver.find_element(By.XPATH, xpath_fecha)
                            print("Encontre fecha por direccion 2")
                        except NoSuchElementException:
                            xpath_fecha = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div/div[2]/div/div/div/article[{i}]/div[1]/div/span'
                            element_fecha = driver.find_element(By.XPATH, xpath_fecha)
                            print("Encontre fecha por direccion 3")

                    #Resena
                    try:
                        xpath_resena = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[2]/div/div/div/article[{i}]/p'
                        print("Encontre reseña por direccion 1")
                    except NoSuchElementException:
                        try:
                            xpath_resena = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[2]/div/div/div/article[{i}]/p'
                            print("Encontre reseña por direccion 2")
                        except NoSuchElementException:
                            xpath_resena = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div/div[2]/div/div/div/article[{i}]/p'
                            print("Encontre reseña por direccion 3")                            

                    #Sacando elementos
                    element_resena = driver.find_element(By.XPATH, xpath_resena)
                    print("Saque los elementos de calificacion, fecha, resena")

                    #Convirtiendo a texto
                    calificacion_text = element_calificacion.text
                    fecha_text = element_fecha.text
                    resena = element_resena.text
                    print("Convirtiendo a texto los elementos de calificacion, fecha, resena")
                    print("Fecha: " + fecha_text)
                    print("Reseña: " + resena)
                
                    #Obtener el segundo elemento del texto
                    calificacion_numero = calificacion_text.split()[1]
                    print("Calificación: " + str(calificacion_numero))

                    #Comprobar si existe imagenes y= = 3 si no y = 2
                    try:
                        try:
                            xpath_imagenes = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[2]/div/div/div/article[{i}]/div[2]/section/div[2]'
                            print("Encontre imagenes por dirección 1")
                        except NoSuchElementException:
                            try:
                                xpath_imagenes = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[2]/div/div/div/article[{i}]/div[2]/section/div[2]'
                                print("Encontre imagenes por dirección 2")
                            except NoSuchElementException:
                                xpath_imagenes = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div/div[2]/div/div/div/article[{i}]/div[2]/section/div[2]'
                                print("Encontre imagenes por dirección 3")                                
                        
                        contenedor_imagenes = driver.find_element(By.XPATH, xpath_imagenes)
                        imagenes = contenedor_imagenes.find_elements(By.TAG_NAME, 'img')
                        cantidad_imagenes = len(imagenes)
                        print("Cantidad de imagenes: " + str(cantidad_imagenes))
                        y = 3

                    except NoSuchElementException:
                        cantidad_imagenes = 0
                        print("Cantidad de imagenes: " + str(cantidad_imagenes))
                        y = 2

                    #Utilidad
                    
                    try:
                        xpath_utilidad = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[2]/div/div/div/article[{i}]/div[{y}]/div[1]/button[1]/span/p'
                        print("Encontre utilidad por direccion 1")
                    except NoSuchElementException:
                        try:
                            xpath_utilidad = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[2]/div/div/div/article[{i}]/div[{y}]/div[1]/button[1]/span/p'
                            print("Encontre utilidad por direccion 2")
                        except NoSuchElementException:
                            xpath_utilidad = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div/div[2]/div/div/div/article[{i}]/div[{y}]/div[1]/button[1]/span/p'
                            print("Encontre utilidad por direccion 3")                            

                    element_utilidad = driver.find_element(By.XPATH, xpath_utilidad) 
                    utilidad =  element_utilidad.text
                    print("Utilidad: " + utilidad)

                    #Agregar los datos al Dataframe
                    info.append({
                        "id": id,
                        "Calificación": calificacion_numero,
                        "Fecha": fecha_text,
                        "Reseña": resena,  
                        "Cantidad de imagenes": cantidad_imagenes,
                        "Utilidad": utilidad,
                    })
                
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
            success = True
        except:
            attempts += 1
            time.sleep(2)  # Pausa antes de reintentar
            
    if not success:
        error.append({"Enlace": enlace})
        pass
  
# Cerrar el controlador de Selenium
driver.quit()

# Crear un DataFrame a partir de la lista de reseñas
info = pd.DataFrame(info)

# Crear un DataFrame a partir de la lista de errores
error = pd.DataFrame(error)

# Guardar los datos en un archivo CSV
info.to_csv(nombre_resena, index=False)

# Guardar los datos de erroresen un archivo CSV
error.to_csv(nombre_error , index=False)
