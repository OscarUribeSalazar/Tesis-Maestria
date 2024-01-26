import pandas as pd
import requests
import time
from datetime import datetime

# https://auth.mercadolibre.com.mx/authorization?response_type=code&client_id=7740131767656174&redirect_uri=https://reypi.com.br
app = 'Bearer APP_USR-7740131767656174-012310-73f5c85d8344358ddefb8a4537265c3a-17228348'
id_categoria = 'MLM191825'
ruta_productos = 'Productos MLM191825 - 2024-01-23_08-03-09.csv'
df = pd.read_csv(ruta_productos)

# Obtener la fecha y hora actual para guardar el dataframe con la fecha que se extrajo
now = datetime.now()

timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
# Crear el nombre del archivo información
nombre_archivo_inforeseñas_csv = f"Info_reseñas_{id_categoria}_{timestamp}.csv"
nombre_archivo_reseña_csv = f"Reseñas_{id_categoria}_{timestamp}.csv"

info_producto = []
info_reseña = []
lista_errores =  []

for id_producto in df['ID']:
    print(id_producto)

    limit = 100
    offset = 0

    url = f"https://api.mercadolibre.com/reviews/item/{id_producto}?limit={limit}&offset={offset}"

    payload = {}
    headers = {
    'Authorization': app
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

    num_reseñas = data.get('paging', {}).get('total', None)
    promedio_reseñas = data.get('rating_average', None)
    num_reseñas_calificacion = data.get('rating_levels', None)
    one = num_reseñas_calificacion.get('one_star', None)
    dos = num_reseñas_calificacion.get('two_star', None)
    tres = num_reseñas_calificacion.get('three_star', None)
    cuatro = num_reseñas_calificacion.get('four_star', None)
    cinco = num_reseñas_calificacion.get('five_star', None)

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
            id = reseña.get('id', None)
            fecha_creacion = reseña.get('date_created', None)
            contenido = reseña.get('content', None)
            valoracion = reseña.get('rate', None)
            rate = reseña.get('valorization', None)
            likes = reseña.get('likes', None)
            dislikes = reseña.get('dislikes', None)
            fecha_compra = reseña.get('buying_date', None)
            num_palabras = reseña.get('relevance', None)
            palabras_prohibidas = reseña.get('forbidden_words', None)
            atributos = reseña.get('attributes', None)
            media = len(reseña.get('media', []))  # default to an empty list if 'media' is not present
            reacciones = reseña.get('reactions', None)
            variacion_atributos = reseña.get('attributes_variation', None)

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
        time.sleep(1)  

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

# Obtener la fecha y hora actual para guardar el dataframe con la fecha que se extrajo
end = datetime.now()

time_pro = end - now

print(time_pro)

print(lista_errores)

