# import requests
# import pandas as pd
# import time
# id_categoria = 'MLM455214'
# limit = 50

# url = f"https://api.mercadolibre.com/sites/MLM/search?limit={limit}&category={id_categoria}&offset=0"

# payload = {}
# headers = {
#     'Authorization': 'Bearer APP_USR-7740131767656174-011120-c400ce882e4471129b76ab486f0d2ac9-17228348'
# }

# response = requests.request("GET", url, headers=headers, data=payload, timeout=50)
# data = response.json()
# num_resultados = 3960

# info_categoria = []

# for j in range(0, num_resultados, 50):
#     offset_3 = j
#     url = f"https://api.mercadolibre.com/sites/MLM/search?limit={limit}&category={id_categoria}&offset={offset_3}"
#     max_attempts = 3
#     for attempt in range(max_attempts):
#         try:
#             response = requests.request("GET", url, headers=headers, data=payload, timeout=50)
#             response.raise_for_status()  # Lanzará una excepción si la solicitud no fue exitosa (código de estado diferente de 2xx)
#             data = response.json()
#             break
#         except requests.exceptions.RequestException as e:
#             print(f"Intento {attempt + 1} fallido. Razón: {str(e)}")
#         if attempt < max_attempts - 1:
#             print("Reintentando en 5 segundos...")
#             time.sleep(5)  # Espera 5 segundos antes de intentar nuevamente
#         else:
#             print("Número máximo de intentos alcanzado. La solicitud no se pudo completar.")

#     resultados = len(data['results'])
#     if resultados == 0:
#         break  # Rompe el bucle si no hay más reseñas

#     for i in range(resultados):
#         elemento = data['results'][1]
#         id = elemento['id']

#         #Agregar los datos al Dataframe
#         info_categoria.append({
#             "ID": id,
#         })  

# # Crear un DataFrame a partir de la lista de reseñas
# categoria_df = pd.DataFrame(info_categoria)

# # Guardar los datos en un archivo CSV
# categoria_df.to_csv('Reseñas', index=False)

import pandas as pd
import requests
import time

id_producto = 'Reseñas.csv'
dataframe = pd.read_csv(id_producto)
uno = dataframe[0]

# limit = 100
# offset = 0


# url = f"https://api.mercadolibre.com/reviews/item/{uno}?limit={limit}&offset={offset}"

# payload = {}
# headers = {
#   'Authorization': 'Bearer APP_USR-7740131767656174-010800-9c309cde5a32da1242242dc03292e9d9-17228348'
# }

# max_attempts = 3
# for attempt in range(max_attempts):
#     try:
#         response = requests.get(url, headers=headers, data=payload, timeout=10)
#         response.raise_for_status()  # Lanzará una excepción si la solicitud no fue exitosa (código de estado diferente de 2xx)
#         data = response.json()
#         break
#     except requests.exceptions.RequestException as e:
#         print(f"Intento {attempt + 1} fallido. Razón: {str(e)}")
#     if attempt < max_attempts - 1:
#         print("Reintentando en 5 segundos...")
#         time.sleep(5)  # Espera 5 segundos antes de intentar nuevamente
#     else:
#         print("Número máximo de intentos alcanzado. La solicitud no se pudo completar.")

# data = response.json()

# info_producto = []

# num_reseñas = data['paging']['total']
# promedio_reseñas = data['rating_average']
# num_reseñas_calificacion = data['rating_levels']
# one = num_reseñas_calificacion['one_star']
# dos = num_reseñas_calificacion['two_star']
# tres = num_reseñas_calificacion['three_star']
# cuatro = cero = num_reseñas_calificacion['four_star']
# cinco = cero = num_reseñas_calificacion['five_star']

# #Agregar los datos al Dataframe
# producto_info = {
#     "ID": id_producto,
#     'Número_Reseñas': num_reseñas,
#     'Promedio_Calificación': promedio_reseñas,
#     'Num_Reseñas_1': one,
#     'Num_Reseñas_2': dos,
#     'Num_Reseñas_3': tres,
#     'Num_Reseñas_4': cuatro,
#     'Num_Reseñas_5': cinco,
# }

# atributos = data.get('quanti_attributes', [])
# atributos_dic = {}
# for i in range(len(atributos)):
#     Qualidad = atributos[i] 
#     nombre = Qualidad['name']
#     rating = Qualidad['average_rating']
#     atributos_dic[f"Atributo {i + 1}"] = nombre
#     atributos_dic[f"Raiting_Promedio {i + 1}"] = rating

# # Agregar cada característica y calificación como columnas separadas en product_info
# for key, value in atributos_dic.items():
#     producto_info[key] = value

# # Agregar el diccionario de info del producto a la lista
# info_producto.append(producto_info)

# # Crear un DataFrame a partir de la lista de reseñas
# info_producto_df= pd.DataFrame(info_producto)

# # Guardar los datos en un archivo CSV
# info_producto_df.to_csv('Info Reseña Producto', index=False)