from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


# Cargar el DataFrame de links
links = pd.read_csv('datos.csv')

# Inicializar el navegador
driver = webdriver.Chrome() 

# Lista para almacenar los resenas
reseñas_data = []

# Iniciar el proceso de bucle para eencontrar y sacar las reseñas


for enlace in links['Enlace'][19:22]:

    max_attempts = 3

    for enlaces in enlace:
        attempts = 0
        success = False

        while attempts < max_attempts and not success:
            try:
                
                driver.get(enlace)
                time.sleep(1)

                #2da carga para que se completen los datos ciempre
                driver.get(enlace)
                time.sleep(1)
                print("Entre a las paginas")


                # Sacar el ID
                xpath_titulo = f'//*[@id="header"]/div/div[2]/h1'
                elemento_titulo = driver.find_element(By.XPATH, xpath_titulo)
                titulo = elemento_titulo.text
                words = titulo.split()
                id = ''.join([word[0] for word in words])
                print("Sauqe el ID Exitosamente")

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

                print("Hice Scrolll")        

                #Encontrar el boton de "show more" y dar click        
                try:
                    show_more_button = driver.find_element(By.XPATH, '//*[@id="reviews_capability_v3"]/div/section/div/div[2]/div[3]/button').click()
                except:
                    show_more_button = driver.find_element(By.CLASS_NAME, "show-more-click").click()

                print("Encontre el boton de show more")

                #Cambiar el iframe de reseñas
                driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="ui-pdp-iframe-reviews"]'))
                print("me cambie de iframe")

                for num_elemento in range(2, 7):  # Iterar del 2 al 6)
                    
                    #Encontrar el boton de ordenar
                    try:
                        xpath_ordenar = '//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[1]/div[2]/div/button'
                        boton_ordenar = driver.find_element(By.XPATH, xpath_ordenar)
                    except:
                        xpath_ordenar = '//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[1]/div[2]/div/button'
                        boton_ordenar = driver.find_element(By.XPATH, xpath_ordenar)
                        print("No encontre el boton y encontre la segunda opcion")
                    
                    boton_ordenar.click()

                    print("Encontre el boton de ordenar")

                    #Tiempo para que carguen los elementos
                    time.sleep(1) 

                    # Encontrar en la lista el número de elemento entre 5 a 1 estreñas
                    try:
                        xpath_estrenas = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[1]/div[2]/div[2]/ul/li[{num_elemento}]'
                        boton_estrenas = driver.find_element(By.XPATH, xpath_estrenas)
                        boton_estrenas.click()
                    except:    
                        xpath_estrenas = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[1]/div[2]/div[2]/ul/li[{num_elemento}]'
                        boton_estrenas = driver.find_element(By.XPATH, xpath_estrenas)
                        boton_estrenas.click()
                    print(num_elemento) 

                    print("Encotre los botones de número", num_elemento)
                    
                    #Tiempo para que carguen los elementos
                    time.sleep(1) 

                    #Realiza el scroll hacia abajo para que vuela a iterar
                    while True:
                        previous_height = driver.execute_script("return document.body.scrollHeight")
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                        time.sleep(1)
                        new_height = driver.execute_script("return document.body.scrollHeight")
                        if new_height == previous_height:
                            break

                    print("Realice scroll hacia abajo")

                    #Tiempo para que carguen los elementos
                    time.sleep(1)

                    # Encontrar los articles
                    article = driver.find_elements(By.XPATH, '//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[2]/div/div/div/article')
                    print("encontre articles")

                    #Enumerar todos los articles empezando de 1
                    for i, element_article in enumerate(article, start=1):
                        
                        #Rutas
                        
                        #Calificación
                        try:
                            xpath_calificacion = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[2]/div/div/div/article[{i}]/div[1]/div/div/p'
                            element_calificacion = driver.find_element(By.XPATH, xpath_calificacion)
                        except NoSuchElementException:
                            xpath_calificacion = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[2]/div/div/div/article[{i}]/div[1]/div/div/p'
                            element_calificacion = driver.find_element(By.XPATH, xpath_calificacion)

                        #Fecha
                        try:
                            xpath_fecha = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[2]/div/div/div/article[{i}]/div[1]/div/span'
                            element_fecha = driver.find_element(By.XPATH, xpath_fecha)
                        except NoSuchElementException:
                            xpath_fecha = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[2]/div/div/div/article[{i}]/div[1]/div/span'
                            element_fecha = driver.find_element(By.XPATH, xpath_fecha)

                        #Resena
                        try:
                            xpath_resena = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[2]/div/div/div/article[{i}]/p'
                        except NoSuchElementException:
                            xpath_resena = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[2]/div/div/div/article[{i}]/p'

                        #Sacando elementos
                        element_resena = driver.find_element(By.XPATH, xpath_resena)
                        print("saque los elementos de calificacion, fecha, resena")

                        #Convirtiendo a texto
                        calificacion_text = element_calificacion.text
                        fecha_text = element_fecha.text
                        resena = element_resena.text
                        print("saque los elementos de calificacion, fecha, resena")

                        #Obtener el segundo elemento del texto
                        calificacion_numero = calificacion_text.split()[1]

                        #Comprobar si existe imagenes y= = 3 si no y = 2
                        try:
                            try:
                                xpath_imagenes = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[2]/div/div/div/article[{i}]/div[2]/section/div[2]'
                                contenedor_imagenes = driver.find_element(By.XPATH, xpath_imagenes)
                            except NoSuchElementException:
                                xpath_imagenes = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[2]/div/div/div/article[{i}]/div[2]/section/div[2]'
                                contenedor_imagenes = driver.find_element(By.XPATH, xpath_imagenes)
                            
                            contenedor_imagenes = driver.find_element(By.XPATH, xpath_imagenes)
                            imagenes = contenedor_imagenes.find_elements(By.TAG_NAME, 'img')
                            cantidad_imagenes = len(imagenes)
                            y = 3

                        except NoSuchElementException:
                            cantidad_imagenes = 0
                            y = 2

                        #Utilidad
                        
                        try:
                            xpath_utilidad = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[2]/div[2]/div/div/div/article[{i}]/div[{y}]/div[1]/button[1]/span/p'
                            element_utilidad = driver.find_element(By.XPATH, xpath_utilidad)  
                        except NoSuchElementException:
                            xpath_utilidad = f'//*[@id="reviews-capability.desktop"]/section/div/div[2]/div[3]/div[2]/div/div/div/article[{i}]/div[{y}]/div[1]/button[1]/span/p'
                            element_utilidad = driver.find_element(By.XPATH, xpath_utilidad)  
            
                        utilidad =  element_utilidad.text

                        # #Regresar el scroll a arriba para volver a iterar      
                        # driver.execute_script("window.scrollTo(0, 0)")
                        # time.sleep(1)
                        
                        #Agregar los datos a la lista
                        reseñas_data.append({
                            "id": id,
                            "Calificación": str(calificacion_numero),
                            "Fecha": fecha_text,
                            "Reseña": resena,  
                            "Cantidad de imagenes": str(cantidad_imagenes),
                            "Utilidad": str(utilidad),
                        })
                        print("Guardando datos...")

                # Características y calificaciones
                try:
                    xpath_caracteristicas = '/html/body/main/div/section/div/div[1]/div/table'
                    tabla = driver.find_element(By.XPATH, xpath_caracteristicas)
                    filas = tabla.find_elements(By.TAG_NAME, "tr")  # Obtener todas las filas de la tabla

                    for idx, fila in enumerate(filas):
                        # Obtener los elementos td (columnas) de la fila actual
                        columnas = fila.find_elements(By.TAG_NAME, "td")
                        if len(columnas) >= 2:  # Asegurarse de que haya al menos 2 columnas en la fila
                            titulo = columnas[0].text
                            calificacion_texto = columnas[1].find_element(By.CSS_SELECTOR, "div p").text

                            # Obtener el segundo elemento del texto
                            calificacion_numero = calificacion_texto.split()[1]

                            # Crear un diccionario para las características y calificaciones
                            reseñas_data.append({
                                f"Titcarac_{idx + 1}": titulo,
                                f"Calfcarac_{idx + 1}": calificacion_numero,
                            })
                        print("hice caracteristicas")
                except:
                    pass
                    print("hice no hay caracteristicas")
                               
                #confirmación
                success = True  # Si llega aquí, la extracción fue exitosa
            except:
                attempts += 1
                time.sleep(2)  # Pausa antes de reintentar
                
                # Cerrar el controlador de Selenium
                driver.quit()

        if not success:
            pass
  

# Crear un DataFrame a partir de la lista de reseñas
df = pd.DataFrame(reseñas_data)
# Guardar los datos en un archivo CSV
df.to_csv('resena.csv', index=False)
# Cerrar el controlador de Selenium
driver.quit()


