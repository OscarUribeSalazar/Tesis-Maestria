import pandas as pd
import requests
import time
from datetime import datetime

# https://auth.mercadolibre.com.mx/authorization?response_type=code&client_id=7740131767656174&redirect_uri=https://reypi.com.br
app = 'APP_USR-7740131767656174-011214-4ae87833e6552ccdac8b2f4a1da1ecce-17228348'

ruta_productos = 'Productos MLM455214 - 2024-01-12_06-05-45.csv'
df = pd.read_csv(ruta_productos)

# Obtener la fecha y hora actual para guardar el dataframe con la fecha que se extrajo
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
# Crear el nombre del archivo información
nombre_archivo_inforeseñas_csv = f"Info_reseñas_{timestamp}.csv"
nombre_archivo_reseña_csv = f"Reseñas_{timestamp}.csv"

info_producto = []
info_reseña = []
lista_errores =  []

for id_producto in df['ID'][200:1200]:
    print(id_producto)

    limit = 100
    offset = 0

    url = f"https://api.mercadolibre.com/reviews/item/{id_producto}?limit={limit}&offset={offset}"

    payload = {}
    headers = {
    'Authorization': 'Bearer APP_USR-7740131767656174-011416-708f26e3ac92b05ce5cc2b89e073de26-17228348'
    }

    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            response = requests.request("GET", url, headers=headers, data=payload, timeout=10)
            response.raise_for_status()  # Lanzará una excepción si la solicitud no fue exitosa (código de estado diferente de 2xx)
            data = response.json()
            break
        except requests.exceptions.RequestException as e:
            print(f"Intento {attempt + 1} fallido. Razón: {str(e)} obteniendo items")
        if attempt < max_attempts - 1:
            print("Reintentando en 5 segundos...")
            time.sleep(5)  # Espera 5 segundos antes de intentar nuevamente
        else:
            lista_errores.append({"Items": id_producto})
            print("Número máximo de intentos alcanzado. La solicitud no se pudo completar.")

    num_reseñas = data['paging']['total']
    promedio_reseñas = data['rating_average']
    num_reseñas_calificacion = data['rating_levels']
    one = num_reseñas_calificacion['one_star']
    dos = num_reseñas_calificacion['two_star']
    tres = num_reseñas_calificacion['three_star']
    cuatro = cero = num_reseñas_calificacion['four_star']
    cinco = cero = num_reseñas_calificacion['five_star']

    #Agregar los datos al Dataframe
    producto_info = {
        "ID": id_producto,
        'Número_Reseñas': num_reseñas,
        'Promedio_Calificación': promedio_reseñas,
        'Num_Reseñas_1': one,
        'Num_Reseñas_2': dos,
        'Num_Reseñas_3': tres,
        'Num_Reseñas_4': cuatro,
        'Num_Reseñas_5': cinco,
    }

    atributos = data.get('quanti_attributes', [])
    atributos_dic = {}
    for i in range(len(atributos)):
        Qualidad = atributos[i] 
        nombre = Qualidad['name']
        rating = Qualidad['average_rating']
        atributos_dic[f"Atributo {i + 1}"] = nombre
        atributos_dic[f"Raiting_Promedio {i + 1}"] = rating

    # Agregar cada característica y calificación como columnas separadas en product_info
    for key, value in atributos_dic.items():
        producto_info[key] = value
    
    # Agregar el diccionario de info del producto a la lista
    info_producto.append(producto_info)

    for j in range(0, num_reseñas, 100):
        offset_2 = j
        url = f"https://api.mercadolibre.com/reviews/item/{id_producto}?limit={limit}&offset={offset_2}"
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                response = requests.request("GET", url, headers=headers, data=payload, timeout=10)
                response.raise_for_status()  # Lanzará una excepción si la solicitud no fue exitosa (código de estado diferente de 2xx)
                data = response.json()
                break
            except requests.exceptions.RequestException as e:
                print(f"Intento {attempt + 1} fallido. Razón: {str(e)} nuevo offset")
            if attempt < max_attempts - 1:
                print("Reintentando en 5 segundos...")
                time.sleep(5)  # Espera 5 segundos antes de intentar nuevamente
            else:
                lista_errores.append({"Offset": id_producto})
                print("Número máximo de intentos alcanzado. La solicitud no se pudo completar.")

        num_reseñas_revisar = len(data['reviews'])

        if num_reseñas_revisar == 0:
            break  # Rompe el bucle si no hay más reseñas

        for i in range(num_reseñas_revisar):
            reseña = data['reviews'][i]
            id = reseña['id']
            fecha_creacion = reseña['date_created']
            contenido = reseña['content']
            valoracion = reseña['rate']
            rate = reseña['valorization']
            likes = reseña['likes']
            dislikes = reseña['dislikes']
            fecha_compra = reseña['buying_date']
            num_palabras = reseña['relevance']
            palabras_prohibidas = reseña['forbidden_words']
            atributos = reseña['attributes']
            media = len(reseña['media'])
            reacciones = reseña['reactions']
            variacion_atributos = reseña['attributes_variation']

            #Agregar los datos al Dataframe
            info_reseña.append({
                "ID": id_producto,
                'Fecha_Creacion': fecha_creacion,
                'Contenido': contenido,
                'Calificacion': rate,
                'Valoracion': valoracion,
                'likes': likes,
                'dislikes': dislikes,
                'fecha_compra': fecha_compra,
                'Numero de Palabras': num_palabras,
                'Palabras_Prohibidas': palabras_prohibidas,
                'Imagenes': media,
                'Reacciones': reacciones,
                'atributos': atributos,
                'Variación_Atributos': variacion_atributos
            })  

# Agregar el diccionario de info del producto a la lista
info_producto.append(producto_info)

# Crear un DataFrame a partir de la lista de reseñas
info_producto_df= pd.DataFrame(info_producto)

# Guardar los datos en un archivo CSV
info_producto_df.to_csv(nombre_archivo_inforeseñas_csv, index=False)

# Crear un DataFrame a partir de la lista de reseñas
info_reseña_df = pd.DataFrame(info_reseña)

# Guardar los datos en un archivo CSV
info_reseña_df.to_csv(nombre_archivo_reseña_csv, index=False)

print(lista_errores)

