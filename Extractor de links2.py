import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


# Inicializar el navegador
driver = webdriver.Chrome()

'''
Actualmente mercado Libre no permite realizar búsquedas mediante el webdriver, es por eso que
link de la búsqueda se debe agregar manualmente. Este link basta con copiarlo y te mostrará 50 productos
'''
# Revisar la cantidad de productos que muestra por link de búsqueda
# URL de búsqueda
url = "https://listado.mercadolibre.com.mx/adornos-y-decoraci%C3%B3n-del-hogar#D[A:Adornos%20y%20Decoraci%C3%B3n%20del%20Hogar]"

# Abrir el link de búsqueda
driver.get(url)

# Tiempo de espera para que la pagina pueda cargar todos elementos, a veces es necesario agregar más tiempo.
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
        xpath_titulos = [f'/html/body/main/div/div[2]/section/ol/li[{i}]/div/div/div[2]/div[1]/a/h2', f'/html/body/main/div/div[2]/section/ol/li[{i}]/div/div/div[2]/div[2]/a/h2']
        for i, xpath_template in enumerate(xpath_titulos, start=1):
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


        #Link:
        xpaths_links = [f'/html/body/main/div/div[2]/section/ol/li[{i}]/div/div/div[2]/div[1]/a', f'/html/body/main/div/div[2]/section/ol/li[{i}]/div/div/div[2]/div[2]/a']
        for i, xpath_template in enumerate(xpaths_links, start=1):
            try:
                xpath_link = xpath_template.format(i)
                elemento_link = driver.find_element(By.XPATH, xpath_link)
                enlace_href = elemento_link.get_attribute('href')
                print("link", i)
                break
            except NoSuchElementException:
                print("No encontre el link", i)
                continue


        # Agregar los datos a la lista
        links.append({
            'ID': id,
            'Titulo': titulo,
            'Enlace': enlace_href
        })
    try:
        xpath_siguientes = ['/html/body/main/div/div[2]/section/div[9]/nav/li[3]/a', '/html/body/main/div/div[2]/section/div[9]/nav/li[4]/a']
        for i, xpath_template in enumerate(xpath_siguientes, start=1):
            try:
                boton_siguiente = driver.find_element(By.XPATH, xpath_template)
                boton_siguiente.click()
                break
            except NoSuchElementException:
                print("No encontre el boton siguiente", i)
                continue
    except:
        print("No se encontró el botón 'Siguiente' o ha finalizado la paginación.")
        break

# Crear un DataFrame a partir de la lista de datos
df = pd.DataFrame(links)

# Guardar el DataFrame como un archivo CSV
df.to_csv('datos2.csv', index=False)  # Cambia el nombre del archivo si lo deseas

# Cerrar el controlador de Selenium
driver.quit()