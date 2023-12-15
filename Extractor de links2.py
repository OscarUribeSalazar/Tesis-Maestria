import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime


# Inicializar el navegador
driver = webdriver.Chrome()

# Obtener la fecha y hora actual para guardar el dataframe con la fecha que se extrajo
now = datetime.now()

# Formato de le fecha y hora
timestamp = now.strftime("%Y-%m-%d_%H-%M")

# Nombre con el que se guardará el dataframe
nombre_df = f"Enlaces{timestamp}.csv"

'''
Actualmente mercado Libre no permite realizar búsquedas mediante el webdriver, es por eso que
link de la búsqueda se debe agregar manualmente. Este link basta con copiarlo y te mostrará 54 productos
'''
# URL de búsqueda
url = "https://listado.mercadolibre.com.mx/adornos-y-decoraci%C3%B3n-del-hogar#D[A:Adornos%20y%20Decoraci%C3%B3n%20del%20Hogar]"

# Abrir el link de búsqueda
driver.get(url)

# Tiempo de espera para que la pagina pueda cargar todos elementos, a veces es necesario agregar más tiempo.
time.sleep(1)

# Lista para almacenar los links
links = []

'''
Este while se utiliza para validar si aun se encuentra el botón de "Siguiente" Si existe continua
dando click para ir a la siguiente pagina, ¿Cuántas paginas son?
'''
while True:

    '''
    Obtiene el tamaño de la ventana en un diccionario con dos datos width y height
    '''
    # Realiza Scroll hacia abajo para cargar todos los elementos
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    # Espera a que carguen todos los elementos
    time.sleep(1)

    # Encuentra todos los elementos que tengan la clase ui-search-layout__item
    '''
    Elementos de búsqueda
    Busca únicamente los elementos de la búsqueda, ya que en la página por lo natural hay mas enlaces 
    que no pertenecen necesariamente a la búsqueda, sino a recomendaciones
    de mercado libre.
    '''
    elemento_busqueda = driver.find_elements(By.CLASS_NAME, 'ui-search-layout__item')
     
    #Bucle para extraer los datos en cada enlace
    for i in elemento_busqueda:
        
        '''
        Titulo
        '''  
        #Para cada elemento i en enlaces encuentra el titulo que contenga la clase ui-search-item__group__element.ui-search-link__title-card.ui-search-link
        titulo_element = i.find_element(By.CLASS_NAME, 'ui-search-item__title')
        # Extrae el título de la variable y lo convierte a texto
        titulo = titulo_element.text

        '''
        ID
        '''
        #Divide el titulo por palabras en una lista
        words = titulo.split()
        # Toma la primera letra de cada palabra y la une para formar el ID
        # [word[0] for word in words] -  Crea una lista con el primer carácter de cada palabra
        # ''.join - concatena (Une) el carácter y el '' evita que no tenga ningún espacio entre cada uno.
        id = ''.join([word[0] for word in words])

        '''
        Enlace
        '''
        # Extrae el link de la variable en un enlace tipo href
        enlace_element = i.find_element(By.TAG_NAME, 'a')
        enlace = enlace_element.get_attribute('href')

        '''
        Agregar los elementos a la lista Links
        '''
        links.append({
            'ID': id,
            'Titulo': titulo,
            'Enlace': enlace
        })
    '''
    Botón siguiente:
    Ya que termina de extraer los datos de la búsqueda revisa si existe el botón "Siguiente" si está
    le da click, si no termina el programa
    '''
    
    
    # Intenta encontrar el botón siguiente y si existe le da click
    # Variable de control
    primera_vez = True

    try:
        div_boton_siguiente = driver.find_element(By.CLASS_NAME, "ui-search-pagination")
        list_boton_siguiente = div_boton_siguiente.find_elements(By.TAG_NAME, 'a')
        if "Siguiente" in list_boton_siguiente[-1].text:
            list_boton_siguiente[-1].click()
        else:
            break
    except Exception as e:
        print("No se puede navegar:", e)
        break


'''
Guardar los datos
'''
# Crear un DataFrame a partir de la lista de datos
df = pd.DataFrame(links)

# Guarda el DataFrame como un archivo CSV
df.to_csv(f'Links/{nombre_df}', index=False)

# Cerrar el controlador de Selenium 
driver.quit()

