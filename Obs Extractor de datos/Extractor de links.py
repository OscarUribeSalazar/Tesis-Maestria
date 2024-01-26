import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


# Inicializar el navegador
driver = webdriver.Chrome()

# Abrir la página web de busqeuda
url = "https://listado.mercadolibre.com.mx/adornos-y-decoraci%C3%B3n-del-hogar#D[A:Adornos%20y%20Decoraci%C3%B3n%20del%20Hogar]"
driver.get(url)
time.sleep(1)

# Lista para almacenar los links
links = []  

while True:
     
    # Obtener el tamaño de la ventana del navegador
    window_size = driver.get_window_size()
    window_height = window_size["height"]

    while True:
        # Scroll hacia abajo
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)  # Esperar a que se carguen más elementos
        
        # Obtener posición actual del scroll
        current_scroll = driver.execute_script("return window.scrollY")
        
        # Si no hay más desplazamiento posible, salir del bucle
        if current_scroll + window_height >= driver.execute_script("return document.body.scrollHeight"):
            break

    # Busqueda de enlaces en el listado ol
    enlaces = driver.find_elements(By.XPATH, '//*[@id="root-app"]/div/div[2]/section/ol/li')

    #Buble para encontrar todos los li
    for i, element_article in enumerate(enlaces, start=1):

        #Titulo
        try:
            xpath_titulo = f'/html/body/main/div/div[2]/section/ol/li[{i}]/div/div/div[2]/div[1]/a/h2'
            titulo = driver.find_element(By.XPATH, xpath_titulo)
        except NoSuchElementException:
            xpath_titulo = f'/html/body/main/div/div[2]/section/ol/li[{i}]/div/div/div[2]/div[2]/a/h2'
            titulo = driver.find_element(By.XPATH, xpath_titulo)

        #Link:
        try: 
            xpath_link = f'/html/body/main/div/div[2]/section/ol/li[{i}]/div/div/div[2]/div[1]/a'
            element_enlace = driver.find_element(By.XPATH, xpath_link)
            enlace_href = element_enlace.get_attribute('href')
        except NoSuchElementException:
            xpath_link = f'/html/body/main/div/div[2]/section/ol/li[{i}]/div/div/div[2]/div[2]/a'
            element_enlace = driver.find_element(By.XPATH, xpath_link)
            enlace_href = element_enlace.get_attribute('href')

        #Id
        titulo_text =titulo.text
        titulo_split = titulo_text.split()
        id = ''.join([word[0] for word in titulo_split])

        # Agregar los datos a la lista
        links.append({
            'ID': id,
            'Titulo': titulo.text,
            'Enlace': enlace_href
        })
    try:
        # Esperar hasta que el botón "Siguiente" esté presente y hacer clic en él
        try:
            boton_siguiente = driver.find_element(By.XPATH, '/html/body/main/div/div[2]/section/div[9]/nav/li[3]/a')
            boton_siguiente.click()
        except:
            boton_siguiente = driver.find_element(By.XPATH, '/html/body/main/div/div[2]/section/div[9]/nav/li[4]/a')
            boton_siguiente.click()
    except:
        print("No se encontró el botón 'Siguiente' o ha finalizado la paginación.")
        break

# Crear un DataFrame a partir de la lista de datos
df = pd.DataFrame(links)

# Guardar el DataFrame como un archivo CSV
df.to_csv('datos.csv', index=False)  # Cambia el nombre del archivo si lo deseas

# Cerrar el controlador de Selenium
driver.quit()